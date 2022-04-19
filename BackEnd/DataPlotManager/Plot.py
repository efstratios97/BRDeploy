# Project Athena
'''
Owner: Efstratios Pahis
Contributors:
Description: Defines a Plot Object
'''


class Plot:

    def __init__(self, plot_id, formdata, grouped, visualization_type,
                 visualization_right, component_name, separated_display, dataset_id="", dataset_label=""):
        self.__plot_id = plot_id
        self.__formdata = formdata
        self.__grouped = grouped
        self.__visualization_type = visualization_type
        self.__visualization_right = visualization_right
        self.__component_name = component_name
        self.__separated_display = separated_display
        self.__dataset_id = dataset_id
        self.__dataset_label = dataset_label

    # Definition of get Methods for Plot Objects

    def get_plotID(self):
        return self.__plot_id

    def get_formdata(self):
        return self.__formdata

    def get_grouped(self):
        return self.__grouped

    def get_visualization_type(self):
        return self.__visualization_type

    def get_visualization_right(self):
        return self.__visualization_right

    def get_component_name(self):
        return self.__component_name

    def get_dataset_id(self):
        return self.__dataset_id

    def get_dataset_label(self):
        return self.__dataset_label

    def get_separated_display(self):
        return self.__separated_display

    # Set Functions for Plot Objects

    def set_formdata(self, formdata):
        self.__formdata = formdata

    def set_grouped(self, grouped):
        self.__grouped = grouped

    def set_visualization_type(self, visualization_type):
        self.__visualization_type = visualization_type

    def set_visualization_right(self, visualization_right):
        self.__visualization_right = visualization_right

    def set_component_name(self, component_name):
        self.__component_name = component_name

    def set_dataset_id(self, dataset_id):
        self.__dataset_id = dataset_id

    def set_dataset_label(self, dataset_label):
        self.__dataset_label = dataset_label

    def set_separated_display(self, separated_display):
        self.__separated_display = separated_display
