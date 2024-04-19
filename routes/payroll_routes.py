from fastapi import APIRouter, Body, HTTPException, Depends, Request, Response, status
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from typing import Union, List, Optional
from datetime import datetime, date , timedelta
from fastapi.responses import JSONResponse

from pydantic import BaseModel

from authentication.authenticate_user import get_current_user

from views.payroll import PayrollTransaction


import strawberry

from routes.graphql import graphql_app


from views.electricity_details import ElectricityDetailsView


payroll_router = APIRouter(include_in_schema=False)
templates = Jinja2Templates(directory="templates")



class EmployeeListDetails(BaseModel):
    employee_id: str 
    first_name: str 
    last_name: str 
    company_id: Optional[int]
    basic_monthly_pay: Optional[float] 
    tax_code: str 
    book_id: Optional[int] 
    department: str 
    is_active: bool
    
    

    class Config:
        from_attributes = True


class CashAdvanceDetails(BaseModel):
    employee_id_id: Optional[int]
    amount_deduction: float
    
    class Config:
        from_attributes = True

class CashAdvanceDetails2(BaseModel):
     
    amount_deduction: float
    
    class Config:
        from_attributes = True

class SssLoanDetails(BaseModel):
    employee_id_id: Optional[int] 
    amount_deduction: float
    is_active: bool
    user: Optional[str] 
    # date_updated: Optional[datetime] 
    # date_created: Optional[datetime]

    class Config:
        from_attributes = True

class SssLoanDetails2(BaseModel):
    
    amount_deduction: float
  

    class Config:
        from_attributes = True




@payroll_router.get("/insert-employee-list/", response_class=HTMLResponse)
async def api_login(request: Request,username: str = Depends(get_current_user)):
    try:
        if username == 'joeysabusido' or username == 'eliza':

            results = PayrollTransaction.get_employee_list()

            

            employee_data = [
                {
                'id': i.id,
                'employee_id': i.employee_id,
                'first_name': i.first_name,
                'last_name': i.last_name,
                'basic_monthly_pay': i.basic_monthly_pay,
                'tax_code': i.tax_code,
                'department': i.department,
                'book': x.project,
                'is_active': i.is_active
            }
            for i, x in results
            
            ]

            return templates.TemplateResponse("payroll/insert_employee.html", {"request": request,'employee_data':employee_data})
    
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not Authorized",
            # headers={"WWW-Authenticate": "Basic"},
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

#============================== this is for inserting employee Details==============================
@payroll_router.post("/api-insert-employee-details/")
async def api_insert_cost_elements(items:EmployeeListDetails,username: str = Depends(get_current_user)):

    if username == 'joeysabusido' or username == 'eliza':
        try:
        
            PayrollTransaction.insert_employee(employee_id=items.employee_id,
                                            first_name=items.first_name,last_name=items.last_name,
                                            company_id=items.company_id,
                                            basic_monthly_pay=items.basic_monthly_pay,
                                            tax_code=items.tax_code,book_id=items.book_id,
                                            department=items.department,is_active=items.is_active,
                                            user=username)
            return {"message": "Data has been saved"}
        except Exception as e:
            error_message = str(e)
            raise HTTPException(status_code=500, detail=error_message)  


    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Not Authorized",
        # headers={"WWW-Authenticate": "Basic"},
    )



@payroll_router.get("/update-employee-list/{id}")
async def grc_template(id:Optional[int],request: Request, username: str = Depends(get_current_user)):


    if username == 'joeysabusido' or username == 'eliza':
        results = PayrollTransaction.get_employee_by_id(item_id=id)

        if results:
            employee_data = [
                {
                    'id': employee.id,
                    'employee_id': employee.employee_id,
                    'first_name': employee.first_name,
                    'last_name': employee.last_name,
                    'company_id': employee.company_id,
                    'basic_monthly_pay': employee.basic_monthly_pay,
                    'tax_code': employee.tax_code,
                    'department': employee.department,
                    'book': book.project,
                    'book_id': employee.book_id,
                    'is_active': employee.is_active
                }
                for employee, book in results
            ]
            # return employee_data
            return templates.TemplateResponse("payroll/update_employee_list.html", {"request":request,"employee_data":employee_data})
        else:
            return None  # Or handle the case where no employees are found

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Not Authorized",
        # headers={"WWW-Authenticate": "Basic"},
    )





    

    
   
@payroll_router.put("/api-update-employee-details/{id}")
async def updateGRCRental(id,items:EmployeeListDetails,username: str = Depends(get_current_user)):

    


    if username == 'joeysabusido' or username == 'eliza':
            
            today = datetime.now()
            try:
                PayrollTransaction.update_employee_details(employee_id=items.employee_id,first_name=items.first_name,
                                                        last_name=items.last_name,company_id=items.company_id,
                                                        basic_monthly_pay=items.basic_monthly_pay,tax_code=items.tax_code,
                                                        book_id=items.book_id,department=items.department,is_active=items.is_active,
                                                        user=username,date_updated=today,item_id=id)

            except Exception as e:
                error_message = str(e)  # Use the actual error message from the exception
            
                return {"error": error_message}


            return  {'Messeges':'Data has been Updated'}

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Not Authorized",
        # headers={"WWW-Authenticate": "Basic"},
    )





#=====================================================this is for Cash Advance=============================================

@payroll_router.get("/insert-cash-advance/", response_class=HTMLResponse)
async def api_login(request: Request,username: str = Depends(get_current_user)):

    if username == 'joeysabusido' or username == 'eliza':

        try:
            results = PayrollTransaction.get_cash_advance_list()

            

            cash_advance_list = [
                {
                'id': cash_advance.id,
                'employee_id': employee_list.employee_id,
                'first_name': employee_list.first_name,
                'last_name': employee_list.last_name,
                'amount_deduction': cash_advance.amount_deduction,
                'is_active': cash_advance.is_active
            }
            for cash_advance,employee_list in results
            
            ]

            return templates.TemplateResponse("payroll/cash_advance.html", {"request": request,'cash_advance_list':cash_advance_list})
        
        except Exception as e:
            error_message = str(e)  # Use the actual error message from the exception
        
            return {"error": error_message}


    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Not Authorized",
        # headers={"WWW-Authenticate": "Basic"},
    )
    

    
    

@payroll_router.get("/api-acutocomplte-employee/")
def autocomplete_branch_code(term: Optional[str] = None,username: str = Depends(get_current_user)):

    try:
            # Assuming PayrollTransaction.get_employee_list() returns a list of Employee objects
            employee_data = PayrollTransaction.get_employee_list()
            
            
            # Filter employees based on the search term
            if term:
                filtered_employee = [item[0] for item in employee_data if term.lower() in item[0].last_name.lower() or term.lower() in item[0].first_name.lower()]
               
            else:
                filtered_employee = []

            # Construct suggestions from filtered employees
            suggestions = [{"value": f"{item.last_name}, {item.first_name}", "id": item.id,
                            "basic_monthly_pay":item.basic_monthly_pay} for item in filtered_employee]
           

            return suggestions

    except Exception as e:
        error_message = str(e)
        return {"error": error_message}
    
@payroll_router.post("/api-insert-cash-advance/")
async def api_insert_cost_elements(items:CashAdvanceDetails,username: str = Depends(get_current_user)):

    if username == 'joeysabusido' or username == 'eliza':
        try:
        
            PayrollTransaction.insert_cash_advance(employee_id_id=items.employee_id_id,amount_deduction=items.amount_deduction,
                                            is_active=items.is_active,
                                            user=username)
            return {"message": "Data has been saved"}
        except Exception as e:
            error_message = str(e)
            raise HTTPException(status_code=500, detail=error_message)  

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Not Authorized",
        # headers={"WWW-Authenticate": "Basic"},
    )

@payroll_router.get("/payroll-computation/", response_class=HTMLResponse)
async def api_login(request: Request,username: str = Depends(get_current_user)):

    if username == 'joeysabusido' or username == 'eliza':

        

        return templates.TemplateResponse("payroll/payroll_computation_1st_cut_off.html", {"request": request})
        
        


    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Not Authorized",
        # headers={"WWW-Authenticate": "Basic"},
    )



@payroll_router.get("/update-cash-advance/{id}")
async def grc_template(id:Optional[int],request: Request, username: str = Depends(get_current_user)):
    

    results = PayrollTransaction.get_cash_advance_id(item_id=id)
    # results = PayrollTransaction.get_cash_advance_list()

    cash_advance_data = [
        
            {
                    "id":i.id,
                    "employee_id_id":j.first_name,
                    "amount_deduction":i.amount_deduction,
                    "is_active":i.is_active,
                    "user":i.user,
                    "date_updated":i.date_updated,
                    "date_created":i.date_created,
               
            }
           for i,j in  results
        ]
    return cash_advance_data
   
    # return templates.TemplateResponse("cost/update_cost.html", {"request":request,"costData":costData})

@payroll_router.put("/api-update-cash-advance/{id}")
async def update_cash_advance(id,items:CashAdvanceDetails2,username: str = Depends(get_current_user)):
    if username == 'joeysabusido' or username == 'eliza':
   
        today = datetime.now()
        try:
            PayrollTransaction.update_cash_advance(amount_deduction=items.amount_deduction,
                                                   date_updated=today,user=username,item_id=id)

        except Exception as e:
            error_message = str(e)  # Use the actual error message from the exception
        
            return {"error": error_message}


        return  {'Messeges':'Data has been Updated'}
    


# =====================================This is for SSS Loan Deduction===============================

@payroll_router.get("/insert-sss-loan/", response_class=HTMLResponse)
async def api_login(request: Request,username: str = Depends(get_current_user)):

    if username == 'joeysabusido' or username == 'eliza':

        try:
            

            return templates.TemplateResponse("payroll/sss_loan_deduction.html", {"request": request})
        
        except Exception as e:
            error_message = str(e)  # Use the actual error message from the exception
        
            return {"error": error_message}


    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Not Authorized",
        # headers={"WWW-Authenticate": "Basic"},
    )

@payroll_router.post("/api-insert-sss-loan/")
async def insert_sss_loan(items:SssLoanDetails,username: str = Depends(get_current_user)):
    if username == 'joeysabusido' or username == 'eliza':
   
        today = datetime.now()
        try:
            PayrollTransaction.insert_sss_loan_deduction(employee_id_id=items.employee_id_id,
                                                         amount_deduction=items.amount_deduction,
                                                         is_active=items.is_active,
                                                         user=username)

        except Exception as e:
            error_message = str(e)  # Use the actual error message from the exception
        
            return {"error": error_message}


        return  {'Messeges':'Data has been Updated'}
    

@payroll_router.put("/api-update-sss-loan/{id}")
async def update_sss_laon(id,items:SssLoanDetails2,username: str = Depends(get_current_user)):
    
    if username == 'joeysabusido' or username == 'eliza':

        today = datetime.now()
        try:
            PayrollTransaction.update_sss_loan(amount_deduction=items.amount_deduction,
                                                date_updated=today,user=username,item_id=id)

        except Exception as e:
            error_message = str(e)  # Use the actual error message from the exception
        
            return {"error": error_message}


        return  {'Messeges':'Data has been Updated'}








    

    
    



