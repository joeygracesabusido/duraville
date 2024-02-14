from fastapi import APIRouter, Body, HTTPException, Depends, Request, Response, status
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from typing import Union, List, Optional
from datetime import datetime, date , timedelta

from pydantic import BaseModel

from views.login import Login_views
from views.cost import CostViews                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      

from authentication.utils import OAuth2PasswordBearerWithCookie

from jose import jwt

JWT_SECRET = 'myjwtsecret'
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 120

# login_router = APIRouter(include_in_schema=False)
login_router = APIRouter(include_in_schema=True)
templates = Jinja2Templates(directory="templates")



from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

oauth_scheme = OAuth2PasswordBearerWithCookie(tokenUrl="token")



from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")




# this is for BaseMOdel

class User(BaseModel):
    """This is for User BaseModel"""
    username: str 
    hashed_password: str 
    email_add: str
    full_name: str
    is_active: bool 

class BranchCode(BaseModel):
    branch_code: str

    class Config:
        from_attributes = True

class CostElementsBaseModel(BaseModel):
    cost: str

    class Config:
        from_attributes = True


class UpdateCostBaseModel(BaseModel):
    sin: str
    can: str
    khw_no: float
    price: float
    cubic_meter: float
    cubic_meter: float
    pic: str = str
    person_incharge_end_user: str 
    no_of_person: float
    activity_made: str 
    plate_no: str
    cost_elements: Optional[str]
    liters: float
    type_of_vehicle: Optional[str]
    

    class Config:
        from_attributes = True

    


def get_password_hash(password):
    return pwd_context.hash(password)

def authenticate_user(username, password):
    # user = mydb.login.find({"username":username})
    user = Login_views.getuser(username=username)
    
    # print(user)
    username = user.username
    hashed_password = user.hashed_password

    if user:
        password_check = pwd_context.verify(password,hashed_password)
        return password_check

    elif user == None:
        return{'Error'}
    else :
        # False
        print("error")

    # if user is not None:
    #     password_check = pwd_context.verify(password,user.hashed_password)
    #     return password_check
    
    # return None



def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()

    expire = datetime.utcnow() + expires_delta

    to_encode.update({"exp": expire})

    
    return to_encode


@login_router.get("/current-user/")
async def get_current_user(request:Request):

    try :
        token = request.cookies.get('access_token')
        # print(token)
        if token is None:
            raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail= "Not Authorized",
            # headers={"WWW-Authenticate": "Basic"},
            )
        else:
            scheme, _, param = token.partition(" ")
            payload = jwt.decode(param, JWT_SECRET, algorithms=ALGORITHM)
        
            username = payload.get("sub")    
            
            expiration_time = datetime.fromtimestamp(payload.get("exp"))

            user = Login_views.getuser(username=username)

            if user == [] :
                 raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail= "Not Authorized",
               
                )
            else:
                
                return username

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail= "Not Authorized Please login",
            # headers={"WWW-Authenticate": "Basic"},
        )
            

            
            # if datetime.utcnow() > expiration_time:
            #     raise HTTPException(
            #         status_code=status.HTTP_401_UNAUTHORIZED,
            #         detail="Token has expired. Please login again.",
            #     )

            # # response_data = {"username": username}
            # return username

    # except Exception as e:
    #     raise HTTPException(
    #         status_code=status.HTTP_401_UNAUTHORIZED,
    #         detail= "Session has expired",
    #         # headers={"WWW-Authenticate": "Basic"},
    #     )




@login_router.get("/", response_class=HTMLResponse)
async def api_login(request: Request):
    return templates.TemplateResponse("login/login.html", {"request":request}) 





@login_router.post('/sign-up')
def sign_up(items: User):
    """This function is for inserting User"""
   
    #     }
    Login_views.insertuser(username=items.username,hashed_password=get_password_hash(items.hashed_password),
               email_add=items.email_add,full_name=items.full_name, is_active=items.is_active)
    
    return {"message":"User has been save"} 



@login_router.get('/api-login/')
def login(username1: Optional[str],password1:Optional[str],response:Response):
    username = username1
    password = password1


    user = authenticate_user(username,password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
        # return {'Message': 'Incorrect username or password'}
        pass
    # access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    # access_token = create_access_token(
    #     data={"sub": username},
    #     expires_delta=access_token_expires,
    # )

    access_token = create_access_token(
                data = {"sub": username,"exp":datetime.utcnow() + timedelta(ACCESS_TOKEN_EXPIRE_MINUTES)}, 
                expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
                                    )

    data = {"sub": username,"exp":datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)}
    jwt_token = jwt.encode(data,JWT_SECRET,algorithm=ALGORITHM)
    response.set_cookie(key="access_token", value=f'Bearer {jwt_token}',httponly=True)
    # return response
    
    return {"access_token": jwt_token, "token_type": "bearer"}

    # user = authenticate_user(username, password)
    # if not user:
    #     raise HTTPException(status_code=400, detail="Incorrect username or password")

    # access_token = create_access_token(
    #             data = {"sub": username}, 
    #             expires_delta=timedelta(minutes=30)
    #                                 )

    # token = jwt.encode(access_token, JWT_SECRET,algorithm=ALGORITHM)
    # response.set_cookie(key="access_token", value=f'Bearer {token}',httponly=True)
    # return response



@login_router.get("/dashboard/", response_class=HTMLResponse)
async def api_login(request: Request,username: str = Depends(get_current_user)):
    return templates.TemplateResponse("dashboard.html", {"request": request})

@login_router.get("/insert-cost/", response_class=HTMLResponse)
async def getAllCost_cost(request: Request,username: str = Depends(get_current_user)):

    results = CostViews.get_all_cost()

    cost_data = [
             
            {
                "id": x.id,
                "voucher_date": x.voucher_date,
                "voucher_no": x.voucher_no,
                "company": x.company,
                "book": x.book,
                "supplier": x.supplier,
                "vat_reg": x.vat_reg,
                "tin_no": x.tin_no,
                "net_ofvat_with_vat_exempt": "{:,.2f}".format(x.net_ofvat_with_vat_exempt),
                "amount_due": x.amount_due,
                "expense_account": x.expense_account,
                "description": x.description,
                "sin": x.sin,
                "cubic_meter": x.cubic_meter,
                "price": x.price,
                "user": x.user


            }
             for x in results
            
        ]
    
   
    return templates.TemplateResponse("cost/cost_transaction.html", {"request":request,"cost_data":cost_data}) 

@login_router.get("/insert-cost-elements/", response_class=HTMLResponse)
async def insert_cost(request: Request):
    return templates.TemplateResponse("cost/insert_cost_element.html", {"request":request}) 


@login_router.post("/api-insert-branch-cost/")
async def insert_branch_cost(items:BranchCode,username: str = Depends(get_current_user)):
    """This function is for inserting equipment to GRC table"""
    # print(username)
    # username = username.strip("'").lower()

    try:
        
        CostViews.insert_branch(branch_code=items.branch_code, user=username)
        return {"message": "Data has been saved"}
    except Exception as e:
        error_message = str(e)
        raise HTTPException(status_code=500, detail=error_message)
    # except DuplicateBranchError as e:
    #     raise HTTPException(status_code=400, detail="Duplicate Branch")
    # except UnauthorizedError as e:
    #     raise HTTPException(status_code=401, detail="Unauthorized credential. Please login")

@login_router.get("/api-get-branch/")
def get_branchs(term: Optional[str] = None):
    # this is to autocomplete Routes
    # Ensure you're correctly handling query parameters, 'term' in this case

    branch = CostViews.get_branch()

    branch_data = [
        
            {
                "id": x.id,
                "branch_code": x.branch_code,
                "user": x.user
                
            }
            for x in branch
        ]
    
    
    return branch_data

@login_router.get("/api-get-cost/")
def get_branchs(term: Optional[str] = None):
    # this is to autocomplete Routes
    # Ensure you're correctly handling query parameters, 'term' in this case

    results = CostViews.get_all_cost()

    cost_data = [
             
            {   
                "id": x.id,
                "voucher_date": x.voucher_date,
                "voucher_no": x.voucher_no,
                "company": x.company,
                "book": x.book,
                "supplier": x.supplier,
                "vat_reg": x.vat_reg,
                "tin_no": x.tin_no,
                "net_of_vat": x.net_of_vat,
                "amount_due": x.amount_due,
                "expense_account": x.expense_account,
                "description": x.description,
                "inclusive_date": x.inclusive_date,
                "sin": x.sin,
                "can": x.can,
                "khw_no": x.khw_no,
                "price": x.price,
                "cubic_meter": x.cubic_meter,
                "pic": x.pic,
                "person_incharge_end_user": x.person_incharge_end_user,
                "no_of_person": x.no_of_person,
                "activity_made": x.activity_made,
                "plate_no": x.plate_no,
                "user": x.user


            }
             for x in results
            
        ]
    
    return cost_data


@login_router.get("/api-search-autocomplete-branch/")
def autocomplete_branch_code(term: Optional[str] = None,username: str = Depends(get_current_user)):
    # this is to autocomplete Routes
    # Ensure you're correctly handling query parameters, 'term' in this case
    # print(username)
    branch = CostViews.get_branch()
    
   

    search_term = term.strip("'").lower()

    
    data =[ {
               "id": x. id,
                "branch_code": x.branch_code,
    
            }
            for x in branch 
    ]

    if term:

        filtered_data = [item for item in data if search_term.lower() in item['branch_code'].lower()]

    else:

        filtered_data = []
    
    
    suggestions = [{"value": item['branch_code'],"id": item['id']} for item in filtered_data]

    return suggestions
   
    # for x in filtered_branches:
      
    

    # Check if term is present in any branch_code
    # matching_branches = [
    #     {
    #         "id": x["id"],
    #         "branch_code": x["branch_code"],
    #     }
    #     for x in filtered_branches
    #     if term.lower() in x["branch_code"].lower()
    # ]



@login_router.get("/api-update-cost/{id}")
async def grc_template(id:Optional[int],request: Request, username: str = Depends(get_current_user)):
    rentalData = 'Nothing'

    results = CostViews.get_all_cost_id(item_id=id)

    costData = [
        
            {
               "id": results.id,
               "voucher_no": results.voucher_no,
                "inclusive_date": results.inclusive_date,
                "sin": results.sin,
                "can": results.can,
                "khw_no": results.khw_no,
                "price": results.price,
                "cubic_meter": results.cubic_meter,
                "pic": results.pic,
                "person_incharge_end_user": results.person_incharge_end_user,
                "no_of_person": results.no_of_person,
                "activity_made": results.activity_made,
                "plate_no": results.plate_no,
                "cost_elements": results.cost_elements,
                "liters": results.liters,
                "type_of_vehicle": results.type_of_vehicle
               
            }
           
        ]
    
   
    return templates.TemplateResponse("cost/update_cost.html", {"request":request,"costData":costData})

@login_router.put("/update-cost/{id}")
async def updateGRCRental(id,items:UpdateCostBaseModel,username: str = Depends(get_current_user)):

    """This function is to update Water"""
    # user =  mydb.access_setting.find({"username":username})
    # for i in user:
        # if i['site'] == 'admin' or i['site'] == 'sgmc' and i['site_transaction_write']:
    today = datetime.now()
    try:
        CostViews.updatecost(sin=items.sin,can=items.can,
                             khw_no=items.khw_no,price=items.price,
                             cubic_meter=items.cubic_meter,pic=items.pic,person_incharge_end_user=items.person_incharge_end_user,
                             no_of_person=items.no_of_person,plate_no=items.plate_no,activity_made=items.activity_made,
                             cost_elements=items.cost_elements,date_updated=today,liters=items.liters,
                             type_of_vehicle=items.type_of_vehicle,user=username,item_id=id)

    except Exception as e:
        error_message = str(e)  # Use the actual error message from the exception
    
        return {"error": error_message}


    return  {'Messeges':'Data has been Updated'}


@login_router.get("/api-get-electricty-graph")
async def api_get_costGRaph(username: str = Depends(get_current_user)):
    

    results = CostViews.get_all_cost_graph()
    print(results)

    costData = [
        
            {
                "id": i.id,
                "khw_no": i.khw_no,
               
                "person_incharge_end_user": i.person_incharge_end_user,
                
            }
           for i in results
        ]
    
   
    return costData



@login_router.get("/electricity-dashboard/", response_class=HTMLResponse)
async def insert_cost(request: Request):
    return templates.TemplateResponse("electricity/electricity_monitoring.html", {"request":request})

@login_router.get("/testing-dashboard/", response_class=HTMLResponse)
async def insert_cost(request: Request):
    return templates.TemplateResponse("electricity/testing.html", {"request":request})






#============================== this is for inserting cost elements==============================
@login_router.post("/api-insert-cost-elements/")
async def api_insert_cost_elements(items:CostElementsBaseModel,username: str = Depends(get_current_user)):
    
    print('im alive')
    try:
        
        CostViews.insert_cost_elements(costElements=items.cost)
        return {"message": "Data has been saved"}
    except Exception as e:
        error_message = str(e)
        raise HTTPException(status_code=500, detail=error_message)
  
@login_router.get("/api-search-autocomplete-cost-elements/")
def autocomplete_branch_code(term: Optional[str] = None,username: str = Depends(get_current_user)):
   
    cost_elements = CostViews.get_cost_elements()
    
   

    search_term = term.strip("'").lower()

    
    data =[ {
               "id": x. id,
                "cost": x.cost,
    
            }
            for x in cost_elements 
    ]

    if term:

        filtered_data = [item for item in data if search_term.lower() in item['cost'].lower()]

    else:

        filtered_data = []
    
    
    suggestions = [{"value": item['cost']} for item in filtered_data]

    return suggestions

   
    
