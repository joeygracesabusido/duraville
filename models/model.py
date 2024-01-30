from pydantic import condecimal
from sqlmodel import Field, Session, SQLModel, create_engine,select,func,funcfilter,within_group,Relationship,Index
from typing import Optional


import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.join(current_dir, '..')
sys.path.append(parent_dir)


from database.mongodb_connection import Connection

from datetime import date, datetime

engine = Connection.db()


class User(SQLModel, table=True):
    """This is to create user Table"""
    __tablename__ = 'user'
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True)
    hashed_password: str = Field(nullable=False)
    email_add: str = Field(nullable=False)
    full_name: str = Field(max_length=70, default=None)
    is_active: bool = Field(default=False)
    date_updated: Optional[datetime] = Field(default=None)
    date_credited: datetime = Field(default_factory=datetime.utcnow)

    __table_args__ = (Index("idx_user_unique", "username", unique=True),)


class CostAccountName(SQLModel, table=True):
    """This is for table of cost account name"""
    __tablename__ = 'cost_account_name'
    id: Optional[int] = Field(default=None, primary_key=True)
    account_name: str = Field(index=True, unique=True)
    date_updated: Optional[datetime] = Field(default=None)
    date_credited: datetime = Field(default_factory=datetime.utcnow)
    user: str =Field(max_length=100, default=None)
    __table_args__ = (Index("idx_cost_account_name_unique", "account_name", unique=True),)

class CostBranchCode(SQLModel, table=True):
    """This is for table of Branch"""
    __tablename__ = 'cost_branch_code'
    id: Optional[int] = Field(default=None, primary_key=True)
    branch_code: str = Field(index=True, unique=True)
    date_updated: Optional[datetime] = Field(default=None)
    date_credited: datetime = Field(default_factory=datetime.utcnow)
    user: str =Field(max_length=100, default=None)
    __table_args__ = (Index("idx_branch_code_unique", "branch_code", unique=True),)

class ChartOfAccount(SQLModel, table=True):
    """This is for table of chart of account"""
    __tablename__ = 'chart_of_account'
    id: Optional[int] = Field(default=None, primary_key=True)
    account_code: str = Field(index=True, unique=True)
    account_title: str = Field(max_length=100)
    account_class: str = Field(max_length=50)
    date_updated: Optional[datetime] = Field(default=None)
    date_credited: datetime = Field(default_factory=datetime.utcnow)
    user: str =Field(max_length=100, default=None)
    __table_args__ = (Index("idx_chart_of_account", "account_code", unique=True),)
    __table_args__ = (Index("idx_chart_of_account", "account_title", unique=True),)


class cost(SQLModel, table=True):
    """This is for table of cost"""
    __tablename__ = 'cost'
    id: Optional[int] = Field(default=None, primary_key=True)
    voucher_date: datetime
    voucher_no: str = Field(max_length=100)
    company: str = Field(max_length=150)
    book: str = Field(max_length=150)
    supplier: str = Field(max_length=250)
    vat_reg: str = Field(max_length=100)
    tin_no: str = Field(max_length=70)
    net_of_vat: condecimal(max_digits=20, decimal_places=2) = Field(default=0)
    amount_due: condecimal(max_digits=20, decimal_places=2) = Field(default=0)
    expense_account: str = Field(max_length=200)
    description: str = Field(max_length=4000)
    sin: str =Field(default=None)
    kwt_cubic_meter: str = Field(default=None)
    amount: condecimal(max_digits=20, decimal_places=2) = Field(default=0)
    user: str =Field(default=None)
    date_updated: Optional[datetime] = Field(default=None)
    date_credited: datetime = Field(default_factory=datetime.utcnow)
    





# class Department(SQLModel, table=True):
#     """This is for department table"""
#     __tablename__ = 'department'
#     id: Optional[int] = Field(default=None, primary_key=True)
#     department: str =Field(index=True, unique=True)

#     __table_args__ = (Index("idx_department_unique", "department", unique=True),)



def create_db_and_tables():
    
    SQLModel.metadata.create_all(engine)

# create_db_and_tables()

