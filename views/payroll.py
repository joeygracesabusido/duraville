from sqlmodel import Field, Session,  create_engine,select,func,funcfilter,within_group,Relationship,Index
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import select, and_

from models.model import (EmployeeList, Books, CashAdvance, 
                          SSSLoanDeduction, HDMFLoanDeduction,PayrollActivity,
                          Allowance)
from database.mongodb_connection import Connection
from typing import Optional
from datetime import date, datetime


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
            # statement = select(EmployeeList).flter(EmployeeList.id == item_id)
            result = session.query(EmployeeList).filter(EmployeeList.id == item_id).one()

          
            
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

    def update_employee_details2(basic_monthly_pay,book_id, item_id):
        """This function is for updating Employee"""
       
        with Session(engine) as session:
            # Retrieve the EmployeeList object by its ID
            result = session.query(EmployeeList).filter(EmployeeList.id == item_id).one()

            # Update the basic_monthly_pay attribute
            result.basic_monthly_pay = basic_monthly_pay
            result.book_id = book_id

            # Commit the changes to the database
            session.add(result)
            session.commit()
            session.refresh(result)
            session.close()
           

#======================================Cash Advance Frame==========================================
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
            
    @staticmethod
    def get_cash_advance_id(item_id): # this function is to get all the employee list
        with Session(engine) as session:
            try:
                statement = select(CashAdvance,EmployeeList).where(
                    (CashAdvance.employee_id_id == EmployeeList.id) 
                )

                
                if item_id:
                    statement = statement.where(CashAdvance.id == item_id)
                          
                results = session.exec(statement) 
                data = results.all()
            
                return data
            except NoResultFound:
                return None
            
    @staticmethod   
    def update_cash_advance(amount_deduction,
                        user,date_updated, item_id):
        """This function is for updating Rizal Equipment"""

        with Session(engine) as session:
            statement = select(CashAdvance).where(CashAdvance.id == item_id)
            results = session.exec(statement)

            result = results.one()
            result.amount_deduction = amount_deduction
          
            result.user = user
            result.date_updated = date_updated

            session.add(result)
            session.commit()
            session.refresh(result)
            session.close()
            
#======================================SSS Loan Deduction   ==========================================
    @staticmethod
    def insert_sss_loan_deduction(employee_id_id,amount_deduction,
                        is_active,
                        user): # this is for inserting cash advances
        
        insertData = SSSLoanDeduction(employee_id_id=employee_id_id,amount_deduction=amount_deduction,
                                 is_active=is_active,user=user)
        

        session = Session(engine)

        session.add(insertData)
        
        session.commit()

        session.close()


    @staticmethod
    def get_sss_loan_list(): # this function is to get all the employee list
        with Session(engine) as session:
            try:
                statement = select(SSSLoanDeduction,EmployeeList).where(
                    (SSSLoanDeduction.employee_id_id == EmployeeList.id)  
                ).order_by(EmployeeList.last_name)

                            
                results = session.exec(statement) 

                data = results.all()
                
                return data
            except NoResultFound:
                return None
            
    @staticmethod
    def get_cash_sss_loan_id(item_id): # this function is to get all the sss loan deduction
        with Session(engine) as session:
            try:
                statement = select(SSSLoanDeduction,EmployeeList).where(
                    (SSSLoanDeduction.employee_id_id == EmployeeList.id) 
                )

                
                if item_id:
                    statement = statement.where(SSSLoanDeduction.id == item_id)
                          
                results = session.exec(statement) 
                data = results.all()
            
                return data
            except NoResultFound:
                return None
            
    @staticmethod   
    def update_sss_loan(amount_deduction: float, user: str, date_updated: datetime, item_id: int):
        """This function is for updating SSS Loan"""
        
        session = Session(engine)
        try:
            result = session.query(SSSLoanDeduction).filter(SSSLoanDeduction.id == item_id).one_or_none()
            
            if result is None:
                return {"error": f"No record found with id {item_id}"}

            result.amount_deduction = amount_deduction
            result.user = user
            result.date_updated = date_updated

            session.commit()
            session.refresh(result)
            
            return {"message": "Data has been updated", "result": result}
        except Exception as e:
            session.rollback()
            return {"error": str(e)}
        finally:
            session.close()


    # def update_sss_loan(amount_deduction,
    #                     user,date_updated, item_id):
    #     """This function is for updating SSS Loan"""

    #     with Session(engine) as session:
    #         statement = select(SSSLoanDeduction).where(SSSLoanDeduction.id == item_id)
    #         results = session.exec(statement)

    #         result = results.one()
    #         result.amount_deduction = amount_deduction
          
    #         result.user = user
    #         result.date_updated = date_updated

    #         session.add(result)
    #         session.commit()
    #         session.refresh(result)
    #         session.close()
    


#======================================HDMF Loan Deduction   ==========================================
    @staticmethod
    def insert_hdmf_loan_deduction(employee_id_id,amount_deduction,
                        is_active,
                        user): # this is for inserting cash advances
        
        insertData = HDMFLoanDeduction(employee_id_id=employee_id_id,amount_deduction=amount_deduction,
                                 is_active=is_active,user=user)
        

        session = Session(engine)

        session.add(insertData)
        
        session.commit()

        session.close()


    @staticmethod
    def get_hdmf_loan_list(): # this function is to get all the employee list
        with Session(engine) as session:
            try:
                statement = select(HDMFLoanDeduction,EmployeeList).where(
                    (HDMFLoanDeduction.employee_id_id == EmployeeList.id)  
                ).order_by(EmployeeList.last_name)

                            
                results = session.exec(statement) 

                data = results.all()
                
                return data
            except NoResultFound:
                return None
            
    @staticmethod
    def get_hdmf_loan_id(item_id): # this function is to get all the sss loan deduction
        with Session(engine) as session:
            try:
                statement = select(HDMFLoanDeduction,EmployeeList).where(
                    (HDMFLoanDeduction.employee_id_id == EmployeeList.id) 
                )

                
                if item_id:
                    statement = statement.where(HDMFLoanDeduction.id == item_id)
                          
                results = session.exec(statement) 
                data = results.all()
            
                return data
            except NoResultFound:
                return None
            
    @staticmethod   
    def update_hdmf_loan(amount_deduction,
                        user,date_updated, item_id):
        """This function is for updating SSS Loan"""

        # with Session(engine) as session:
        #     try:
        #         result = session.exec(select(HDMFLoanDeduction).filter(HDMFLoanDeduction.id == item_id)).one_or_none()

        #         if result is None:
        #             return {"error": f"No record found with id {item_id}"}

        #         result.amount_deduction = amount_deduction
        #         result.user = user
        #         result.date_updated = date_updated

        #         session.add(result)
        #         session.commit()
        #         session.refresh(result)

        #         return {"message": "Data has been updated", "result": result}
        #     except Exception as e:
        #         session.rollback()
        #         return {"error": str(e)}


        session = Session(engine)
        try:
            result = session.query(HDMFLoanDeduction).filter(HDMFLoanDeduction.id == item_id).one_or_none()
            
            if result is None:
                return {"error": f"No record found with id {item_id}"}

            result.amount_deduction = amount_deduction
            result.user = user
            result.date_updated = date_updated

            session.commit()
            session.refresh(result)
            
            return {"message": "Data has been updated", "result": result}
        except Exception as e:
            session.rollback()
            return {"error": str(e)}
        finally:
            session.close()

        # with Session(engine) as session:
        #     statement = select(HDMFLoanDeduction).where(HDMFLoanDeduction.id == item_id)
        #     results = session.query(statement)

        #     result = results.one()
        #     result.amount_deduction = amount_deduction
          
        #     result.user = user
        #     result.date_updated = date_updated

        #     session.add(result)
        #     session.commit()
        #     session.refresh(result)
        #     session.close()
# ==================================this is for joint ==========================================
    # @staticmethod
    # def testJoinTable():
    #     """Function for Testing Joining Table using sqlmodel"""
    #     with Session(engine) as session:
    #         subquery_cash_advance = (
    #             select(
    #                 CashAdvance.employee_id_id,
    #                 func.sum(CashAdvance.amount_deduction).label("totalCashAdvance")
    #             )
    #             .where(CashAdvance.employee_id_id == EmployeeList.id)  # Filter by employee_id
    #             .group_by(CashAdvance.employee_id_id)
    #             .subquery()
    #         )

    #         subquery_sss_loan = (
    #             select(
    #                 SSSLoanDeduction.employee_id_id,
    #                 func.sum(SSSLoanDeduction.amount_deduction).label("totalSSSLoanDeduction")
    #             )
    #             .where(SSSLoanDeduction.employee_id_id == EmployeeList.id)  # Filter by employee_id
    #             .group_by(SSSLoanDeduction.employee_id_id)
    #             .subquery()
    #         )

    #         subquery_hdmf_loan = (
    #             select(
    #                 HDMFLoanDeduction.employee_id_id,
    #                 func.sum(HDMFLoanDeduction.amount_deduction).label("totalHDMFLoanDeduction")
    #             )
    #             .where(HDMFLoanDeduction.employee_id_id == EmployeeList.id)  # Filter by employee_id
    #             .group_by(HDMFLoanDeduction.employee_id_id)
    #             .subquery()
    #         )

    #         statement = select(EmployeeList,Books).where(
    #                 (EmployeeList.book_id == Books.id)  
    #             ).order_by(EmployeeList.last_name)

    #         statement = (
    #             select(
    #                 EmployeeList,
    #                 func.coalesce(subquery_cash_advance.c.totalCashAdvance, 0).label("TotalCashAdvance"),
    #                 func.coalesce(subquery_sss_loan.c.totalSSSLoanDeduction, 0).label("TotalSSSLoanDeduction"),
    #                 func.coalesce(subquery_hdmf_loan.c.totalHDMFLoanDeduction, 0).label("TotalHDMFLoanDeduction")
    #             )
    #             .select_from(EmployeeList)
    #             .outerjoin(subquery_cash_advance, EmployeeList.id == subquery_cash_advance.c.employee_id_id)
    #             .outerjoin(subquery_sss_loan, EmployeeList.id == subquery_sss_loan.c.employee_id_id)
    #             .outerjoin(subquery_hdmf_loan, EmployeeList.id == subquery_hdmf_loan.c.employee_id_id)
    #             .order_by(EmployeeList.id)
    #         )


    #         results = session.exec(statement)
    #         data = results.all()
    #         return data
        
    @staticmethod
    def testJoinTable():
        """Function for Testing Joining Table using sqlmodel"""
        with Session(engine) as session:
            subquery_cash_advance = (
                select(
                    CashAdvance.employee_id_id,
                    func.sum(CashAdvance.amount_deduction).label("totalCashAdvance")
                )
                .where(CashAdvance.employee_id_id == EmployeeList.id)  # Filter by employee_id
                .group_by(CashAdvance.employee_id_id)
                .subquery()
            )

            subquery_sss_loan = (
                select(
                    SSSLoanDeduction.employee_id_id,
                    func.sum(SSSLoanDeduction.amount_deduction).label("totalSSSLoanDeduction")
                )
                .where(SSSLoanDeduction.employee_id_id == EmployeeList.id)  # Filter by employee_id
                .group_by(SSSLoanDeduction.employee_id_id)
                .subquery()
            )

            subquery_hdmf_loan = (
                select(
                    HDMFLoanDeduction.employee_id_id,
                    func.sum(HDMFLoanDeduction.amount_deduction).label("totalHDMFLoanDeduction")
                )
                .where(HDMFLoanDeduction.employee_id_id == EmployeeList.id)  # Filter by employee_id
                .group_by(HDMFLoanDeduction.employee_id_id)
                .subquery()
            )

            final_statement = (
                select(
                    EmployeeList,
                    Books,
                    func.coalesce(subquery_cash_advance.c.totalCashAdvance, 0).label("TotalCashAdvance"),
                    func.coalesce(subquery_sss_loan.c.totalSSSLoanDeduction, 0).label("TotalSSSLoanDeduction"),
                    func.coalesce(subquery_hdmf_loan.c.totalHDMFLoanDeduction, 0).label("TotalHDMFLoanDeduction")
                )
                .select_from(EmployeeList)
                .join(Books, EmployeeList.book_id == Books.id)
                .outerjoin(subquery_cash_advance, EmployeeList.id == subquery_cash_advance.c.employee_id_id)
                .outerjoin(subquery_sss_loan, EmployeeList.id == subquery_sss_loan.c.employee_id_id)
                .outerjoin(subquery_hdmf_loan, EmployeeList.id == subquery_hdmf_loan.c.employee_id_id)
                .order_by(EmployeeList.id)
            )

            results = session.exec(final_statement)
            data = results.all()
            return data
    

    @staticmethod
    def insert_payroll_activity(
                                date_from, date_to, payroll_date, basic_pay, late, absent, undertime, 
                                normal_working_day_ot, spl_30, legal, holiday_ot, basic_pay_adjustment, 
                                gross_pay, housing_loan, sss_loan, hdmf_loan, general_loan, 
                                company_loan, other_adjustment, total_deduction, net_pay, sss, 
                                phic, hdmf, tax_withheld, books, employee_specs, employee_id_id, user,sss_provident_emp,
                                adjustment_not_taxable
                            ): # this function is for inserting payroll acitivity

        insertData = PayrollActivity(date_from=date_from,
                date_to=date_to,
                payroll_date=payroll_date,
                basic_pay=basic_pay,
                late=late,
                absent=absent,
                undertime=undertime,
                normal_working_day_ot=normal_working_day_ot,
                spl_30=spl_30,
                legal=legal,
                holiday_ot=holiday_ot,
                basic_pay_adjustment=basic_pay_adjustment,
                gross_pay=gross_pay,
                housing_loan=housing_loan,
                sss_loan=sss_loan,
                hdmf_loan=hdmf_loan,
                general_loan=general_loan,
                company_loan=company_loan,
                other_adjustment=other_adjustment,
                total_deduction=total_deduction,
                sss=sss,
                phic=phic,
                hdmf=hdmf,
                tax_withheld=tax_withheld,
                net_pay=net_pay,
                books=books,
                employee_specs=employee_specs,
                employee_id_id=employee_id_id,
                user=user,
                sss_provident_emp=sss_provident_emp,
                adjustment_not_taxable=adjustment_not_taxable)
            

        session = Session(engine)

        session.add(insertData)
        
        session.commit()

        session.close()

    @staticmethod
    def get_payroll_all(): # this function is to query for payroll activity
        with Session(engine) as session:
            try:
                # statement = select(PayrollActivity,EmployeeList,Books).where(
                #     (PayrollActivity.employee_id_id == EmployeeList.id)
                    
                # )
                statement = select(PayrollActivity, EmployeeList, Books).where(
                and_(
                    PayrollActivity.employee_id_id == EmployeeList.id,
                        EmployeeList.book_id == Books.id
                    )
                )



                         
                results = session.exec(statement) 
                data = results.all()
            
                return data
            except NoResultFound:
                return None

    @staticmethod
    def get_payroll_for_tax_comp(payroll_date,employee_id_search): # this function is to query for payroll activity
        with Session(engine) as session:
            try:
                statement = select(PayrollActivity,EmployeeList).where(
                    (PayrollActivity.employee_id_id == EmployeeList.id) 
                )

                                
                if payroll_date and employee_id_search:
                    statement = statement.where(PayrollActivity.employee_id_id == employee_id_search).where(
                        PayrollActivity.payroll_date == payroll_date
                    )
                          
                results = session.exec(statement) 
                data = results.all()
            
                return data
            except NoResultFound:
                return None

    
       

    @staticmethod
    def insert_allowance(employee_id_id, allowance, meal_allowance, developmental, holiday_rdot_pay,
                        allowance_deduction, allowance_adjustment,payroll_date, user):
        insert_data = Allowance(employee_id_id=employee_id_id, allowance=allowance, meal_allowance=meal_allowance,
                                developmental=developmental, holiday_rdot_pay=holiday_rdot_pay,
                                allowance_deduction=allowance_deduction, 
                                allowance_adjustment=allowance_adjustment,payroll_date=payroll_date,
                                user=user)
        
        session = Session(engine)
        session.add(insert_data)
        session.commit()
        session.close()

    @staticmethod
    def get_allowance_list(): # this function is to get all the employee list
        with Session(engine) as session:
            try:
                statement = select(Allowance,EmployeeList).where(
                    (Allowance.employee_id_id == EmployeeList.id)  
                )

                            
                results = session.exec(statement) 

                data = results.all()
                
                return data
            except NoResultFound:
                return None
            
    @staticmethod
    def payroll_report_monthly_testing(datefrom,dateto):
        """This function is for """
        with Session(engine) as session:



            subquery_payroll_list = (
                select(
                    PayrollActivity.employee_id_id,
                    func.sum(PayrollActivity.gross_pay).label("TotalGrossPay"),
                    func.sum(PayrollActivity.net_pay).label("NetPay"),
                    func.sum(PayrollActivity.sss).label("SSSS"),
                    func.sum(PayrollActivity.sss_provident_emp).label("SssProvidentEmp"),
                    func.sum(PayrollActivity.phic).label("Phic"),
                    func.sum(PayrollActivity.hdmf).label("Hdmf"),
                    func.sum(PayrollActivity.tax_withheld).label("TaxWithheld"),
                )
                .where(PayrollActivity.payroll_date.between(datefrom,dateto))
                .where(PayrollActivity.employee_id_id == EmployeeList.id)  # Filter by employee_id
                .group_by(PayrollActivity.employee_id_id)
                .subquery()
            )

            subquery_allowance = (
                select(
                    Allowance.employee_id_id,
                    func.sum(Allowance.allowance).label("TotalAllowance"),
                    func.sum(Allowance.meal_allowance).label("Totalmeals"),
                    func.sum(Allowance.developmental).label("AllowanceDevelopment"),
                    func.sum(Allowance.allowance_deduction).label("AllowanceDeduction")
                )
                .where(Allowance.payroll_date.between(datefrom,dateto))
                .where(Allowance.employee_id_id == EmployeeList.id)  # Filter by employee_id
                .group_by(Allowance.employee_id_id)
                .subquery()
            )

            

            final_statement = (
                select(
                    EmployeeList,
                    Books,
                    func.coalesce(subquery_payroll_list.c.TotalGrossPay, 0).label("TotalGrossPay"),
                    func.coalesce(subquery_payroll_list.c.NetPay, 0).label("NetPay"),
                    func.coalesce(subquery_payroll_list.c.SSSS, 0).label("SSSS"),
                    func.coalesce(subquery_payroll_list.c.SssProvidentEmp, 0).label("SssProvidentEmp"),
                    func.coalesce(subquery_payroll_list.c.Phic, 0).label("Phic"),
                    func.coalesce(subquery_payroll_list.c.Hdmf, 0).label("Hdmf"),
                    func.coalesce(subquery_payroll_list.c.TaxWithheld, 0).label("TaxWithheld"),
                    func.coalesce(subquery_allowance.c.TotalAllowance, 0).label("TotalAllowance"),
                    func.coalesce(subquery_allowance.c.Totalmeals, 0).label("TotalMeals"),
                    func.coalesce(subquery_allowance.c.AllowanceDevelopment, 0).label("AllowanceDevelopment"),
                    func.coalesce(subquery_allowance.c.AllowanceDeduction, 0).label("AllowanceDeduction"),
                   
                )
                .select_from(EmployeeList)
                .join(Books, EmployeeList.book_id == Books.id)
                .outerjoin(subquery_payroll_list, EmployeeList.id == subquery_payroll_list.c.employee_id_id)
                .outerjoin(subquery_allowance, EmployeeList.id == subquery_allowance.c.employee_id_id)
                
                .order_by(EmployeeList.id)
            )

            results = session.exec(final_statement)
            data = results.all()
            return data
        
    @staticmethod
    def get_payrollMonthly(datefrom: Optional[str], dateto: Optional[str], emp_id:Optional[int] = None):
        with Session(engine) as session:
            statement = select(
                EmployeeList.first_name,EmployeeList.last_name,
                func.sum(PayrollActivity.gross_pay).label("gross_pay")
            ).join(
                PayrollActivity,
                EmployeeList.id == PayrollActivity.employee_id_id
            )

            if datefrom and dateto:
                statement = statement.where(
                    PayrollActivity.payroll_date.between(datefrom, dateto)
                ).group_by(EmployeeList.id)

            if datefrom and dateto and emp_id:
                statement = statement.where(
                    PayrollActivity.payroll_date.between(datefrom, dateto),
                    PayrollActivity.employee_id_id == emp_id
                ).group_by(EmployeeList.id)

            results = session.execute(statement)
            data = results.all()

            return data
     
        # with Session(engine) as session:
           
        #     statement = select(
        #         PayrollActivity.employee_id_id,
        #             func.sum(PayrollActivity.gross_pay).label("gross_pay")
        #     )

        #     if datefrom and dateto:
        #         statement = statement.where(
        #              PayrollActivity.payroll_date.between(datefrom, dateto),
                        
        #         ).group_by(PayrollActivity.employee_id_id)

        #     if datefrom and dateto and emp_id:
        #         statement = statement.where(
        #              PayrollActivity.payroll_date.between(datefrom, dateto),
                        
        #         ).where(PayrollActivity.employee_id_id == emp_id ).group_by(PayrollActivity.employee_id_id)


        #     results = session.exec(statement)
        #     data = results.all()

        #     return data

        # return data
            # result = (
            # session.query(
            #     PayrollActivity.employee_id_id,
            #     func.sum(PayrollActivity.gross_pay)
            # )
            # .filter(
            #         PayrollActivity.payroll_date.between(datefrom, dateto)
            #     )
            #     .group_by(PayrollActivity.employee_id_id)
            #     .all()
            # )
            # return result

        

        
        
