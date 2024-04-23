from sqlmodel import  Session, select
from sqlalchemy.orm.exc import NoResultFound

from models.model import Books
from database.mongodb_connection import Connection

engine = Connection.db()

class BooksView():
    @staticmethod
    def insert_books_details(company_id,project,user):
        """This function is for inserting books"""
        insertData = Books(company_id=company_id,project=project,user=user)
        

        session = Session(engine)

        session.add(insertData)
        
        session.commit()

        session.close()


    @staticmethod
    def autocomplete_books(): # this function is for autocomplete of books
        with Session(engine) as session:
            try:
                statement = select(Books)
                            
                results = session.exec(statement) 

                data = results.all()
                
                return data
            except NoResultFound:
                return None