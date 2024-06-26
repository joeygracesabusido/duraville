from sqlmodel import Field, Session, SQLModel, create_engine,select,func,funcfilter,within_group,Relationship,Index
from sqlalchemy.orm.exc import NoResultFound

from models.model import CostBranchCode,Cost, CostElements
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
    def get_all_cost_graph(): # this function is for getting all the cost expense from cost table

        searchData = 'ELECTRICITY'
        with Session(engine) as session:
            try:
                # statement = select(Cost).order_by(Cost.person_incharge_end_user)

                statement = select(Cost.id,Cost.person_incharge_end_user,func.sum(Cost.khw_no).label('khw_no'),
                    ).group_by(Cost.id,Cost.person_incharge_end_user).where(Cost.cost_elements.ilike(f'%{searchData}%')).order_by(Cost.person_incharge_end_user)
                            
                results = session.exec(statement) 

                data = results.all()
                
                return data
            except NoResultFound:
                return None
            
    @staticmethod   
    def updatecost(sin,can,khw_no,price,cubic_meter,pic,person_incharge_end_user,
                   no_of_person,plate_no,activity_made,cost_elements,date_updated,liters,type_of_vehicle,user,item_id):
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
            result.cost_elements = cost_elements
            result.liters = liters
            result.type_of_vehicle = type_of_vehicle
            result.user = user
            result.date_updated = date_updated

            session.add(result)
            session.commit()
            session.refresh(result)
            session.close()

#============================================This is for Cost Elements Transactions======================
    @staticmethod
    def insert_cost_elements(costElements): # this is to insert cost elements

        insertData = CostElements(cost=costElements)
        

        session = Session(engine)

        session.add(insertData)
        
        session.commit()

        session.close()


    @staticmethod
    def get_cost_elements(): # this function is for getting all the cost elements 
        with Session(engine) as session:
            try:
                statement = select(CostElements).order_by(CostElements.cost)
                            
                results = session.exec(statement) 

                data = results.all()
                
                return data
            except NoResultFound:
                return None


