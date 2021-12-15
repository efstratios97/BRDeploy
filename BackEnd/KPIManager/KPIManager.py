# Project Athena
'''
Owner: Efstratios Pahis
Contributors:
Description: Implements main functionality of the KPIManager
'''

import KPIManager.KPI as kpi_obj
import DataManager.DataManager as dm
import KPIFormulaManager.FormulaManager as fa_m
import KPIFormulaManager.FormulaExecutor as fa_e
import KPIManager.KPI_Category_Type as kpi_c_t
import KPIFormulaManager.Result as res
import KPIAspectManager.AspectManager as aspct_m
import Utils.DataBaseUtils as db_utils
import Utils.DataBaseSQL as sql_stmt
import Utils.Settings as st
import Utils.SettingsBR as st_br
import os
import pandas as pd
import numpy as np


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
                              "category_3": st.ASPECT_OPERATION_TYPE_CATEGORICAL_5_SCALE}
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

    def update_kpi_aspect(self, kpi_aspects_weights, kpi_id, local=False):
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

    def update_kpi_formula(self, formula, kpi_id, local=False):
        db_utils.DataBaseUtils.execute_sql(db_utils.DataBaseUtils,
                                           sql_statement=sql_stmt.DataBaseSQL.
                                           update_value(sql_stmt.DataBaseSQL, table=st.TABLE_KPI,
                                                        column=st.TB_KPI_COL_FORMULA, value=formula,
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

    def render_application_landscape_kpi(self, kpi, parameter, dataset_id, dataset_label):
        formula = self.get_suitable_formula(
            KPIManager, kpi_id=kpi)
        formula = fa_m.FormulaManager.get_formula_by_id(
            fa_m.FormulaManager, formula_id=formula.get_formulaID())
        departments_from_dataset = dm.DataManager.get_departments_from_dataset(
            dm.DataManager, dataset_id=dataset_id, dataset_label=dataset_label)
        departments_br = dm.DataManager.get_departments_by_department_hierarchy_br(
            dm.DataManager, department=parameter["department"], dataset_id=dataset_id, dataset_label=dataset_label)
        results = {"label": "Application Landscape of Department: {department}".format(department=parameter["department"]),
                   "fillcolor": "595f5d",
                   "data": []}
        dataset_id = dm.DataManager.check_dataset_exists_and_return_alternative_based_on_label(
            dm.DataManager, dataset_id=dataset_id, dataset_label=dataset_label)
        data = dm.DataManager.get_table_as_df(dm.DataManager, table=dataset_id)
        if not parameter["department"] == "":
            if parameter["department"] == st.ALL_VALUES_INPUT_FIELD:
                for department_br in departments_br:
                    if any(department_br in string for string in departments_from_dataset) or department_br.startswith("HA "):
                        if not any(department_br in string for string in departments_from_dataset):
                            departments_from_dataset.append(department_br)
                        if department_br in list(st_br.departments_bayerischer_rundfunk["Hauptabteilungen"].keys()):
                            haupt_abteilung = self.__find_hauptabteilung_br(
                                KPIManager, dep_br=department_br, departments_from_dataset=departments_from_dataset, data=data, formula=formula, kpi=kpi, dataset_id=dataset_id, dataset_label=dataset_label)
                            for abteilung_br in list(st_br.departments_bayerischer_rundfunk["Hauptabteilungen"][department_br]["Abteilungen"].keys()):
                                if any(abteilung_br in string for string in departments_from_dataset):
                                    new_abteilung_br = self.__find_abteilung_br(
                                        KPIManager, dep_br=abteilung_br, departments_from_dataset=departments_from_dataset, data=data, formula=formula, kpi=kpi, dataset_id=dataset_id, dataset_label=dataset_label)
                                    if new_abteilung_br != False:
                                        for fg_br in list(st_br.departments_bayerischer_rundfunk["Hauptabteilungen"][department_br]["Abteilungen"][abteilung_br].values())[0]:
                                            if any(fg_br in string for string in departments_from_dataset):
                                                new_fg_br = self.__find_fg_br(
                                                    KPIManager, dep_br=fg_br, departments_from_dataset=departments_from_dataset, data=data, formula=formula, kpi=kpi, dataset_id=dataset_id, dataset_label=dataset_label)
                                                if new_fg_br != False:
                                                    new_abteilung_br["data"].append(
                                                        new_fg_br)
                                        haupt_abteilung["data"].append(
                                            new_abteilung_br)
                            results["data"].append(haupt_abteilung)
            elif parameter["department"] == st.NO_ENTRY_INPUT_FIELD:
                department_br = "Undefined"
                results["data"].append(self.__create_json_dep_apps_kpi_app_landscape(
                    KPIManager, dep_br=department_br, department_dataset="", data=data, formula=formula, kpi=kpi, dataset_id=dataset_id, dataset_label=dataset_label))
            elif parameter["department"].startswith("HA "):
                department_br = st_br.clean_department_from_dataset(
                    parameter["department"])
                department_dataset = [
                    val for val in departments_from_dataset if parameter["department"] in val][0]
                haupt_abteilung = self.__create_json_dep_apps_kpi_app_landscape(
                    KPIManager, dep_br=department_br, department_dataset=department_dataset, data=data, formula=formula, kpi=kpi, dataset_id=dataset_id, dataset_label=dataset_label, fillcolor="#898686")
                try:
                    for abteilung_br in list(st_br.departments_bayerischer_rundfunk["Hauptabteilungen"][department_br]["Abteilungen"].keys()):
                        if any(abteilung_br in string for string in departments_from_dataset):
                            new_abteilung_br = self.__find_abteilung_br(
                                KPIManager, dep_br=abteilung_br, departments_from_dataset=departments_from_dataset, data=data, formula=formula, kpi=kpi, dataset_id=dataset_id, dataset_label=dataset_label)
                            if new_abteilung_br != False:
                                for fg_br in list(st_br.departments_bayerischer_rundfunk["Hauptabteilungen"][department_br]["Abteilungen"][abteilung_br].values())[0]:
                                    if any(fg_br in string for string in departments_from_dataset):
                                        new_fg_br = self.__find_fg_br(
                                            KPIManager, dep_br=fg_br, departments_from_dataset=departments_from_dataset, data=data, formula=formula, kpi=kpi, dataset_id=dataset_id, dataset_label=dataset_label)
                                        if new_fg_br != False:
                                            new_abteilung_br["data"].append(
                                                new_fg_br)
                    haupt_abteilung["data"].append(
                        new_abteilung_br)
                except:
                    print("only HA available")
                results["data"].append(haupt_abteilung)
            elif parameter["department"].startswith("Abt. "):
                department_br = st_br.clean_department_from_dataset(
                    parameter["department"])
                ha_abteilungen = list(
                    st_br.departments_bayerischer_rundfunk["Hauptabteilungen"].keys())
                current_ha_abteilung = ""
                for ha_abteilung in ha_abteilungen:
                    for abteilung_br in list(st_br.departments_bayerischer_rundfunk["Hauptabteilungen"][ha_abteilung]["Abteilungen"].keys()):
                        if department_br in abteilung_br:
                            current_ha_abteilung = ha_abteilung
                            break
                    if current_ha_abteilung != "":
                        break
                if not "," in parameter["department"]:
                    department_dataset = [
                        val for val in departments_from_dataset if department_br in val and not "," in val and "abt. " in val.lower()][0]
                else:
                    department_dataset = parameter["department"]
                new_abteilung_br = self.__create_json_dep_apps_kpi_app_landscape(
                    KPIManager, dep_br=department_br, department_dataset=department_dataset, data=data, formula=formula, kpi=kpi, dataset_id=dataset_id, dataset_label=dataset_label, fillcolor="#9a9999")
                try:
                    for fg_br in list(st_br.departments_bayerischer_rundfunk["Hauptabteilungen"][current_ha_abteilung]["Abteilungen"][department_br].values())[0]:
                        if any(fg_br in string for string in departments_from_dataset):
                            new_fg_br = self.__find_fg_br(
                                KPIManager, dep_br=fg_br, departments_from_dataset=departments_from_dataset, data=data, formula=formula, kpi=kpi, dataset_id=dataset_id, dataset_label=dataset_label)
                            if new_fg_br != False:
                                new_abteilung_br["data"].append(
                                    new_fg_br)
                    results["data"].append(new_abteilung_br)
                except:
                    print("somethin wrong")
                    results["data"].append(new_abteilung_br)
            else:
                department_br = st_br.clean_department_from_dataset(
                    parameter["department"])
                all_failed = False
                try:
                    department_dataset = [
                        val for val in departments_from_dataset if parameter["department"] in val and not "," in val][0]
                except:
                    try:
                        department_dataset = [
                            val for val in departments_from_dataset if parameter["department"] in val and "," in val][0]
                    except:
                        department_dataset = ""
                        all_failed = True
                if not all_failed:
                    new_fg_br = self.__create_json_dep_apps_kpi_app_landscape(
                        KPIManager, dep_br=department_br, department_dataset=department_dataset, data=data, formula=formula, kpi=kpi, dataset_id=dataset_id, dataset_label=dataset_label)
                    results["data"].append(new_fg_br)
        return results

    def __find_hauptabteilung_br(self, dep_br, departments_from_dataset,  data, formula, kpi, dataset_id, dataset_label, fillcolor="#898686"):
        try:
            department_dataset = [
                val for val in departments_from_dataset if dep_br in val and not "," in val and "HA " in val][0]
            if len(st_br.clean_department_from_dataset(department_dataset).split(" ")) != len(dep_br.split(" ")):
                department_dataset = [
                    val for val in departments_from_dataset if dep_br in val and not "," in val and "HA " in val and len(st_br.clean_department_from_dataset(val).split(" ")) == len(dep_br.split(" "))][0]
            return self.__create_json_dep_apps_kpi_app_landscape(KPIManager, dep_br=dep_br, department_dataset=department_dataset, data=data, formula=formula, kpi=kpi, dataset_id=dataset_id, dataset_label=dataset_label, fillcolor=fillcolor)
        except:
            print(dep_br + " not in dep from dataset")
            return False

    def __find_abteilung_br(self, dep_br, departments_from_dataset, data, formula, kpi, dataset_id, dataset_label, fillcolor="#9a9999"):
        try:
            department_dataset = [
                val for val in departments_from_dataset if dep_br in val and not "," in val and "abt. " in val.lower()][0]
            if len(st_br.clean_department_from_dataset(department_dataset).split(" ")) != len(dep_br.split(" ")):
                department_dataset = [
                    val for val in departments_from_dataset if dep_br in val and not "," in val and "abt. " in val.lower() and len(st_br.clean_department_from_dataset(val).split(" ")) == len(dep_br.split(" "))][0]
            return self.__create_json_dep_apps_kpi_app_landscape(KPIManager, dep_br=dep_br, department_dataset=department_dataset, data=data, formula=formula, kpi=kpi, dataset_id=dataset_id, dataset_label=dataset_label, fillcolor=fillcolor)
        except:
            print(dep_br + " not in dep from dataset")
            return False

    def __find_fg_br(self, dep_br, departments_from_dataset,  data, formula, kpi, dataset_id, dataset_label, fillcolor="bcbcbc"):
        try:
            department_dataset = [
                val for val in departments_from_dataset if dep_br in val and not "," in val and "fg " in val.lower()][0]
            if len(st_br.clean_department_from_dataset(department_dataset).split(" ")) != len(dep_br.split(" ")):
                department_dataset = [
                    val for val in departments_from_dataset if dep_br in val and not "," in val and "fg " in val.lower() and len(st_br.clean_department_from_dataset(val).split(" ")) == len(dep_br.split(" "))][0]
            return self.__create_json_dep_apps_kpi_app_landscape(KPIManager, dep_br=dep_br, department_dataset=department_dataset, data=data, formula=formula, kpi=kpi, dataset_id=dataset_id, dataset_label=dataset_label, fillcolor=fillcolor)
        except:
            print(dep_br + " not in dep from dataset")
            return False

    def __create_json_dep_apps_kpi_app_landscape(self, dep_br, department_dataset, data, formula, kpi, dataset_id, dataset_label, fillcolor="#bcbcbc"):
        new_dep_br = {"label": dep_br,
                      "fillcolor": fillcolor,
                      "data": []}
        apps = data[data["Verantwortliche Organisationseinheit"]
                    == department_dataset]["Name"].to_list()
        for app in apps:
            val = self.__calc_kpi_value_for_kpi_app_landscape(
                KPIManager, app=app, data=data, formula=formula, kpi=kpi, dataset_id=dataset_id, dataset_label=dataset_label)
            if val == 0.0:
                val = 0.01
            new_dep_br["data"].append(
                {"label": app,
                    "value": val,
                    "sValue": val,
                 }
            )
        return new_dep_br

    def __calc_kpi_value_for_kpi_app_landscape(self, app, data, formula, kpi, dataset_id, dataset_label):
        return fa_e.FormulaExecutor.execute_formula(
            operation=formula.get_operation(), purpose=formula.get_purpose(), kpi_id=kpi,
            dataset_id=dataset_id, dataset_label=dataset_label, parameter={"app": app, "department": "", "domain": ""}, fast_landscape_kpi=True, dataset_data=data)["result"]

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

    def analyze_applicability(self, raw_component, dataset_id="", dataset_label=""):
        dataset_id = dm.DataManager.check_dataset_exists_and_return_alternative_based_on_label(
            dm.DataManager, dataset_id=dataset_id, dataset_label=dataset_label)
        data = dm.DataManager.get_table_as_df(
            dm.DataManager, dataset_id)
        if "Anzahl" in raw_component:
            data[raw_component] = data[raw_component].apply(
                lambda x: np.nan if x == 0 or x == "0" else x)
        else:
            data[raw_component] = data[raw_component].apply(
                lambda x: np.nan if x == "" or x == "Kein Eintrag" else x)
        value = ((len(data[raw_component]) - data[raw_component].isna().sum()
                  ) / len(data[raw_component])) * 100
        return value

    def analyze_applicability_kpi_based_on_aspect(self, aspect_id, dataset_id="", dataset_label=""):
        dataset_id = dm.DataManager.check_dataset_exists_and_return_alternative_based_on_label(
            dm.DataManager, dataset_id=dataset_id, dataset_label=dataset_label)
        data = dm.DataManager.get_table_as_df(
            dm.DataManager, dataset_id)
        aspect = aspct_m.AspectManager.get_aspect_by_id(
            aspct_m.AspectManager, aspect_id=aspect_id)
        aspect_raw_components = aspect.get_raw_components_from_dataset()
        raw_components = [
            val for sublist in aspect_raw_components for val in sublist]
        value = 0
        all_raw_aspects_count = 0
        aspects_completed_data_count = 0
        for raw_component in raw_components:
            if "Anzahl" in raw_component:
                data[raw_component] = data[raw_component].apply(
                    lambda x: np.nan if x == 0 or x == "0" else x)
            else:
                data[raw_component] = data[raw_component].apply(
                    lambda x: np.nan if x == "" or x == "Kein Eintrag" else x)
            all_raw_aspects_count += len(data[raw_component])
            aspects_completed_data_count += len(
                data[raw_component]) - data[raw_component].isna().sum()
        value = aspects_completed_data_count / all_raw_aspects_count * 100
        return value

    def analyze_applicability_kpi(self, kpi_id, dataset_id="", dataset_label="", parameters="all"):
        dataset_id = dm.DataManager.check_dataset_exists_and_return_alternative_based_on_label(
            dm.DataManager, dataset_id=dataset_id, dataset_label=dataset_label)
        data = dm.DataManager.get_table_as_df(
            dm.DataManager, dataset_id)
        if not parameters == "all":
            parameters = st.string_list_with_string_dict_into_list_dict(
                parameters)
            for param in parameters:
                if "dep" in list(param.keys()):
                    if not param["dep"] == st.ALL_VALUES_INPUT_FIELD:
                        parameter = param["dep"]
                        slicer = "Verantwortliche Organisationseinheit"
                        data = data[data[slicer] == parameter]
                if "app" in list(param.keys()):
                    parameter = param['app']
                    slicer = "Name"
                    data = data[data[slicer] == parameter]
                if "domain" in list(param.keys()):
                    parameter = param['domain']
                    data["Zugeordnete Domäne"] = data["Zugeordnete Domäne"].apply(
                        lambda x: x if parameter in x else np.NaN)
                    data.dropna(inplace=True, subset=[
                        'Zugeordnete Domäne'])
        kpi = KPIManager.get_kpi_by_id(
            KPIManager, kpi_id=kpi_id)
        aspects = [val for sublist in kpi.get_kpi_aspects_weights()
                   for val in sublist]
        value = 0
        all_raw_aspects_count = 0
        aspects_completed_data_count = 0
        for aspect_name in aspects:
            aspect = aspct_m.AspectManager.get_aspect_by_name(
                aspct_m.AspectManager, name=aspect_name)
            aspect_raw_components = aspect.get_raw_components_from_dataset()
            raw_components = [
                val for sublist in aspect_raw_components for val in sublist]
            for raw_component in raw_components:
                if "Anzahl" in raw_component:
                    data[raw_component] = data[raw_component].apply(
                        lambda x: np.nan if x == 0 or x == "0" else x)
                else:
                    data[raw_component] = data[raw_component].apply(
                        lambda x: np.nan if x == "" or x == "Kein Eintrag" else x)
                all_raw_aspects_count += len(data[raw_component])
                aspects_completed_data_count += len(
                    data[raw_component]) - data[raw_component].isna().sum()
        value = aspects_completed_data_count / all_raw_aspects_count * 100
        return value

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
