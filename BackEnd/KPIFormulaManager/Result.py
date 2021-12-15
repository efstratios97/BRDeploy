import Utils.DataBaseUtils as db_utils
import Utils.DataBaseSQL as sql_stmt
import Utils.Settings as st


class Result:

    def create_result_table(self, table_name=st.TABLE_RESULT, local=False):
        db_utils.DataBaseUtils.execute_sql(
            db_utils.DataBaseUtils, sql_statement=sql_stmt.DataBaseSQL.
            create_Result_table_sql(sql_stmt.DataBaseSQL, table_name=table_name), local=local)

    def save_result(self, result, table_name=st.TABLE_RESULT):
        result = str(result)
        result_id = "result_" + st.create_id()
        db_utils.DataBaseUtils.execute_sql(
            db_utils.DataBaseUtils, sql_statement=sql_stmt.DataBaseSQL.
            insert_result_values(sql_stmt.DataBaseSQL, result_id=result_id, result=result, table_name=table_name), local=False)

    def clean_result(self, result_id, table_name=st.TABLE_RESULT, local=False):
        db_utils.DataBaseUtils.execute_sql(
            db_utils.DataBaseUtils,
            sql_statement=sql_stmt.DataBaseSQL.delete_row_from_table(
                sql_stmt.DataBaseSQL, table=table_name, condition=st.TB_RESULT_ID,
                condition_value=result_id, condition_operator="="), local=local)

    def drop_result_table(self, table_name=st.TABLE_RESULT, local=False):
        db_utils.DataBaseUtils.execute_sql(
            db_utils.DataBaseUtils,
            sql_statement=sql_stmt.DataBaseSQL.drop_table(
                sql_stmt.DataBaseSQL, table=table_name), local=local)

    def get_results(self, table_name=st.TABLE_RESULT):
        data = []
        result = db_utils.DataBaseUtils.execute_sql(db_utils.DataBaseUtils,
                                                    sql_stmt.DataBaseSQL.select_all_data_from_table(
                                                        sql_stmt.DataBaseSQL, table=table_name),
                                                    fetchall=True, local=False)
        for row in result:
            data.append(
                {"result_id": row[0], "result": st.string_dict_to_dict(row[1])})
        return data

    def get_result(self, result_id, table_name=st.TABLE_RESULT):
        result = db_utils.DataBaseUtils.execute_sql(db_utils.DataBaseUtils,
                                                    sql_stmt.DataBaseSQL.select_all_from_column(
                                                        sql_stmt.DataBaseSQL, table=table_name,
                                                        condition=st.TB_RESULT_ID, condition_value=result_id),
                                                    fetchone=True, local=False)
        return st.string_dict_to_dict(result[1])
