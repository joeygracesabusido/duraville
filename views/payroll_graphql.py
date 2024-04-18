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

    
