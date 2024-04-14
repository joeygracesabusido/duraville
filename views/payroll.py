from sqlmodel import Field, Session, SQLModel, create_engine,select,func,funcfilter,within_group,Relationship,Index
from sqlalchemy.orm.exc import NoResultFound

from models.model import EmployeeList, Books, CashAdvance
from database.mongodb_connection import Connection


from sqlalchemy.orm import selectinload

engine = Connection.db()


class PayrollTransaction(): # this class is for payroll  Transaction

    @staticmethod
    def insert_employee(employee_id,first_name,last_name,
                        company_id,basic_monthly_pay,
                        tax_code,book_id,department,is_active,
                        user): # this is for inserting employee 
        
        insertData = EmployeeList(employee_id=employee_id,first_name=first_name,
                                  last_name=last_name,company_id=company_id,
                                  basic_monthly_pay=basic_monthly_pay,
                                  tax_code=tax_code,book_id= book_id,
                                  department=department,is_active=is_active,user=user)
        

        session = Session(engine)

        session.add(insertData)
        
        session.commit()

        session.close()


    @staticmethod
    def get_employee_list(): # this function is to get all the employee kist
        with Session(engine) as session:
            try:
                statement = select(EmployeeList,Books).where(
                    (EmployeeList.book_id == Books.id)  
                ).order_by(EmployeeList.last_name)

                # statement = select(EmployeeList, Books).join(Books, EmployeeList.book_id == Books.id)
                            
                results = session.exec(statement) 

                data = results.all()
                
                return data
            except NoResultFound:
                return None
            

    @staticmethod
    def get_employee_list2():
        with Session(engine) as session:
            try:
                statement = select(EmployeeList).options(selectinload(EmployeeList.Book)).order_by(EmployeeList.last_name)
                results = session.exec(statement).all()
                return results
            except NoResultFound:
                return None
            
    @staticmethod
    def get_employee_by_id(item_id): # this function is for getting the employee list by the trans id
        with Session(engine) as session:
            try:
                # statement = select(EmployeeList).where(EmployeeList.id == item_id)
                statement = select(EmployeeList,Books).where(
                    (EmployeeList.book_id == Books.id)  
                ).where(EmployeeList.id == item_id)
                            
                results = session.exec(statement) 

                data = results.all()
                
                return data
            except NoResultFound:
                return None
            
    @staticmethod
    def get_employee_by_term(): # this function is for getting the employee list by the trans id
        with Session(engine) as session:
            try:
                # statement = select(EmployeeList).where(EmployeeList.id == item_id)
                statement = select(EmployeeList,Books).where(
                    (EmployeeList.book_id == Books.id)  
                ).order_by(EmployeeList.last_name)
                            
                results = session.exec(statement) 

                data = results.all()
                
                return data
            except NoResultFound:
                return None
            
    @staticmethod   
    def update_employee_details(employee_id,first_name,last_name,
                        company_id,basic_monthly_pay,
                        tax_code,book_id,department,is_active,
                        user,date_updated,item_id):
        """This function is for updating Rizal Equipment"""

        with Session(engine) as session:
            statement = select(EmployeeList).where(EmployeeList.id == item_id)
            results = session.exec(statement)

            result = results.one()

            
            result.employee_id = employee_id
            result.first_name = first_name
            result.last_name  = last_name
            result.company_id = company_id
            result.basic_monthly_pay = basic_monthly_pay
            result.tax_code = tax_code
            result.book_id = book_id
            result.department = department
           
            result.is_active = is_active
            
            result.user = user
            result.date_updated = date_updated

            session.add(result)
            session.commit()
            session.refresh(result)
            session.close()

    @staticmethod
    def insert_cash_advance(employee_id_id,amount_deduction,
                        is_active,
                        user): # this is for inserting cash advances
        
        insertData = CashAdvance(employee_id_id=employee_id_id,amount_deduction=amount_deduction,
                                 is_active=is_active,user=user)
        

        session = Session(engine)

        session.add(insertData)
        
        session.commit()

        session.close()

    @staticmethod
    def get_cash_advance_list(): # this function is to get all the employee list
        with Session(engine) as session:
            try:
                statement = select(CashAdvance,EmployeeList).where(
                    (CashAdvance.employee_id_id == EmployeeList.id)  
                )

                # statement = select(EmployeeList, Books).join(Books, EmployeeList.book_id == Books.id)
                            
                results = session.exec(statement) 

                data = results.all()
                
                return data
            except NoResultFound:
                return None
            




        