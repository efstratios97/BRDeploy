# Project Athena
'''
Owner: Efstratios Pahis
Contributors:
Description: Implements main functionality of the AspectManager
'''

import KPIAspectManager.Aspect as aspct
import DataManager.DataManager as dm
import KPIFormulaManager.FormulaManager as fa_m
import KPIManager.KPIManager as kpi_m
import Utils.DataBaseUtils as db_utils
import Utils.DataBaseSQL as sql_stmt
import Utils.Settings as st
import BRIndividual.Utils.SettingsBR as st_br
import KPIFormulaManager.FormulaExecutor as fa_e
import os
import pandas as pd


class AspectManager:

    # DataSet Object is created
    def create_aspect(self, name, description, raw_components_from_dataset, skala_size,
                      weight, threshold, operation_type, formula, dataset_id, dataset_labels, kpi_family):
        aspect_id = "aspect_" + st.create_id()
        aspect = aspct.ASPECT(aspect_id=aspect_id, name=name, description=description,
                              raw_components_from_dataset=raw_components_from_dataset, skala_size=skala_size,
                              weight=weight, threshold=threshold, operation_type=operation_type, formula=formula,
                              dataset_id=dataset_id, dataset_labels=dataset_labels, kpi_family=kpi_family)
        self.insert_aspect_db(AspectManager, aspect=aspect)
        formula = fa_m.FormulaManager.get_formula_by_name(
            fa_m.FormulaManager, name=formula)
        self.insert_aspect_formula_relation_db(
            AspectManager, aspect=aspect, formula_id=formula.get_formulaID())
        return aspect

    # Creates Table (if not already exists) and then inserts data into the table
    def insert_aspect_db(self, aspect: aspct.ASPECT, local=False):
        # Creates Table
        kpi_m.KPIManager.init_tables(kpi_m.KPIManager)
        db_utils.DataBaseUtils.execute_sql(
            db_utils.DataBaseUtils, sql_statement=sql_stmt.DataBaseSQL.
            create_ASPECT_table_sql(sql_stmt.DataBaseSQL), local=local)
        db_utils.DataBaseUtils.execute_sql(
            db_utils.DataBaseUtils, sql_statement=sql_stmt.DataBaseSQL.
            create_KPI_ASPECT_WEIGHT_relation_table_sql(sql_stmt.DataBaseSQL), local=local)
        # Inserts data
        db_utils.DataBaseUtils.execute_sql(db_utils.DataBaseUtils,
                                           sql_statement=sql_stmt.DataBaseSQL.
                                           insert_aspect_values(sql_stmt.DataBaseSQL,
                                                                aspect_id=aspect.get_aspectID(), name=aspect.get_name(), description=aspect.get_description(),
                                                                raw_components_from_dataset=aspect.get_raw_components_from_dataset(), operation_type=aspect.get_operation_type(),
                                                                skala_size=aspect.get_skala_size(), weight=aspect.get_weight(), threshold=aspect.get_threshold(),
                                                                formula=aspect.get_formula(), dataset_id=aspect.get_dataset_id(), dataset_labels=aspect.get_dataset_labels(),
                                                                kpi_family=aspect.get_kpi_family()), local=local)

    def insert_aspect_formula_relation_db(self, aspect: aspct.ASPECT, formula_id, local=False):
        # Creates Table
        kpi_m.KPIManager.init_tables(kpi_m.KPIManager)
        db_utils.DataBaseUtils.execute_sql(
            db_utils.DataBaseUtils, sql_statement=sql_stmt.DataBaseSQL.
            create_Aspect_Formula_relation_table_sql(sql_stmt.DataBaseSQL), local=local)
        # Inserts data
        # for formula in kpi.get_formula().split(','):
        db_utils.DataBaseUtils.execute_sql(
            db_utils.DataBaseUtils, sql_statement=sql_stmt.DataBaseSQL.
            insert_aspect_formula_relation_values(
                sql_stmt.DataBaseSQL, aspect_id=aspect.get_aspectID(), formula_id=formula_id),
            local=local)

    def update_aspect(self, aspect: aspct.ASPECT, local=False):
        aspect_id = aspect.get_aspectID()
        self.update_aspect_dataset_labels(
            AspectManager, dataset_labels=aspect.get_dataset_labels(), aspect_id=aspect_id, local=local)
        self.update_aspect_name(
            AspectManager, name=aspect.get_name(), aspect_id=aspect_id, local=local)
        self.update_aspect_formula(
            AspectManager, formula=aspect.get_formula(), aspect_id=aspect_id, local=local)
        self.update_raw_components_from_dataset(
            AspectManager, raw_components_from_dataset=aspect.get_raw_components_from_dataset(), aspect_id=aspect_id, local=local)
        self.update_skala_size(
            AspectManager, skala_size=aspect.get_skala_size(), aspect_id=aspect_id, local=local)

    def update_aspect_dataset_labels(self, dataset_labels, aspect_id, local=False):
        db_utils.DataBaseUtils.execute_sql(db_utils.DataBaseUtils,
                                           sql_statement=sql_stmt.DataBaseSQL.
                                           update_value(sql_stmt.DataBaseSQL, table=st.TABLE_ASPECT,
                                                        column=st.TB_ASPECT_COL_DATASET_LABELS, value=dataset_labels,
                                                        condition=st.TB_ASPECT_COL_ID,
                                                        condition_operator='=', condition_value=aspect_id),
                                           local=local)

    def update_threshold(self, threshold, aspect_id, local=False):
        db_utils.DataBaseUtils.execute_sql(db_utils.DataBaseUtils,
                                           sql_statement=sql_stmt.DataBaseSQL.
                                           update_value(sql_stmt.DataBaseSQL, table=st.TABLE_ASPECT,
                                                        column=st.TB_ASPECT_COL_THRESHOLD, value=threshold,
                                                        condition=st.TB_ASPECT_COL_ID,
                                                        condition_operator='=', condition_value=aspect_id),
                                           local=local)

    def update_skala_size(self, skala_size, aspect_id, local=False):
        db_utils.DataBaseUtils.execute_sql(db_utils.DataBaseUtils,
                                           sql_statement=sql_stmt.DataBaseSQL.
                                           update_value(sql_stmt.DataBaseSQL, table=st.TABLE_ASPECT,
                                                        column=st.TB_ASPECT_COL_SKALA_SIZE, value=skala_size,
                                                        condition=st.TB_ASPECT_COL_ID,
                                                        condition_operator='=', condition_value=aspect_id),
                                           local=local)

    def update_kpi_family(self, kpi_family, aspect_id, local=False):
        db_utils.DataBaseUtils.execute_sql(db_utils.DataBaseUtils,
                                           sql_statement=sql_stmt.DataBaseSQL.
                                           update_value(sql_stmt.DataBaseSQL, table=st.TABLE_ASPECT,
                                                        column=st.TB_ASPECT_COL_KPI_FAMILY, value=kpi_family,
                                                        condition=st.TB_ASPECT_COL_ID,
                                                        condition_operator='=', condition_value=aspect_id),
                                           local=local)

    def update_aspect_name(self, name, aspect_id, local=False):
        db_utils.DataBaseUtils.execute_sql(db_utils.DataBaseUtils,
                                           sql_statement=sql_stmt.DataBaseSQL.
                                           update_value(sql_stmt.DataBaseSQL, table=st.TABLE_ASPECT,
                                                        column=st.TB_ASPECT_COL_NAME, value=name,
                                                        condition=st.TB_ASPECT_COL_ID,
                                                        condition_operator='=', condition_value=aspect_id),
                                           local=local)

    def update_aspect_formula(self, formula, aspect_id, local=False):
        db_utils.DataBaseUtils.execute_sql(db_utils.DataBaseUtils,
                                           sql_statement=sql_stmt.DataBaseSQL.
                                           update_value(sql_stmt.DataBaseSQL, table=st.TABLE_ASPECT,
                                                        column=st.TB_ASPECT_COL_FORMULA, value=formula,
                                                        condition=st.TB_ASPECT_COL_ID,
                                                        condition_operator='=', condition_value=aspect_id),
                                           local=local)

    def update_weight(self, weight, aspect_id, local=False):
        db_utils.DataBaseUtils.execute_sql(db_utils.DataBaseUtils,
                                           sql_statement=sql_stmt.DataBaseSQL.
                                           update_value(sql_stmt.DataBaseSQL, table=st.TABLE_ASPECT,
                                                        column=st.TB_ASPECT_COL_WEIGHT, value=weight,
                                                        condition=st.TB_ASPECT_COL_ID,
                                                        condition_operator='=', condition_value=aspect_id),
                                           local=local)

    def update_raw_components_from_dataset(self, raw_components_from_dataset, aspect_id, local=False):
        db_utils.DataBaseUtils.execute_sql(db_utils.DataBaseUtils,
                                           sql_statement=sql_stmt.DataBaseSQL.
                                           update_value(sql_stmt.DataBaseSQL, table=st.TABLE_ASPECT,
                                                        column=st.TB_ASPECT_COL_RAW_COMPONENTS_FROM_DATASET,
                                                        value=raw_components_from_dataset,
                                                        condition=st.TB_ASPECT_COL_ID,
                                                        condition_operator='=', condition_value=aspect_id),
                                           local=local)

    def update_operation_type(self, operation_type, aspect_id, local=False):
        db_utils.DataBaseUtils.execute_sql(db_utils.DataBaseUtils,
                                           sql_statement=sql_stmt.DataBaseSQL.
                                           update_value(sql_stmt.DataBaseSQL, table=st.TABLE_ASPECT,
                                                        column=st.TB_ASPECT_COL_OPERATION_TYPE, value=operation_type,
                                                        condition=st.TB_ASPECT_COL_ID,
                                                        condition_operator='=', condition_value=aspect_id),
                                           local=local)

    def get_aspect_by_id(self, aspect_id):
        result = db_utils.DataBaseUtils.execute_sql(db_utils.DataBaseUtils,
                                                    sql_stmt.DataBaseSQL.
                                                    select_object_by_condition(
                                                        sql_stmt.DataBaseSQL, table=st.TABLE_ASPECT,
                                                        condition=st.TB_ASPECT_COL_ID,
                                                        condition_value=aspect_id),
                                                    fetchone=True, local=False)
        aspect = self.parse_aspect_obj(AspectManager, result)
        return aspect

    def get_aspect_by_name(self, name):
        result = db_utils.DataBaseUtils.execute_sql(db_utils.DataBaseUtils,
                                                    sql_stmt.DataBaseSQL.
                                                    select_object_by_condition(
                                                        sql_stmt.DataBaseSQL, table=st.TABLE_ASPECT,
                                                        condition=st.TB_ASPECT_COL_NAME,
                                                        condition_value=name),
                                                    fetchone=True, local=False)
        aspect = self.parse_aspect_obj(AspectManager, result)
        return aspect

    def get_all_aspects(self):
        data = []
        result = db_utils.DataBaseUtils.execute_sql(db_utils.DataBaseUtils,
                                                    sql_stmt.DataBaseSQL.select_all_data_from_table(
                                                        sql_stmt.DataBaseSQL, table=st.TABLE_ASPECT),
                                                    fetchall=True, local=False)
        for row in result:
            aspect = self.parse_aspect_obj(AspectManager, row)
            data.append(aspect)
        return data

    def get_all_aspects_by_dataset_label(self, dataset_label):
        data = []
        result = db_utils.DataBaseUtils.execute_sql(db_utils.DataBaseUtils,
                                                    sql_stmt.DataBaseSQL.select_all_data_from_table(
                                                        sql_stmt.DataBaseSQL, table=st.TABLE_ASPECT),
                                                    fetchall=True, local=False)
        dataset_label = dm.DataManager.get_label_by_name(
            dm.DataManager, name=dataset_label)
        for row in result:
            aspect = self.parse_aspect_obj(AspectManager, row)
            if dataset_label.get_labelID() in aspect.get_dataset_labels():
                data.append(aspect)
        return data

    def get_raw_components_from_dataset(self, dataset_id="", dataset_label=""):
        kpi_m.KPIManager.init_tables(kpi_m.KPIManager)
        if dataset_id == "":
            dataset_tmp = dm.DataManager.get_newest_dataset_replacement_by_dataset_label(
                dm.DataManager, dataset_label=dataset_label)
            dataset_id = dataset_tmp.get_datasetID()
        dataset_data = dm.DataManager.get_table_as_df(
            dm.DataManager, table=dataset_id)
        raw_components = dataset_data.columns.values.tolist()
        return raw_components

    def get_suitable_formula(self, aspect_id, local=False):
        result = db_utils.DataBaseUtils.execute_sql(db_utils.DataBaseUtils,
                                                    sql_statement=sql_stmt.DataBaseSQL.
                                                    select_all_from_column(sql_stmt.DataBaseSQL, table=st.TABLE_ASPECT_FORMULA_RELATION,
                                                                           condition=st.TB_ASPECT_COL_ID,
                                                                           condition_operator='=', condition_value=aspect_id),
                                                    fetchone=True, local=local)
        formula = fa_m.FormulaManager.get_formula_by_id(
            fa_m.FormulaManager, result[1])
        return formula

    def delete_aspect(self, aspect_id, local=False, condition_operator='='):
        db_utils.DataBaseUtils.execute_sql(
            db_utils.DataBaseUtils,
            sql_statement=sql_stmt.DataBaseSQL.delete_row_from_table(
                sql_stmt.DataBaseSQL, table=st.TABLE_ASPECT, condition=st.TB_ASPECT_COL_ID,
                condition_value=aspect_id, condition_operator=condition_operator), local=local)

    def parse_aspect_obj(self, db_row):
        if db_row:
            aspect_id = db_row[0]
            name = db_row[1]
            descrption = db_row[2]
            raw_components_from_dataset = db_row[3]
            skala_size = db_row[4]
            weight = db_row[5]
            threshold = db_row[6]
            operation_type = db_row[7]
            formula = db_row[8]
            dataset_id = db_row[9]
            dataset_labels = db_row[10]
            kpi_family = db_row[11]
            aspect = aspct.ASPECT(aspect_id=aspect_id, name=name, description=descrption,
                                  raw_components_from_dataset=raw_components_from_dataset,
                                  skala_size=skala_size, weight=weight, threshold=threshold,
                                  operation_type=operation_type, formula=formula, dataset_id=dataset_id,
                                  dataset_labels=dataset_labels, kpi_family=kpi_family)
            return aspect
        pass
