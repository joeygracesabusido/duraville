from fastapi import APIRouter, Body, HTTPException, Depends, Request, Response, status
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from typing import Union, List, Optional
from datetime import datetime, date , timedelta

from pydantic import BaseModel

from authentication.authenticate_user import get_current_user


from views.cost import CostViews 


smart_globe_router = APIRouter(include_in_schema=False)
templates = Jinja2Templates(directory="templates")

@smart_globe_router.get("/smart-globe-dashboard/", response_class=HTMLResponse)
async def api_login(request: Request,username: str = Depends(get_current_user)):
    return templates.TemplateResponse("smart_globe/smart_globe.html", {"request": request})


