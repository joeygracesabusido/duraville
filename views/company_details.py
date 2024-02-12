from sqlmodel import Field, Session, SQLModel, create_engine,select,func,funcfilter,within_group,Relationship,Index
from sqlalchemy.orm.exc import NoResultFound

from models.model import CompanyDetails
from database.mongodb_connection import Connection

engine = Connection.db()

class CompanyDetailsView():
    @staticmethod
    def insert_company(company_name,address,tin):
        """This function is for inserting user"""
        insertData = CompanyDetails(company_name=company_name,address=address,
                        tin=tin)
        

        session = Session(engine)

        session.add(insertData)
        
        session.commit()

        session.close()


    def get_company(company_name):
        """This function is querying user """
        with Session(engine) as session:
            try:
                statement = select(CompanyDetails).filter(CompanyDetails.company_name == company_name)
                            
                results = session.exec(statement) 

                data = results.one()
                
                return data
            except NoResultFound:
                return None
            
    def get_companys():
        """This function is querying user """
        with Session(engine) as session:
            try:
                statement = select(CompanyDetails)
                            
                results = session.exec(statement) 

                data = results.all()
                return data
            except NoResultFound:
                return None