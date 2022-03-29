# Project Athena
'''
Owner: Efstratios Pahis
Contributors:
Description: SQL Statements for creating the Database Architecture
'''

import Utils.Settings as st
import json


class DataBaseSQL:

    # Returns SQL statement for creating the DataSet Table
    def create_DataSet_table_sql(self, archive=False, archive_uploads=False):
        if archive:
            table_name = st.TABLE_DATASET_ARCHIVE
            col_dataset_id = st.ARCHIVE_ID_PREFIX + st.TB_DATASET_COL_DATASET_ID
        elif archive_uploads:
            table_name = st.TABLE_DATASET_UPLOAD_ARCHIVE
            col_dataset_id = st.ARCHIVE_ID_PREFIX + st.TB_DATASET_COL_DATASET_ID
        else:
            table_name = st.TABLE_DATASET
            col_dataset_id = st.TB_DATASET_COL_DATASET_ID
        sql = ('CREATE TABLE IF NOT EXISTS {table} ('
               + '{col_DATASET_ID} VARCHAR(255) NOT NULL PRIMARY KEY,'
               + '{col_NAME} VARCHAR(255) NOT NULL,'
               + '{col_OWNER} VARCHAR(255) NOT NULL,'
               + '{col_HASH_OF_DATASET} VARCHAR(255) NOT NULL,'
               + '{col_CLEANED} INT NOT NULL,'
               + '{col_SIZE} INT NOT NULL,'
               + '{col_ACCESS_USER_LIST} TEXT(65535) NOT NULL,'
               + '{col_ACCESS_BUSINESS_UNIT_LIST} TEXT(65535) NOT NULL,'
               + '{col_STORAGE_TYPE} VARCHAR(45) NOT NULL,'
               + '{col_LABEL} VARCHAR(255),'
               + '{col_DESCRIPTION} TEXT(65535),'
               + '{col_CREATED_AT} TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL)')
        sql = sql.format(table=table_name, col_DATASET_ID=col_dataset_id, col_NAME=st.TB_DATASET_COL_NAME,
                         col_OWNER=st.TB_DATASET_COL_OWNER, col_HASH_OF_DATASET=st.TB_DATASET_COL_HASH_OF_DATASET,
                         col_CLEANED=st.TB_DATASET_COL_CLEANED, col_SIZE=st.TB_DATASET_COL_SIZE,
                         col_ACCESS_USER_LIST=st.TB_DATASET_COL_ACCESS_USER_LIST, col_ACCESS_BUSINESS_UNIT_LIST=st.TB_DATASET_COL_ACCESS_BUSINESS_UNIT_LIST,
                         col_STORAGE_TYPE=st.TB_DATASET_COL_STORAGE_TYPE, col_LABEL=st.TB_DATASET_COL_LABEL, col_DESCRIPTION=st.TB_DATASET_COL_DESCRIPTION,
                         col_CREATED_AT=st.TB_DATASET_COL_CREATED_AT)
        return sql

    # Returns SQL statement for creating the User Table
    def create_User_table_sql(self):
        sql = ('CREATE TABLE IF NOT EXISTS {table} ('
               + '{col_USER_ID} VARCHAR(255) NOT NULL PRIMARY KEY,'
               + '{col_FIRST_NAME} VARCHAR(255) NOT NULL,'
               + '{col_LAST_NAME} VARCHAR(255) NOT NULL,'
               + '{col_EMAIL} VARCHAR(255) NOT NULL UNIQUE,'
               + '{col_PASSWORD} VARCHAR(513) NOT NULL,'
               + '{col_BUSINESS_UNIT} VARCHAR(255) NOT NULL,'
               + '{col_ACCESS_RIGHTS} VARCHAR(255),'
               + '{col_ADMIN} INT NOT NULL DEFAULT 0,'
               + '{col_ROLE_MANAGER} INT NOT NULL DEFAULT 0,'
               + '{col_USER_DIRECTORY_PATH} VARCHAR(255) DEFAULT "C:\\USERS\\YOUR_USER",'
               + '{col_CREATED_AT} TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL);')
        sql = sql.format(table=st.TABLE_USER, col_USER_ID=st.TB_USER_COL_USER_ID, col_FIRST_NAME=st.TB_USER_COL_FIRST_NAME,
                         col_LAST_NAME=st.TB_USER_COL_LAST_NAME, col_EMAIL=st.TB_USER_COL_EMAIL,
                         col_PASSWORD=st.TB_USER_COL_PASSWORD, col_BUSINESS_UNIT=st.TB_USER_COL_BUSINESS_UNIT,
                         col_ACCESS_RIGHTS=st.TB_USER_COL_ACCESS_RIGHTS, col_ADMIN=st.TB_USER_COL_ADMIN,
                         col_ROLE_MANAGER=st.TB_USER_COL_ROLE_MANAGER, col_USER_DIRECTORY_PATH=st.TB_USER_COL_USER_DIRECTORY_PATH,
                         col_CREATED_AT=st.TB_USER_COL_CREATED_AT)
        return sql

    # Returns SQL statement for creating the Cleanser Table
    def create_Cleanser_table_sql(self):
        sql = ('CREATE TABLE IF NOT EXISTS {table} ('
               + '{col_CLEANSER_ID} VARCHAR(255) NOT NULL PRIMARY KEY,'
               + '{col_NAME} VARCHAR(512) NOT NULL UNIQUE,'
               + '{col_DESCRIPTION} TEXT(65535) NOT NULL,'
               + '{col_HEADER_LIST} TEXT(4294967295) NOT NULL,'
               + '{col_DATASETIDS} TEXT(65535) NOT NULL,'
               + '{col_CLEANSER_OPERATION_TYPES} TEXT(65535) NOT NULL,'
               + '{col_CREATED_AT} TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL);')
        sql = sql.format(table=st.TABLE_CLEANSER, col_CLEANSER_ID=st.TB_CLEANSER_COL_CLEANSER_ID, col_NAME=st.TB_CLEANSER_COL_NAME,
                         col_DESCRIPTION=st.TB_CLEANSER_COL_DESCRIPTION, col_HEADER_LIST=st.TB_CLEANSER_COL_HEADER_LIST,
                         col_DATASETIDS=st.TB_CLEANSER_COL_DATASETIDS, col_CLEANSER_OPERATION_TYPES=st.TB_CLEANSER_OPERATION_TYPES,
                         col_CREATED_AT=st.TB_CLEANSER_COL_CREATED_AT)
        return sql

    # Returns SQL statement for creating the Department Table
    def create_department_table_sql(self):
        sql = ('CREATE TABLE IF NOT EXISTS {table} ('
               + '{col_DEPARTMENT_ID} VARCHAR(255) NOT NULL PRIMARY KEY,'
               + '{col_NAME} VARCHAR(255) NOT NULL UNIQUE,'
               + '{col_CREATED_AT} TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL);')
        sql = sql.format(table=st.TABLE_DEPARTMENTS, col_DEPARTMENT_ID=st.TB_DEPARTMENTS_COL_DEPARTMENT_ID,
                         col_NAME=st.TB_DEPARTMENTS_COL_NAME,
                         col_CREATED_AT=st.TB_DEPARTMENTS_COL_CREATED_AT)
        return sql

    # Returns SQL statement for creating the Architecture Views Table
    def create_architecture_views_table_sql(self):
        sql = ('CREATE TABLE IF NOT EXISTS {table} ('
               + '{col_ARCHITECTURE_VIEW_ID} VARCHAR(255) NOT NULL PRIMARY KEY,'
               + '{col_NAME} VARCHAR(255) NOT NULL UNIQUE,'
               + '{col_DESCRIPTION} TEXT(65535) NOT NULL,'
               + '{col_ARCHITECTURE_VIEW_COMPONENTS} TEXT(4294967295) NOT NULL,'
               + '{col_CREATED_AT} TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL);')
        sql = sql.format(table=st.TABLE_ARCHITECTURE_VIEWS, col_ARCHITECTURE_VIEW_ID=st.TB_ARCHITECTURE_VIEWS_COL_ARCHITECTURE_VIEW_ID,
                         col_NAME=st.TB_ARCHITECTURE_VIEWS_COL_ARCHITECTURE_VIEW_NAME,
                         col_DESCRIPTION=st.TB_ARCHITECTURE_VIEWS_COL_ARCHITECTURE_VIEW_DESCRIPTION,
                         col_ARCHITECTURE_VIEW_COMPONENTS=st.TB_ARCHITECTURE_VIEWS_COL_ARCHITECTURE_VIEW_COMPONENTS,
                         col_CREATED_AT=st.TB_ARCHITECTURE_VIEWS_COL_CREATED_AT)
        return sql

    # Returns SQL statement for creating the Executive Dashboard Table
    def create_Executive_Dashboard_table_sql(self):
        sql = ('CREATE TABLE IF NOT EXISTS {table} ('
               + '{col_EXECUTIVE_DASHBOARD_ID} VARCHAR(255) PRIMARY KEY,'
               + '{col_NAME} VARCHAR(255) NOT NULL,'
               + '{col_DESCRIPTION} TEXT(65535),'
               + '{col_ACCESS_USER_LIST} TEXT(65535) NOT NULL,'
               + '{col_ACCESS_BUSINESS_UNIT_LIST} TEXT(65535) NOT NULL,'
               + '{col_PLOTS} TEXT(65535) NOT NULL,'
               + '{col_DATASET_ID} VARCHAR(255) NOT NULL,'
               + '{col_DATASET_LABEL} VARCHAR(255) NOT NULL,'
               + '{col_DATASET_CHOICE_RULE} VARCHAR(255) NOT NULL,'
               + '{col_VISUALIZATION_RIGHT} VARCHAR(255) NOT NULL,'
               + '{col_CREATED_AT} TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL)')
        sql = sql.format(table=st.TABLE_EXECUTIVE_DASHBOARDS, col_EXECUTIVE_DASHBOARD_ID=st.TB_EXECUTIVE_DASHBOARDS_COL_ID,
                         col_NAME=st.TB_EXECUTIVE_DASHBOARDS_COL_NAME,
                         col_DESCRIPTION=st.TB_EXECUTIVE_DASHBOARDS_COL_DESCRIPTION,
                         col_ACCESS_USER_LIST=st.TB_EXECUTIVE_DASHBOARDS_COL_ACCESS_USER_LIST,
                         col_ACCESS_BUSINESS_UNIT_LIST=st.TB_EXECUTIVE_DASHBOARDS_COL_ACCESS_BUSINESS_UNIT_LIST,
                         col_PLOTS=st.TB_EXECUTIVE_DASHBOARDS_COL_PLOTS, col_DATASET_ID=st.TB_EXECUTIVE_DASHBOARDS_COL_DATASET_ID,
                         col_DATASET_LABEL=st.TB_EXECUTIVE_DASHBOARDS_COL_DATASET_LABEL, col_DATASET_CHOICE_RULE=st.TB_EXECUTIVE_DASHBOARDS_COL_DATASET_CHOICE_RULE,
                         col_VISUALIZATION_RIGHT=st.TB_EXECUTIVE_DASHBOARDS_COL_VISUALIZATION_RIGHT,
                         col_CREATED_AT=st.TB_EXECUTIVE_DASHBOARDS_COL_CREATED_AT)
        return sql

    # Returns SQL statement for creating the Executive Dashboard Table
    def create_Plots_table_sql(self):
        sql = ('CREATE TABLE IF NOT EXISTS {table} ('
               + '{col_PLOT_ID} VARCHAR(255) PRIMARY KEY,'
               + '{col_FORMDATA} TEXT(4294967295) NOT NULL,'
               + '{col_GROUPED} VARCHAR(255) NOT NULL,'
               + '{col_VISUALIZATION_TYPE} VARCHAR(512) NOT NULL,'
               + '{col_VISUALIZATION_RIGHT} VARCHAR(512) NOT NULL,'
               + '{col_COMPONENT_NAME} VARCHAR(255) NOT NULL,'
               + '{col_CREATED_AT} TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL)')
        sql = sql.format(table=st.TABLE_PLOTS, col_PLOT_ID=st.TB_PLOTS_COL_ID,
                         col_FORMDATA=st.TB_PLOTS_COL_FORMDATA,
                         col_GROUPED=st.TB_PLOTS_COL_GROUPED,
                         col_VISUALIZATION_TYPE=st.TB_PLOTS_COL_VISUALIZATION_TYPE,
                         col_VISUALIZATION_RIGHT=st.TB_PLOTS_COL_VISUALIZATION_RIGHT,
                         col_COMPONENT_NAME=st.TB_PLOTS_COL_COMPONENT_NAME,
                         col_CREATED_AT=st.TB_PLOTS_COL_CREATED_AT)
        return sql

    # Returns SQL statement for creating the Category Table

    def create_label_table_sql(self):
        sql = ('CREATE TABLE IF NOT EXISTS {table} ('
               + '{col_LABEL_ID} VARCHAR(255) NOT NULL PRIMARY KEY,'
               + '{col_NAME} VARCHAR(255) NOT NULL UNIQUE,'
               + '{col_HEADER_LIST} TEXT(4294967295), '
               + '{col_OPERATIONS_LIST} TEXT(4294967295), '
               + '{col_CREATED_AT} TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL);')
        sql = sql.format(table=st.TABLE_LABEL, col_LABEL_ID=st.TB_LABEL_COL_ID,
                         col_NAME=st.TB_LABEL_COL_NAME, col_HEADER_LIST=st.TB_LABEL_COL_HEADER,
                         col_OPERATIONS_LIST=st.TB_LABEL_COL_OPERATIONS_CLEANSER, col_CREATED_AT=st.TB_LABEL_COL_CREATED_AT)
        return sql

    def create_KPI_table_sql(self):
        sql = ('CREATE TABLE IF NOT EXISTS {table} ('
               + '{col_KPI_ID} VARCHAR(255) NOT NULL PRIMARY KEY,'
               + '{col_NAME} VARCHAR(255) NOT NULL UNIQUE,'
               + '{col_DESCRIPTION} TEXT(65535),'
               + '{col_HIGH_LEVEL_KPI_COMPONENT_KPI_WEIGHT} TEXT(4294967295),'
               + '{col_KPI_ASPECTS_WEIGHTS} TEXT(4294967295),'
               + '{col_THRESHOLD} INT NOT NULL DEFAULT 0,'
               + '{col_FORMULA} TEXT(65535),'
               + '{col_DATASET_ID} TEXT(65535),'
               + '{col_DATASET_LABELS} TEXT(65535),'
               + '{col_KPI_FAMILY} TEXT(65535) NOT NULL,'
               + '{col_COLOR_CODING} TEXT(512) NOT NULL,'
               + '{col_CREATED_AT} TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL)')
        sql = sql.format(table=st.TABLE_KPI, col_KPI_ID=st.TB_KPI_COL_KPI_ID, col_NAME=st.TB_KPI_COL_NAME,
                         col_DESCRIPTION=st.TB_KPI_COL_DESCRIPTION, col_HIGH_LEVEL_KPI_COMPONENT_KPI_WEIGHT=st.TB_KPI_COL_HIGH_LEVEL_KPI_COMPONENT_KPI_WEIGHT,
                         col_KPI_ASPECTS_WEIGHTS=st.TB_KPI_COL_KPI_ASPECTS_WEIGHTS, col_THRESHOLD=st.TB_KPI_COL_THRESHOLD,
                         col_FORMULA=st.TB_KPI_COL_FORMULA, col_DATASET_ID=st.TB_KPI_COL_DATASET_ID,
                         col_DATASET_LABELS=st.TB_KPI_COL_DATASET_LABELS, col_KPI_FAMILY=st.TB_KPI_COL_KPI_FAMILY,
                         col_COLOR_CODING=st.TB_KPI_COL_COLOR_CODING, col_CREATED_AT=st.TB_KPI_COL_CREATED_AT)
        return sql

    def create_ASPECT_table_sql(self):
        sql = ('CREATE TABLE IF NOT EXISTS {table} ('
               + '{col_ASPECT_ID} VARCHAR(255) NOT NULL PRIMARY KEY,'
               + '{col_NAME} VARCHAR(255) NOT NULL UNIQUE,'
               + '{col_DESCRIPTION} TEXT(65535),'
               + '{col_RAW_COMPONENTS_FROM_DATASET} TEXT(4294967295),'
               + '{col_SKALA_SIZE} INT NOT NULL DEFAULT 0,'
               + '{col_WEIGHT} INT NOT NULL DEFAULT 0,'
               + '{col_THRESHOLD} INT NOT NULL DEFAULT 0,'
               + '{col_OPERATION_TYPE} TEXT(65535),'
               + '{col_FORMULA} TEXT(65535),'
               + '{col_DATASET_ID} TEXT(65535),'
               + '{col_DATASET_LABELS} TEXT(65535),'
               + '{col_KPI_FAMILY} TEXT(65535) NOT NULL,'
               + '{col_CREATED_AT} TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL)')
        sql = sql.format(table=st.TABLE_ASPECT, col_ASPECT_ID=st.TB_ASPECT_COL_ID, col_NAME=st.TB_ASPECT_COL_NAME,
                         col_DESCRIPTION=st.TB_ASPECT_COL_DESCRIPTION, col_RAW_COMPONENTS_FROM_DATASET=st.TB_ASPECT_COL_RAW_COMPONENTS_FROM_DATASET,
                         col_SKALA_SIZE=st.TB_ASPECT_COL_SKALA_SIZE, col_WEIGHT=st.TB_ASPECT_COL_WEIGHT, col_OPERATION_TYPE=st.TB_ASPECT_COL_OPERATION_TYPE,
                         col_THRESHOLD=st.TB_ASPECT_COL_THRESHOLD, col_FORMULA=st.TB_ASPECT_COL_FORMULA, col_DATASET_ID=st.TB_ASPECT_COL_DATASET_ID,
                         col_DATASET_LABELS=st.TB_ASPECT_COL_DATASET_LABELS, col_KPI_FAMILY=st.TB_ASPECT_COL_KPI_FAMILY,
                         col_CREATED_AT=st.TB_ASPECT_COL_CREATED_AT)
        return sql

    def create_Formula_table_sql(self):
        sql = ('CREATE TABLE IF NOT EXISTS {table} ('
               + '{col_FORMULA_ID} VARCHAR(255) NOT NULL PRIMARY KEY,'
               + '{col_NAME} VARCHAR(255) NOT NULL UNIQUE,'
               + '{col_DESCRIPTION} TEXT(65535),'
               + '{col_OPERATION} TEXT(65535),'
               + '{col_PURPOSE} VARCHAR(512),'
               + '{col_KPI_FAMILIES} TEXT(65535),'
               + '{col_CREATED_AT} TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL)')
        sql = sql.format(table=st.TABLE_FORMULA, col_FORMULA_ID=st.TB_FORMULA_COL_FORMULA_ID, col_NAME=st.TB_FORMULA_COL_NAME,
                         col_DESCRIPTION=st.TB_FORMULA_COL_DESCRIPTION, col_OPERATION=st.TB_FORMULA_COL_OPERATION,
                         col_PURPOSE=st.TB_FORMULA_COL_PURPOSE, col_KPI_FAMILIES=st.TB_FORMULA_COL_KPI_FAMILIES,
                         col_CREATED_AT=st.TB_FORMULA_COL_CREATED_AT)
        return sql

    def create_KPI_Category_Type_table_sql(self):
        sql = ('CREATE TABLE IF NOT EXISTS {table} ('
               + '{col_CATEGORY_TYPE_ID} VARCHAR(255) NOT NULL PRIMARY KEY,'
               + '{col_NAME} VARCHAR(512) NOT NULL UNIQUE,'
               + '{col_CREATED_AT} TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL)')
        sql = sql.format(table=st.TABLE_KPI_CATEGORY_TYPE, col_CATEGORY_TYPE_ID=st.TB_KPI_CATEGORY_TYPE_COL_ID,
                         col_NAME=st.TB_KPI_CATEGORY_TYPE_COL_NAME,
                         col_CREATED_AT=st.TB_KPI_COL_CREATED_AT)
        return sql

    def create_dataset_choice_rule_table_sql(self):
        sql = ('CREATE TABLE IF NOT EXISTS {table} ('
               + '{col_DATA_CHOICE_RULE_ID} VARCHAR(255) NOT NULL PRIMARY KEY,'
               + '{col_NAME} VARCHAR(512) NOT NULL UNIQUE,'
               + '{col_DESCRIPTION} TEXT(65535),'
               + '{col_CREATED_AT} TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL)')
        sql = sql.format(table=st.TABLE_DATASET_CHOICE_RULE, col_DATA_CHOICE_RULE_ID=st.TB_DATASET_CHOICE_RULE_COL_ID,
                         col_NAME=st.TB_DATASET_CHOICE_RULE_COL_NAME, col_DESCRIPTION=st.TB_DATASET_CHOICE_RULE_COL_DESCRIPTION,
                         col_CREATED_AT=st.TB_DATASET_CHOICE_RULE_COL_CREATED_AT)
        return sql

    def create_visualization_right_table_sql(self):
        sql = ('CREATE TABLE IF NOT EXISTS {table} ('
               + '{col_VISUALIZATION_RIGHT_ID} VARCHAR(255) NOT NULL PRIMARY KEY,'
               + '{col_NAME} VARCHAR(512) NOT NULL UNIQUE,'
               + '{col_DESCRIPTION} TEXT(65535),'
               + '{col_CREATED_AT} TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL)')
        sql = sql.format(table=st.TABLE_VISUALIZATION_RIGHT, col_VISUALIZATION_RIGHT_ID=st.TB_VISUALIZATION_RIGHT_COL_ID,
                         col_NAME=st.TB_VISUALIZATION_RIGHT_COL_NAME, col_DESCRIPTION=st.TB_VISUALIZATION_RIGHT_COL_DESCRIPTION,
                         col_CREATED_AT=st.TB_VISUALIZATION_RIGHT_COL_CREATED_AT)
        return sql

    def create_Result_table_sql(self, table_name):
        sql = ('CREATE TABLE IF NOT EXISTS {table} ('
               + '{col_Result_ID} VARCHAR(255) NOT NULL PRIMARY KEY,'
               + '{col_Result} TEXT(4294967295),'
               + '{col_CREATED_AT} TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL)')
        sql = sql.format(table=table_name, col_Result_ID=st.TB_RESULT_ID, col_Result=st.TB_RESULT_RESULT,
                         col_CREATED_AT=st.TB_RESULT_CREATED_AT)
        return sql

    # Returns SQL statement for creating a many-to-may relation table
    # for datasets and user to define access rights
    def create_User_Dataset_access_relation_table_sql(self):
        sql = ('CREATE TABLE IF NOT EXISTS {table} ('
               + '{foreign_key_1} VARCHAR(255) NOT NULL,'
               + '{foreign_key_2} VARCHAR(255) NOT NULL,'
               + 'PRIMARY KEY ({foreign_key_1}, {foreign_key_2}), '
               + 'FOREIGN KEY ({foreign_key_1}) REFERENCES {table_foreign_key_1}({foreign_key_1}), '
               + 'FOREIGN KEY ({foreign_key_2}) REFERENCES {table_foreign_key_2}({foreign_key_2}), '
               + 'CONSTRAINT {foreign_key_1} '
               + 'FOREIGN KEY ({foreign_key_1}) '
               + 'REFERENCES {table_foreign_key_1} ({foreign_key_1}) '
               + 'ON DELETE CASCADE '
               + 'ON UPDATE CASCADE, '
               + 'CONSTRAINT {foreign_key_2} '
               + 'FOREIGN KEY ({foreign_key_2}) '
               + 'REFERENCES {table_foreign_key_2} ({foreign_key_2}) '
               + 'ON DELETE CASCADE '
               + 'ON UPDATE CASCADE, '
               + 'UNIQUE ({foreign_key_1}, {foreign_key_2}));')
        sql = sql.format(table=st.TABLE_USER_DATASET_ACCESS_RELATION,
                         table_foreign_key_1=st.TABLE_DATASET, table_foreign_key_2=st.TABLE_USER,
                         foreign_key_1=st.TB_DATASET_COL_DATASET_ID, foreign_key_2=st.TB_USER_COL_USER_ID)
        return sql

    def create_Department_Dataset_access_relation_table_sql(self):
        sql = ('CREATE TABLE IF NOT EXISTS {table} ('
               + '{foreign_key_1} VARCHAR(255) NOT NULL,'
               + '{foreign_key_2} VARCHAR(255) NOT NULL,'
               + 'PRIMARY KEY ({foreign_key_1}, {foreign_key_2}), '
               + 'FOREIGN KEY ({foreign_key_1}) REFERENCES {table_foreign_key_1}({foreign_key_1}), '
               + 'FOREIGN KEY ({foreign_key_2}) REFERENCES {table_foreign_key_2}({foreign_key_2}), '
               + 'CONSTRAINT {foreign_key_1}_fk_n3 '
               + 'FOREIGN KEY ({foreign_key_1}) '
               + 'REFERENCES {table_foreign_key_1} ({foreign_key_1}) '
               + 'ON DELETE CASCADE '
               + 'ON UPDATE CASCADE, '
               + 'CONSTRAINT {foreign_key_2}_fk_n3 '
               + 'FOREIGN KEY ({foreign_key_2}) '
               + 'REFERENCES {table_foreign_key_2} ({foreign_key_2}) '
               + 'ON DELETE CASCADE '
               + 'ON UPDATE CASCADE, '
               + 'UNIQUE ({foreign_key_1}, {foreign_key_2}));')
        sql = sql.format(table=st.TABLE_DEPARTMENT_DATASET_ACCESS_RELATION,
                         table_foreign_key_1=st.TABLE_DATASET, table_foreign_key_2=st.TABLE_DEPARTMENTS,
                         foreign_key_1=st.TB_DATASET_COL_DATASET_ID, foreign_key_2=st.TB_DEPARTMENTS_COL_DEPARTMENT_ID)
        return sql

    # Returns SQL statement for creating a many-to-may relation table
    # for cleansers and datasetsd to define compatibility
    def create_Cleanser_Dataset_compatibility_relation_table_sql(self):
        sql = ('CREATE TABLE IF NOT EXISTS {table} ('
               + '{foreign_key_1} VARCHAR(255) NOT NULL,'
               + '{foreign_key_2} VARCHAR(255) NOT NULL,'
               + 'PRIMARY KEY ({foreign_key_1}, {foreign_key_2}), '
               + 'FOREIGN KEY ({foreign_key_1}) REFERENCES {table_foreign_key_1}({foreign_key_1}), '
               + 'FOREIGN KEY ({foreign_key_2}) REFERENCES {table_foreign_key_2}({foreign_key_2}), '
               + 'CONSTRAINT {foreign_key_1}_fk_n2  '
               + 'FOREIGN KEY ({foreign_key_1}) '
               + 'REFERENCES {table_foreign_key_1} ({foreign_key_1}) '
               + 'ON DELETE CASCADE '
               + 'ON UPDATE CASCADE, '
               + 'CONSTRAINT {foreign_key_2}_fk_n2 '
               + 'FOREIGN KEY ({foreign_key_2}) '
               + 'REFERENCES {table_foreign_key_2} ({foreign_key_2}) '
               + 'ON DELETE CASCADE '
               + 'ON UPDATE CASCADE, '
               + 'UNIQUE ({foreign_key_1}, {foreign_key_2}));')
        sql = sql.format(table=st.TABLE_CLEANSER_DATASET_COMPATIBILITY,
                         table_foreign_key_1=st.TABLE_DATASET, table_foreign_key_2=st.TABLE_CLEANSER,
                         foreign_key_1=st.TB_DATASET_COL_DATASET_ID, foreign_key_2=st.TB_CLEANSER_COL_CLEANSER_ID)
        return sql

    def create_ExecutiveDashboard_Plot_relation_table_sql(self):
        sql = ('CREATE TABLE IF NOT EXISTS {table} ('
               + '{foreign_key_1} VARCHAR(255) NOT NULL,'
               + '{foreign_key_2} VARCHAR(255) NOT NULL,'
               + 'PRIMARY KEY ({foreign_key_1}, {foreign_key_2}), '
               + 'FOREIGN KEY ({foreign_key_1}) REFERENCES {table_foreign_key_1}({foreign_key_1}), '
               + 'FOREIGN KEY ({foreign_key_2}) REFERENCES {table_foreign_key_2}({foreign_key_2}), '
               + 'CONSTRAINT {foreign_key_1}_fk_n4 '
               + 'FOREIGN KEY ({foreign_key_1}) '
               + 'REFERENCES {table_foreign_key_1} ({foreign_key_1}) '
               + 'ON DELETE CASCADE '
               + 'ON UPDATE CASCADE, '
               + 'CONSTRAINT {foreign_key_2}_fk_n4 '
               + 'FOREIGN KEY ({foreign_key_2}) '
               + 'REFERENCES {table_foreign_key_2} ({foreign_key_2}) '
               + 'ON DELETE CASCADE '
               + 'ON UPDATE CASCADE, '
               + 'UNIQUE ({foreign_key_1}, {foreign_key_2}));')
        sql = sql.format(table=st.TABLE_EXECUTIVE_DASHBOARDS_PLOTS_RELATION,
                         table_foreign_key_1=st.TABLE_EXECUTIVE_DASHBOARDS, table_foreign_key_2=st.TABLE_PLOTS,
                         foreign_key_1=st.TB_EXECUTIVE_DASHBOARDS_COL_ID, foreign_key_2=st.TB_PLOTS_COL_ID)
        return sql

    def create_KPI_Formula_relation_table_sql(self):
        sql = ('CREATE TABLE IF NOT EXISTS {table} ('
               + '{foreign_key_1} VARCHAR(255) NOT NULL,'
               + '{foreign_key_2} VARCHAR(255) NOT NULL,'
               + 'PRIMARY KEY ({foreign_key_1}, {foreign_key_2}), '
               + 'FOREIGN KEY ({foreign_key_1}) REFERENCES {table_foreign_key_1}({foreign_key_1}), '
               + 'FOREIGN KEY ({foreign_key_2}) REFERENCES {table_foreign_key_2}({foreign_key_2}), '
               + 'CONSTRAINT {foreign_key_1}_fk_n5 '
               + 'FOREIGN KEY ({foreign_key_1}) '
               + 'REFERENCES {table_foreign_key_1} ({foreign_key_1}) '
               + 'ON DELETE CASCADE '
               + 'ON UPDATE CASCADE, '
               + 'CONSTRAINT {foreign_key_2}_fk_n5 '
               + 'FOREIGN KEY ({foreign_key_2}) '
               + 'REFERENCES {table_foreign_key_2} ({foreign_key_2}) '
               + 'ON DELETE CASCADE '
               + 'ON UPDATE CASCADE, '
               + 'UNIQUE ({foreign_key_1}, {foreign_key_2}));')
        sql = sql.format(table=st.TABLE_KPI_FORMULA_RELATION,
                         table_foreign_key_1=st.TABLE_KPI, table_foreign_key_2=st.TABLE_FORMULA,
                         foreign_key_1=st.TB_KPI_COL_KPI_ID, foreign_key_2=st.TB_FORMULA_COL_FORMULA_ID)
        return sql

    def create_Aspect_Formula_relation_table_sql(self):
        sql = ('CREATE TABLE IF NOT EXISTS {table} ('
               + '{foreign_key_1} VARCHAR(255) NOT NULL,'
               + '{foreign_key_2} VARCHAR(255) NOT NULL,'
               + 'PRIMARY KEY ({foreign_key_1}, {foreign_key_2}), '
               + 'FOREIGN KEY ({foreign_key_1}) REFERENCES {table_foreign_key_1}({foreign_key_1}), '
               + 'FOREIGN KEY ({foreign_key_2}) REFERENCES {table_foreign_key_2}({foreign_key_2}), '
               + 'CONSTRAINT {foreign_key_1}_fk_n6 '
               + 'FOREIGN KEY ({foreign_key_1}) '
               + 'REFERENCES {table_foreign_key_1} ({foreign_key_1}) '
               + 'ON DELETE CASCADE '
               + 'ON UPDATE CASCADE, '
               + 'CONSTRAINT {foreign_key_2}_fk_n6 '
               + 'FOREIGN KEY ({foreign_key_2}) '
               + 'REFERENCES {table_foreign_key_2} ({foreign_key_2}) '
               + 'ON DELETE CASCADE '
               + 'ON UPDATE CASCADE, '
               + 'UNIQUE ({foreign_key_1}, {foreign_key_2}));')
        sql = sql.format(table=st.TABLE_ASPECT_FORMULA_RELATION,
                         table_foreign_key_1=st.TABLE_ASPECT, table_foreign_key_2=st.TABLE_FORMULA,
                         foreign_key_1=st.TB_ASPECT_COL_ID, foreign_key_2=st.TB_FORMULA_COL_FORMULA_ID)
        return sql

    def create_KPI_ASPECT_WEIGHT_relation_table_sql(self):
        sql = ('CREATE TABLE IF NOT EXISTS {table} ('
               + '{foreign_key_1} VARCHAR(255) NOT NULL,'
               + '{foreign_key_2} VARCHAR(255) NOT NULL,'
               + '{col_ASPECT_WEIGHT} INT NOT NULL,'
               + 'PRIMARY KEY ({foreign_key_1}, {foreign_key_2}), '
               + 'FOREIGN KEY ({foreign_key_1}) REFERENCES {table_foreign_key_1}({foreign_key_1}), '
               + 'FOREIGN KEY ({foreign_key_2}) REFERENCES {table_foreign_key_2}({foreign_key_2}), '
               + 'CONSTRAINT {foreign_key_1}_fk_n7 '
               + 'FOREIGN KEY ({foreign_key_1}) '
               + 'REFERENCES {table_foreign_key_1} ({foreign_key_1}) '
               + 'ON DELETE CASCADE '
               + 'ON UPDATE CASCADE, '
               + 'CONSTRAINT {foreign_key_2}_fk_n7 '
               + 'FOREIGN KEY ({foreign_key_2}) '
               + 'REFERENCES {table_foreign_key_2} ({foreign_key_2}) '
               + 'ON DELETE CASCADE '
               + 'ON UPDATE CASCADE, '
               + 'UNIQUE ({foreign_key_1}, {foreign_key_2}));')
        sql = sql.format(table=st.TABLE_KPI_ASPECT_RELATION,
                         table_foreign_key_1=st.TABLE_KPI, table_foreign_key_2=st.TABLE_ASPECT,
                         foreign_key_1=st.TB_KPI_COL_KPI_ID, foreign_key_2=st.TB_ASPECT_COL_ID,
                         col_ASPECT_WEIGHT=st.TB_ASPECT_COL_WEIGHT)
        return sql

    def insert_kpi_formula_relation_values(self, kpi_id, formula_id):
        sql = ('INSERT INTO {table} ({col_KPI_ID}, {col_FORMULA_ID}) '
               + 'VALUES ("{KPI_ID}", "{FORMULA_ID}");')
        sql = sql.format(table=st.TABLE_KPI_FORMULA_RELATION,
                         col_KPI_ID=st.TB_KPI_COL_KPI_ID,
                         col_FORMULA_ID=st.TB_FORMULA_COL_FORMULA_ID,
                         KPI_ID=kpi_id, FORMULA_ID=formula_id)
        return sql

    def insert_aspect_formula_relation_values(self, aspect_id, formula_id):
        sql = ('INSERT INTO {table} ({col_ASPECT_ID}, {col_FORMULA_ID}) '
               + 'VALUES ("{ASPECT_ID}", "{FORMULA_ID}");')
        sql = sql.format(table=st.TABLE_ASPECT_FORMULA_RELATION,
                         col_ASPECT_ID=st.TB_ASPECT_COL_ID,
                         col_FORMULA_ID=st.TB_FORMULA_COL_FORMULA_ID,
                         ASPECT_ID=aspect_id, FORMULA_ID=formula_id)
        return sql

    def insert_kpi_aspect_relation_values(self, kpi_id, aspect_id, weight):
        sql = ('INSERT INTO {table} ({col_KPI_ID}, {col_ASPECT_ID}, {col_WEIGHT}) '
               + 'VALUES ("{KPI_ID}","{ASPECT_ID}", "{WEIGHT}");')
        sql = sql.format(table=st.TABLE_KPI_ASPECT_RELATION,
                         col_KPI_ID=st.TB_KPI_COL_KPI_ID,
                         col_ASPECT_ID=st.TB_ASPECT_COL_ID,
                         col_WEIGHT=st.TB_ASPECT_COL_WEIGHT,
                         KPI_ID=kpi_id, ASPECT_ID=aspect_id, WEIGHT=weight)
        return sql

    def insert_user_dataset_access_relation_values(self, dataset_id, user_id):
        sql = ('INSERT INTO {table} ({col_DATASET_ID}, {col_USER_ID}) '
               + 'VALUES ("{DATASET_ID}", "{USER_ID}");')
        sql = sql.format(table=st.TABLE_USER_DATASET_ACCESS_RELATION,
                         col_DATASET_ID=st.TB_DATASET_COL_DATASET_ID,
                         col_USER_ID=st.TB_USER_COL_USER_ID,
                         DATASET_ID=dataset_id, USER_ID=user_id)
        return sql

    def insert_department_dataset_access_relation_values(self, dataset_id, department_id):
        sql = ('INSERT INTO {table} ({col_DATASET_ID}, {col_DEPARTMENT_ID}) '
               + 'VALUES ("{DATASET_ID}", "{DEPARTMENT_ID}");')
        sql = sql.format(table=st.TABLE_DEPARTMENT_DATASET_ACCESS_RELATION,
                         col_DATASET_ID=st.TB_DATASET_COL_DATASET_ID,
                         col_DEPARTMENT_ID=st.TB_DEPARTMENTS_COL_DEPARTMENT_ID,
                         DATASET_ID=dataset_id, DEPARTMENT_ID=department_id)
        return sql

    def insert_cleanser_dataset_compatability_relation_values(self, dataset_id, cleanser_id):
        sql = ('INSERT INTO {table} ({col_DATASET_ID}, {col_CLEANSER_ID}) '
               + 'VALUES ("{DATASET_ID}", "{CLEANSER_ID}");')
        sql = sql.format(table=st.TABLE_CLEANSER_DATASET_COMPATIBILITY,
                         col_DATASET_ID=st.TB_DATASET_COL_DATASET_ID,
                         col_CLEANSER_ID=st.TB_CLEANSER_COL_CLEANSER_ID,
                         DATASET_ID=dataset_id, CLEANSER_ID=cleanser_id)
        return sql

    def insert_executive_dashboard_plots_relation_values(self, executive_dashboard_id, plot_id):
        sql = ('INSERT INTO {table} ({col_EXECUTIVE_DASHBOARD_ID}, {col_PLOT_ID}) '
               + 'VALUES ("{EXECUTIVE_DASHBOARD_ID}", "{PLOT_ID}");')
        sql = sql.format(table=st.TABLE_EXECUTIVE_DASHBOARDS_PLOTS_RELATION,
                         col_EXECUTIVE_DASHBOARD_ID=st.TB_EXECUTIVE_DASHBOARDS_COL_ID,
                         col_PLOT_ID=st.TB_PLOTS_COL_ID,
                         EXECUTIVE_DASHBOARD_ID=executive_dashboard_id, PLOT_ID=plot_id)
        return sql

    # Returns SQL statement for inserting a architecture_view in architecture_view table
    def insert_architecture_view_values(self, architecture_viewID, architecture_view_name,
                                        architecture_view_description, architecture_view_components):
        sql = ('INSERT INTO {table} ({col_ARCHITECTURE_VIEW_ID}, {col_NAME}, {col_DESCRIPTION}, {col_ARCHITECTURE_VIEW_COMPONENTS}) '
               + 'VALUES ("{ARCHITECTURE_VIEW_ID}", "{NAME}", "{DESCRIPTION}", "{ARCHITECTURE_VIEW_COMPONENTS}");')
        sql = sql.format(table=st.TABLE_ARCHITECTURE_VIEWS, col_ARCHITECTURE_VIEW_ID=st.TB_ARCHITECTURE_VIEWS_COL_ARCHITECTURE_VIEW_ID,
                         col_NAME=st.TB_ARCHITECTURE_VIEWS_COL_ARCHITECTURE_VIEW_NAME,
                         col_DESCRIPTION=st.TB_ARCHITECTURE_VIEWS_COL_ARCHITECTURE_VIEW_DESCRIPTION,
                         col_ARCHITECTURE_VIEW_COMPONENTS=st.TB_ARCHITECTURE_VIEWS_COL_ARCHITECTURE_VIEW_COMPONENTS,
                         ARCHITECTURE_VIEW_ID=architecture_viewID, NAME=architecture_view_name,
                         DESCRIPTION=architecture_view_description, ARCHITECTURE_VIEW_COMPONENTS=architecture_view_components)
        return sql

    # Returns SQL statement for inserting a executive_dashboard in executive_dashboard table
    def insert_executive_dashboard_values(self, executive_dashboard_id, executive_dashboard_name,
                                          executive_dashboard_description, access_user_list, access_business_unit_list,
                                          executive_dashboard_plots, dataset_id, dataset_label, dataset_choice_rule, visualization_right=""):
        sql = ('INSERT INTO {table} ({col_ID}, {col_NAME}, {col_DESCRIPTION}, {col_ACCESS_USER_LIST},'
               + '{col_ACCESS_BUSINESS_UNIT_LIST}, {col_PLOTS}, {col_DATASET_ID}, {col_DATASET_LABEL},'
               + '{col_DATASET_CHOICE_RULE}, {col_VISUALIZATION_RIGHT}) '
               + 'VALUES ("{EXECUTIVE_DASHBOARD_ID}", "{NAME}", "{DESCRIPTION}", "{ACCESS_USER_LIST}",'
               + '"{ACCESS_BUSINESS_UNIT_LIST}" , "{EXECUTIVE_DASHBOARD_COMPONENTS}", "{EXECUTIVE_DASHBOARD_DATASET_ID}",'
               + '"{EXECUTIVE_DASHBOARD_DATASET_LABEL}", "{EXECUTIVE_DASHBOARD_DATASET_CHOICE_RULE}", "{EXECUTIVE_DASHBOARD_VISUALIZATION_RIGHT}"); ')
        sql = sql.format(table=st.TABLE_EXECUTIVE_DASHBOARDS, col_ID=st.TB_EXECUTIVE_DASHBOARDS_COL_ID,
                         col_NAME=st.TB_EXECUTIVE_DASHBOARDS_COL_NAME,
                         col_DESCRIPTION=st.TB_EXECUTIVE_DASHBOARDS_COL_DESCRIPTION,
                         col_ACCESS_USER_LIST=st.TB_EXECUTIVE_DASHBOARDS_COL_ACCESS_USER_LIST,
                         col_ACCESS_BUSINESS_UNIT_LIST=st.TB_EXECUTIVE_DASHBOARDS_COL_ACCESS_BUSINESS_UNIT_LIST,
                         col_PLOTS=st.TB_EXECUTIVE_DASHBOARDS_COL_PLOTS,
                         col_DATASET_ID=st.TB_EXECUTIVE_DASHBOARDS_COL_DATASET_ID,
                         col_DATASET_LABEL=st.TB_EXECUTIVE_DASHBOARDS_COL_DATASET_LABEL,
                         col_DATASET_CHOICE_RULE=st.TB_EXECUTIVE_DASHBOARDS_COL_DATASET_CHOICE_RULE,
                         col_VISUALIZATION_RIGHT=st.TB_EXECUTIVE_DASHBOARDS_COL_VISUALIZATION_RIGHT,
                         EXECUTIVE_DASHBOARD_ID=executive_dashboard_id, NAME=executive_dashboard_name,
                         DESCRIPTION=executive_dashboard_description, ACCESS_USER_LIST=access_user_list,
                         ACCESS_BUSINESS_UNIT_LIST=access_business_unit_list,
                         EXECUTIVE_DASHBOARD_COMPONENTS=executive_dashboard_plots,
                         EXECUTIVE_DASHBOARD_DATASET_ID=dataset_id, EXECUTIVE_DASHBOARD_DATASET_LABEL=dataset_label,
                         EXECUTIVE_DASHBOARD_DATASET_CHOICE_RULE=dataset_choice_rule,
                         EXECUTIVE_DASHBOARD_VISUALIZATION_RIGHT=visualization_right)
        return sql

    # Returns SQL statement for inserting a executive_dashboard in executive_dashboard table
    def insert_plots_values(self, plot_id, formdata, grouped, visualization_type, visualization_right, component_name):
        sql = ('INSERT INTO {table} ({col_ID}, {COL_FORMDATA}, {COL_GROUPED}, {COL_VISUALIZATION_TYPE},'
               + '{COL_VISUALIZATION_RIGHT}, {COL_COMPONENT_NAME}) '
               + 'VALUES ("{PLOT_ID}",' + "'" + "{FORMDATA}" + "'" + ',"{GROUPED}","{VISUALIZATION_TYPE}","{VISUALIZATION_RIGHT}","{COMPONENT_NAME}");')
        sql = sql.format(table=st.TABLE_PLOTS, col_ID=st.TB_PLOTS_COL_ID,
                         COL_FORMDATA=st.TB_PLOTS_COL_FORMDATA,
                         COL_GROUPED=st.TB_PLOTS_COL_GROUPED,
                         COL_VISUALIZATION_TYPE=st.TB_PLOTS_COL_VISUALIZATION_TYPE,
                         COL_VISUALIZATION_RIGHT=st.TB_PLOTS_COL_VISUALIZATION_RIGHT,
                         COL_COMPONENT_NAME=st.TB_PLOTS_COL_COMPONENT_NAME,
                         PLOT_ID=plot_id, FORMDATA=formdata,
                         GROUPED=grouped, VISUALIZATION_TYPE=visualization_type,
                         VISUALIZATION_RIGHT=visualization_right, COMPONENT_NAME=component_name)
        return sql

    # Returns SQL statement for inserting a datasets in dataset table
    def insert_datasets_values(self, dataset_id, name, owner, hash_of_dataset, size,
                               cleaned, access_user_list, access_business_unit_list, description, storage_type, label,
                               archive=False, archive_uploads=False):
        if archive:
            table_name = st.TABLE_DATASET_ARCHIVE
            col_dataset_id = st.ARCHIVE_ID_PREFIX + st.TB_DATASET_COL_DATASET_ID
        elif archive_uploads:
            table_name = st.TABLE_DATASET_UPLOAD_ARCHIVE
            col_dataset_id = st.ARCHIVE_ID_PREFIX + st.TB_DATASET_COL_DATASET_ID
        else:
            table_name = st.TABLE_DATASET
            col_dataset_id = st.TB_DATASET_COL_DATASET_ID
        sql = ('INSERT INTO {table} ({col_DATASET_ID}, {col_NAME}, {col_OWNER}, {col_HASH_OF_DATASET}, {col_CLEANED},'
               + '{col_SIZE}, {col_ACCESS_USER_LIST}, {col_ACCESS_BUSINESS_UNIT_LIST}, {col_STORAGE_TYPE}, {col_DESCRIPTION}, {col_LABEL}) '
               + 'VALUES ("{DATASET_ID}", "{NAME}", "{OWNER}", "{HASH_OF_DATASET}", {CLEANED},'
               + '{SIZE}, "{ACCESS_USER_LIST}", "{ACCESS_BUSINESS_UNIT_LIST}", "{STORAGE_TYPE}", "{DESCRIPTION}", "{LABEL}");')
        sql = sql.format(table=table_name, col_DATASET_ID=col_dataset_id, col_NAME=st.TB_DATASET_COL_NAME,
                         col_OWNER=st.TB_DATASET_COL_OWNER, col_HASH_OF_DATASET=st.TB_DATASET_COL_HASH_OF_DATASET,
                         col_CLEANED=st.TB_DATASET_COL_CLEANED, col_SIZE=st.TB_DATASET_COL_SIZE,
                         col_ACCESS_USER_LIST=st.TB_DATASET_COL_ACCESS_USER_LIST, col_ACCESS_BUSINESS_UNIT_LIST=st.TB_DATASET_COL_ACCESS_BUSINESS_UNIT_LIST,
                         col_STORAGE_TYPE=st.TB_DATASET_COL_STORAGE_TYPE, col_DESCRIPTION=st.TB_DATASET_COL_DESCRIPTION, col_LABEL=st.TB_DATASET_COL_LABEL,
                         DATASET_ID=dataset_id, NAME=name, OWNER=owner, HASH_OF_DATASET=hash_of_dataset,
                         SIZE=size, ACCESS_USER_LIST=access_user_list,
                         ACCESS_BUSINESS_UNIT_LIST=access_business_unit_list, STORAGE_TYPE=storage_type,
                         CLEANED=cleaned, DESCRIPTION=description, LABEL=label)
        return sql

    # Returns SQL statement for inserting a user in users table
    def insert_user_values(self, userID, first_name, last_name, email,
                           password, business_unit, access_rights_pillars, admin,
                           role_manager, user_directory_path='C:\\USERS\\YOUR_USER'):
        sql = ('INSERT INTO {table} ({col_USER_ID}, {col_FIRST_NAME}, {col_LAST_NAME}, {col_EMAIL}, {col_PASSWORD},'
               + '{col_BUSINESS_UNIT}, {col_ACCESS_RIGHTS}, {col_ADMIN}, {col_ROLE_MANAGER}, {col_USER_DIRECTORY_PATH}) '
               + 'VALUES ("{USER_ID}", "{FIRST_NAME}", "{LAST_NAME}", "{EMAIL}", "{PASSWORD}",'
               + '"{BUSINESS_UNIT}", "{ACCESS_RIGHTS}", {ADMIN}, {ROLE_MANAGER}, "{USER_DIRECTORY_PATH}");')
        sql = sql.format(table=st.TABLE_USER, col_USER_ID=st.TB_USER_COL_USER_ID, col_FIRST_NAME=st.TB_USER_COL_FIRST_NAME,
                         col_LAST_NAME=st.TB_USER_COL_LAST_NAME, col_EMAIL=st.TB_USER_COL_EMAIL,
                         col_PASSWORD=st.TB_USER_COL_PASSWORD, col_BUSINESS_UNIT=st.TB_USER_COL_BUSINESS_UNIT,
                         col_ACCESS_RIGHTS=st.TB_USER_COL_ACCESS_RIGHTS, col_ADMIN=st.TB_USER_COL_ADMIN,
                         col_ROLE_MANAGER=st.TB_USER_COL_ROLE_MANAGER, col_USER_DIRECTORY_PATH=st.TB_USER_COL_USER_DIRECTORY_PATH,
                         USER_ID=userID, FIRST_NAME=first_name, LAST_NAME=last_name, EMAIL=email,
                         PASSWORD=password, BUSINESS_UNIT=business_unit,
                         ACCESS_RIGHTS=access_rights_pillars, ADMIN=admin,
                         ROLE_MANAGER=role_manager, USER_DIRECTORY_PATH=user_directory_path)
        return sql

    # Returns SQL statement for inserting a kpi in kpis table
    def insert_kpi_values(self, kpiID, name, description, high_level_kpi_component_weight,
                          kpi_aspects_weights, threshold, formula, dataset_id,
                          dataset_labels, kpi_family, color_coding):
        sql = ('INSERT INTO {table} ({col_KPI_ID}, {col_NAME}, {col_DESCRIPTION}, {col_HIGH_LEVEL_KPI_COMPONENT_KPI_WEIGHT}, {col_KPI_KPI_ASPECTS_WEIGHTS},'
               + '{col_THRESHOLD}, {col_FORMULA}, {col_DATASET_ID}, {col_DATASET_LABELS}, {col_KPI_FAMILY}, {col_COLOR_CODING}) '
               + 'VALUES ("{KPI_ID}", "{NAME}", "{DESCRIPION}", "{HIGH_LEVEL_KPI_COMPONENT_KPI_WEIGHT}", "{KPI_KPI_ASPECTS_WEIGHTS}",'
               + '"{THRESHOLD}", "{FORMULA}", "{DATASET_ID}", "{DATASET_LABELS}", "{KPI_FAMILY}", "{COLOR_CODING}");')
        sql = sql.format(table=st.TABLE_KPI, col_KPI_ID=st.TB_KPI_COL_KPI_ID, col_NAME=st.TB_KPI_COL_NAME,
                         col_DESCRIPTION=st.TB_KPI_COL_DESCRIPTION, col_HIGH_LEVEL_KPI_COMPONENT_KPI_WEIGHT=st.TB_KPI_COL_HIGH_LEVEL_KPI_COMPONENT_KPI_WEIGHT,
                         col_KPI_KPI_ASPECTS_WEIGHTS=st.TB_KPI_COL_KPI_ASPECTS_WEIGHTS, col_THRESHOLD=st.TB_KPI_COL_THRESHOLD,
                         col_FORMULA=st.TB_KPI_COL_FORMULA, col_DATASET_ID=st.TB_KPI_COL_DATASET_ID,
                         col_DATASET_LABELS=st.TB_KPI_COL_DATASET_LABELS, col_KPI_FAMILY=st.TB_KPI_COL_KPI_FAMILY, col_COLOR_CODING=st.TB_KPI_COL_COLOR_CODING,
                         KPI_ID=kpiID, NAME=name, DESCRIPION=description, HIGH_LEVEL_KPI_COMPONENT_KPI_WEIGHT=high_level_kpi_component_weight,
                         KPI_KPI_ASPECTS_WEIGHTS=kpi_aspects_weights, THRESHOLD=threshold,
                         FORMULA=formula, DATASET_ID=dataset_id, DATASET_LABELS=dataset_labels,
                         KPI_FAMILY=kpi_family, COLOR_CODING=color_coding)
        return sql

    def insert_aspect_values(self, aspect_id, name, description, raw_components_from_dataset, skala_size,
                             weight, threshold, operation_type, formula, dataset_id, dataset_labels, kpi_family):
        print(raw_components_from_dataset)
        sql = ('INSERT INTO {table} ({col_ASPECT_ID}, {col_NAME}, {col_DESCRIPTION}, {col_RAW_COMPONENTS_FROM_DATASET}, {col_SKALA_SIZE},'
               + '{col_WEIGHT}, {col_THRESHOLD}, {col_OPERATION_TYPE}, {col_FORMULA}, {col_DATASET_ID}, {col_DATASET_LABELS}, {col_KPI_FAMILY}) '
               + 'VALUES ("{ASPECT_ID}", "{NAME}", "{DESCRIPION}", "{RAW_COMPONENTS_FROM_DATASET}", "{SKALA_SIZE}",'
               + '"{WEIGHT}", "{THRESHOLD}", "{OPERATION_TYPE}" ,"{FORMULA}", "{DATASET_ID}", "{DATASET_LABELS}", "{KPI_FAMILY}");')
        sql = sql.format(table=st.TABLE_ASPECT, col_ASPECT_ID=st.TB_ASPECT_COL_ID, col_NAME=st.TB_ASPECT_COL_NAME,
                         col_DESCRIPTION=st.TB_ASPECT_COL_DESCRIPTION, col_RAW_COMPONENTS_FROM_DATASET=st.TB_ASPECT_COL_RAW_COMPONENTS_FROM_DATASET,
                         col_SKALA_SIZE=st.TB_ASPECT_COL_SKALA_SIZE, col_WEIGHT=st.TB_ASPECT_COL_WEIGHT, col_THRESHOLD=st.TB_ASPECT_COL_THRESHOLD,
                         col_OPERATION_TYPE=st.TB_ASPECT_COL_OPERATION_TYPE, col_FORMULA=st.TB_ASPECT_COL_FORMULA, col_DATASET_ID=st.TB_ASPECT_COL_DATASET_ID,
                         col_DATASET_LABELS=st.TB_ASPECT_COL_DATASET_LABELS, col_KPI_FAMILY=st.TB_ASPECT_COL_KPI_FAMILY,
                         ASPECT_ID=aspect_id, NAME=name, DESCRIPION=description, RAW_COMPONENTS_FROM_DATASET=raw_components_from_dataset,
                         SKALA_SIZE=skala_size, WEIGHT=weight, THRESHOLD=threshold,
                         OPERATION_TYPE=operation_type, FORMULA=formula, DATASET_ID=dataset_id,
                         DATASET_LABELS=dataset_labels, KPI_FAMILY=kpi_family)
        return sql

    def insert_formula_values(self, formulaID, name, description, operation, purpose, kpi_families):
        sql = ('INSERT INTO {table} ({col_FORMULA_ID}, {col_NAME}, {col_DESCRIPTION}, {col_OPERATION},{col_PURPOSE}, {col_KPI_FAMILIES}) '
               + 'VALUES ("{FORMULA_ID}", "{NAME}", "{DESCRIPION}", "{OPERATION}", "{PURPOSE}", "{KPI_FAMILIES}");')
        sql = sql.format(table=st.TABLE_FORMULA, col_FORMULA_ID=st.TB_FORMULA_COL_FORMULA_ID, col_NAME=st.TB_FORMULA_COL_NAME,
                         col_DESCRIPTION=st.TB_FORMULA_COL_DESCRIPTION, col_OPERATION=st.TB_FORMULA_COL_OPERATION,
                         col_PURPOSE=st.TB_FORMULA_COL_PURPOSE, col_KPI_FAMILIES=st.TB_FORMULA_COL_KPI_FAMILIES,
                         FORMULA_ID=formulaID, NAME=name, DESCRIPION=description, OPERATION=operation,
                         PURPOSE=purpose, KPI_FAMILIES=kpi_families)
        return sql

    def insert_kpi_category_type_values(self, kpi_category_type_id, name):
        sql = ('INSERT INTO {table} ({col_KPI_CATEGORY_TYPE_ID}, {col_NAME}) '
               + 'VALUES ("{KPI_CATEGORY_TYPE_ID}", "{NAME}");')
        sql = sql.format(table=st.TABLE_KPI_CATEGORY_TYPE, col_KPI_CATEGORY_TYPE_ID=st.TB_KPI_CATEGORY_TYPE_COL_ID,
                         col_NAME=st.TB_KPI_CATEGORY_TYPE_COL_NAME,
                         KPI_CATEGORY_TYPE_ID=kpi_category_type_id, NAME=name)
        return sql

    def insert_dataset_choice_rules_values(self, dataset_choice_rule_id, name, description=""):
        sql = ('INSERT INTO {table} ({col_DATASET_CHOICE_RULE_ID}, {col_NAME}, {col_DESCRIPTION}) '
               + 'VALUES ("{DATASET_CHOICE_RULE_ID}", "{NAME}", "{DESCRIPTION}");')
        sql = sql.format(table=st.TABLE_DATASET_CHOICE_RULE, col_DATASET_CHOICE_RULE_ID=st.TB_DATASET_CHOICE_RULE_COL_ID,
                         col_NAME=st.TB_DATASET_CHOICE_RULE_COL_NAME, col_DESCRIPTION=st.TB_DATASET_CHOICE_RULE_COL_DESCRIPTION,
                         DATASET_CHOICE_RULE_ID=dataset_choice_rule_id, NAME=name, DESCRIPTION=description)
        return sql

    def insert_visualization_right_values(self, visualization_right_id, name, description=""):
        sql = ('INSERT INTO {table} ({col_VISUALIZATION_RIGHT_ID}, {col_NAME}, {col_DESCRIPTION}) '
               + 'VALUES ("{VISUALIZATION_RIGHT_ID}", "{NAME}", "{DESCRIPTION}");')
        sql = sql.format(table=st.TABLE_VISUALIZATION_RIGHT, col_VISUALIZATION_RIGHT_ID=st.TB_VISUALIZATION_RIGHT_COL_ID,
                         col_NAME=st.TB_VISUALIZATION_RIGHT_COL_NAME, col_DESCRIPTION=st.TB_VISUALIZATION_RIGHT_COL_DESCRIPTION,
                         VISUALIZATION_RIGHT_ID=visualization_right_id, NAME=name, DESCRIPTION=description)
        return sql

    def insert_result_values(self, result_id, result, table_name):
        sql = ('INSERT INTO {table} ({col_RESULT_ID},{col_RESULT}) '
               + 'VALUES ("{RESULT_ID}","{RESULT}");')
        sql = sql.format(table=table_name, col_RESULT_ID=st.TB_RESULT_ID, col_RESULT=st.TB_RESULT_RESULT,
                         RESULT_ID=result_id, RESULT=result)
        return sql

    # Returns SQL statement for inserting a department in department table
    def insert_department_values(self, departmentID, department_name):
        sql = ('INSERT INTO {table} ({col_DEPARTMENT_ID}, {col_NAME}) '
               + 'VALUES ("{DEPARTMENT_ID}", "{NAME}");')
        sql = sql.format(table=st.TABLE_DEPARTMENTS, col_DEPARTMENT_ID=st.TB_DEPARTMENTS_COL_DEPARTMENT_ID, col_NAME=st.TB_DEPARTMENTS_COL_NAME,
                         DEPARTMENT_ID=departmentID, NAME=department_name)
        return sql

    def insert_label_values(self, label_id, label_name, dataset_header_list, operations_cleanser):
        sql = ('INSERT INTO {table} ({col_LABEL_ID}, {col_NAME}, {col_HEADER_LIST}, {col_OPERATIONS_LIST}) '
               + 'VALUES ("{LABEL_ID}", "{NAME}", "{HEADER_LIST}", "{OPERATION_LIST}");')
        sql = sql.format(table=st.TABLE_LABEL, col_LABEL_ID=st.TB_LABEL_COL_ID, col_NAME=st.TB_LABEL_COL_NAME,
                         col_HEADER_LIST=st.TB_LABEL_COL_HEADER, col_OPERATIONS_LIST=st.TB_LABEL_COL_OPERATIONS_CLEANSER,
                         LABEL_ID=label_id, NAME=label_name, HEADER_LIST=dataset_header_list, OPERATION_LIST=operations_cleanser)
        return sql

    # Returns SQL statement for inserting a cleanser in cleansers table
    def insert_cleanser_values(self, cleanserID, name, description, header_list, datasets, cleanser_operation_types):
        sql = ('INSERT INTO {table} ({col_CLEANSER_ID}, {col_NAME}, {col_DESCRIPTION}, {col_HEADER_LIST}, {col_DATASETS}, {col_CLEANSER_OPERATION_TYPES}) '
               + 'VALUES ("{CLEANSER_ID}", "{NAME}", "{DESCRIPTION}", "{HEADER_LIST}", "{DATASETS}", "{CLEANSER_OPERATION_TYPES}");')
        sql = sql.format(table=st.TABLE_CLEANSER, col_CLEANSER_ID=st.TB_CLEANSER_COL_CLEANSER_ID, col_NAME=st.TB_CLEANSER_COL_NAME,
                         col_DESCRIPTION=st.TB_CLEANSER_COL_DESCRIPTION, col_HEADER_LIST=st.TB_CLEANSER_COL_HEADER_LIST,
                         col_DATASETS=st.TB_CLEANSER_COL_DATASETIDS, col_CLEANSER_OPERATION_TYPES=st.TB_CLEANSER_OPERATION_TYPES,
                         CLEANSER_ID=cleanserID, NAME=name, DESCRIPTION=description, HEADER_LIST=header_list, DATASETS=datasets,
                         CLEANSER_OPERATION_TYPES=cleanser_operation_types)
        return sql

    # Returns SQL statement for returning all datasets
    def select_all_from_table_by_access_rights(self, from_table, join_table, join_col_from_table,
                                               join_col_join_table, condition_table, condition,
                                               condition_value, condition_operator='='):
        if isinstance(condition_value, str):
            condition_value = '"{}"'.format(condition_value)
        sql = ('SELECT * '
               + 'FROM {from_table} '
               + 'LEFT JOIN {join_table} ON {from_table}.{join_col_from_table} = {join_table}.{join_col_join_table} '
               + 'WHERE {condition_table}.{condition} {condition_operator} {condition_value}')
        sql = sql.format(from_table=from_table, join_table=join_table,
                         join_col_from_table=join_col_from_table, join_col_join_table=join_col_join_table,
                         condition_table=condition_table, condition=condition, condition_operator=condition_operator,
                         condition_value=condition_value)
        return sql

    # Returns SQL statement for returning an object like dataset, user etc. based on condition like an id.
    # condition represents the column and condition value the specific value like the actual id of an object
    def select_object_by_condition(self, table, condition, condition_value, condition_operator='='):
        if isinstance(condition_value, str):
            condition_value = '"{}"'.format(condition_value)
        sql = ('SELECT * '
               + 'FROM {table} '
               + 'WHERE {column} {condition_operator} {condition_value}')
        sql = sql.format(table=table,
                         column=condition,
                         condition_operator=condition_operator,
                         condition_value=condition_value)
        return sql

    # Returns SQL statement for returning all data contained in a table
    def select_all_data_from_table(self, table):
        sql = ('SELECT * '
               + 'FROM {table}')
        sql = sql.format(table=table)
        return sql

    # Returns SQL statement for returning all entries of column matching the given condition
    def select_all_from_column(self, table, condition, condition_value, condition_operator="="):
        if isinstance(condition_value, str):
            condition_value = '"{}"'.format(condition_value)
        sql = ('SELECT * '
               + 'FROM {table} '
               + 'WHERE {condition} {condition_operator} {condition_value}')
        sql = sql.format(table=table,
                         condition=condition,
                         condition_operator=condition_operator,
                         condition_value=condition_value)
        return sql

    # Returns SQL statement for updating a column value in a table. Table, column and the value must be submitted.
    # Additionally a condition can be defined.
    def update_value(self, table, column, value, condition=None, condition_operator='=', condition_value=None):
        if isinstance(value, str):
            value = '"{}"'.format(value)
        elif isinstance(value, list):
            value_as_string = ''
            for val in value:
                isString = isinstance(val, str)
                if isString:
                    value_as_string += val + ','
                else:
                    break
            if isString:
                value = '"{}"'.format(value_as_string[:-1])
            else:
                value = '"{}"'.format(value)
        if isinstance(condition_value, str):
            condition_value = '"{}"'.format(condition_value)
        if condition:
            sql = ('UPDATE {table} '
                   + 'SET {column} = {value} '
                   + 'WHERE {condition} {condition_operator} {condition_value}')
            sql = sql.format(table=table, column=column, value=value, condition=condition,
                             condition_operator=condition_operator, condition_value=condition_value)
        else:
            sql = ('UPDATE {table} '
                   + 'SET {column} = {value} ')
            sql = sql.format(table=table, column=column, value=value)
        return sql

    # Returns SQL statement for deleting a rntry from an arbitrary table
    def delete_row_from_table(self, table, condition, condition_value, condition_operator='='):
        if isinstance(condition_value, str):
            condition_value = '"{}"'.format(condition_value)
        sql = ('DELETE FROM {table} '
               + 'WHERE {condition} {condition_operator} {condition_value}')
        sql = sql.format(table=table, condition=condition,
                         condition_operator=condition_operator, condition_value=condition_value)
        return sql

    # Returns SQL statement for deleting a rntry from an arbitrary table
    def drop_table(self, table):
        sql = ('DROP TABLE {table}')
        sql = sql.format(table=table)
        return sql

    # Returns sql with only the headers of a specified table
    def get_column_names_from_table(self, table):
        sql = ('SELECT COLUMN_NAME '
               + 'FROM INFORMATION_SCHEMA.COLUMNS '
               + 'WHERE TABLE_NAME = "{table}"')
        sql = sql.format(table=table)
        return sql
