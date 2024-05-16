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
    employee_id: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    company_id: Optional[int] | None = None
    basic_monthly_pay: float | None = None
    tax_code: str | None = None
    book_id: Optional[int]  | None = None
    department: str  | None = None
    is_active: bool | None = None
    
    

    class Config:
        from_attributes = True


class CashAdvanceDetails(BaseModel):
    employee_id_id: Optional[int]
    amount_deduction: float
    is_active: bool | None = None
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
    user: str | None = None
    date_updated: datetime | None = None
    # date_created: Optional[datetime]

    class Config:
        from_attributes = True

class SssLoanDetails2(BaseModel):
    
    amount_deduction: float
  

    class Config:
        from_attributes = True


class HmdfLoanDetails(BaseModel):

    employee_id_id: Optional[int] | None = None
    amount_deduction: float | None = None
    is_active: bool | None = None
    user: str | None = None
    date_updated: datetime | None = None
    date_created: datetime | None = None

    class Config:
        from_attributes = True

class EmployeeWithDeductions(BaseModel):
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

    class Config:
        from_attributes = True


class PayrollActivityDetails(BaseModel):
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
    sss_provident_emp: float | None = None
    phic: float | None = None
    hdmf: float  | None = None
    tax_withheld: float | None = None
    books: str
    employee_specs: str

    employee_id_id: Optional[int] 

    adjustment_not_taxable: Optional[float] = None
    user: str | None = None
    date_updated: datetime | None = None
    date_created: datetime | None = None

    class Config:
        from_attributes = True
    



@payroll_router.get("/insert-employee-list/", response_class=HTMLResponse)
async def api_login(request: Request,username: str = Depends(get_current_user)):
    try:
        if username == 'joeysabusido' or username == 'eliza' or username == 'drdc-admin':

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

    if username == 'joeysabusido' or username == 'eliza' or username == 'drdc-admin':
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


    if username == 'joeysabusido' or username == 'eliza' or username == 'drdc-admin':
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
async def update_employee_endpoint(id: int, items: EmployeeListDetails, username: str = Depends(get_current_user)):
    if username in ['joeysabusido', 'eliza', 'drdc-admin']:
        today = datetime.now()
        try:
            PayrollTransaction.update_employee_details(
                employee_id=items.employee_id,
                first_name=items.first_name,
                last_name=items.last_name,
                company_id=items.company_id,
                basic_monthly_pay=items.basic_monthly_pay,
                tax_code=items.tax_code,
                book_id=items.book_id,
                department=items.department,
                is_active=items.is_active,
                user=username,
                date_updated=today,
                item_id=id
            )
            return {'Messages': 'Data has been Updated'}
        except Exception as e:
            return {'error': str(e)}

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Not Authorized",
    )


@payroll_router.put("/api-update-employee-details2/{id}")
async def update_employee_endpoint2(id: int, items:EmployeeListDetails , username: str = Depends(get_current_user)):
    if username in ['joeysabusido', 'eliza', 'drdc-admin']:
        today = datetime.now()
        try:
            PayrollTransaction.update_employee_details2(
                # employee_id=items.employee_id,
                # first_name=items.first_name,
                # last_name=items.last_name,
                # company_id=items.company_id,
                basic_monthly_pay=items.basic_monthly_pay,
                # tax_code=items.tax_code,
                # book_id=items.book_id,
                # department=items.department,
                # is_active=items.is_active,
                # user=username,
                # date_updated=today,
                item_id=id
            )
            return {'Messages': 'Data has been Updated'}
        except Exception as e:
            return {'error': str(e)}

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Not Authorized",
    )






#=====================================================this is for Cash Advance=============================================

@payroll_router.get("/insert-cash-advance/", response_class=HTMLResponse)
async def api_login(request: Request,username: str = Depends(get_current_user)):

    if username == 'joeysabusido' or username == 'eliza' or username == 'drdc-admin':

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

    if username == 'joeysabusido' or username == 'eliza' or username == 'drdc-admin':
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

    if username == 'joeysabusido' or username == 'eliza' or username == 'drdc-admin':

        

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
    if username == 'joeysabusido' or username == 'eliza' or username == 'drdc-admin':
   
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

    if username == 'joeysabusido' or username == 'eliza' or username == 'drdc-admin':

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
    if username == 'joeysabusido' or username == 'eliza' or username == 'drdc-admin':
   
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
    
    if username == 'joeysabusido' or username == 'eliza' or username == 'drdc-admin':

        today = datetime.now()
        try:
            PayrollTransaction.update_sss_loan(amount_deduction=items.amount_deduction,
                                                date_updated=today,user=username,item_id=id)

        except Exception as e:
            error_message = str(e)  # Use the actual error message from the exception
        
            return {"error": error_message}


        return  {'Messeges':'Data has been Updated'}

# =====================================HDMF loan Frame =======================================
@payroll_router.get("/insert-hdmf-loan/", response_class=HTMLResponse)
async def hdmf_frame(request: Request,username: str = Depends(get_current_user)):

    if username == 'joeysabusido' or username == 'eliza' or username == 'drdc-admin':

        try:
            

            return templates.TemplateResponse("payroll/hdmf_loan.html", {"request": request})
        
        except Exception as e:
            error_message = str(e)  # Use the actual error message from the exception
        
            return {"error": error_message}


    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Not Authorized",
        # headers={"WWW-Authenticate": "Basic"},
    )

@payroll_router.post("/api-insert-hdmf-loan/")
async def insert_sss_loan(items:HmdfLoanDetails,username: str = Depends(get_current_user)):
    if username == 'joeysabusido' or username == 'eliza' or username == 'drdc-admin':
   
        today = datetime.now()
        try:
            PayrollTransaction.insert_hdmf_loan_deduction(employee_id_id=items.employee_id_id,
                                                         amount_deduction=items.amount_deduction,
                                                         is_active=items.is_active,
                                                         user=username)

        except Exception as e:
            error_message = str(e)  # Use the actual error message from the exception
        
            return {"error": error_message}


        return  {'Messeges':'Data has been Updated'}
    
@payroll_router.put("/api-update-hdmf-loan/{id}")
async def update_hdmf_laon(id,items:HmdfLoanDetails,username: str = Depends(get_current_user)):
    
    if username == 'joeysabusido' or username == 'eliza' or username == 'drdc-admin':

        today = datetime.now()
        try:
            PayrollTransaction.update_hdmf_loan(amount_deduction=items.amount_deduction,
                                                date_updated=today,user=username,item_id=id)

        except Exception as e:
            error_message = str(e)  # Use the actual error message from the exception
        
            return {"error": error_message}


        return  {'Messeges':'Data has been Updated'}
    
@payroll_router.get("/employee-with-deductions/")
async def get_employee_with_deductions(term: Optional[str] = None,username: str = Depends(get_current_user)):
    data = PayrollTransaction.testJoinTable()
    employees_with_deductions = []

    for emp, ca, ss, hd in data:
        employee_with_deductions = EmployeeWithDeductions(
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

    # Construct suggestions from filtered employees
    suggestions = [{"value": f"{item.last_name}, {item.first_name}", "id": item.id,
                    "basic_monthly_pay":item.basic_monthly_pay,
                    'total_cash_advance':item.total_cash_advance,
                    'total_sss_loan_deduction':item.total_sss_loan_deduction,
                    'total_hdmf_loan_deduction':item.total_hdmf_loan_deduction} for item in filtered_employees]

    return suggestions

@payroll_router.get("/employee-with-deductions2")
async def get_employee_with_deductions2(term: Optional[str] = None):
    data = PayrollTransaction.testJoinTable()
    employees_with_deductions = []

    for emp, ca, ss, hd in data:
        employee_with_deductions = {
            "id": emp.id,
            "first_name": emp.first_name,
            "last_name": emp.last_name,
            "basic_monthly_pay": emp.basic_monthly_pay,
            "department": emp.department,
            "user": emp.user,
            "date_created": emp.date_created,
            "is_active": emp.is_active,
            "date_updated": emp.date_updated,
            "total_cash_advance": ca if ca else 0,
            "total_sss_loan_deduction": ss if ss else 0,
            "total_hdmf_loan_deduction": hd if hd else 0
        }
        employees_with_deductions.append(employee_with_deductions)

   

    return employees_with_deductions


@payroll_router.post("/api-insert-payroll-activity/")
async def api_insert_payroll_activity(items:PayrollActivityDetails, username: str = Depends(get_current_user)):

    if username == 'joeysabusido' or username == 'eliza' or username == 'drdc-admin':
        try:
           

            PayrollTransaction.insert_payroll_activity(
                date_from=items.date_from,
                date_to=items.date_to,
                payroll_date=items.payroll_date,
                basic_pay=items.basic_pay,
                late=items.late,
                absent=items.absent,
                undertime=items.undertime,
                normal_working_day_ot=items.normal_working_day_ot,
                spl_30=items.spl_30,
                legal=items.legal,
                holiday_ot=items.holiday_ot,
                basic_pay_adjustment=items.basic_pay_adjustment,
                gross_pay=items.gross_pay,
                housing_loan=items.housing_loan,
                sss_loan=items.sss_loan,
                hdmf_loan=items.hdmf_loan,
                general_loan=items.general_loan,
                company_loan=items.company_loan,
                other_adjustment=items.other_adjustment,
                total_deduction=items.total_deduction,
                net_pay=items.net_pay,
                sss=items.sss,
                phic=items.phic,
                hdmf=items.hdmf,
                tax_withheld=items.tax_withheld,
                books=items.books,
                employee_specs=items.employee_specs,
                employee_id_id=items.employee_id_id,
                user=username,
                sss_provident_emp=items.sss_provident_emp,
                adjustment_not_taxable=items.adjustment_not_taxable
            )

            return {"message": "Data has been saved"}

        except Exception as e:
            error_message = str(e)
            raise HTTPException(status_code=500, detail=error_message)

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Not Authorized",
        # headers={"WWW-Authenticate": "Basic"},
    )

@payroll_router.get("/payroll-report-display/", response_class=HTMLResponse)
async def payroll_reports(request: Request,username: str = Depends(get_current_user)):

    if username == 'joeysabusido' or username == 'eliza' or username == 'drdc-admin':

        try:
            

            return templates.TemplateResponse("reports/payroll_activity.html", {"request": request})
        
        except Exception as e:
            error_message = str(e)  # Use the actual error message from the exception
        
            return {"error": error_message}
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Not Authorized",
        # headers={"WWW-Authenticate": "Basic"},
    )


@payroll_router.get("/payroll-2nd-comp/", response_class=HTMLResponse) # this function is for templae for 2nd cut-off
async def payroll_computation_2nd(request: Request,username: str = Depends(get_current_user)):

    if username == 'joeysabusido' or username == 'eliza' or username == 'drdc-admin':

        try:
            
           
            return templates.TemplateResponse("payroll/payroll_computation_2nd_cut_off.html", {"request": request})
        
        except Exception as e:
            error_message = str(e)  # Use the actual error message from the exception
        
            return {"error": error_message}
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Not Authorized",
        # headers={"WWW-Authenticate": "Basic"},
    )


# =====================================ALLOWANCE FRAME =======================================
@payroll_router.get("/frame-allowance/", response_class=HTMLResponse)
async def allowance(request: Request,username: str = Depends(get_current_user)):

    if username in ['joeysabusido', 'eliza', 'drdc-admin']:

        try:
            
            return templates.TemplateResponse("payroll/allowance.html", {"request": request,'username': username})
        
        except Exception as e:
            error_message = str(e)  # Use the actual error message from the exception
        
            return {"error": error_message}


    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Not Authorized",
        # headers={"WWW-Authenticate": "Basic"},
    )


@payroll_router.get("/frame-allowance-report/", response_class=HTMLResponse)
async def get_allowance_api(request: Request,username: str = Depends(get_current_user)):
    

    if username in ['joeysabusido', 'eliza', 'drdc-admin']:

        try:
            
            
            return templates.TemplateResponse("reports/allowance_report.html", {"request": request})
        
        except Exception as e:
            error_message = str(e)  # Use the actual error message from the exception
        
            return {"error": error_message}


    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Not Authorized",
        # headers={"WWW-Authenticate": "Basic"},
    )

# =====================================reports frame =======================================
@payroll_router.get("/frame-payroll-monthly-report/", response_class=HTMLResponse)
async def hdmf_frame(request: Request,username: str = Depends(get_current_user)):

    if username == 'joeysabusido' or username == 'eliza' or username == 'drdc-admin':

        try:
            

            return templates.TemplateResponse("reports/monthly_payroll_report.html", {"request": request})
        
        except Exception as e:
            error_message = str(e)  # Use the actual error message from the exception
        
            return {"error": error_message}


    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Not Authorized",
        # headers={"WWW-Authenticate": "Basic"},
    )

@payroll_router.get("/monthly-payroll-report/")
async def get_payroll_report(datefrom: Optional[str] = None,dateto: Optional[str] = None ):
    data = PayrollTransaction.get_payrollMonthly(datefrom=datefrom,dateto=dateto)
    print(data)
    employees_with_deductions = []

    for employee_id, total_gross_pay in data:
        employee_with_deductions = {
            "employee_id":employee_id,
            "gross_pay": total_gross_pay,
          
            
        }
        employees_with_deductions.append(employee_with_deductions)

   

    return employees_with_deductions


# ===========================================ALLOWANCE===========================================





    

    
    



