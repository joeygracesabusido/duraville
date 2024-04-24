from pydantic import condecimal
from sqlmodel import Field, Session, SQLModel, create_engine,select,func,funcfilter,within_group,Relationship,Index
from typing import Optional
from decimal import Decimal




import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.join(current_dir, '..')
sys.path.append(parent_dir)


from database.mongodb_connection import Connection

from datetime import date, datetime, timezone

engine = Connection.db()


class CompanyDetails(SQLModel, table=True):
    __tablename__ = 'company'
    id: Optional[int] = Field(default=None, primary_key=True)
    company_name: str = Field(max_length=250)
    address: str
    tin: str


class Books(SQLModel, table=True):
    __tablename__ = 'books'
    id: Optional[int] = Field(default=None, primary_key=True)
    company_id: Optional[int] = Field(default=None, foreign_key="company.id") 
    project: str = Field(index=True, unique=True)
    user: str =Field(default=None)
    date_updated: Optional[datetime] = Field(default=None)
    date_credited: datetime = Field(default_factory=datetime.utcnow)


    __table_args__ = (Index("idx_project", "project", unique=True),)
   


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

class CostElements(SQLModel, table=True):
    """This is for creating cost element table"""
    __tablename__ = 'cost_elements'
    id: Optional[int] = Field(default=None, primary_key=True)
    cost: str = Field(index=True, unique=True)

    __table_args__ = (Index("idx_cost", "cost", unique=True),)

    


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


class Cost(SQLModel, table=True):
    """This is for table of cost"""
    __tablename__ = 'cost'
    id: Optional[int] = Field(default=None, primary_key=True)
    voucher_date: Optional[date]
    voucher_no: str = Field(max_length=100, index=True)
    company: str = Field(max_length=150)
    book: str = Field(max_length=150)
    supplier: str = Field(max_length=250)
    vat_reg: str = Field(max_length=100)
    tin_no: str = Field(max_length=70)
    net_of_vat: Decimal = Field(default=0, max_digits=20, decimal_places=2)
    vat_exempt: Decimal = Field(default=0, max_digits=20, decimal_places=2)
    net_ofvat_with_vat_exempt: Decimal = Field(default=0, max_digits=20, decimal_places=2)
    amount_due: Decimal = Field(default=0, max_digits=20, decimal_places=2)
    with_holding_tax: Decimal = Field(default=0, max_digits=20, decimal_places=2)
    total_amount_due: Decimal = Field(default=0, max_digits=20, decimal_places=2)
    expense_account: str = Field(max_length=200)
    description: str = Field(max_length=4000)
    inclusive_date: str = Field(default=None)
    sin: str =Field(default=None)
    can: str =Field(default=None)
    khw_no: Decimal = Field(default=0, max_digits=9, decimal_places=2)
    price: Decimal = Field(default=0, max_digits=9, decimal_places=2)
    cubic_meter: Decimal = Field(default=0, max_digits=9, decimal_places=2)
    pic: str = Field(default=None)
    person_incharge_end_user: str = Field(default=None)
    no_of_person: Decimal = Field(default=0, max_digits=9, decimal_places=2)
    activity_made: str = Field(default=None)
    plate_no: str = Field(default=None)
    cost_elements: str = Field(max_length=255, default=None)
    liters: Decimal = Field(default=0, max_digits=9, decimal_places=2)
    type_of_vehicle: str = Field(max_length=255, default=None)

    user: str =Field(default=None)
    date_updated: Optional[datetime] = Field(default=None)
    date_credited: datetime = Field(default_factory=datetime.utcnow)


class ElectricityDetails(SQLModel, table = True):
    """This is for table of electricity Details"""
    __tablename__ = 'electricity_details'
    id: Optional[int] = Field(default=None, primary_key=True)
    company_id: Optional[int] = Field(default=None, foreign_key="company.id") 
    customer_account_no: str = Field(index=True, unique=True)
    service_id_no: str = Field(index=True, unique=True)
    book_id: Optional[int] = Field(default=None, foreign_key="books.id")
    end_user: str
    subject_to_ewt: bool
    user: str =Field(default=None)
    date_updated: Optional[datetime] = Field(default=None)
    date_credited: datetime = Field(default_factory=datetime.utcnow)


    __table_args__ = (Index("idx_customer_account_no", "customer_account_no", unique=True),)
    __table_args__ = (Index("idx_service_id_no", "service_id_no", unique=True),)
    
class EmployeeList(SQLModel, table = True):
    """this is for table of employee list"""
    __tablename__ = 'employee_list'
    id: Optional[int] = Field(default=None, primary_key=True)
    employee_id: str = Field(index=True, unique=True)
    first_name: str = Field(default=None, max_length=150)
    last_name: str = Field(default=None, max_length=150)
    company_id: Optional[int] = Field(default=None, foreign_key="company.id")
    basic_monthly_pay: float = Field(default=None)
    tax_code: str = Field(default=None, max_length=100)
    book_id: Optional[int] = Field(default=None, foreign_key="books.id")
    department: str = Field(default=None, max_length=150)
    is_active: bool
    user: str =Field(default=None)
    date_updated: Optional[datetime] = Field(default=None)
    date_created: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    __table_args__ = (Index("idx_employee_id", "employee_id", unique=True),)

class CashAdvance(SQLModel, table=True):
    """This is for cash advances"""
    __tablename__ = 'cash_advance'
    id: Optional[int] = Field(default=None, primary_key=True)
    employee_id_id: Optional[int] = Field(default=None, foreign_key="employee_list.id")
    amount_deduction: float = Field(default=None)
    is_active: bool
    user: str =Field(default=None)
    date_updated: Optional[datetime] = Field(default=None)
    date_created: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class SSSLoanDeduction(SQLModel, table=True):
    """This is for cash advances"""
    __tablename__ = 'sss_loan_deduction'
    id: Optional[int] = Field(default=None, primary_key=True)
    employee_id_id: Optional[int] = Field(index=True,default=None, foreign_key="employee_list.id")
    amount_deduction: float = Field(default=None)
    is_active: bool
    user: str =Field(default=None)
    date_updated: Optional[datetime] = Field(default=None)
    date_created: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class HDMFLoanDeduction(SQLModel, table=True):
    """This is for cash advances"""
    __tablename__ = 'hdmf_loan_deduction'
    id: Optional[int] = Field(default=None, primary_key=True)
    employee_id_id: Optional[int] = Field(index=True,default=None, foreign_key="employee_list.id")
    amount_deduction: float = Field(default=None)
    is_active: bool
    user: str =Field(default=None)
    date_updated: Optional[datetime] = Field(default=None)
    date_created: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class PayrollActivity(SQLModel, table=True):
    """This is for table for Payroll Activity"""
    __tablename__ = 'payroll_activity'
    id: Optional[int] = Field(default=None, primary_key=True)
    date_from: date
    date_to: date
    payroll_date: date
    basic_pay: float = Field(default= 0)
    late: float = Field(default= 0)
    absent: float = Field(default= 0)
    undertime: float = Field(default= 0)
    normal_working_day_ot: float = Field(default= 0)
    spl_30: float = Field(default= 0)
    legal: float = Field(default= 0)
    holiday_ot: float = Field(default= 0)
    basic_pay_adjustment: float = Field(default= 0)
    gross_pay: float = Field(default= 0)
    housing_loan: float = Field(default= 0)
    sss_loan: float = Field(default= 0)
    hdmf_loan: float = Field(default= 0)
    general_loan:float = Field(default= 0)
    company_loan: float = Field(default= 0)
    other_adjustment: float = Field(default= 0)
    total_deduction: float = Field(default= 0)
    net_pay: float = Field(default= 0)
    sss: float = Field(default= 0)
    sss_provident_emp: float = Field(default= 0)
    phic: float = Field(default= 0)
    hdmf: float = Field(default= 0)
    tax_withheld: float = Field(default= 0)
    books: str
    employee_specs: str

    employee_id_id: Optional[int] = Field(index=True,default=None, foreign_key="employee_list.id")


    user: str =Field(default=None)
    date_updated: Optional[datetime] = Field(default=None)
    date_created: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    
    









def create_db_and_tables():
    
    SQLModel.metadata.create_all(engine)

# create_db_and_tables()


