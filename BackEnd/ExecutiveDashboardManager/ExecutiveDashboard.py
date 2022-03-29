# Project Athena
'''
Owner: Efstratios Pahis
Contributors:
Description: Defines a ExecutiveDashboard Object
'''

import Utils.Settings as st
from datetime import datetime


class ExecutiveDashboard:

    def __init__(self, executive_dashboard_id, name, description,
                 access_user_list, access_business_unit_list, plots,
                 dataset_choice_rule, visualization_right, dataset_id="",
                 dataset_label="",
                 creation_date=datetime.utcnow()):
        self.__executive_dashboard_id = executive_dashboard_id
        self.__name = name
        self.__description = description
        self.__access_user_list = access_user_list
        self.__access_business_unit_list = access_business_unit_list
        self.__plots = plots
        self.__dataset_choice_rule = dataset_choice_rule
        self.__visualization_right = visualization_right
        self.__dataset_id = dataset_id
        self.__dataset_label = dataset_label
        self.__creation_date = creation_date

    # Definition of get Methods for Cleaner Objects
    def get_executive_dashboardID(self):
        return self.__executive_dashboard_id

    def get_name(self):
        return self.__name

    def get_description(self):
        return self.__description

    def get_dataset_choice_rule(self):
        return self.__dataset_choice_rule

    def get_visualization_right(self):
        return self.__visualization_right

    def get_dataset_label(self):
        return self.__dataset_label

    def get_dataset_id(self):
        return self.__dataset_id

    def get_access_user_list(self):
        return self.__access_user_list

    def get_access_business_unit_list(self):
        return self.__access_business_unit_list

    def get_plots(self):
        return self.__plots

    def get_creation_date(self):
        return self.__creation_date

    # Set functions for Executive Dashboard

    def set_name(self, name):
        self.__name = name

    def set_description(self, description):
        self.__description = description

    def set_dataset_choice_rule(self, dataset_choice_rule):
        self.__dataset_choice_rule = dataset_choice_rule

    def set_visualization_right(self, visualization_right):
        self.__visualization_right = visualization_right

    def set_dataset_label(self, dataset_label):
        self.__dataset_label = dataset_label

    def set_dataset_id(self, dataset_id):
        self.__dataset_id = dataset_id

    def set_access_user_list(self, access_user_list):
        self.__access_user_list = access_user_list

    def set_access_business_unit_list(self, access_business_unit_list):
        self.__access_business_unit_list = access_business_unit_list

    def set_plots(self, plots):
        self.__plots = plots
