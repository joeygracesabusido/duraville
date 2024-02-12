from sqlmodel import Field, Session, SQLModel, create_engine,select,func,funcfilter,within_group,Relationship,Index
from sqlalchemy.orm.exc import NoResultFound

from models.model import CostBranchCode,Cost
from database.mongodb_connection import Connection

engine = Connection.db()


class CostViews():

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
                statement = select(Cost)
                            
                results = session.exec(statement) 

                data = results.all()
                
                return data
            except NoResultFound:
                return None
            
    @staticmethod
    def get_all_cost_id(item_id): # this function is for getting all the cost expense from cost table
        with Session(engine) as session:
            try:
                statement = select(Cost).where(Cost.id == item_id)
                            
                results = session.exec(statement) 

                data = results.one()
                
                return data
            except NoResultFound:
                return None
            
    @staticmethod   
    def updatecost(sin,can,khw_no,price,cubic_meter,pic,person_incharge_end_user,
                   no_of_person,plate_no,activity_made,date_updated,user,item_id):
        """This function is for updating Rizal Equipment"""

        with Session(engine) as session:
            statement = select(Cost).where(Cost.id == item_id)
            results = session.exec(statement)

            result = results.one()

            
            result.sin = sin
            result.can = can
            result.khw_no  = khw_no
            result.price = price
            result.cubic_meter = cubic_meter
            result.pic = pic
            result.person_incharge_end_user = person_incharge_end_user
            result.no_of_person = no_of_person
            result.activity_made = activity_made
            result.plate_no = plate_no
            result.user = user
            result.date_updated = date_updated

            session.add(result)
            session.commit()
            session.refresh(result)
            session.close()




