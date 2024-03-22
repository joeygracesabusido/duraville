from fastapi import APIRouter, Body, HTTPException, Depends, Request, Response, status
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from typing import Union, List, Optional
from datetime import datetime, date , timedelta

from pydantic import BaseModel

from authentication.authenticate_user import get_current_user

from views.payroll import PayrollTransaction


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


@payroll_router.get("/insert-employee-list/", response_class=HTMLResponse)
async def api_login(request: Request,username: str = Depends(get_current_user)):
    try:
        if username == 'joeysabusido' or username == 'eliza':

            results = PayrollTransaction.get_employee_list()

            

            employee_data = [
                {
                'employee_id': i.employee_id,
                'first_name': i.first_name,
                'last_name': i.last_name,
                'basic_monthly_pay': i.basic_monthly_pay,
                'tax_code': i.tax_code,
                'department': i.department,
                'is_active': i.is_active
            }
            for i in results
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


    



