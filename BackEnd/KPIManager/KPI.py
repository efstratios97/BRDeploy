# Project Athena
'''
Owner: Efstratios Pahis
Contributors:
Description: Defines a KPI object
'''

import Utils.Settings as st


class KPI:

    def __init__(self, kpiID, name, description, high_level_kpi_component_kpi_weight, kpi_aspects_weights,
                 threshold, formula, dataset_id, dataset_labels, kpi_family, color_coding):
        self.__kpiID = kpiID
        self.__name = name
        self.__description = description
        self.__high_level_kpi_component_kpi_weight = high_level_kpi_component_kpi_weight
        self.__kpi_aspects_weights = kpi_aspects_weights
        self.__threshold = threshold
        self.__formula = formula
        self.__dataset_id = dataset_id
        self.__dataset_labels = dataset_labels
        self.__kpi_family = kpi_family
        self.__color_coding = color_coding

    # Definition of get Methods for KPI Objects
    def get_KPIID(self):
        return self.__kpiID

    def get_KPI_name(self):
        return self.__name

    def get_description(self):
        return self.__description

    def get_kpi_aspects_weights(self):
        if isinstance(self.__kpi_aspects_weights, str):
            res = st.string_list_with_string_dict_into_list_dict(
                self.__kpi_aspects_weights)
            return res
        else:
            return self.__kpi_aspects_weights

    def get_threshold(self):
        return self.__threshold

    def get_formula(self):
        return self.__formula

    def get_dataset_id(self):
        return self.__dataset_id

    def get_dataset_labels(self):
        return self.__dataset_labels

    def get_high_level_kpi_component_kpi_weight(self):
        return self.__high_level_kpi_component_kpi_weight

    def get_kpi_family(self):
        return self.__kpi_family

    def get_color_coding(self):
        return self.__color_coding

    # Setter Methods for certain Attributes of KPI Objects
    def set_name(self, name):
        self.__name = name

    def set_description(self, description):
        self.__description = description

    def set_high_level_kpi_component_kpi_weight(self, high_level_kpi_component_kpi_weight):
        self.__high_level_kpi_component_kpi_weight = high_level_kpi_component_kpi_weight

    def set_kpi_aspects_weights(self, kpi_aspects_weights):
        self.__kpi_aspects_weights = kpi_aspects_weights

    def set_threshold(self, threshold):
        self.__threshold = threshold

    def set_formula(self, formula):
        self.__formula = formula

    def set_dataset_id(self, dataset_id):
        self.__dataset_id = dataset_id

    def set_dataset_labels(self, dataset_labels):
        self.__dataset_labels = dataset_labels

    def set_kpi_family(self, kpi_family):
        self.__kpi_family = kpi_family

    def set_color_coding(self, color_coding):
        self.__color_coding = color_coding
