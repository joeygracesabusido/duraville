from fastapi import APIRouter, Body, HTTPException, Depends, Request, Response, status
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from typing import Union, List, Optional
from datetime import datetime, date , timedelta

from pydantic import BaseModel

from authentication.authenticate_user import get_current_user


from views.electricity_details import ElectricityDetailsView


electricity_router = APIRouter(include_in_schema=False)
templates = Jinja2Templates(directory="templates")



class MeralcoDetails(BaseModel):
    company_id: int
    customer_account_no: str
    service_id_no: str
    book_id: int
    end_user: str
    subject_to_ewt: bool


    class Config:
        from_attributes = True

# @electricity_router.get("/smart-globe-dashboard/", response_class=HTMLResponse)
# async def api_login(request: Request,username: str = Depends(get_current_user)):
#     return templates.TemplateResponse("smart_globe/smart_globe.html", {"request": request})

@electricity_router.post("/api-insert-meralco-details/")
async def api_insert_electricity_details(items:MeralcoDetails,username: str = Depends(get_current_user)):
    """This function is for inserting equipment to GRC table"""
    
    

    try:
        
        ElectricityDetailsView.insert_electricity_details(company_id=items.company_id,customer_account_no=items.customer_account_no,
                                                service_id_no=items.service_id_no,book_id=items.book_id,
                                                end_user=items.end_user,subject_to_ewt=items.subject_to_ewt,
                                                user=username)
        return {"message": "Data has been saved"}
    except Exception as e:
        error_message = str(e)
        raise HTTPException(status_code=500, detail=error_message)
    
@electricity_router.post("/api-insert-meralco-consumption/") # this function is for inserting meralco consumption
async def api_insert_electricity_details(items:MeralcoDetails,username: str = Depends(get_current_user)):
    """This function is for inserting equipment to GRC table"""
    
    

    try:
        
        ElectricityDetailsView.insert_electricity_details(company_id=items.company_id,customer_account_no=items.customer_account_no,
                                                service_id_no=items.service_id_no,book_id=items.book_id,
                                                end_user=items.end_user,subject_to_ewt=items.subject_to_ewt,
                                                user=username)
        return {"message": "Data has been saved"}
    except Exception as e:
        error_message = str(e)
        raise HTTPException(status_code=500, detail=error_message)

   



