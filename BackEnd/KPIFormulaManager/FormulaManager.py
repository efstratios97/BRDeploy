# Project Athena
'''
Owner: Efstratios Pahis
Contributors:
Description: Implements main functionality of the FormulaManager
'''

import KPIFormulaManager.Formula as fa
import KPIManager.KPIManager as kpi_m
import Utils.DataBaseUtils as db_utils
import Utils.DataBaseSQL as sql_stmt
import Utils.Settings as st
import os
import pandas as pd


class FormulaManager:

    # DataSet Object is created
    def create_formula(self, name, description, operation, purpose, kpi_families):
        formula_ID = "formula_" + st.create_id()
        formula = fa.Formula(formulaID=formula_ID, name=name, description=description,
                             operation=operation, purpose=purpose, kpi_families=kpi_families)
        self.insert_formula_db(FormulaManager, formula=formula)
        return formula

    # Creates Table (if not already exists) and then inserts data into the table
    def insert_formula_db(self, formula: fa.Formula, local=False):
        # Creates Table
        db_utils.DataBaseUtils.execute_sql(
            db_utils.DataBaseUtils, sql_statement=sql_stmt.DataBaseSQL.
            create_Formula_table_sql(sql_stmt.DataBaseSQL), local=local)
        # Inserts data
        db_utils.DataBaseUtils.execute_sql(db_utils.DataBaseUtils,
                                           sql_statement=sql_stmt.DataBaseSQL.
                                           insert_formula_values(sql_stmt.DataBaseSQL,
                                                                 formulaID=formula.get_formulaID(), name=formula.get_formula_name(),
                                                                 description=formula.get_description(), purpose=formula.get_purpose(),
                                                                 operation=formula.get_operation(), kpi_families=formula.get_kpi_families()), local=local)

    def update_kpi_family(self, kpi_families, formula_id, local=False):
        db_utils.DataBaseUtils.execute_sql(db_utils.DataBaseUtils,
                                           sql_statement=sql_stmt.DataBaseSQL.
                                           update_value(sql_stmt.DataBaseSQL, table=st.TABLE_FORMULA,
                                                        column=st.TB_FORMULA_COL_KPI_FAMILIES, value=kpi_families,
                                                        condition=st.TB_FORMULA_COL_FORMULA_ID,
                                                        condition_operator='=', condition_value=formula_id),
                                           local=local)

    def update_formula_name(self, name, formula_id, local=False):
        db_utils.DataBaseUtils.execute_sql(db_utils.DataBaseUtils,
                                           sql_statement=sql_stmt.DataBaseSQL.
                                           update_value(sql_stmt.DataBaseSQL, table=st.TABLE_FORMULA,
                                                        column=st.TB_FORMULA_COL_NAME, value=name,
                                                        condition=st.TB_FORMULA_COL_FORMULA_ID,
                                                        condition_operator='=', condition_value=formula_id),
                                           local=local)

    def get_all_formulas(self):
        data = []
        result = db_utils.DataBaseUtils.execute_sql(db_utils.DataBaseUtils,
                                                    sql_stmt.DataBaseSQL.select_all_data_from_table(
                                                        sql_stmt.DataBaseSQL, table=st.TABLE_FORMULA),
                                                    fetchall=True, local=False)
        for row in result:
            formula = self.parse_formula_obj(FormulaManager, row)
            data.append(formula)
        return data

    def get_formula_by_id(self, formula_id):
        result = db_utils.DataBaseUtils.execute_sql(db_utils.DataBaseUtils,
                                                    sql_stmt.DataBaseSQL.
                                                    select_all_from_column(
                                                        sql_stmt.DataBaseSQL, table=st.TABLE_FORMULA,
                                                        condition=st.TB_FORMULA_COL_FORMULA_ID,
                                                        condition_value=formula_id, condition_operator="="),
                                                    fetchone=True, local=False)
        formula = self.parse_formula_obj(FormulaManager, result)
        return formula

    def get_formula_by_name(self, name):

        result = db_utils.DataBaseUtils.execute_sql(db_utils.DataBaseUtils,
                                                    sql_stmt.DataBaseSQL.
                                                    select_object_by_condition(
                                                        sql_stmt.DataBaseSQL, table=st.TABLE_FORMULA,
                                                        condition=st.TB_FORMULA_COL_NAME,
                                                        condition_value=name),
                                                    fetchone=True, local=False)
        formula = self.parse_formula_obj(FormulaManager, result)
        return formula

    def get_all_formulas_by_kpi_family(self, kpi_family):
        data = []
        result = db_utils.DataBaseUtils.execute_sql(db_utils.DataBaseUtils,
                                                    sql_stmt.DataBaseSQL.
                                                    select_object_by_condition(
                                                        sql_stmt.DataBaseSQL, table=st.TABLE_FORMULA,
                                                        condition=st.TB_FORMULA_COL_KPI_FAMILIES,
                                                        condition_value=kpi_family),
                                                    fetchall=True, local=False)
        for row in result:
            formula = self.parse_formula_obj(FormulaManager, row)
            data.append(formula)
        return data

    def get_all_formulas_by_purpose(self, purpose):
        kpi_m.KPIManager.init_tables(kpi_m.KPIManager)
        data = []
        result = db_utils.DataBaseUtils.execute_sql(db_utils.DataBaseUtils,
                                                    sql_stmt.DataBaseSQL.
                                                    select_object_by_condition(
                                                        sql_stmt.DataBaseSQL, table=st.TABLE_FORMULA,
                                                        condition=st.TB_FORMULA_COL_PURPOSE,
                                                        condition_value=purpose),
                                                    fetchall=True, local=False)
        for row in result:
            formula = self.parse_formula_obj(FormulaManager, row)
            data.append(formula)
        return data

    def delete_formula(self, formula_id, local=False, condition_operator='='):
        db_utils.DataBaseUtils.execute_sql(
            db_utils.DataBaseUtils,
            sql_statement=sql_stmt.DataBaseSQL.delete_row_from_table(
                sql_stmt.DataBaseSQL, table=st.TABLE_FORMULA, condition=st.TB_FORMULA_COL_FORMULA_ID,
                condition_value=formula_id, condition_operator=condition_operator), local=local)

    def parse_formula_obj(self, db_row):
        if db_row:
            formula_id = db_row[0]
            name = db_row[1]
            descrption = db_row[2]
            operation = db_row[3]
            purpose = db_row[4]
            kpi_families = db_row[5]
            formula = fa.Formula(formulaID=formula_id, name=name, description=descrption,
                                 operation=operation, purpose=purpose, kpi_families=kpi_families)
            return formula
        pass
