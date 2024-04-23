import strawberry
from typing import Optional,List

from datetime import date, datetime


# import datetime


from fastapi import APIRouter, Body, HTTPException, Depends, Request, Response, status

from views.payroll import PayrollTransaction
from views.books import BooksView

from authentication.authenticate_user import get_current_user

from database.mongodb_connection import create_mongo_client
mydb = create_mongo_client()


@strawberry.type
class EmployeeDetails:
    id: Optional[int] 
    employee_id: str 
    first_name: str 
    last_name: str
    company_id: str
    basic_monthly_pay: float
    tax_code: str
    book_id: str
    department: str 
    is_active: bool
    user: str 
    date_updated: str
    date_created: datetime 

@strawberry.type
class CashAdvanceList:
   
    amount_deduction: float

@strawberry.type
class CashAdvanceDetails:
    id: Optional[int] 
    employee_id_id: str
    amount_deduction: float 
    is_active: bool
    user: str 
    date_updated: str  # Represent date_updated as a datetime object
    date_created: Optional[datetime]  # Assuming date_created is also a datetime object


@strawberry.type
class SSSLoanDeductionDetails:
    id: Optional[int]
    employee_id: Optional[int]
    last_name: str
    first_name: str
    amount_deduction: Optional[float]
    is_active: Optional[bool]
    user: Optional[str]
    date_updated: Optional[datetime]
    date_created: Optional[datetime]

@strawberry.type
class HmdfLoanDetails:
    id: Optional[int] 
    employee_id: Optional[int] | None = None
    last_name: str | None = None
    first_name: str
    amount_deduction: float | None = None
    is_active: bool | None = None
    user: str | None = None
    date_updated: datetime | None = None
    date_created: datetime | None = None

@strawberry.type
class jointTableDetails:

    id: Optional[int] 
    employee_id: Optional[int] | None = None
    last_name: str | None = None
    first_name: str
    amount_deduction: float | None = None
    cash_advance_amount: float | None = None
    sss_loan_deduction_amount: float | None = None
    hdmf_loan_deduction_amount: float | None = None
    is_active: bool | None = None
    user: str | None = None
    date_updated: datetime | None = None
    date_created: datetime | None = None

@strawberry.type
class EmployeeListObject:
    id: int
    first_name: str
    last_name: str
    name: str | None = None
    basic_monthly_pay: float
    department: str
    books: str | None = None
    user: str
    date_created: datetime
    is_active: bool
    date_updated: datetime | None = None
    total_cash_advance: float
    total_sss_loan_deduction: float
    total_hdmf_loan_deduction: float

@strawberry.type
class PayrollActivityDetails:
    date_from: date 
    date_to: date
    payroll_date: date
    basic_pay: float
    late: float 
    absent: float 
    undertime: float 
    normal_working_day_ot: float 
    spl_30: float 
    legal: float 
    holiday_ot: float 
    basic_pay_adjustment: float
    gross_pay: float 
    housing_loan: float | None = None
    sss_loan: float | None = None
    hdmf_loan: float | None = None
    general_loan:float | None = None
    company_loan: float | None = None
    other_adjustment: float | None = None
    total_deduction: float 
    net_pay: float 
    sss: float | None = None
    phic: float | None = None
    hdmf: float  | None = None
    tax_withheld: float | None = None
    books: str | None = None
    employee_specs: str | None = None

    employee_id_id: Optional[int] | None = None
    name: str | None = None

    user: str | None = None
    date_updated: datetime | None = None
    date_created: datetime | None = None

@strawberry.type
class SssTableObject:
    rate_from: float  | None = None
    rate_to: float | None = None
    employee_shares: float | None = None
    ss_provident_emp: float | None = None
    employer_Share: float | None = None
    ss_provident_empr: float | None = None
    ecc: float | None = None
   
    

@strawberry.type
class Query:

    @strawberry.field
    async def EmployeeList(self) -> List[EmployeeDetails]: # this function is for querying employee list

       


        results = PayrollTransaction.get_employee_list()
        
        
        employeeData = [EmployeeDetails(id=x[0].employee_id,employee_id=x[0].employee_id,
                                        first_name=x[0].first_name,last_name=x[0].last_name,
                                        company_id=x[1].company_id,
                                        basic_monthly_pay=x[0].basic_monthly_pay,
                                        tax_code=x[0].tax_code,book_id=x[1].project,
                                        department=x[0].department,
                                        is_active=x[0].is_active,
                                        user=x[0].user,date_created=x[0].date_created,
                                        date_updated=x[0].date_updated if x[0].date_updated else '0'
                            ) for x in results]


        return employeeData
    
    @strawberry.field
    async def get_cash_advance_by_term(self, search_term: str) -> List[float]:
        data = PayrollTransaction.get_cash_advance_list()

        results = search_term.split(',')

        filtered_data = [
            (ca, emp) for ca, emp in data
            if any(result.lower() in emp.last_name.lower() or result.lower() in emp.first_name.lower() for result in results)
        ]

        amounts = [ca.amount_deduction for ca, _ in filtered_data]
        
        
        # filtered_data = [
        #     (ca, emp) for ca, emp in data
        #     if search_term.lower() in emp.last_name.lower()
        #     or search_term.lower() in emp.first_name.lower()
        # ]

        # amounts = [ca.amount_deduction for ca, _ in filtered_data]

        # If the filtered_data is empty, return a list with a default value (0.0)
        if not amounts:
            return [0.0]

        return amounts
    
   
    @strawberry.field
    async def get_cash_advance_by_id(self, search_term: str) -> Optional[List[CashAdvanceDetails]]:
        # Assuming search_term is the item ID
        data = PayrollTransaction.get_cash_advance_id(search_term)
       
        cash_advance_details = []

        if data:
            # Process data as per your requirements and create CashAdvanceDetails objects
            
            for cash_advance, employee in data:  # Unpack the tuple
                # If date_updated is None (NULL), set it to 0
                date_updated = cash_advance.date_updated or 0
                cash_advance_detail = CashAdvanceDetails(
                    id=cash_advance.id,  # Access "id" from CashAdvance object
                    employee_id_id=employee.first_name,
                    amount_deduction=cash_advance.amount_deduction,
                    is_active=cash_advance.is_active,
                    user=cash_advance.user,
                    date_updated=date_updated,
                    date_created=cash_advance.date_created,
                
                )
                cash_advance_details.append(cash_advance_detail)

        return cash_advance_details or None
    
#=========================================SSS Loan Frame=======================================
    
    @strawberry.field
    async def get_sss_loan_deductions(self) -> Optional[List[SSSLoanDeductionDetails]]:
        data = PayrollTransaction.get_sss_loan_list()

        sss_loan_deduction_details = []

        if data:
            for sss_loan_deduction, employee in data:
                sss_loan_deduction_detail = SSSLoanDeductionDetails(
                    id=sss_loan_deduction.id,
                    employee_id=employee.employee_id,
                    last_name=employee.last_name,
                    first_name=employee.first_name,
                    amount_deduction=sss_loan_deduction.amount_deduction,
                    is_active=sss_loan_deduction.is_active,
                    user=sss_loan_deduction.user,
                    date_updated=sss_loan_deduction.date_updated,
                    date_created=sss_loan_deduction.date_created
                )
                sss_loan_deduction_details.append(sss_loan_deduction_detail)

        return sss_loan_deduction_details or None
    

    @strawberry.field
    async def get_sss_loan_by_id(self, search_term: str) -> Optional[List[SSSLoanDeductionDetails]]:
        # Assuming search_term is the item ID
        data = PayrollTransaction.get_cash_sss_loan_id(search_term)
        
        cash_advance_details = []

        if data:
            # Process data as per your requirements and create CashAdvanceDetails objects
            
            for cash_advance, employee in data:  # Unpack the tuple
                # If date_updated is None (NULL), set it to 0
                date_updated = cash_advance.date_updated or 0
                cash_advance_detail = SSSLoanDeductionDetails(
                    id=cash_advance.id,  # Access "id" from CashAdvance object
                    employee_id=cash_advance.employee_id_id,
                    first_name=employee.first_name,
                    last_name=employee.last_name,
                    amount_deduction=cash_advance.amount_deduction,
                    is_active=cash_advance.is_active,
                    user=cash_advance.user,
                    date_updated=date_updated,
                    date_created=cash_advance.date_created,
                
                )
                cash_advance_details.append(cash_advance_detail)

        return cash_advance_details or None
    
    @strawberry.field
    async def get_sss_by_term(self, search_term: str) -> List[float]:
        data = PayrollTransaction.get_sss_loan_list()

        results = search_term.split(',')

        filtered_data = [
            (ca, emp) for ca, emp in data
            if any(result.lower() in emp.last_name.lower() or result.lower() in emp.first_name.lower() for result in results)
        ]

        amounts = [ca.amount_deduction for ca, _ in filtered_data]
        
        
        
        if not amounts:
            return [0.0]

        return amounts
    

#=========================================HDMF Loan Frame=======================================
    
    @strawberry.field
    async def get_hdmf_loan_deductions(self) -> Optional[List[HmdfLoanDetails]]:
        data = PayrollTransaction.get_hdmf_loan_list()

        hdmf_loan_deduction_details = []

        if data:
            for hdmf_loan_deduction, employee in data:
                sss_loan_deduction_detail = HmdfLoanDetails(
                    id=hdmf_loan_deduction.id,
                    employee_id=employee.employee_id,
                    last_name=employee.last_name,
                    first_name=employee.first_name,
                    amount_deduction=hdmf_loan_deduction.amount_deduction,
                    is_active=hdmf_loan_deduction.is_active,
                    user=hdmf_loan_deduction.user,
                    date_updated=hdmf_loan_deduction.date_updated,
                    date_created=hdmf_loan_deduction.date_created
                )
                hdmf_loan_deduction_details.append(sss_loan_deduction_detail)

        return hdmf_loan_deduction_details or None
    

    @strawberry.field
    async def get_hdmf_loan_by_id(self, search_term: str) -> Optional[List[HmdfLoanDetails]]:
        data = PayrollTransaction.get_hdmf_loan_id(search_term)

        hdmf_loan_deduction_details = []

        if data:
            for hdmf_loan_deduction, employee in data:
                sss_loan_deduction_detail = HmdfLoanDetails(
                    id=hdmf_loan_deduction.id,
                    employee_id=employee.employee_id,
                    last_name=employee.last_name,
                    first_name=employee.first_name,
                    amount_deduction=hdmf_loan_deduction.amount_deduction,
                    is_active=hdmf_loan_deduction.is_active,
                    user=hdmf_loan_deduction.user,
                    date_updated=hdmf_loan_deduction.date_updated,
                    date_created=hdmf_loan_deduction.date_created
                )
                hdmf_loan_deduction_details.append(sss_loan_deduction_detail)

        return hdmf_loan_deduction_details or None
    

    @strawberry.field
    async def get_employee_with_deductions(self) -> Optional[List[jointTableDetails]]:
        data = PayrollTransaction.testJoinTable()  # Replace YourClassName with the appropriate class name containing the testJoinTable() method

        employee_with_deductions = []

        if data:
            for item in data:
                # Extract the relevant data from the returned tuple
                employee = item[0]
                cash_advance_amount = item[1]
                sss_loan_deduction_amount = item[2]
                hdmf_loan_deduction_amount = item[3]

                # Construct the jointTableDetails object
                employee_with_deduction = jointTableDetails(
                    id=employee.id,
                    employee_id=employee.employee_id,
                    last_name=employee.last_name,
                    first_name=employee.first_name,
                    cash_advance_amount=cash_advance_amount,
                    sss_loan_deduction_amount=sss_loan_deduction_amount,
                    hdmf_loan_deduction_amount=hdmf_loan_deduction_amount
                    # Add other fields as needed
                )
                employee_with_deductions.append(employee_with_deduction)

        return employee_with_deductions or None
    
    @strawberry.field
    def get_employee_with_deductions2(term: Optional[str] = None) -> List[EmployeeListObject]:
        data = PayrollTransaction.testJoinTable()
        employees_with_deductions = []

        for emp, bok,ca, ss, hd in data:
            employee_with_deductions = EmployeeListObject(
                id=emp.id,
                first_name=emp.first_name,
                last_name=emp.last_name,
                name=f"{emp.last_name}, {emp.first_name}",
                basic_monthly_pay=emp.basic_monthly_pay,
                books=bok.project,
                department=emp.department,
                user=emp.user,
                date_created=emp.date_created,
                is_active=emp.is_active,
                date_updated=emp.date_updated,
                total_cash_advance=ca if ca else 0,
                total_sss_loan_deduction=ss if ss else 0,
                total_hdmf_loan_deduction=hd if hd else 0
            )
            employees_with_deductions.append(employee_with_deductions)

        # Filter employees based on the search term
        if term:
            term = term.lower()
            filtered_employees = [emp for emp in employees_with_deductions if term in emp.last_name.lower() or term in emp.first_name.lower()]
        else:
            filtered_employees = employees_with_deductions

        # Construct suggestions from filtered employees
        print(filtered_employees)
        
        

        return filtered_employees
    

    @strawberry.field
    async def get_payroll_all_api(self) -> Optional[List[PayrollActivityDetails]]:
        data = PayrollTransaction.get_payroll_all()

        username: str = Depends(get_current_user)

        if username:

            payroll_activities = []
            for payroll_activity, employee in data:
                payroll_activity_detail = PayrollActivityDetails(
                    date_from=payroll_activity.date_from,
                    date_to=payroll_activity.date_to,
                    payroll_date=payroll_activity.payroll_date,
                    basic_pay=payroll_activity.basic_pay,
                    late=payroll_activity.late,
                    absent=payroll_activity.absent,
                    undertime=payroll_activity.undertime,
                    normal_working_day_ot=payroll_activity.normal_working_day_ot,
                    spl_30=payroll_activity.spl_30,
                    legal=payroll_activity.legal,
                    holiday_ot=payroll_activity.holiday_ot,
                    basic_pay_adjustment=payroll_activity.basic_pay_adjustment,
                    gross_pay=payroll_activity.gross_pay,
                    housing_loan=payroll_activity.housing_loan,
                    sss_loan=payroll_activity.sss_loan,
                    hdmf_loan=payroll_activity.hdmf_loan,
                    general_loan=payroll_activity.general_loan,
                    company_loan=payroll_activity.company_loan,
                    other_adjustment=payroll_activity.other_adjustment,
                    total_deduction=payroll_activity.total_deduction,
                    net_pay=payroll_activity.net_pay,
                    sss=payroll_activity.sss,
                    phic=payroll_activity.phic,
                    hdmf=payroll_activity.hdmf,
                    tax_withheld=payroll_activity.tax_withheld,
                    books=payroll_activity.books,
                    employee_specs=payroll_activity.employee_specs,
                    employee_id_id=payroll_activity.employee_id_id,
                    name=f"{employee.last_name}, {employee.first_name}",
                    user=payroll_activity.user,
                    date_updated=payroll_activity.date_updated,
                    date_created=payroll_activity.date_created
                )
                payroll_activities.append(payroll_activity_detail)

            return payroll_activities
        
        raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Not Authorized",
        # headers={"WWW-Authenticate": "Basic"},
    )
   
    @strawberry.field
    async def get_sss_table(self, amount: float) -> Optional[List[SssTableObject]]:

        # results = mydb.sss_table.find()

        query = {
        "rate_from": {"$lte": amount},
        "rate_to": {"$gte": amount}
        }

        # Retrieve the document matching the query
        results = mydb.sss_table.find_one(query)

        # sssTableData = [SssTableObject(rate_from=x['rate_from'],rate_to=x['rate_to'],
        #                                employee_shares=x['employee_share'],
        #                                ss_provident_emp=x['ss_provident_emp'],
        #                                employer_Share=x['employer_Share'],
        #                                ss_provident_empr=x['ss_provident_empr'],
        #                                ecc=x['ecc']) for x in results]

         # Convert the result to SssTableObject
        if results:
            sssTableData = [SssTableObject(employee_shares=results['employee_share'],
                                           ss_provident_emp=results['ss_provident_emp'],
                                           employer_Share=results['employer_Share'],
                                           ss_provident_empr=results['ss_provident_empr'],
                                            ecc=results['ecc']) ]
        else:
            sssTableData = []


        return sssTableData



    


# ========================================This is for Mutation ===========================================
@strawberry.type
class Mutation:

    @strawberry.mutation
    async def insert_books(company_id: int,project: str,
                          ) -> str:
        username: str = Depends(get_current_user)
        
        if username:
            BooksView.insert_books_details(company_id=company_id,project=project,user=username)


        raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Not Authorized",
        # headers={"WWW-Authenticate": "Basic"},
    )
