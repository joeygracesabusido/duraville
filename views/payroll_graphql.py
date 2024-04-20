import strawberry
from typing import Optional,List

from datetime import date, datetime

# import datetime

from views.payroll import PayrollTransaction


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
    basic_monthly_pay: float
    department: str
    user: str
    date_created: datetime
    is_active: bool
    date_updated: datetime | None = None
    total_cash_advance: float
    total_sss_loan_deduction: float
    total_hdmf_loan_deduction: float
    

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
        data = PayrollTransaction.get_cash_sss_loan_list()

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

        for emp, ca, ss, hd in data:
            employee_with_deductions = EmployeeListObject(
                id=emp.id,
                first_name=emp.first_name,
                last_name=emp.last_name,
                basic_monthly_pay=emp.basic_monthly_pay,
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

        return filtered_employees
