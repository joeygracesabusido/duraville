from sqlmodel import Field, Session, SQLModel, create_engine,select,func,funcfilter,within_group,Relationship,Index
from sqlalchemy.orm.exc import NoResultFound

from models.model import CostBranchCode,cost
from database.mongodb_connection import Connection

engine = Connection.db()


class Cost():

    @staticmethod
    def insert_branch(branch_code,user): # this  function is to insert branch for costing
       
        """This function is for inserting user"""
        insertData = CostBranchCode(branch_code=branch_code,user=user)
        

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
            

    @staticmethod
    def get_all_cost(): # this function is for getting all the cost expense from cost table
        with Session(engine) as session:
            try:
                statement = select(cost)
                            
                results = session.exec(statement) 

                data = results.all()
                
                return data
            except NoResultFound:
                return None
            
    @staticmethod
    def get_all_cost_id(item_id): # this function is for getting all the cost expense from cost table
        with Session(engine) as session:
            try:
                statement = select(cost).where(cost.id == item_id)
                            
                results = session.exec(statement) 

                data = results.one()
                
                return data
            except NoResultFound:
                return None




