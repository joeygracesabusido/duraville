from sqlmodel import  Session

from models.model import ElectricityDertails
from database.mongodb_connection import Connection

engine = Connection.db()

class ElectricityDetailsView():
    @staticmethod
    def insert_electricity_details(company_id,customer_account_no,service_id_no,
                                   book_id,end_user,subject_to_ewt,user):
        """This function is for inserting user"""
        insertData = ElectricityDertails(company_id=company_id,customer_account_no=customer_account_no,
                                         service_id_no=service_id_no,)
        

        session = Session(engine)

        session.add(insertData)
        
        session.commit()

        session.close()