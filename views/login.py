from sqlmodel import Field, Session, SQLModel, create_engine,select,func,funcfilter,within_group,Relationship,Index
from sqlalchemy.orm.exc import NoResultFound

from models.model import User
from database.mongodb_connection import Connection

engine = Connection.db()

class Login_views():

    def insertuser(username,hashed_password,email_add,full_name,
                is_active):
        """This function is for inserting user"""
        insertData = User(username=username,hashed_password=hashed_password,
                        email_add=email_add,full_name=full_name,is_active=is_active)
        

        session = Session(engine)

        session.add(insertData)
        
        session.commit()

        session.close()


    def getuser(username):
        """This function is querying user """
        with Session(engine) as session:
            try:
                statement = select(User).filter(User.username == username)
                            
                results = session.exec(statement) 

                data = results.one()
                
                return data
            except NoResultFound:
                return None