# Project Athena
'''
Owner: Efstratios Pahis
Contributors:
Description: Defines a Formula object
'''


class Formula:

    def __init__(self, formulaID, name, description, operation, purpose, kpi_families):
        self.__formulaID = formulaID
        self.__name = name
        self.__description = description
        self.__operation = operation
        self.__purpose = purpose
        self.__kpi_families = kpi_families

    # Definition of get Methods for KPI Objects

    def get_formulaID(self):
        return self.__formulaID

    def get_formula_name(self):
        return self.__name

    def get_description(self):
        return self.__description

    def get_operation(self):
        return self.__operation

    def get_purpose(self):
        return self.__purpose

    def get_kpi_families(self):
        return self.__kpi_families

    # Setter Methods for certain Attributes of User Objects
    def set_name(self, name):
        self.__name = name

    def set_description(self, description):
        self.__description = description

    def set_operation(self, operation):
        self.__operation = operation

    def set_kpi_families(self, kpi_families):
        self.__kpi_families = kpi_families
