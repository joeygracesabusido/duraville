from sqlmodel import Field, Session, SQLModel, create_engine,select,func,funcfilter,within_group,Relationship,Index
from sqlalchemy.orm.exc import NoResultFound

from models.model import EmployeeList, Books
from database.mongodb_connection import Connection

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

        
