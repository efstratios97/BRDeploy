# Project Athena
'''
Owner: Efstratios Pahis
Contributors:
Description: Implements main functionality of the FormulaExecutor
'''

import KPIFormulaManager.Formula as fa
import KPIAspectManager.AspectManager as aspct_m
import Utils.DataBaseUtils as db_utils
import Utils.DataBaseSQL as sql_stmt
import Utils.Settings as st
import os
import pandas as pd
import sys
import json
import KPIFormulaManager.Result as res
import KPIManager.KPIManager as kpi_m
import KPIFormulaManager.FormulasIndividual.BR_EAM_KPI_Formel_J_LEDERLE as ind_kpi
import DataManager.DataManager as dm
import subprocess


class FormulaExecutor:

    def execute_formula(operation, purpose, kpi_id="", aspect_id=[], dataset_id="", dataset_label="", parameter="{}", fast_landscape_kpi=False, dataset_data=""):
        if not fast_landscape_kpi:
            res_table_name = "result_" + st.create_id()
            res.Result.create_result_table(
                res.Result, table_name=res_table_name)
        parameter = json.dumps(parameter)
        if purpose == st.FORMULA_PURPOSE_KPI:
            if fast_landscape_kpi:
                return ind_kpi.kpi_calculation(
                    kpi_id=kpi_id, dataset_id=dataset_id, parameter=parameter, dataset_data=dataset_data, fast=True)
            else:
                subprocess.call(['python', os.path.dirname(os.path.abspath(__file__)) +
                                 "\\FormulasIndividual\\{operation}.py".format(operation=operation), kpi_id, dataset_id, parameter, res_table_name], shell=False)
        elif purpose == st.FORMULA_PURPOSE_ASPECT:
            subprocess.call(['python', os.path.dirname(os.path.abspath(__file__)) +
                             "\\FormulasIndividual\\{operation}.py".format(operation=operation), aspect_id, dataset_id, parameter, res_table_name], shell=False)
        results = res.Result.get_results(res.Result, table_name=res_table_name)
        result = False
        if len(results) == 1:
            result = res.Result.get_result(
                res.Result, result_id=results[0]['result_id'], table_name=res_table_name)
        for rslt in results:
            res.Result.clean_result(
                res.Result, result_id=rslt['result_id'], table_name=res_table_name)
        res.Result.drop_result_table(res.Result, table_name=res_table_name)
        return result
