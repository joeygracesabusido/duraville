from sqlmodel import Field, Session, SQLModel, create_engine,select,func,funcfilter,within_group,Relationship,Index
from sqlalchemy.orm.exc import NoResultFound

from models.model import CostBranchCode
from database.mongodb_connection import Connection

engine = Connection.db()


class Cost():

    @staticmethod
    def insert_branch(branch_code): # this  function is to insert branch for costing
       
        """This function is for inserting user"""
        insertData = CostBranchCode(branch_code=branch_code)
        

        session = Session(engine)

        session.add(insertData)
        
        session.commit()

        session.close()


    @staticmethod
    def get_branch(): # this funcotion is for getting all the branch
        with Session(engine) as session:
            try:
                statement = select(CostBranchCode)
                            
                results = session.exec(statement) 

                data = results.all()
                
                return data
            except NoResultFound:
                return None




