# Project Athena
'''
Owner: Efstratios Pahis
Contributors:
Description: Defines a ASPECT object
'''

import Utils.Settings as st


class ASPECT:

    def __init__(self, aspect_id, name, description, raw_components_from_dataset, skala_size,
                 weight, threshold, operation_type, formula, dataset_id, dataset_labels, kpi_family):
        self.__aspectID = aspect_id
        self.__name = name
        self.__description = description
        self.__raw_components_from_dataset = raw_components_from_dataset
        self.__skala_size = skala_size
        self.__weight = weight
        self.__threshold = threshold
        self.__operation_type = operation_type
        self.__formula = formula
        self.__dataset_id = dataset_id
        self.__dataset_labels = dataset_labels
        self.__kpi_family = kpi_family

    # Definition of get Methods for ASPECT Objects
    def get_aspectID(self):
        return self.__aspectID

    def get_name(self):
        return self.__name

    def get_description(self):
        return self.__description

    def get_raw_components_from_dataset(self):
        if isinstance(self.__raw_components_from_dataset, str):
            res = st.string_list_with_string_dict_into_list_dict(
                self.__raw_components_from_dataset)
            return res
        else:
            return self.__raw_components_from_dataset

    def get_formula(self):
        return self.__formula

    def get_dataset_id(self):
        return self.__dataset_id

    def get_dataset_labels(self):
        return self.__dataset_labels

    def get_skala_size(self):
        return self.__skala_size

    def get_weight(self):
        return self.__weight

    def get_threshold(self):
        return self.__threshold

    def get_kpi_family(self):
        return self.__kpi_family

    def get_operation_type(self):
        return self.__operation_type

    # Setter Methods for certain Attributes of ASPECT Objects
    def set_name(self, name):
        self.__name = name

    def set_description(self, description):
        self.__description = description

    def set_skala_size(self, skala_size):
        self.__skala_size = skala_size

    def set_weight(self, weight):
        self.__weight = weight

    def set_threshold(self, threshold):
        self.__threshold = threshold

    def set_raw_components_from_dataset(self, raw_components_from_dataset):
        self.__raw_components_from_dataset = raw_components_from_dataset

    def set_formula(self, formula):
        self.__formula = formula

    def set_dataset_id(self, dataset_id):
        self.__dataset_id = dataset_id

    def set_dataset_labels(self, dataset_labels):
        self.__dataset_labels = dataset_labels

    def set_kpi_family(self, kpi_family):
        self.__kpi_family = kpi_family

    def set_operation_type(self, operation_type):
        self.__operation_type = operation_type
