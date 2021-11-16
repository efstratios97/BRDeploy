# Project Athena
'''
Owner: Efstratios Pahis
Contributors:
Description: Implements main functionality of the Executive Dashboard Manager
'''

import pandas as pd
import Utils.DataBaseSQL as sql_stmt
import Utils.DataBaseUtils as db_utils
import Utils.Settings as st
import ExecutiveDashboardManager.ExecutiveDashboard as ed
import DataPlotManager.DataPlotManager as dpm


class ExecutiveDashboardManager:

    def create_executive_dashboard(self, name, description, access_user_list, access_business_unit_list, plots, dataset, local=False):
        executive_dashboard_id = "executive_dashboard_" + st.create_id()

        executive_dashboard = ed.ExecutiveDashboard(executive_dashboard_id=executive_dashboard_id, name=name, description=description,
                                                    access_user_list=access_user_list,
                                                    access_business_unit_list=access_business_unit_list,
                                                    plots=plots, dataset=dataset)
        self.insert_executive_dashboard_db(
            ExecutiveDashboardManager, executive_dashboard=executive_dashboard, local=local)
        return dataset

    def insert_executive_dashboard_db(self, executive_dashboard: ed.ExecutiveDashboard, local=False):
        # Creates Table
        db_utils.DataBaseUtils.execute_sql(
            db_utils.DataBaseUtils, sql_statement=sql_stmt.DataBaseSQL.
            create_Executive_Dashboard_table_sql(sql_stmt.DataBaseSQL), local=local)
        # Inserts data
        db_utils.DataBaseUtils.execute_sql(db_utils.DataBaseUtils,
                                           sql_statement=sql_stmt.DataBaseSQL.
                                           insert_executive_dashboard_values(sql_stmt.DataBaseSQL, executive_dashboard_id=executive_dashboard.get_executive_dashboardID(),
                                                                             executive_dashboard_name=executive_dashboard.get_name(),
                                                                             executive_dashboard_description=executive_dashboard.get_description(),
                                                                             access_user_list=executive_dashboard.get_access_user_list(),
                                                                             access_business_unit_list=executive_dashboard.get_access_business_unit_list(),
                                                                             executive_dashboard_plots=executive_dashboard.get_plots(),
                                                                             dataset_id=executive_dashboard.get_dataset()), local=local)

    def get_all_executive_dashboards(self):
        data = []
        result = db_utils.DataBaseUtils.execute_sql(db_utils.DataBaseUtils,
                                                    sql_stmt.DataBaseSQL.select_all_data_from_table(
                                                        sql_stmt.DataBaseSQL, table=st.TABLE_EXECUTIVE_DASHBOARDS),
                                                    fetchall=True, local=False)
        if result:
            for row in result:
                executive_dashboard = self.__parse_executive_dashboard_obj(
                    ExecutiveDashboardManager, row)
                data.append(executive_dashboard)
        return data

    def get_plots_from_executive_dashboard(self, executive_dashboard_id, local=False):
        result = db_utils.DataBaseUtils.execute_sql(db_utils.DataBaseUtils,
                                                    sql_statement=sql_stmt.DataBaseSQL.
                                                    select_all_from_column(sql_stmt.DataBaseSQL, table=st.TABLE_EXECUTIVE_DASHBOARDS_PLOTS_RELATION,
                                                                           condition=st.TB_EXECUTIVE_DASHBOARDS_COL_ID,
                                                                           condition_operator='=', condition_value=executive_dashboard_id),
                                                    fetchall=True, local=local)
        # TODO FIX
        plots = []
        data = []
        for row in result:
            # if not row[0] in plots:
            plot = dpm.DataPlotManager.get_plot_by_id(
                dpm.DataPlotManager, row[1])
            data.append(plot)
            # plots.append(plot)
        return data

    def get_executive_dashboard_by_id(self, executive_dashboard_id, local=False):
        result = db_utils.DataBaseUtils.execute_sql(db_utils.DataBaseUtils,
                                                    sql_statement=sql_stmt.DataBaseSQL.select_object_by_condition(
                                                        sql_stmt.DataBaseSQL, table=st.TABLE_EXECUTIVE_DASHBOARDS,
                                                        condition=st.TB_EXECUTIVE_DASHBOARDS_COL_ID, condition_value=executive_dashboard_id),
                                                    local=local, fetchone=True)
        executive_dashboard = self.__parse_executive_dashboard_obj(
            ExecutiveDashboardManager, db_row=result)
        return executive_dashboard

    def delete_executive_dashboard(self, executive_dashboard_id, condition_operator='=', local=False):
        db_utils.DataBaseUtils.execute_sql(
            db_utils.DataBaseUtils,
            sql_statement=sql_stmt.DataBaseSQL.delete_row_from_table(
                sql_stmt.DataBaseSQL, table=st.TABLE_EXECUTIVE_DASHBOARDS, condition=st.TB_EXECUTIVE_DASHBOARDS_COL_ID,
                condition_value=executive_dashboard_id, condition_operator=condition_operator), local=local)

    def __parse_executive_dashboard_obj(self, db_row):
        if db_row:
            executive_dashboard_id = db_row[0]
            name = db_row[1]
            description = db_row[2]
            access_user_list = db_row[3]
            access_business_unit_list = db_row[4]
            plots = db_row[5]
            executive_dashboard = ed.ExecutiveDashboard(executive_dashboard_id=executive_dashboard_id, name=name, description=description,
                                                        access_user_list=access_user_list,
                                                        access_business_unit_list=access_business_unit_list, plots=plots)
            return executive_dashboard
        pass
