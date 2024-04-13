import strawberry
from fastapi import FastAPI
from strawberry.asgi import GraphQL

from views.payroll_graphql import Query


# Create a Strawberry schema
schema = strawberry.Schema(query=Query)
 
graphql_app = GraphQL(schema)

