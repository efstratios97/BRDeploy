# Project Athena
'''
Owner: Efstratios Pahis
Contributors:
Description: Various Helpermethods and Attributes for re-use
'''

from inspect import currentframe, getframeinfo
from typing import Pattern
import uuid
import hashlib
import pandas as pd
import functools
import ast
import re
import datetime

ATHENA_CLOUD_DB_HOST = 'localhost'
ATHENA_CLOUD_DB_USER = 'br'
ATHENA_CLOUD_DB_PW = 'BRApp12345!'
ATHENA_CLOUD_DB_DBNAME = 'BRArchitectureManager'
# ATHENA_CLOUD_DB_HOST = 'mysql.efspah.dreamhosters.com'
# ATHENA_CLOUD_DB_USER = 'efspahdreamhoste'
# ATHENA_CLOUD_DB_PW = 'hiathena'
# ATHENA_CLOUD_DB_DBNAME = 'projectathena'
# ATHENA_CLOUD_DB_HOST = 'localhost'
# ATHENA_CLOUD_DB_USER = 'root'
# ATHENA_CLOUD_DB_PW = '12345'
# ATHENA_CLOUD_DB_DBNAME = 'BRArchitectureManager'

# Table names
TABLE_DATASET = 'datasets'
TABLE_USER = 'users'
TABLE_USER_DATASET_ACCESS_RELATION = "user_dataset_access_relation"
TABLE_DEPARTMENT_DATASET_ACCESS_RELATION = "department_dataset_access_relation"
TABLE_CLEANSER_DATASET_COMPATIBILITY = "cleanser_dataset_compatibility"
TABLE_CLEANSER = 'cleansers'
TABLE_DEPARTMENTS = "departments"
TABLE_ARCHITECTURE_VIEWS = "architecture_views"
TABLE_EXECUTIVE_DASHBOARDS = "executive_dashboards"
TABLE_PLOTS = "executive_dashboards_plots"
TABLE_EXECUTIVE_DASHBOARDS_PLOTS_RELATION = "executive_dashboard_plot_relation"
TABLE_LABEL = "labels"
TABLE_DATASET_ARCHIVE = "dataset_archive"
TABLE_KPI = "kpis"
TABLE_ASPECT = "aspects"
TABLE_FORMULA = "formulas"
TABLE_KPI_FORMULA_RELATION = "kpi_formula_relation"
TABLE_ASPECT_FORMULA_RELATION = "aspect_formula_relation"
TABLE_KPI_ASPECT_RELATION = "kpi_aspect_relation"
TABLE_KPI_CATEGORY_TYPE = "kpi_category_types"
TABLE_RESULT = "result"


# Dataset Table columns
TB_DATASET_COL_CLEANED = 'CLEANED'
TB_DATASET_COL_DATASET_ID = 'DATASET_ID'
TB_DATASET_COL_NAME = 'NAME'
TB_DATASET_COL_ACCESS_USER_LIST = 'ACCESS_USER_LIST'
TB_DATASET_COL_ACCESS_BUSINESS_UNIT_LIST = 'ACCESS_BUSINESS_UNIT_LIST'
TB_DATASET_COL_DESCRIPTION = 'DESCRIPTION'
TB_DATASET_COL_OWNER = 'OWNER'
TB_DATASET_COL_HASH_OF_DATASET = 'HASH_OF_DATASET'
TB_DATASET_COL_SIZE = 'SIZE'
TB_DATASET_COL_STORAGE_TYPE = 'STORAGE_TYPE'
TB_DATASET_COL_LABEL = 'LABEL'
TB_DATASET_COL_CREATED_AT = 'CREATED_AT'

# User Table Columns
TB_USER_COL_USER_ID = 'USER_ID'
TB_USER_COL_FIRST_NAME = 'FIRST_NAME'
TB_USER_COL_LAST_NAME = 'LAST_NAME'
TB_USER_COL_EMAIL = 'EMAIL'
TB_USER_COL_PASSWORD = 'PASSWORD'
TB_USER_COL_BUSINESS_UNIT = 'BUSINESS_UNIT'
TB_USER_COL_ACCESS_RIGHTS = 'ACCESS_RIGHTS'
TB_USER_COL_ADMIN = 'ADMIN'
TB_USER_COL_ROLE_MANAGER = 'ROLE_MANAGER'
TB_USER_COL_USER_DIRECTORY_PATH = 'USER_DIRECTORY_PATH'
TB_USER_COL_CREATED_AT = 'CREATED_AT'

# Cleanser Table Columns
TB_CLEANSER_COL_CLEANSER_ID = 'CLEANSER_ID'
TB_CLEANSER_COL_NAME = 'NAME'
TB_CLEANSER_COL_DESCRIPTION = 'DESCRIPTION'
TB_CLEANSER_COL_HEADER_LIST = 'HEADER_LIST'
TB_CLEANSER_COL_DATASETIDS = 'DATASETS'
TB_CLEANSER_OPERATION_TYPES = 'CLEANSER_OPERATION_TYPES'
TB_CLEANSER_COL_CREATED_AT = 'CREATED_AT'

# Departments Table Columns
TB_DEPARTMENTS_COL_DEPARTMENT_ID = "DEPARTMENT_ID"
TB_DEPARTMENTS_COL_NAME = "NAME"
TB_DEPARTMENTS_COL_CREATED_AT = "CREATED_AT"

# Architecture Views Table Columns
TB_ARCHITECTURE_VIEWS_COL_ARCHITECTURE_VIEW_ID = "ARCHITECTURE_VIEW_ID"
TB_ARCHITECTURE_VIEWS_COL_ARCHITECTURE_VIEW_NAME = "ARCHITECTURE_VIEW_NAME"
TB_ARCHITECTURE_VIEWS_COL_ARCHITECTURE_VIEW_DESCRIPTION = "ARCHITECTURE_VIEW_DESCRIPTION"
TB_ARCHITECTURE_VIEWS_COL_ARCHITECTURE_VIEW_COMPONENTS = "ARCHITECTURE_VIEW_ID_COMPONENTS"
TB_ARCHITECTURE_VIEWS_COL_CREATED_AT = "CREATED_AT"

# Executive Dashboards Table Columns
TB_EXECUTIVE_DASHBOARDS_COL_ID = "EXECUTIVE_DASHBOARD_ID"
TB_EXECUTIVE_DASHBOARDS_COL_NAME = "EXECUTIVE_DASHBOARD_NAME"
TB_EXECUTIVE_DASHBOARDS_COL_DESCRIPTION = "EXECUTIVE_DASHBOARD_DESCRIPTION"
TB_EXECUTIVE_DASHBOARDS_COL_ACCESS_USER_LIST = 'ACCESS_USER_LIST'
TB_EXECUTIVE_DASHBOARDS_COL_ACCESS_BUSINESS_UNIT_LIST = 'ACCESS_BUSINESS_UNIT_LIST'
TB_EXECUTIVE_DASHBOARDS_COL_PLOTS = "EXECUTIVE_DASHBOARD_PLOTS"
TB_EXECUTIVE_DASHBOARDS_COL_DATASET = "EXECUTIVE_DASHBOARD_DATASET"
TB_EXECUTIVE_DASHBOARDS_COL_CREATED_AT = "CREATED_AT"

# Plots Table Columns
TB_PLOTS_COL_ID = "PLOT_ID"
TB_PLOTS_COL_TITLE = "PLOT_TITLE"
TB_PLOTS_COL_SUBTITLE = "PLOT_SUBTITLE"
TB_PLOTS_COL_LEGEND_SHOW = "PLOT_LEGEND_SHOW"  # BOOL
TB_PLOTS_COL_DATASET_ID_FOR_CHART = "PLOT_DATASET_ID_FOR_CHART"
TB_PLOTS_COL_DATASET_LABEL = "PLOT_DATASET_LABEL"
TB_PLOTS_COL_CHART_TYPE = "PLOT_CHART_TYPE"
TB_PLOTS_COL_CHART_WIDTH = "PLOT_DATASET_CHART_WIDTH"
TB_PLOTS_COL_CHART_HEIGHT = "PLOT_DATASET_CHART_HEIGHT"
TB_PLOTS_COL_XAXIS_CATEGORIES = "PLOT_XAXIS_CATEGORIES"
TB_PLOTS_COL_INPUT_FIELDS = "PLOT_INPUT_FIELDS"  # BOOL
TB_PLOTS_COL_INPUT_FIELDS_ID = "PLOT_INPUT_FIELDS_ID"
TB_PLOTS_COL_EMPTY_FIELD = "PLOT_EMPTY_FIELD"
TB_PLOTS_COL_EMPTY_FIELD_2 = "PLOT_EMPTY_FIELD_2"
TB_PLOTS_COL_CREATED_AT = "CREATED_AT"

# LABEL Table
TB_LABEL_COL_ID = "LABEL_ID"
TB_LABEL_COL_NAME = "LABEL_NAME"
TB_LABEL_COL_HEADER = "LABEL_HEADER_DATASET"
TB_LABEL_COL_OPERATIONS_CLEANSER = "LABEL_OPERATIONS_CLEANSER"
TB_LABEL_COL_CREATED_AT = "CREATED_AT"

# KPI Table
TB_KPI_COL_KPI_ID = 'KPI_ID'
TB_KPI_COL_NAME = 'NAME'
TB_KPI_COL_DESCRIPTION = 'DESCRIPTION'
TB_KPI_COL_HIGH_LEVEL_KPI_COMPONENT_KPI_WEIGHT = 'HIGH_LEVEL_KPI_COMPONENT_KPI_WEIGHT'
TB_KPI_COL_KPI_ASPECTS_WEIGHTS = 'KPI_ASPECTS_WEIGHTS'
TB_KPI_COL_THRESHOLD = 'THRESHOLD'
TB_KPI_COL_FORMULA = 'FORMULA'
TB_KPI_COL_DATASET_ID = 'DATASET_ID'
TB_KPI_COL_DATASET_LABELS = 'DATASET_LABELS'
TB_KPI_COL_KPI_FAMILY = 'KPI_FAMILY'
TB_KPI_COL_COLOR_CODING = 'COLOR_CODING'
TB_KPI_COL_CREATED_AT = 'CREATED_AT'

# Aspect Table
TB_ASPECT_COL_ID = 'ASPECT_ID'
TB_ASPECT_COL_NAME = 'NAME'
TB_ASPECT_COL_DESCRIPTION = 'DESCRIPTION'
TB_ASPECT_COL_RAW_COMPONENTS_FROM_DATASET = 'RAW_COMPONENTS_FROM_DATASET'
TB_ASPECT_COL_SKALA_SIZE = 'SKALA_SIZE'
TB_ASPECT_COL_WEIGHT = 'WEIGHT'
TB_ASPECT_COL_THRESHOLD = 'THRESHOLD'
TB_ASPECT_COL_OPERATION_TYPE = 'OPERATION_TYPE'
TB_ASPECT_COL_FORMULA = 'FORMULA'
TB_ASPECT_COL_DATASET_ID = 'DATASET_ID'
TB_ASPECT_COL_DATASET_LABELS = 'DATASET_LABELS'
TB_ASPECT_COL_KPI_FAMILY = 'KPI_FAMILY'
TB_ASPECT_COL_CREATED_AT = 'CREATED_AT'

# Formula Table
TB_FORMULA_COL_FORMULA_ID = 'FORMULA_ID'
TB_FORMULA_COL_NAME = 'NAME'
TB_FORMULA_COL_DESCRIPTION = 'DESCRIPTION'
TB_FORMULA_COL_OPERATION = 'OPERATION'
TB_FORMULA_COL_PURPOSE = 'PURPOSE'
TB_FORMULA_COL_KPI_FAMILIES = 'KPI_FAMILY'
TB_FORMULA_COL_CREATED_AT = 'CREATED_AT'

# KPI Category Type Table
TB_KPI_CATEGORY_TYPE_COL_ID = 'KPI_CATEGORY_TYPE_ID'
TB_KPI_CATEGORY_TYPE_COL_NAME = 'NAME'
TB_KPI_CATEGORY_TYPE_COL_CREATED_AT = 'CREATED_AT'

# TABLE Result
TB_RESULT_ID = 'RESULT_ID'
TB_RESULT_RESULT = 'RESULT'
TB_RESULT_CREATED_AT = 'CREATED_AT'

# Other Global variables
DEPARTMENT_GENESIS = "None Department Assigned"
NO_LABEL = "NO_LABEL_6aba48df0cb55992803d864977c3aa204520d659"
ARCHIVE_ID_PREFIX = "archive_"
TB_ARCHIVE_DATASET_COL_DATASET_ID = ARCHIVE_ID_PREFIX + TB_DATASET_COL_DATASET_ID
# Names after APEX Graphs Package
STANDARD_VIEW_TYPES = ["bar", "treemap", "pie"]
FORMULA_PURPOSE_ASPECT = "aspect"
FORMULA_PURPOSE_KPI = "kpi"
ASPECT_OPERATION_TYPE_COUNT = "Count #"
ASPECT_OPERATION_TYPE_CATEGORICAL_3_SCALE = "Categorical with 3 Options (Niedrig; Mittel; Hoch)"
ASPECT_OPERATION_TYPE_CATEGORICAL_5_SCALE = "Categorical with 5 Options (Sehr Niedrig; Niedrig; Mittel; Hoch; Sehr Hoch)"
ASPECT_OPERATION_TYPE_CATEGORICAL_LIFE_CYCLE_END = "Application Lifecycle End (<2 years imminent action required; >2 & <5 years planning action required; >5 years no action required)"
ALL_VALUES_INPUT_FIELD = "All"
NO_ENTRY_INPUT_FIELD = "Undefined"


def get_filename_of_occured_error():
    cf = currentframe()
    filename = getframeinfo(cf).filename
    return filename


def get_linenumber_of_occured_error():
    cf = currentframe()
    return cf.f_back.f_lineno

# Creates a unique and privacy safe id


def create_id():
    u_id = uuid.uuid4()
    return u_id.hex

# Create a hash out of DataFrame


def hash_data(data: pd.DataFrame):
    hash_of_dataset = hashlib.sha256(
        pd.util.hash_pandas_object(data).values).hexdigest()
    return hash_of_dataset

# Create Password with sha512 encoding


def create_hash_password_sha512(password, complementary_input):
    hash_pw = hashlib.sha512(
        str(password+complementary_input).encode('utf-8')).hexdigest()
    return hash_pw


def check_list_identical(list_1, list_2):
    list_1.sort()
    list_2.sort()
    if list_1 == list_2:
        return True
    else:
        return False


def check_list_1_subset_list_2(list_1, list_2):
    return set(list_1).issubset(set(list_2))


def make_list_to_str(list_1):
    list_str = ''
    for el in list_1:
        list_str += el + ','
    list_1 = list_str[:-1]
    return list_1


def make_str_to_list(string_1, based_character=","):
    return string_1.split(based_character)


def make_dataset_id_to_archive_id(dataset_id):
    return ARCHIVE_ID_PREFIX + dataset_id


def enum_storage_type(storage_type):
    enum_storage_type = {
        'local': 'local',
        'cloud': 'cloud',
        True: 'local',
        False: 'cloud',
        'true': 'local',
        'false': 'cloud',
        'lokal': 'local',
        str(1): 'local',
        str(0): 'cloud',
        1: 'local',
        0: 'cloud'
    }
    try:
        if isinstance(storage_type, str):
            res = enum_storage_type[storage_type.lower()]
        else:
            res = enum_storage_type[storage_type]
    except:
        res = 0
        print('Not Able to identify storage_type of DataSet\n' +
              'Line: ' + str(get_linenumber_of_occured_error())
              + 'File: ' + str(get_filename_of_occured_error()))
    return res


def enum_storage_type_bool(storage_type):
    enum_storage_type = {
        'local': True,
        'cloud': False,
        'True': True,
        'False': False,
        'true': True,
        'false': False,
        'lokal': True,
        str(1): True,
        str(0): False,
        1: True,
        0: False
    }
    try:
        if isinstance(storage_type, str):
            res = enum_storage_type[storage_type.lower()]
        else:
            res = enum_storage_type[storage_type]
    except:
        res = 0
        print('Not Able to identify storage_type of DataSet\n' +
              'Line: ' + str(get_linenumber_of_occured_error())
              + 'File: ' + str(get_filename_of_occured_error()))
    return res


def string_list_with_string_dict_into_list_dict(representation: str):
    list_new = []
    representation = representation.replace(
        "},", "}§").replace(",", "$%$").replace("}§", "},")
    if "[(" or ")]" in representation:
        list_with_string_dict = representation.strip(')][(').split(', ')
    else:
        list_with_string_dict = representation.strip('][').split(', ')
    for string_dict in list_with_string_dict:
        string_dict = string_dict.replace("$%$", ",")
        list_new.append(ast.literal_eval(string_dict))
    return list_new


def string_list_with_nested_string_dict_into_list_dict(representation: str):
    try:
        list_new = []
        if "[(" or ")]" in representation:
            tuple_with_dict = ast.literal_eval(
                representation.strip(')][(').split('}}, ')[0])
        else:
            tuple_with_dict = ast.literal_eval(
                representation.strip('][').split('}}, ')[0])
        if len(tuple_with_dict) == 1:
            list_new.append(tuple_with_dict)
        else:
            for dict in tuple_with_dict:
                list_new.append(dict)
        return list_new
    except:
        return representation


def string_dict_to_dict(string_dict: str):
    representation = string_dict.replace("),", ")$$").replace("\n", "$Spacer$")
    dict = ast.literal_eval(representation)

    dict = {key: value.replace(")$$", "),").replace(
        "$Spacer$", "\n") if isinstance(value, str) else value for (key, value) in dict.items()}
    return dict


def string_list_to_list(representation: str):
    list_new = []
    list_with_string = representation.strip('][').split(',')
    for string in list_with_string:
        list_new.append(string.replace('"', ""))
    return list_new


def prepend_elem_to_list(list: list, elem):
    list.insert(0, elem)
    return list


def get_all_values_from_nested_dict(dict: dict):
    list_tmp = list(__get_all_values_from_nested_dict_helper(dict_=dict))
    return [item for sublist in list_tmp for item in sublist]


def __get_all_values_from_nested_dict_helper(dict_):
    for val in dict_.values():
        if isinstance(val, dict):
            yield from __get_all_values_from_nested_dict_helper(val)
        else:
            yield val


def get_keys_by_value(dict: dict, valueToFind):
    listOfKeys = list()
    for item in dict.items():
        if item[1] == valueToFind:
            listOfKeys.append(item[0])
    return listOfKeys
