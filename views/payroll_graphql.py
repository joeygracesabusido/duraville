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

@ strawberry.type
class CashAdvanceList:
   
    amount_deduction: float
    
    

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