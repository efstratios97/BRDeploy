# Project Athena
'''
Owner: Efstratios Pahis
Contributors:
Description: Implements main functionality of the Data Plot Manager
'''

import json
import Utils.DataBaseSQL as sql_stmt
import Utils.DataBaseUtils as db_utils
import Utils.Settings as st
import DataPlotManager.Plot as plt
import ExecutiveDashboardManager.ExecutiveDashboardManager as edm
import DataManager.DataManager as dm


class DataPlotManager:

    def create_data_plot(self, formdata, grouped, visualization_type, visualization_right, component_name, executive_dashboard_id=False):
        plot_id = "plot_" + st.create_id()
        plot = plt.Plot(plot_id=plot_id, formdata=formdata, grouped=grouped, visualization_type=visualization_type,
                        visualization_right=visualization_right, component_name=component_name)
        self.insert_plot_db(
            DataPlotManager, plot=plot)
        if executive_dashboard_id:
            self.insert_executive_dashboard_plot_relation_db(
                DataPlotManager, executive_dashboard_id=executive_dashboard_id, plot_id=plot_id)
        return plot

    def insert_plot_db(self, plot: plt.Plot, local=False):
        # Creates Table
        db_utils.DataBaseUtils.execute_sql(
            db_utils.DataBaseUtils, sql_statement=sql_stmt.DataBaseSQL.
            create_Plots_table_sql(sql_stmt.DataBaseSQL), local=local)
        # Inserts data
        db_utils.DataBaseUtils.execute_sql(db_utils.DataBaseUtils,
                                           sql_statement=sql_stmt.DataBaseSQL.insert_plots_values(sql_stmt.DataBaseSQL,
                                                                                                  plot_id=plot.get_plotID(), formdata=plot.get_formdata(), grouped=plot.get_grouped(),
                                                                                                  visualization_type=plot.get_visualization_type(),
                                                                                                  visualization_right=plot.get_visualization_right(),
                                                                                                  component_name=plot.get_component_name()), local=local)

    def insert_executive_dashboard_plot_relation_db(self, executive_dashboard_id, plot_id, local=False):
        # Creates Table
        db_utils.DataBaseUtils.execute_sql(
            db_utils.DataBaseUtils, sql_statement=sql_stmt.DataBaseSQL.
            create_ExecutiveDashboard_Plot_relation_table_sql(sql_stmt.DataBaseSQL), local=local)
        # Inserts data
        db_utils.DataBaseUtils.execute_sql(
            db_utils.DataBaseUtils, sql_statement=sql_stmt.DataBaseSQL.insert_executive_dashboard_plots_relation_values(
                sql_stmt.DataBaseSQL, executive_dashboard_id=executive_dashboard_id, plot_id=plot_id),
            local=local)
        # Inset Plot to Executive Dashboard Column
        self.update_executive_dashboard_plot(
            DataPlotManager, plot_id=plot_id, executive_dashboard_id=executive_dashboard_id)

    def update_executive_dashboard_plot(self, plot_id, executive_dashboard_id, local=False):
        executive_dashboard = edm.ExecutiveDashboardManager.get_executive_dashboard_by_id(
            edm.ExecutiveDashboardManager, executive_dashboard_id)
        if executive_dashboard.get_plots() == "":
            executive_dashboard.set_plots(plots=plot_id)
        else:
            executive_dashboard.set_plots(
                executive_dashboard.get_plots() + "," + plot_id)
        db_utils.DataBaseUtils.execute_sql(db_utils.DataBaseUtils,
                                           sql_statement=sql_stmt.DataBaseSQL.
                                           update_value(sql_stmt.DataBaseSQL, table=st.TABLE_EXECUTIVE_DASHBOARDS,
                                                        column=st.TB_EXECUTIVE_DASHBOARDS_COL_PLOTS, value=executive_dashboard.get_plots(),
                                                        condition=st.TB_EXECUTIVE_DASHBOARDS_COL_ID,
                                                        condition_operator='=', condition_value=executive_dashboard_id),
                                           local=local)
        # self.insert_executive_dashboard_plot_relation_db(
        #     DataPlotManager, executive_dashboard_id=executive_dashboard_id, plot_id=plot_id)

    def get_all_plots(self):
        data = []
        result = db_utils.DataBaseUtils.execute_sql(db_utils.DataBaseUtils,
                                                    sql_stmt.DataBaseSQL.select_all_data_from_table(
                                                        sql_stmt.DataBaseSQL, table=st.TABLE_PLOTS),
                                                    fetchall=True, local=False)
        if result:
            for row in result:
                plot = self.__parse_plot_obj(
                    DataPlotManager, row)
                data.append(plot)
        return data

    def get_plot_by_id(self, plot_id, dataset_id="", dataset_label="", local=False):
        result = db_utils.DataBaseUtils.execute_sql(db_utils.DataBaseUtils,
                                                    sql_statement=sql_stmt.DataBaseSQL.select_object_by_condition(
                                                        sql_stmt.DataBaseSQL, table=st.TABLE_PLOTS,
                                                        condition=st.TB_PLOTS_COL_ID, condition_value=plot_id),
                                                    local=local, fetchone=True)
        plot = self.__parse_plot_obj(
            DataPlotManager, db_row=result, dataset_id=dataset_id, dataset_label=dataset_label)
        return plot

    def get_plots_from_executive_dashboard(self, executive_dashboard_id, local=False):
        result = db_utils.DataBaseUtils.execute_sql(db_utils.DataBaseUtils,
                                                    sql_statement=sql_stmt.DataBaseSQL.
                                                    select_all_from_column(sql_stmt.DataBaseSQL, table=st.TABLE_EXECUTIVE_DASHBOARDS_PLOTS_RELATION,
                                                                           condition=st.TB_EXECUTIVE_DASHBOARDS_COL_ID,
                                                                           condition_operator='=', condition_value=executive_dashboard_id),
                                                    fetchall=True, local=local)
        executive_dashboard = edm.ExecutiveDashboardManager.get_executive_dashboard_by_id(
            edm.ExecutiveDashboardManager, executive_dashboard_id=executive_dashboard_id)
        dataset_choice_rule = executive_dashboard.get_dataset_choice_rule()
        if dataset_choice_rule == st.DATA_CHOICE_RULE_SPECIFIC_DATASET:
            dataset_id = dm.DataManager.check_dataset_exists_and_return_alternative_based_on_label(
                dm.DataManager, dataset_id=executive_dashboard.get_dataset_id(), dataset_label=executive_dashboard.get_dataset_label())
        elif dataset_choice_rule == st.DATA_CHOICE_RULE_RECENT_DATASET:
            dataset_id = dm.DataManager.get_newest_dataset_replacement_by_dataset_label(
                dm.DataManager, dataset_label=executive_dashboard.get_dataset_label()).get_datasetID()
        elif dataset_choice_rule == st.DATA_CHOICE_RULE_USER_CHOICE:
            dataset_id = ""
            dataset_label = ""
        else:
            dataset_id = dm.DataManager.get_newest_dataset_replacement_by_dataset_label(
                dm.DataManager, dataset_label=executive_dashboard.get_dataset_label())
        dataset_label = executive_dashboard.get_dataset_label()
        data = []
        for row in result:
            plot = self.get_plot_by_id(
                DataPlotManager, row[1], dataset_id=dataset_id, dataset_label=dataset_label)
            data.append(plot)
        return data

    def delete_plot(self, plot_id, condition_operator='=', local=False):
        db_utils.DataBaseUtils.execute_sql(
            db_utils.DataBaseUtils,
            sql_statement=sql_stmt.DataBaseSQL.delete_row_from_table(
                sql_stmt.DataBaseSQL, table=st.TABLE_PLOTS, condition=st.TB_PLOTS_COL_ID,
                condition_value=plot_id, condition_operator=condition_operator), local=local)

    def __parse_plot_obj(self, db_row, dataset_id="", dataset_label=""):
        if db_row:
            plot_id = db_row[0]
            formdata = json.loads(db_row[1][1:-1])
            grouped = db_row[2]
            visualization_type = db_row[3]
            visualization_right = db_row[4]
            component_name = db_row[5]
            plot = plt.Plot(plot_id=plot_id, formdata=formdata, grouped=grouped, visualization_type=visualization_type,
                            visualization_right=visualization_right, component_name=component_name)
            plot.set_dataset_id(dataset_id=dataset_id)
            plot.set_dataset_label(dataset_label=dataset_label)
            return plot
        pass
