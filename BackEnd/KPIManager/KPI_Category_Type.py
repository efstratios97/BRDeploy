# Project Athena
'''
Owner: Efstratios Pahis
Contributors:
Description: Defines a KPI_CATEGORY_TYPE object
'''


class KPI_CATEGORY_TYPE:

    def __init__(self, kpi_category_type_id, name):
        self.__kpi_category_type_id = kpi_category_type_id
        self.__name = name

    def get_kpi_category_type_id(self):
        return self.__kpi_category_type_id

    def get_name(self):
        return self.__name
