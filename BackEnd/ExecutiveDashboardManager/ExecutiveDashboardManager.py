# Project Athena
'''
Owner: Efstratios Pahis
Contributors:
Description: Implements main functionality of the Executive Dashboard Manager
'''

import ExecutiveDashboardManager.DatsetChoiceRule as dt_ch_rl
import ExecutiveDashboardManager.VisualizationRight as vs_rg
import Utils.DataBaseSQL as sql_stmt
import Utils.DataBaseUtils as db_utils
import Utils.Settings as st
import ExecutiveDashboardManager.ExecutiveDashboard as ed
import UserManager.UserManager as um


class ExecutiveDashboardManager:

    def create_executive_dashboard(self, name, description, access_user_list, access_business_unit_list, plots,
                                   dataset_choice_rule, visualization_right, dataset_id="", dataset_label=""):
        executive_dashboard_id = "executive_dashboard_" + st.create_id()
        executive_dashboard = ed.ExecutiveDashboard(executive_dashboard_id=executive_dashboard_id, name=name, description=description,
                                                    access_user_list=access_user_list,
                                                    access_business_unit_list=access_business_unit_list,
                                                    plots=plots, dataset_id=dataset_id, dataset_label=dataset_label,
                                                    visualization_right=visualization_right, dataset_choice_rule=dataset_choice_rule)
        self.init_dataset_choice_rules(ExecutiveDashboardManager)
        self.init_visualization_rights(ExecutiveDashboardManager)
        self.insert_executive_dashboard_db(
            ExecutiveDashboardManager, executive_dashboard=executive_dashboard)
        return executive_dashboard

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
                                                                             dataset_id=executive_dashboard.get_dataset_id(),
                                                                             dataset_label=executive_dashboard.get_dataset_label(),
                                                                             dataset_choice_rule=executive_dashboard.get_dataset_choice_rule(),
                                                                             visualization_right=executive_dashboard.get_visualization_right()), local=local)

    def update_executive_dashboard(self, executive_dashboard: ed.ExecutiveDashboard):
        executive_dashboard_id = executive_dashboard.get_executive_dashboardID()
        self.update_name(
            ExecutiveDashboardManager, name=executive_dashboard.get_name(), executive_dashboard_id=executive_dashboard_id)
        self.update_description(
            ExecutiveDashboardManager, description=executive_dashboard.get_description(), executive_dashboard_id=executive_dashboard_id)
        self.update_access_user_list(
            ExecutiveDashboardManager, access_user_list=executive_dashboard.get_access_user_list(), executive_dashboard_id=executive_dashboard_id)
        self.update_access_business_unit_list(
            ExecutiveDashboardManager, access_business_unit_list=executive_dashboard.get_access_business_unit_list(), executive_dashboard_id=executive_dashboard_id)
        self.update_dataset_choice_rules(
            ExecutiveDashboardManager, dataset_choice_rule=executive_dashboard.get_dataset_choice_rule(), executive_dashboard_id=executive_dashboard_id)
        self.update_dataset_label(
            ExecutiveDashboardManager, dataset_label=executive_dashboard.get_dataset_label(), executive_dashboard_id=executive_dashboard_id)
        self.update_dataset_id(
            ExecutiveDashboardManager, dataset_id=executive_dashboard.get_dataset_id(), executive_dashboard_id=executive_dashboard_id)

    def update_name(self, name, executive_dashboard_id):
        db_utils.DataBaseUtils.execute_sql(db_utils.DataBaseUtils,
                                           sql_statement=sql_stmt.DataBaseSQL.
                                           update_value(sql_stmt.DataBaseSQL, table=st.TABLE_EXECUTIVE_DASHBOARDS,
                                                        column=st.TB_EXECUTIVE_DASHBOARDS_COL_NAME, value=name,
                                                        condition=st.TB_EXECUTIVE_DASHBOARDS_COL_ID,
                                                        condition_operator='=', condition_value=executive_dashboard_id))

    def update_description(self, description, executive_dashboard_id):
        db_utils.DataBaseUtils.execute_sql(db_utils.DataBaseUtils,
                                           sql_statement=sql_stmt.DataBaseSQL.
                                           update_value(sql_stmt.DataBaseSQL, table=st.TABLE_EXECUTIVE_DASHBOARDS,
                                                        column=st.TB_EXECUTIVE_DASHBOARDS_COL_DESCRIPTION, value=description,
                                                        condition=st.TB_EXECUTIVE_DASHBOARDS_COL_ID,
                                                        condition_operator='=', condition_value=executive_dashboard_id))

    def update_access_user_list(self, access_user_list, executive_dashboard_id):
        db_utils.DataBaseUtils.execute_sql(db_utils.DataBaseUtils,
                                           sql_statement=sql_stmt.DataBaseSQL.
                                           update_value(sql_stmt.DataBaseSQL, table=st.TABLE_EXECUTIVE_DASHBOARDS,
                                                        column=st.TB_EXECUTIVE_DASHBOARDS_COL_ACCESS_USER_LIST, value=access_user_list,
                                                        condition=st.TB_EXECUTIVE_DASHBOARDS_COL_ID,
                                                        condition_operator='=', condition_value=executive_dashboard_id))

    def update_access_business_unit_list(self, access_business_unit_list, executive_dashboard_id):
        db_utils.DataBaseUtils.execute_sql(db_utils.DataBaseUtils,
                                           sql_statement=sql_stmt.DataBaseSQL.
                                           update_value(sql_stmt.DataBaseSQL, table=st.TABLE_EXECUTIVE_DASHBOARDS,
                                                        column=st.TB_EXECUTIVE_DASHBOARDS_COL_ACCESS_BUSINESS_UNIT_LIST, value=access_business_unit_list,
                                                        condition=st.TB_EXECUTIVE_DASHBOARDS_COL_ID,
                                                        condition_operator='=', condition_value=executive_dashboard_id))

    def update_dataset_choice_rules(self, dataset_choice_rule, executive_dashboard_id):
        db_utils.DataBaseUtils.execute_sql(db_utils.DataBaseUtils,
                                           sql_statement=sql_stmt.DataBaseSQL.
                                           update_value(sql_stmt.DataBaseSQL, table=st.TABLE_EXECUTIVE_DASHBOARDS,
                                                        column=st.TB_EXECUTIVE_DASHBOARDS_COL_DATASET_CHOICE_RULE, value=dataset_choice_rule,
                                                        condition=st.TB_EXECUTIVE_DASHBOARDS_COL_ID,
                                                        condition_operator='=', condition_value=executive_dashboard_id))

    def update_dataset_label(self, dataset_label, executive_dashboard_id):
        db_utils.DataBaseUtils.execute_sql(db_utils.DataBaseUtils,
                                           sql_statement=sql_stmt.DataBaseSQL.
                                           update_value(sql_stmt.DataBaseSQL, table=st.TABLE_EXECUTIVE_DASHBOARDS,
                                                        column=st.TB_EXECUTIVE_DASHBOARDS_COL_DATASET_LABEL, value=dataset_label,
                                                        condition=st.TB_EXECUTIVE_DASHBOARDS_COL_ID,
                                                        condition_operator='=', condition_value=executive_dashboard_id))

    def update_dataset_id(self, dataset_id, executive_dashboard_id):
        db_utils.DataBaseUtils.execute_sql(db_utils.DataBaseUtils,
                                           sql_statement=sql_stmt.DataBaseSQL.
                                           update_value(sql_stmt.DataBaseSQL, table=st.TABLE_EXECUTIVE_DASHBOARDS,
                                                        column=st.TB_EXECUTIVE_DASHBOARDS_COL_DATASET_ID, value=dataset_id,
                                                        condition=st.TB_EXECUTIVE_DASHBOARDS_COL_ID,
                                                        condition_operator='=', condition_value=executive_dashboard_id))

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

    def get_all_executive_dashboards_by_user(self, user_id):
        data = []
        user = um.UserManager.get_user_by_id(
            um.UserManager, user_id=user_id)
        user_bu_id = user.get_business_unit()
        result = db_utils.DataBaseUtils.execute_sql(db_utils.DataBaseUtils,
                                                    sql_stmt.DataBaseSQL.select_all_data_from_table(
                                                        sql_stmt.DataBaseSQL, table=st.TABLE_EXECUTIVE_DASHBOARDS),
                                                    fetchall=True, local=False)
        if result:
            for row in result:
                executive_dashboard = self.__parse_executive_dashboard_obj(
                    ExecutiveDashboardManager, row)
                if (user_bu_id in executive_dashboard.get_access_business_unit_list()
                        or user_id in executive_dashboard.get_access_user_list()):
                    data.append(executive_dashboard)
        return data

    def get_executive_dashboard_by_id(self, executive_dashboard_id):
        result = db_utils.DataBaseUtils.execute_sql(db_utils.DataBaseUtils,
                                                    sql_statement=sql_stmt.DataBaseSQL.select_object_by_condition(
                                                        sql_stmt.DataBaseSQL, table=st.TABLE_EXECUTIVE_DASHBOARDS,
                                                        condition=st.TB_EXECUTIVE_DASHBOARDS_COL_ID, condition_value=executive_dashboard_id),
                                                    fetchone=True)
        executive_dashboard = self.__parse_executive_dashboard_obj(
            ExecutiveDashboardManager, db_row=result)
        return executive_dashboard

    def delete_executive_dashboard(self, executive_dashboard_id, condition_operator='=', local=False):
        db_utils.DataBaseUtils.execute_sql(
            db_utils.DataBaseUtils,
            sql_statement=sql_stmt.DataBaseSQL.delete_row_from_table(
                sql_stmt.DataBaseSQL, table=st.TABLE_EXECUTIVE_DASHBOARDS, condition=st.TB_EXECUTIVE_DASHBOARDS_COL_ID,
                condition_value=executive_dashboard_id, condition_operator=condition_operator), local=local)

    def init_dataset_choice_rules(self, local=False):
        # Creates Table
        db_utils.DataBaseUtils.execute_sql(
            db_utils.DataBaseUtils, sql_statement=sql_stmt.DataBaseSQL.
            create_dataset_choice_rule_table_sql(sql_stmt.DataBaseSQL), local=local)
        # Inserts data
        try:
            for dataset_choice_rule in st.DATA_CHOICE_RULES:
                dataset_choice_rule = dt_ch_rl.DatsetChoiceRule(
                    dataset_choice_rule_id=dataset_choice_rule, name=dataset_choice_rule, description=dataset_choice_rule)
                db_utils.DataBaseUtils.execute_sql(db_utils.DataBaseUtils,
                                                   sql_statement=sql_stmt.DataBaseSQL.
                                                   insert_dataset_choice_rules_values(sql_stmt.DataBaseSQL, dataset_choice_rule_id=dataset_choice_rule.get_dataset_choice_rule_id(),
                                                                                      name=dataset_choice_rule.get_name(), description=dataset_choice_rule.get_description()), local=local)
        except:
            print("alreay_initiated_tables_and_values")

    def init_visualization_rights(self, local=False):
        # Creates Table
        db_utils.DataBaseUtils.execute_sql(
            db_utils.DataBaseUtils, sql_statement=sql_stmt.DataBaseSQL.
            create_visualization_right_table_sql(sql_stmt.DataBaseSQL), local=local)
        # Inserts data
        try:
            for visualization_right in st.VISUALIZATION_RIGHTS:
                if not visualization_right == st.VISUALIZATION_RIGHTS_OWN_ANALYSIS_RESTRICTED:  # For now
                    visualization_right = vs_rg.VisualizationRight(
                        visualization_right_id=visualization_right, name=visualization_right, description=visualization_right)
                    db_utils.DataBaseUtils.execute_sql(db_utils.DataBaseUtils,
                                                       sql_statement=sql_stmt.DataBaseSQL.
                                                       insert_visualization_right_values(sql_stmt.DataBaseSQL, visualization_right_id=visualization_right.get_visualization_right_id(),
                                                                                         name=visualization_right.get_name(), description=visualization_right.get_description()), local=local)
        except:
            print("alreay_initiated_tables_and_values")

    def get_dataset_choice_rules(self):
        self.init_dataset_choice_rules(ExecutiveDashboardManager)
        data = []
        result = db_utils.DataBaseUtils.execute_sql(db_utils.DataBaseUtils,
                                                    sql_stmt.DataBaseSQL.select_all_data_from_table(
                                                        sql_stmt.DataBaseSQL, table=st.TABLE_DATASET_CHOICE_RULE),
                                                    fetchall=True, local=False)
        if result:
            for row in result:
                dataset_choice_rule = self.__parse_dataset_choice_rule_obj(
                    ExecutiveDashboardManager, row)
                data.append(dataset_choice_rule)
        return data

    def get_visualization_rights(self):
        self.init_visualization_rights(ExecutiveDashboardManager)
        data = []
        result = db_utils.DataBaseUtils.execute_sql(db_utils.DataBaseUtils,
                                                    sql_stmt.DataBaseSQL.select_all_data_from_table(
                                                        sql_stmt.DataBaseSQL, table=st.TABLE_VISUALIZATION_RIGHT),
                                                    fetchall=True, local=False)
        if result:
            for row in result:
                visualization_right = self.__parse_visualization_right_obj(
                    ExecutiveDashboardManager, row)
                data.append(visualization_right)
        return data

    def __parse_executive_dashboard_obj(self, db_row):
        if db_row:
            executive_dashboard_id = db_row[0]
            name = db_row[1]
            description = db_row[2]
            access_user_list = db_row[3]
            access_business_unit_list = db_row[4]
            plots = db_row[5]
            dataset_id = db_row[6]
            dataset_label = db_row[7]
            dataset_choice_rule = db_row[8]
            visualization_right = db_row[9]
            executive_dashboard = ed.ExecutiveDashboard(executive_dashboard_id=executive_dashboard_id, name=name, description=description,
                                                        access_user_list=access_user_list, access_business_unit_list=access_business_unit_list, plots=plots,
                                                        dataset_id=dataset_id, dataset_label=dataset_label, dataset_choice_rule=dataset_choice_rule,
                                                        visualization_right=visualization_right)
            return executive_dashboard
        pass

    def __parse_dataset_choice_rule_obj(self, db_row):
        if db_row:
            dataset_choice_rule_id = db_row[0]
            name = db_row[1]
            description = db_row[2]
            dataset_choice_rule = dt_ch_rl.DatsetChoiceRule(
                dataset_choice_rule_id=dataset_choice_rule_id, name=name, description=description)
            return dataset_choice_rule
        pass

    def __parse_visualization_right_obj(self, db_row):
        if db_row:
            visualization_right_id = db_row[0]
            name = db_row[1]
            description = db_row[2]
            visualization_right = vs_rg.VisualizationRight(
                visualization_right_id=visualization_right_id, name=name, description=description)
            return visualization_right
        pass
