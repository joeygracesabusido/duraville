
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware




from routes.admin import login_router
from routes.smart_globe import smart_globe_router
from routes.books import books_router
from routes.electricity import electricity_router
from routes.payroll_routes import payroll_router
#from routes.forms import form_htlm


from routes.graphql import graphql_app


app = FastAPI()




app.mount("/static", StaticFiles(directory="static"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins = ['*'],
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"],
)

app.include_router(login_router)
app.include_router(smart_globe_router)
app.include_router(books_router)
app.include_router(electricity_router)
app.include_router(payroll_router)
# Mount Strawberry's GraphQL app onto FastAPI
app.mount("/graphql", graphql_app)
# app.include_router(graphql_app, prefix="/graphql")
# app.include_router(graph)

# app.include_router(graphql_app, prefix="/graphql")
