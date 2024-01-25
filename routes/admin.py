
from fastapi import APIRouter, Body, HTTPException, Depends, Request, Response, status
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from typing import Union, List, Optional



# basemodel import
from pydantic import BaseModel
from datetime import datetime, date
from typing import Optional

# tesing lang

from views.cost import Cost

from datetime import datetime, timedelta

from views.login import Login_views

from  database.mongodb_connection import create_mongo_client
mydb = create_mongo_client()


from authentication.utils import OAuth2PasswordBearerWithCookie

from jose import jwt

JWT_SECRET = 'myjwtsecret'
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

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
    """This is for Branch BaseModel"""

    BranchCode: str


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
async def api_login(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})

@login_router.get("/insert-cost/", response_class=HTMLResponse)
async def insert_cost(request: Request):
    return templates.TemplateResponse("cost/cost_transaction.html", {"request":request}) 

@login_router.get("/insert-cost-elements/", response_class=HTMLResponse)
async def insert_cost(request: Request):
    return templates.TemplateResponse("cost/insert_cost_element.html", {"request":request}) 

@login_router.post("/api-insert-branch-cost/")
async def insert_branch_cost(items:BranchCode):
    """This function is for inserting equipment to GRC table"""
    try:
        Cost.insert_branch(branch_code=items.BranchCode)

        return('Data has been Save')

    except Exception as e:
        error_message = str(e)  # Use the actual error message from the exception
       
        return {"error": error_message}

@login_router.get("/api-search-autocomplete-branch/")
def autocomplete_branch_code(term: Optional[str] = None):
    # this is to autocomplete Routes
    # Ensure you're correctly handling query parameters, 'term' in this case

    branch = Cost.get_branch()
    for i in branch:
        ab = i.branch_code
        print(ab)

    if term:
       # Case-insensitive search for branch codes
        filtered_branch = [item for item in branch if term.lower() in item.branch_code.lower()]
        print(filtered_branch)
    else:
        filtered_branch = []

    suggestions = [{"value": item.branch_code,"branch_code": item.branch_code,"id": item.id} for item in filtered_branch]
    return suggestions
    
