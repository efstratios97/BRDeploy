# Project Athena
'''
Owner: Efstratios Pahis
Contributors:
Description: Defines a Plot Object
'''

import Utils.Settings as st


class Plot:

    def __init__(self, plot_id, plot_title, plot_subtitle, plot_legend_show, plot_dataset_id_for_chart,
                 plot_dataset_label, plot_chart_type, plot_chart_width="300px", plot_chart_height="300px",
                 plot_xaxis_categories=[], plot_input_fields=0, plot_input_fields_id="", plot_empty_field="",
                 plot_empty_field_2=""):
        self.__plot_id = plot_id
        self.__plot_title = plot_title
        self.__plot_subtitle = plot_subtitle
        self.__plot_legend_show = 1 if plot_legend_show else 0
        self.__plot_dataset_id_for_chart = plot_dataset_id_for_chart
        self.__plot_dataset_label = plot_dataset_label
        self.__plot_chart_type = plot_chart_type
        self.__plot_chart_width = plot_chart_width
        self.__plot_chart_height = plot_chart_height
        self.__plot_xaxis_categories = plot_xaxis_categories
        self.__plot_input_fields = 1 if plot_input_fields else 0
        self.__plot_input_fields_id = plot_input_fields_id
        self.__plot_empty_field = plot_empty_field
        self.__plot_empty_field_2 = plot_empty_field_2

    # Definition of get Methods for Plot Objects

    def get_plotID(self):
        return self.__plot_id

    def get_title(self):
        return self.__plot_title

    def get_subtitle(self):
        return self.__plot_subtitle

    def get_legend_show(self):
        return self.__plot_legend_show

    def get_dataset_id_for_chart(self):
        return self.__plot_dataset_id_for_chart

    def get_dataset_label(self):
        return self.__plot_dataset_label

    def get_chart_type(self):
        return self.__plot_chart_type

    def get_chart_width(self):
        return self.__plot_chart_width

    def get_chart_height(self):
        return self.__plot_chart_height

    def get_xaxis_categories(self):
        return self.__plot_xaxis_categories

    def get_input_fields(self):
        return self.__plot_input_fields

    def get_input_fields_id(self):
        return self.__plot_input_fields_id

    # Set Functions for Plot Objects

    def set_title(self, title):
        self.__plot_title = title

    def set_subtitle(self, subtitle):
        self.__plot_subtitle = subtitle

    def set_legend_show(self, legend_show):
        self.__plot_legend_show = legend_show

    def set_dataset_id_for_chart(self, dataset_id_for_chart):
        self.__plot_dataset_id_for_chart = dataset_id_for_chart

    def set_dataset_label(self, dataset_label):
        self.__plot_dataset_label = dataset_label

    def set_chart_type(self, chart_type):
        self.__plot_chart_type = chart_type

    def set_chart_width(self, chart_width):
        self.__plot_chart_width = chart_width

    def set_chart_height(self, chart_height):
        self.__plot_chart_height = chart_height

    def set_xaxis_categories(self, xaxis_categories):
        self.__plot_xaxis_categories = xaxis_categories

    def set_input_fields(self, input_fields):
        self.__plot_input_fields = input_fields

    def set_input_fields_id(self, input_fields_id):
        self.__plot_input_fields_id = input_fields_id
