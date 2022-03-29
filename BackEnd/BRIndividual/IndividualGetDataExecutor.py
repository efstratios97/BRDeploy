# Project Athena
'''
Owner: Efstratios Pahis
Contributors:
Description: Implements main functionality of the KPIManager
'''


import BRIndividual.IndividualMethods.GetData as gt_dt
import KPIManager.KPIManager as kpi_m
import BRIndividual.Utils.SettingsBR as st_br
import Utils.Settings as st


class IndividualGetDataExecutor:

    def __init__(self):
        self.execution_switch = {
            'get_departments_by_br_hiararchy': self.__get_departments_by_br_hiararchy,
            'get_departments_from_dataset': self.__get_departments_from_dataset,
            'get_domains_from_dataset': self.__get_domains_from_dataset,
            'get_apps_from_dataset': self.__get_apps_from_dataset
        }

    def execute_get_data_operation(self, get_data_operation, dataset_id="", dataset_label="", department=""):
        self.__init__(IndividualGetDataExecutor)
        if get_data_operation == 'get_departments_by_br_hiararchy':
            result = self.execution_switch[get_data_operation](
                IndividualGetDataExecutor, department, dataset_id, dataset_label)
        else:
            result = self.execution_switch[get_data_operation](
                IndividualGetDataExecutor, dataset_id, dataset_label)
        return result

    def __get_departments_from_dataset(self, dataset_id, dataset_label):
        result = {}
        result['data'] = []
        departments = gt_dt.GetData.get_departments_from_dataset(
            gt_dt.GetData, dataset_id=dataset_id, dataset_label=dataset_label)
        for department in departments:
            result['data'].append(department)
        return result

    def __get_departments_by_br_hiararchy(self, department, dataset_id, dataset_label):
        result = {}
        result['data'] = []
        departments = gt_dt.GetData.get_departments_by_department_hierarchy_br(
            gt_dt.GetData, dataset_id=dataset_id, dataset_label=dataset_label, department=department)
        for department in departments:
            result['data'].append(department)
        return result

    def __get_domains_from_dataset(self, dataset_id, dataset_label):
        result = {}
        result['data'] = []
        domains = gt_dt.GetData.get_domains_from_dataset(
            gt_dt.GetData, dataset_id=dataset_id, dataset_label=dataset_label)
        for domain in domains:
            result['data'].append(domain)
        return result

    def __get_apps_from_dataset(self, dataset_id, dataset_label):
        result = {}
        result['data'] = []
        apps = gt_dt.GetData.get_apps_from_dataset(
            gt_dt.GetData, dataset_id, dataset_label)
        for app in apps:
            result['data'].append(app)
        return result
