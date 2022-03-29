# Project Athena
'''
Owner: Efstratios Pahis
Contributors:
Description: Implements main functionality of the KPIManager
'''

import KPIManager.KPI as kpi_obj
import DataManager.DataManager as dm
import KPIFormulaManager.FormulaManager as fa_m
import KPIManager.KPI_Category_Type as kpi_c_t
import KPIFormulaManager.Result as res
import KPIAspectManager.AspectManager as aspct_m
import Utils.DataBaseUtils as db_utils
import Utils.DataBaseSQL as sql_stmt
import Utils.Settings as st


class KPIManager:

    # DataSet Object is created
    def create_kpi(self, name, description, high_level_kpi_component_kpi_weight, kpi_aspects_weights,
                   threshold, formula, dataset_id, dataset_labels, kpi_family, color_coding):
        kpi_ID = "kpi_" + st.create_id()
        kpi = kpi_obj.KPI(kpiID=kpi_ID, name=name, description=description, high_level_kpi_component_kpi_weight=high_level_kpi_component_kpi_weight,
                          kpi_aspects_weights=kpi_aspects_weights, threshold=threshold, formula=formula,
                          dataset_id=dataset_id, dataset_labels=dataset_labels, kpi_family=kpi_family, color_coding=color_coding)
        self.insert_kpi_db(KPIManager, kpi=kpi)
        formula = fa_m.FormulaManager.get_formula_by_name(
            fa_m.FormulaManager, name=formula)
        self.insert_kpi_formula_relation_db(
            KPIManager, kpi=kpi, formula_id=formula.get_formulaID())
        return kpi

    # Creates Table (if not already exists) and then inserts data into the table
    def insert_kpi_db(self, kpi: kpi_obj.KPI, local=False):
        # Creates Table
        db_utils.DataBaseUtils.execute_sql(
            db_utils.DataBaseUtils, sql_statement=sql_stmt.DataBaseSQL.
            create_KPI_table_sql(sql_stmt.DataBaseSQL), local=local)
        # Inserts data
        db_utils.DataBaseUtils.execute_sql(db_utils.DataBaseUtils,
                                           sql_statement=sql_stmt.DataBaseSQL.
                                           insert_kpi_values(sql_stmt.DataBaseSQL,
                                                             kpiID=kpi.get_KPIID(), name=kpi.get_KPI_name(), description=kpi.get_description(),
                                                             high_level_kpi_component_weight=kpi.get_high_level_kpi_component_kpi_weight(),
                                                             kpi_aspects_weights=kpi.get_kpi_aspects_weights(), threshold=kpi.get_threshold(),
                                                             formula=kpi.get_formula(), dataset_id=kpi.get_dataset_id(), dataset_labels=kpi.get_dataset_labels(),
                                                             kpi_family=kpi.get_kpi_family(), color_coding=kpi.get_color_coding()), local=local)

    def init_tables(self, local=False):
        db_utils.DataBaseUtils.execute_sql(
            db_utils.DataBaseUtils, sql_statement=sql_stmt.DataBaseSQL.
            create_KPI_table_sql(sql_stmt.DataBaseSQL), local=local)
        db_utils.DataBaseUtils.execute_sql(
            db_utils.DataBaseUtils, sql_statement=sql_stmt.DataBaseSQL.
            create_Formula_table_sql(sql_stmt.DataBaseSQL), local=local)
        db_utils.DataBaseUtils.execute_sql(
            db_utils.DataBaseUtils, sql_statement=sql_stmt.DataBaseSQL.
            create_KPI_Category_Type_table_sql(sql_stmt.DataBaseSQL), local=local)
        db_utils.DataBaseUtils.execute_sql(
            db_utils.DataBaseUtils, sql_statement=sql_stmt.DataBaseSQL.
            create_ASPECT_table_sql(sql_stmt.DataBaseSQL), local=local)
        db_utils.DataBaseUtils.execute_sql(
            db_utils.DataBaseUtils, sql_statement=sql_stmt.DataBaseSQL.
            create_KPI_ASPECT_WEIGHT_relation_table_sql(sql_stmt.DataBaseSQL), local=local)
        db_utils.DataBaseUtils.execute_sql(
            db_utils.DataBaseUtils, sql_statement=sql_stmt.DataBaseSQL.
            create_Aspect_Formula_relation_table_sql(sql_stmt.DataBaseSQL), local=local)
        db_utils.DataBaseUtils.execute_sql(
            db_utils.DataBaseUtils, sql_statement=sql_stmt.DataBaseSQL.
            create_KPI_Formula_relation_table_sql(sql_stmt.DataBaseSQL), local=local)
        res.Result.create_result_table(res.Result)
        try:

            fa_m.FormulaManager.create_formula(fa_m.FormulaManager, name="EAM KPIs des BR nach Lederle",
                                               description="EAM interne KPIs", operation="BR_EAM_KPI_Formel_J_LEDERLE",
                                               purpose=st.FORMULA_PURPOSE_KPI, kpi_families="EAM BR")
        except:
            print(
                "alreay_initiated_BR_EAM_KPI_Formel_J_LEDERLE")
        try:
            fa_m.FormulaManager.create_formula(fa_m.FormulaManager, name="EAM Aspects des BR nach Lederle",
                                               description="EAM interne Apects für KPIS", operation="BR_EAM_ASPECT_Formel_J_LEDERLE",
                                               purpose=st.FORMULA_PURPOSE_ASPECT, kpi_families="EAM BR")
        except:
            print(
                "alreay_initiated_BR_EAM_ASPECT_Formel_J_LEDERLE")
        try:
            fa_m.FormulaManager.create_formula(fa_m.FormulaManager, name="EAM Aspects des BR nach Lederle (Scale max value Adjusted to Department)",
                                               description="EAM interne Apects für KPIS", operation="BR_EAM_ASPECT_Formel_J_LEDERLE_scale_adj_to_department",
                                               purpose=st.FORMULA_PURPOSE_ASPECT, kpi_families="EAM BR")
        except:
            print(
                "alreay_initiated_BR_EAM_ASPECT_Formel_J_LEDERLE_scale_adj_to_department")
        kpi_category_types = {"category_1": st.ASPECT_OPERATION_TYPE_COUNT,
                              "category_2": st.ASPECT_OPERATION_TYPE_CATEGORICAL_3_SCALE,
                              "category_3": st.ASPECT_OPERATION_TYPE_CATEGORICAL_5_SCALE,
                              "category_4": st.ASPECT_OPERATION_TYPE_CATEGORICAL_LIFE_CYCLE_END}
        for k, v in kpi_category_types.items():
            try:
                kpi_category_type = kpi_c_t.KPI_CATEGORY_TYPE(k, v)
                db_utils.DataBaseUtils.execute_sql(db_utils.DataBaseUtils,
                                                   sql_statement=sql_stmt.DataBaseSQL.
                                                   insert_kpi_category_type_values(sql_stmt.DataBaseSQL,
                                                                                   kpi_category_type_id=kpi_category_type.get_kpi_category_type_id(),
                                                                                   name=kpi_category_type.get_name()), local=local)
            except:
                print("alreay_initiated_tables_and_values")

    def insert_kpi_formula_relation_db(self, kpi: kpi_obj.KPI, formula_id, local=False):
        # Creates Table
        self.init_tables(KPIManager)
        db_utils.DataBaseUtils.execute_sql(
            db_utils.DataBaseUtils, sql_statement=sql_stmt.DataBaseSQL.
            create_KPI_Formula_relation_table_sql(sql_stmt.DataBaseSQL), local=local)
        # Inserts data
        # for formula in kpi.get_formula().split(','):
        db_utils.DataBaseUtils.execute_sql(
            db_utils.DataBaseUtils, sql_statement=sql_stmt.DataBaseSQL.
            insert_kpi_formula_relation_values(
                sql_stmt.DataBaseSQL, kpi_id=kpi.get_KPIID(), formula_id=formula_id),
            local=local)

    # Currently not in use
    def insert_kpi_aspect_weight_relation_db(self, kpi: kpi_obj.KPI, local=False):
        # Creates Table
        self.init_tables(KPIManager)
        db_utils.DataBaseUtils.execute_sql(
            db_utils.DataBaseUtils, sql_statement=sql_stmt.DataBaseSQL.
            create_KPI_ASPECT_WEIGHT_relation_table_sql(sql_stmt.DataBaseSQL), local=local)
        # Inserts data
        # for formula in kpi.get_formula().split(','):
        for aspect, weight in kpi.get_kpi_aspects_weights():
            db_utils.DataBaseUtils.execute_sql(
                db_utils.DataBaseUtils, sql_statement=sql_stmt.DataBaseSQL.
                insert_kpi_aspect_relation_values(
                    sql_stmt.DataBaseSQL, kpi_id=kpi.get_KPIID(), aspect_id=aspect, weight=weight),
                local=local)

    def update_kpi(self, kpi: kpi_obj.KPI):
        kpi_id = kpi.get_KPIID()
        self.update_kpi_dataset_labels(
            KPIManager, kpi_id=kpi_id, dataset_labels=kpi.get_dataset_labels())
        self.update_high_level_kpi_component_kpi_weight(
            KPIManager, kpi_id=kpi_id, high_level_kpi_component_kpi_weight=kpi.get_high_level_kpi_component_kpi_weight())
        self.update_kpi_aspect_weights(
            KPIManager, kpi_id=kpi_id, kpi_aspects_weights=kpi.get_kpi_aspects_weights())
        self.update_kpi_family(KPIManager, kpi_id=kpi_id,
                               kpi_family=kpi.get_kpi_family())
        self.update_kpi_formula(
            KPIManager, kpi_id=kpi_id, formula=kpi.get_formula())
        self.update_kpi_name(KPIManager, kpi_id=kpi_id,
                             name=kpi.get_KPI_name())
        self.update_threshold(KPIManager, kpi_id=kpi_id,
                              threshold=kpi.get_threshold())
        self.update_kpi_description(
            KPIManager, kpi_id=kpi_id, description=kpi.get_description())
        self.update_kpi_color_coding(
            KPIManager, kpi_id=kpi_id, color_coding=kpi.get_color_coding())

    def update_kpi_dataset_labels(self, dataset_labels, kpi_id, local=False):
        db_utils.DataBaseUtils.execute_sql(db_utils.DataBaseUtils,
                                           sql_statement=sql_stmt.DataBaseSQL.
                                           update_value(sql_stmt.DataBaseSQL, table=st.TABLE_KPI,
                                                        column=st.TB_KPI_COL_DATASET_LABELS, value=dataset_labels,
                                                        condition=st.TB_KPI_COL_KPI_ID,
                                                        condition_operator='=', condition_value=kpi_id),
                                           local=local)

    def update_threshold(self, threshold, kpi_id, local=False):
        db_utils.DataBaseUtils.execute_sql(db_utils.DataBaseUtils,
                                           sql_statement=sql_stmt.DataBaseSQL.
                                           update_value(sql_stmt.DataBaseSQL, table=st.TABLE_KPI,
                                                        column=st.TB_KPI_COL_THRESHOLD, value=threshold,
                                                        condition=st.TB_KPI_COL_KPI_ID,
                                                        condition_operator='=', condition_value=kpi_id),
                                           local=local)

    def update_kpi_aspect_weights(self, kpi_aspects_weights, kpi_id, local=False):
        db_utils.DataBaseUtils.execute_sql(db_utils.DataBaseUtils,
                                           sql_statement=sql_stmt.DataBaseSQL.
                                           update_value(sql_stmt.DataBaseSQL, table=st.TABLE_KPI,
                                                        column=st.TB_KPI_COL_KPI_ASPECTS_WEIGHTS, value=kpi_aspects_weights,
                                                        condition=st.TB_KPI_COL_KPI_ID,
                                                        condition_operator='=', condition_value=kpi_id),
                                           local=local)

    def update_high_level_kpi_component_kpi_weight(self, high_level_kpi_component_kpi_weight, kpi_id, local=False):
        db_utils.DataBaseUtils.execute_sql(db_utils.DataBaseUtils,
                                           sql_statement=sql_stmt.DataBaseSQL.
                                           update_value(sql_stmt.DataBaseSQL, table=st.TABLE_KPI,
                                                        column=st.TB_KPI_COL_HIGH_LEVEL_KPI_COMPONENT_KPI_WEIGHT, value=high_level_kpi_component_kpi_weight,
                                                        condition=st.TB_KPI_COL_KPI_ID,
                                                        condition_operator='=', condition_value=kpi_id),
                                           local=local)

    def update_kpi_family(self, kpi_family, kpi_id, local=False):
        db_utils.DataBaseUtils.execute_sql(db_utils.DataBaseUtils,
                                           sql_statement=sql_stmt.DataBaseSQL.
                                           update_value(sql_stmt.DataBaseSQL, table=st.TABLE_KPI,
                                                        column=st.TB_KPI_COL_KPI_FAMILY, value=kpi_family,
                                                        condition=st.TB_KPI_COL_KPI_ID,
                                                        condition_operator='=', condition_value=kpi_id),
                                           local=local)

    def update_kpi_name(self, name, kpi_id, local=False):
        db_utils.DataBaseUtils.execute_sql(db_utils.DataBaseUtils,
                                           sql_statement=sql_stmt.DataBaseSQL.
                                           update_value(sql_stmt.DataBaseSQL, table=st.TABLE_KPI,
                                                        column=st.TB_KPI_COL_NAME, value=name,
                                                        condition=st.TB_KPI_COL_KPI_ID,
                                                        condition_operator='=', condition_value=kpi_id),
                                           local=local)

    def update_kpi_description(self, description, kpi_id, local=False):
        db_utils.DataBaseUtils.execute_sql(db_utils.DataBaseUtils,
                                           sql_statement=sql_stmt.DataBaseSQL.
                                           update_value(sql_stmt.DataBaseSQL, table=st.TABLE_KPI,
                                                        column=st.TB_KPI_COL_DESCRIPTION, value=description,
                                                        condition=st.TB_KPI_COL_KPI_ID,
                                                        condition_operator='=', condition_value=kpi_id),
                                           local=local)

    def update_kpi_formula(self, formula, kpi_id, local=False):
        db_utils.DataBaseUtils.execute_sql(db_utils.DataBaseUtils,
                                           sql_statement=sql_stmt.DataBaseSQL.
                                           update_value(sql_stmt.DataBaseSQL, table=st.TABLE_KPI,
                                                        column=st.TB_KPI_COL_FORMULA, value=formula,
                                                        condition=st.TB_KPI_COL_KPI_ID,
                                                        condition_operator='=', condition_value=kpi_id),
                                           local=local)

    def update_kpi_color_coding(self, color_coding, kpi_id, local=False):
        db_utils.DataBaseUtils.execute_sql(db_utils.DataBaseUtils,
                                           sql_statement=sql_stmt.DataBaseSQL.
                                           update_value(sql_stmt.DataBaseSQL, table=st.TABLE_KPI,
                                                        column=st.TB_KPI_COL_COLOR_CODING, value=color_coding,
                                                        condition=st.TB_KPI_COL_KPI_ID,
                                                        condition_operator='=', condition_value=kpi_id),
                                           local=local)

    def get_kpi_by_id(self, kpi_id):
        result = db_utils.DataBaseUtils.execute_sql(db_utils.DataBaseUtils,
                                                    sql_stmt.DataBaseSQL.
                                                    select_object_by_condition(
                                                        sql_stmt.DataBaseSQL, table=st.TABLE_KPI,
                                                        condition=st.TB_KPI_COL_KPI_ID,
                                                        condition_value=kpi_id),
                                                    fetchone=True, local=False)
        kpi = self.parse_kpi_obj(KPIManager, result)
        return kpi

    def get_kpi_by_name(self, name):
        result = db_utils.DataBaseUtils.execute_sql(db_utils.DataBaseUtils,
                                                    sql_stmt.DataBaseSQL.
                                                    select_object_by_condition(
                                                        sql_stmt.DataBaseSQL, table=st.TABLE_KPI,
                                                        condition=st.TB_KPI_COL_NAME,
                                                        condition_value=name),
                                                    fetchone=True, local=False)
        kpi = self.parse_kpi_obj(KPIManager, result)
        return kpi

    def get_all_kpis(self):
        data = []
        result = db_utils.DataBaseUtils.execute_sql(db_utils.DataBaseUtils,
                                                    sql_stmt.DataBaseSQL.select_all_data_from_table(
                                                        sql_stmt.DataBaseSQL, table=st.TABLE_KPI),
                                                    fetchall=True, local=False)
        for row in result:
            kpi = self.parse_kpi_obj(KPIManager, row)
            data.append(kpi)
        return data

    def get_all_kpi_category_types(self):
        self.init_tables(KPIManager)
        data = []
        result = db_utils.DataBaseUtils.execute_sql(db_utils.DataBaseUtils,
                                                    sql_stmt.DataBaseSQL.select_all_data_from_table(
                                                        sql_stmt.DataBaseSQL, table=st.TABLE_KPI_CATEGORY_TYPE),
                                                    fetchall=True, local=False)
        for row in result:
            kpi_category_type = self.parse_kpi_category_type_obj(
                KPIManager, row)
            data.append(kpi_category_type)
        return data

    def get_suitable_kpi_category_types(self, raw_component, dataset_id, dataset_label):
        self.init_tables(KPIManager)
        data = []
        dataset_id = dm.DataManager.check_dataset_exists_and_return_alternative_based_on_label(
            dm.DataManager, dataset_id=dataset_id, dataset_label=dataset_label)
        dataset_data = dm.DataManager.get_table_as_df(
            dm.DataManager, dataset_id)
        if any("," in element for element in dataset_data[raw_component].tolist()):
            result = db_utils.DataBaseUtils.execute_sql(db_utils.DataBaseUtils,
                                                        sql_stmt.DataBaseSQL.
                                                        select_object_by_condition(
                                                            sql_stmt.DataBaseSQL, table=st.TABLE_KPI_CATEGORY_TYPE,
                                                            condition=st.TB_KPI_COL_NAME,
                                                            condition_value=st.ASPECT_OPERATION_TYPE_COUNT),
                                                        fetchall=True, local=False)
        elif (("Niedrig" in str(dataset_data[raw_component].tolist()) or
               ("Mittel" in str(dataset_data[raw_component].tolist())) or
               ("Hoch" in str(dataset_data[raw_component].tolist()))) and not
              (("Normal" in str(dataset_data[raw_component].tolist())) or
                ("Sehr" in str(dataset_data[raw_component].tolist())))):
            result = db_utils.DataBaseUtils.execute_sql(db_utils.DataBaseUtils,
                                                        sql_stmt.DataBaseSQL.
                                                        select_object_by_condition(
                                                            sql_stmt.DataBaseSQL, table=st.TABLE_KPI_CATEGORY_TYPE,
                                                            condition=st.TB_KPI_COL_NAME,
                                                            condition_value=st.ASPECT_OPERATION_TYPE_CATEGORICAL_3_SCALE),
                                                        fetchall=True, local=False)
        elif (("Normal" in str(dataset_data[raw_component].tolist())) or
              ("Sehr" in str(dataset_data[raw_component].tolist()))):
            result = db_utils.DataBaseUtils.execute_sql(db_utils.DataBaseUtils,
                                                        sql_stmt.DataBaseSQL.
                                                        select_object_by_condition(
                                                            sql_stmt.DataBaseSQL, table=st.TABLE_KPI_CATEGORY_TYPE,
                                                            condition=st.TB_KPI_COL_NAME,
                                                            condition_value=st.ASPECT_OPERATION_TYPE_CATEGORICAL_5_SCALE),
                                                        fetchall=True, local=False)
        else:
            result = db_utils.DataBaseUtils.execute_sql(db_utils.DataBaseUtils,
                                                        sql_stmt.DataBaseSQL.select_all_data_from_table(
                                                            sql_stmt.DataBaseSQL, table=st.TABLE_KPI_CATEGORY_TYPE),
                                                        fetchall=True, local=False)
        for row in result:
            kpi_category_type = self.parse_kpi_category_type_obj(
                KPIManager, row)
            data.append(kpi_category_type)
        return data

    def get_aspects_by_kpi_id(self, kpi_id):
        result = []
        kpi = self.get_kpi_by_id(KPIManager, kpi_id=kpi_id)
        aspects = [val for sublist in kpi.get_kpi_aspects_weights()
                   for val in sublist]
        for aspect_name in aspects:
            aspect = aspct_m.AspectManager.get_aspect_by_name(
                aspct_m.AspectManager, name=aspect_name)
            result.append(aspect)
        return result

    def get_all_kpis_by_dataset_label(self, dataset_label):
        data = []
        result = db_utils.DataBaseUtils.execute_sql(db_utils.DataBaseUtils,
                                                    sql_stmt.DataBaseSQL.select_all_data_from_table(
                                                        sql_stmt.DataBaseSQL, table=st.TABLE_KPI),
                                                    fetchall=True, local=False)
        dataset_label = dm.DataManager.get_label_by_name(
            dm.DataManager, name=dataset_label)
        for row in result:
            kpi = self.parse_kpi_obj(KPIManager, row)
            if dataset_label.get_labelID() in kpi.get_dataset_labels():
                data.append(kpi)
        return data

    def get_suitable_formula(self, kpi_id, local=False):
        result = db_utils.DataBaseUtils.execute_sql(db_utils.DataBaseUtils,
                                                    sql_statement=sql_stmt.DataBaseSQL.
                                                    select_all_from_column(sql_stmt.DataBaseSQL, table=st.TABLE_KPI_FORMULA_RELATION,
                                                                           condition=st.TB_KPI_COL_KPI_ID,
                                                                           condition_operator='=', condition_value=kpi_id),
                                                    fetchone=True, local=local)
        formula = fa_m.FormulaManager.get_formula_by_id(
            fa_m.FormulaManager, result[1])
        return formula

    def delete_kpi(self, kpi_id, local=False, condition_operator='='):
        db_utils.DataBaseUtils.execute_sql(
            db_utils.DataBaseUtils,
            sql_statement=sql_stmt.DataBaseSQL.delete_row_from_table(
                sql_stmt.DataBaseSQL, table=st.TABLE_KPI, condition=st.TB_KPI_COL_KPI_ID,
                condition_value=kpi_id, condition_operator=condition_operator), local=local)

    def parse_kpi_obj(self, db_row):
        if db_row:
            kpi_id = db_row[0]
            name = db_row[1]
            descrption = db_row[2]
            high_level_kpi_component_kpi_weight = db_row[3]
            kpi_aspects_weights = db_row[4]
            threshold = db_row[5]
            formula = db_row[6]
            dataset_id = db_row[7]
            dataset_labels = db_row[8]
            kpi_family = db_row[9]
            color_coding = db_row[10]
            kpi = kpi_obj.KPI(kpiID=kpi_id, name=name, description=descrption,
                              high_level_kpi_component_kpi_weight=high_level_kpi_component_kpi_weight,
                              kpi_aspects_weights=kpi_aspects_weights, threshold=threshold,
                              formula=formula, dataset_id=dataset_id, dataset_labels=dataset_labels,
                              kpi_family=kpi_family, color_coding=color_coding)
            return kpi
        pass

    def parse_kpi_category_type_obj(self, db_row):
        if db_row:
            kpi_category_type_id = db_row[0]
            name = db_row[1]
            kpi_category_type = kpi_c_t.KPI_CATEGORY_TYPE(
                kpi_category_type_id=kpi_category_type_id, name=name)
            return kpi_category_type
        pass
