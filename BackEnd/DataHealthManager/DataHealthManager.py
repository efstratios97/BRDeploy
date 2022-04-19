# Project Athena
'''
Owner: Efstratios Pahis
Contributors:
Description: Implements main functionality of the DataManager
'''

import Utils.DataBaseUtils as db_utils
import Utils.DataBaseSQL as sql_stmt
import Utils.Settings as st
import DataManager.DataManager as dm
import pandas as pd


class DataHealthManager:

    def count_applications_by_department(self, dataset_id):
        data_included = []
        data = []
        df = dm.DataManager.get_table_as_df(dm.DataManager, table=dataset_id)
        # df['Verantwortliche Organisationseinheit'] = df['Verantwortliche Organisationseinheit'].apply(
        #     lambda x: 'NICHT EINGEPFLEGT' if not isinstance(x, str) else x)
        df['Verantwortliche Organisationseinheit'] = df['Verantwortliche Organisationseinheit'].apply(
            lambda x: 'NICHT EINGEPFLEGT' if x == '' else x)  # Because change of how read datasets --> None replaced with ""
        df['Verantwortliche Organisationseinheit'] = df['Verantwortliche Organisationseinheit'].apply(
            lambda x: x.replace(" (Organisationseinheit)", ""))

        def get_dep_count_pairs(x):
            if not x['Verantwortliche Organisationseinheit'] in data_included:
                data.append(
                    {"x": x['Verantwortliche Organisationseinheit'], "y": 1})
                data_included.append(x['Verantwortliche Organisationseinheit'])
            else:
                for pair in data:
                    if pair['x'] == x['Verantwortliche Organisationseinheit']:
                        pair['y'] = pair['y'] + 1
        df.apply(lambda x: get_dep_count_pairs(x), axis=1)
        data = sorted(data, key=lambda i: i['y'], reverse=True)
        return data
