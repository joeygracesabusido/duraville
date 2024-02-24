from sqlmodel import  Session, select
from sqlalchemy.orm.exc import NoResultFound

from models.model import ElectricityDetails
from database.mongodb_connection import Connection

engine = Connection.db()

class ElectricityDetailsView():
    @staticmethod
    def insert_electricity_details(company_id,customer_account_no,service_id_no,
                                   book_id,end_user,subject_to_ewt,user):
        """This function is for inserting user"""
        insertData = ElectricityDetails(company_id=company_id,customer_account_no=customer_account_no,
                                         service_id_no=service_id_no,book_id=book_id,
                                         end_user=end_user,subject_to_ewt=subject_to_ewt,user=user)
        

        session = Session(engine)

        session.add(insertData)
        
        session.commit()

        session.close()


    @staticmethod
    def autocomplete_books_meralco(): # this function is for autocomplete of books
        with Session(engine) as session:
            try:
                statement = select(ElectricityDetails)
                            
                results = session.exec(statement) 

                data = results.all()
                
                return data
            except NoResultFound:
                return None
            

    @staticmethod
    def insert_meralco_consuption(company_id): # this function is for insert meralco consumption
       
        insertData = ElectricityDetails(company_id=company_id)
            

        session = Session(engine)

        session.add(insertData)
        
        session.commit()

        session.close()
       
         
        
            