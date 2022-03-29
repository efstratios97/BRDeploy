# Project Athena
'''
Owner: Efstratios Pahis
Contributors:
Description: Defines a VisualizationRight object
'''


class VisualizationRight:

    def __init__(self, visualization_right_id, name, description=""):
        self.__visualization_right_id = visualization_right_id
        self.__name = name
        self.__description = description

    def get_visualization_right_id(self):
        return self.__visualization_right_id

    def get_name(self):
        return self.__name

    def get_description(self):
        return self.__description
