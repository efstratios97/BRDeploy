# Project Athena
'''
Owner: Efstratios Pahis
Contributors:
Description: Implements main functionality of the Data Plot Manager
'''

import pandas as pd
import Utils.DataBaseSQL as sql_stmt
import Utils.DataBaseUtils as db_utils
import Utils.Settings as st
import DataPlotManager.Plot as plt
import ExecutiveDashboardManager.ExecutiveDashboardManager as edm


class DataPlotManager:

    def create_data_plot(self, plot_title, plot_subtitle, plot_legend_show, plot_dataset_id_for_chart,
                         plot_dataset_label, plot_chart_type, plot_chart_width, plot_chart_height, plot_xaxis_categories,
                         plot_input_fields, plot_input_fields_id, executive_dashboard_id=False, local=False):
        plot_id = "plot_" + st.create_id()
        plot = plt.Plot(plot_id=plot_id, plot_title=plot_title, plot_subtitle=plot_subtitle, plot_legend_show=plot_legend_show,
                        plot_dataset_id_for_chart=plot_dataset_id_for_chart, plot_dataset_label=plot_dataset_label,
                        plot_chart_type=plot_chart_type, plot_chart_width=plot_chart_width, plot_chart_height=plot_chart_height,
                        plot_xaxis_categories=plot_xaxis_categories, plot_input_fields=plot_input_fields, plot_input_fields_id=plot_input_fields_id)
        self.insert_plot_db(
            DataPlotManager, plot=plot, local=local)
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
                                                                                                  plot_id=plot.get_plotID(), plot_title=plot.get_title(), plot_subtitle=plot.get_subtitle(),
                                                                                                  plot_show_legend=plot.get_legend_show(), plot_dataset_id_for_chart=plot.get_dataset_id_for_chart(),
                                                                                                  plot_dataset_label=plot.get_dataset_label(), plot_chart_type=plot.get_chart_type(),
                                                                                                  plot_chart_width=plot.get_chart_width(), plot_chart_height=plot.get_chart_height(),
                                                                                                  plot_xaxis_categories=plot.get_xaxis_categories(), plot_input_fields=plot.get_input_fields(),
                                                                                                  plot_input_fields_id=plot.get_input_fields_id()), local=local)

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

    def get_plot_by_id(self, plot_id, local=False):
        result = db_utils.DataBaseUtils.execute_sql(db_utils.DataBaseUtils,
                                                    sql_statement=sql_stmt.DataBaseSQL.select_object_by_condition(
                                                        sql_stmt.DataBaseSQL, table=st.TABLE_PLOTS,
                                                        condition=st.TB_PLOTS_COL_ID, condition_value=plot_id),
                                                    local=local, fetchone=True)
        plot = self.__parse_plot_obj(
            DataPlotManager, db_row=result)
        return plot

    def delete_plot(self, plot_id, condition_operator='=', local=False):
        db_utils.DataBaseUtils.execute_sql(
            db_utils.DataBaseUtils,
            sql_statement=sql_stmt.DataBaseSQL.delete_row_from_table(
                sql_stmt.DataBaseSQL, table=st.TABLE_PLOTS, condition=st.TB_PLOTS_COL_ID,
                condition_value=plot_id, condition_operator=condition_operator), local=local)

    def __parse_plot_obj(self, db_row):
        if db_row:
            plot_id = db_row[0]
            plot_title = db_row[1]
            plot_subtitle = db_row[2]
            plot_legend_show = db_row[3]
            plot_dataset_id_for_chart = db_row[4]
            plot_dataset_label = db_row[5]
            plot_chart_type = db_row[6]
            plot_chart_width = db_row[7]
            plot_chart_height = db_row[8]
            plot_xaxis_categories = db_row[9]
            plot_input_fields = db_row[10]
            plot_input_fields_id = db_row[11]
            plot = plt.Plot(plot_id=plot_id, plot_title=plot_title, plot_subtitle=plot_subtitle, plot_legend_show=plot_legend_show,
                            plot_dataset_id_for_chart=plot_dataset_id_for_chart, plot_dataset_label=plot_dataset_label,
                            plot_chart_type=plot_chart_type, plot_chart_width=plot_chart_width, plot_chart_height=plot_chart_height,
                            plot_xaxis_categories=plot_xaxis_categories, plot_input_fields=plot_input_fields, plot_input_fields_id=plot_input_fields_id)
            return plot
        pass
