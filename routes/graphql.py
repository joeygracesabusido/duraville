import strawberry
from fastapi import FastAPI
from strawberry.asgi import GraphQL

from views.payroll_graphql import Query, Mutation


# Create a Strawberry schema
schema = strawberry.Schema(query=Query, mutation=Mutation)
 
graphql_app = GraphQL(schema)

