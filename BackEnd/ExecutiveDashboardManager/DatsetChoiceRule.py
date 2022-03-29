# Project Athena
'''
Owner: Efstratios Pahis
Contributors:
Description: Defines a DatsetChoiceRule object
'''


class DatsetChoiceRule:

    def __init__(self, dataset_choice_rule_id, name, description=""):
        self.__dataset_choice_rule_id = dataset_choice_rule_id
        self.__name = name
        self.__description = description

    def get_dataset_choice_rule_id(self):
        return self.__dataset_choice_rule_id

    def get_name(self):
        return self.__name

    def get_description(self):
        return self.__description
