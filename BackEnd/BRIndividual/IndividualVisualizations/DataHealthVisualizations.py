# Project Athena
'''
Owner: Efstratios Pahis
Contributors:
Description: Implements Data Health Visualizations
'''

import DataManager.DataManager as dm
import BRIndividual.Utils.SettingsBR as st_br
import Utils.Settings as st
import ArchitectureViewManager.ArchitectureViewManager as avm
import numpy as np
import pandas as pd


class DataHealthVisualizations:

    architecture_view_analysis_max_bar_display = 15

    def architecture_view_analysis_complete_conditional(self, parameter, architecture_view, dataset_id, dataset_label):
        results = []
        architecture_view_components = architecture_view[0]['architecture_view']['components'].split(
            ",")
        if len(architecture_view_components) > self.architecture_view_analysis_max_bar_display:
            results.append(self.architecture_view_analysis_complete_view(DataHealthVisualizations, parameter=parameter,
                                                                         architecture_view=architecture_view, dataset_id=dataset_id, dataset_label=dataset_label)[0])
        results.append(self.architecture_view_analysis(DataHealthVisualizations, parameter=parameter,
                                                       architecture_view=architecture_view, dataset_id=dataset_id, dataset_label=dataset_label)[0])

        return results

    # Scrolllable column 2d
    def architecture_view_analysis(self, parameter, architecture_view,
                                   dataset_id, dataset_label):
        results = []
        architecture_view = avm.ArchitectureViewManager.get_architecture_view_by_id(
            avm.ArchitectureViewManager, architecture_view_id=architecture_view[0]['architecture_view']['architecture_view_id'])
        dataset_id = dm.DataManager.check_dataset_exists_and_return_alternative_based_on_label(
            dm.DataManager, dataset_id=dataset_id, dataset_label=dataset_label)
        data = dm.DataManager.get_table_as_df(
            dm.DataManager, table=dataset_id)
        apps_data_set = st_br.get_apps_df_by_parameter(
            parameter=parameter, dataset_data=data, dataset_id=dataset_id, return_apps=False)
        architecture_view_components = architecture_view.get_components().split(",")
        category = []
        values = []
        for component in architecture_view_components:
            if "Anzahl" in component or "kosten" in component:
                apps_data_set[component] = apps_data_set[component].apply(
                    lambda x: np.nan if x == 0 or x == "0" else x)
            else:
                apps_data_set[component] = apps_data_set[component].apply(
                    lambda x: np.nan if x == "" or x == "Kein Eintrag" or x == "-" else x)
            values.append(
                {"value": (1 - (apps_data_set[component].isna().sum() / len(apps_data_set[component])))*100})
            category.append({"label": component})
        results.append({
            "id": st.create_id(),
            "type": 'scrollColumn2D',
            'width': '100%',
            'height': '675',
            "dataFormat": 'json',
            "dataSource": {
                "chart": {
                    "theme": "fusion",
                    "caption": "Architecture View Analysis",
                    "subcaption": "Based on: " + st_br.get_parameter_as_string_from_parameter_dict(parameter) + " & " + architecture_view.get_name(),
                    "xaxisname": "Components",
                    "yaxisname": "Percentage",
                    "showvalues": 1 if len(architecture_view_components) < self.architecture_view_analysis_max_bar_display else 0,
                    "numbersuffix": "%",
                    "numVisiblePlot": self.architecture_view_analysis_max_bar_display,
                    "scrollheight": "10",
                    "flatScrollBars": "1",
                    "scrollShowButtons": "1",
                    "scrollColor": "#cccccc",
                    "showHoverEffect": "1",
                    "yAxisMaxValue": 100,
                    "exportEnabled": "1",
                },
                "categories": [{
                    "category": category
                }],
                "dataset": [{
                    "data": values
                }]
            }
        })
        return results

    # Not scrollable column 2d
    def architecture_view_analysis_complete_view(self, parameter, architecture_view,
                                                 dataset_id, dataset_label):
        results = []
        architecture_view = avm.ArchitectureViewManager.get_architecture_view_by_id(
            avm.ArchitectureViewManager, architecture_view_id=architecture_view[0]['architecture_view']['architecture_view_id'])
        dataset_id = dm.DataManager.check_dataset_exists_and_return_alternative_based_on_label(
            dm.DataManager, dataset_id=dataset_id, dataset_label=dataset_label)
        data = dm.DataManager.get_table_as_df(
            dm.DataManager, table=dataset_id)
        apps_data_set = st_br.get_apps_df_by_parameter(
            parameter=parameter, dataset_data=data, dataset_id=dataset_id, return_apps=False)
        architecture_view_components = architecture_view.get_components().split(",")
        values = []
        for component in architecture_view_components:
            if "Anzahl" in component or "kosten" in component:
                apps_data_set[component] = apps_data_set[component].apply(
                    lambda x: np.nan if x == 0 or x == "0" else x)
            else:
                apps_data_set[component] = apps_data_set[component].apply(
                    lambda x: np.nan if x == "" or x == "Kein Eintrag" or x == "-" else x)
            values.append(
                {"label": component, "value": (1 - (apps_data_set[component].isna().sum() / len(apps_data_set[component])))*100})
        results.append({
            "id": st.create_id(),
            "type": 'column2d',
            "width": '100%',
            "height": '675',
            "dataFormat": 'json',
            "dataSource": {
                "chart": {
                    "caption": "Architecture View Analysis: Complete View",
                    "subcaption": "Based on: " + st_br.get_parameter_as_string_from_parameter_dict(parameter) + " & " + architecture_view.get_name(),
                    "xaxisname": "Components",
                    "yaxisname": "Percentage",
                    "showvalues": 1 if len(architecture_view_components) < 20 else 0,
                    "numbersuffix": "%",
                    "showHoverEffect": "1",
                    "yAxisMaxValue": 100,
                    "exportEnabled": "1",
                    "theme": "fusion",
                },
                "data": values
            }
        })
        return results

    def application_status_radar(self, parameters, architecture_view,
                                 dataset_id, dataset_label):
        def calculate_application_status(data: pd.DataFrame, component):
            result = data[component].to_string().count(
                ',')
            return result
        results = []
        architecture_view = avm.ArchitectureViewManager.get_architecture_view_by_id(
            avm.ArchitectureViewManager, architecture_view_id=architecture_view[0]['architecture_view']['architecture_view_id'])
        dataset_id = dm.DataManager.check_dataset_exists_and_return_alternative_based_on_label(
            dm.DataManager, dataset_id=dataset_id, dataset_label=dataset_label)
        data = dm.DataManager.get_table_as_df(
            dm.DataManager, table=dataset_id)
        components = st_br.get_elegible_components_for_counting_based_on_condition(
            data=data, components=architecture_view.get_components().split(','))
        dataset = []
        categories = []
        for param in parameters:
            category = []
            values = []
            parameter_str = st_br.get_parameter_as_string_from_parameter_dict(
                param)
            apps_data_set = st_br.get_apps_df_by_parameter(
                parameter=param, dataset_data=data, dataset_id=dataset_id, return_apps=False, return_trimmed_dataset_based_app=True)
            for component in components:
                if "Anzahl" in component or "kosten" in component:
                    apps_data_set[component] = apps_data_set[component].apply(
                        lambda x: np.nan if x == 0 or x == "0" else x)
                else:
                    apps_data_set[component] = apps_data_set[component].apply(
                        lambda x: np.nan if x == "" or x == "Kein Eintrag" or x == "-" else x)
                values.append({"value": calculate_application_status(
                    data=apps_data_set, component=component)})
                category.append({"label": component})
            categories.append({"category": category})
            dataset.append({"seriesname": parameter_str,
                           "data": values, "alpha": 60})
        results.append({
            "id": st.create_id(),
            "type": 'radar',
            "width": '100%',
            "height": '825',
            "dataFormat": 'json',
            "dataSource": {
                "chart": {
                    "caption": "Application Status Analysis",
                    "subCaption": "Based on: " + architecture_view.get_name(),
                    "numberPreffix": "#",
                    "theme": "fusion",
                    "radarRadius": "250",
                    "radarfillcolor": "#ffffff",
                    "animation": 1,
                    "animationDuration": 3,
                    "showValues": 1 if len(categories) < 2 and len(components) < 5 else 0,
                    "showToolTip": 1,
                    "exportEnabled": 1,
                    "showHoverEffect": 1,
                },
                "categories": [{
                    "category": category
                }],
                "dataset": dataset
            }
        })
        return results
