from sqlmodel import Field, Session, SQLModel, create_engine,select,func,funcfilter,within_group,Relationship,Index
from sqlalchemy.orm.exc import NoResultFound

from models.model import EmployeeList
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
                statement = select(EmployeeList)
                            
                results = session.exec(statement) 

                data = results.all()
                
                return data
            except NoResultFound:
                return None
        
