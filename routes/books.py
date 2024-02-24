from fastapi import APIRouter, Body, HTTPException, Depends, Request, Response, status
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from typing import Union, List, Optional
from datetime import datetime, date , timedelta

from pydantic import BaseModel

from authentication.authenticate_user import get_current_user


from views.books import BooksView 


books_router = APIRouter(include_in_schema=False)
templates = Jinja2Templates(directory="templates")

@books_router.get("/api-search-autocomplete-books/")
def autocomplete_books_code(term: Optional[str] = None,username: str = Depends(get_current_user)):
    # this is to autocomplete Routes
    # Ensure you're correctly handling query parameters, 'term' in this case
    # print(username)
    results = BooksView.autocomplete_books()
    
   

    search_term = term.strip("'").lower()

    
    data =[ {
               "id": x. id,
                "company_id": x.company_id,
                "project": x.project
    
            }
            for x in results 
    ]

    if term:

        filtered_data = [item for item in data if search_term.lower() in item['project'].lower()]

    else:

        filtered_data = []
    
    
    suggestions = [{"value": item['project'],"id": item['id'],"company_id":item['company_id']} for item in filtered_data]

    return suggestions


