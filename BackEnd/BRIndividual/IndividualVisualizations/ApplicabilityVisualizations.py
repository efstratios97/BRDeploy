# Project Athena
'''
Owner: Efstratios Pahis
Contributors:
Description: Implements main functionality of the kpi_m.KPIManager
'''

import DataManager.DataManager as dm
import KPIAspectManager.AspectManager as aspct_m
import KPIManager.KPIManager as kpi_m
import Utils.Settings as st
import numpy as np


class ApplicabilityVisualizations:

    def analyze_applicability_by_raw_component(self, raw_component, dataset_id="", dataset_label="", gauge_type="hlineargauge"):
        dataset_id = dm.DataManager.check_dataset_exists_and_return_alternative_based_on_label(
            dm.DataManager, dataset_id=dataset_id, dataset_label=dataset_label)
        data = dm.DataManager.get_table_as_df(
            dm.DataManager, dataset_id)
        if "Anzahl" in raw_component or "kosten" in raw_component:
            data[raw_component] = data[raw_component].apply(
                lambda x: np.nan if x == 0 or x == "0" else x)
        else:
            data[raw_component] = data[raw_component].apply(
                lambda x: np.nan if x == "" or x == "Kein Eintrag" or x == "-" else x)
        value = ((len(data[raw_component]) - data[raw_component].isna().sum()
                  ) / len(data[raw_component])) * 100
        result = self.applicability_json_creator(
            ApplicabilityVisualizations, value=value, component=raw_component, gauge_type=gauge_type, width="100%", height="30%")
        return [result]

    def analyze_applicability_kpi_based_on_aspect(self, aspect_id, dataset_id="", dataset_label="", gauge_type="hlineargauge"):
        dataset_id = dm.DataManager.check_dataset_exists_and_return_alternative_based_on_label(
            dm.DataManager, dataset_id=dataset_id, dataset_label=dataset_label)
        data = dm.DataManager.get_table_as_df(
            dm.DataManager, dataset_id)
        aspect = aspct_m.AspectManager.get_aspect_by_id(
            aspct_m.AspectManager, aspect_id=aspect_id)
        aspect_raw_components = aspect.get_raw_components_from_dataset()
        raw_components = [
            val for sublist in aspect_raw_components for val in sublist]
        value = 0
        all_raw_aspects_count = 0
        aspects_completed_data_count = 0
        for raw_component in raw_components:
            if "Anzahl" in raw_component or "kosten" in raw_component:
                data[raw_component] = data[raw_component].apply(
                    lambda x: np.nan if x == 0 or x == "0" else x)
            else:
                data[raw_component] = data[raw_component].apply(
                    lambda x: np.nan if x == "" or x == "Kein Eintrag" or x == "-" else x)
            all_raw_aspects_count += len(data[raw_component])
            aspects_completed_data_count += len(
                data[raw_component]) - data[raw_component].isna().sum()
        value = aspects_completed_data_count / all_raw_aspects_count * 100
        result = self.applicability_json_creator(
            ApplicabilityVisualizations, value=value, component=raw_component, gauge_type=gauge_type, width="100%", height="30%")
        return [result]

    def analyze_applicability_kpi(self, kpi, dataset_id="", dataset_label="", parameters="all", gauge_type="hlineargauge"):
        dataset_id = dm.DataManager.check_dataset_exists_and_return_alternative_based_on_label(
            dm.DataManager, dataset_id=dataset_id, dataset_label=dataset_label)
        data = dm.DataManager.get_table_as_df(
            dm.DataManager, dataset_id)
        if not parameters == "all":
            for param in parameters:
                if "dep" in list(param.keys()):
                    if not param["dep"] == st.ALL_VALUES_INPUT_FIELD:
                        parameter = param["dep"]
                        slicer = "Verantwortliche Organisationseinheit"
                        data = data[data[slicer] == parameter]
                if "app" in list(param.keys()):
                    parameter = param['app']
                    slicer = "Name"
                    data = data[data[slicer] == parameter]
                if "domain" in list(param.keys()):
                    parameter = param['domain']
                    data["Zugeordnete Domäne"] = data["Zugeordnete Domäne"].apply(
                        lambda x: x if parameter in x else np.NaN)
                    data.dropna(inplace=True, subset=[
                        'Zugeordnete Domäne'])
        aspects = [val for sublist in kpi.get_kpi_aspects_weights()
                   for val in sublist]
        value = 0
        all_raw_aspects_count = 0
        aspects_completed_data_count = 0
        for aspect_name in aspects:
            aspect = aspct_m.AspectManager.get_aspect_by_name(
                aspct_m.AspectManager, name=aspect_name)
            aspect_raw_components = aspect.get_raw_components_from_dataset()
            raw_components = [
                val for sublist in aspect_raw_components for val in sublist]
            for raw_component in raw_components:
                if "Anzahl" in raw_component and "kosten" in raw_component:
                    data[raw_component] = data[raw_component].apply(
                        lambda x: np.nan if x == 0 or x == "0" else x)
                else:
                    data[raw_component] = data[raw_component].apply(
                        lambda x: np.nan if x == "" or x == "Kein Eintrag" or x == "-" else x)
                all_raw_aspects_count += len(data[raw_component])
                aspects_completed_data_count += len(
                    data[raw_component]) - data[raw_component].isna().sum()
        if all_raw_aspects_count == 0:
            value = 0
        else:
            value = aspects_completed_data_count / all_raw_aspects_count * 100
        result = self.applicability_json_creator(
            ApplicabilityVisualizations, value=value, component=kpi.get_KPI_name(), gauge_type=gauge_type)
        return [result]

    def applicability_json_creator(self, value, component="all", gauge_type="hlineargauge", width=400, height=300):
        return {
            "id": st.create_id(),
            "type": gauge_type,
            "width": width,
            "height": height,
            "dataFormat": "json",
            "dataSource": {
                "chart": {
                    "theme": "fusion",
                    "caption": "Applicability Analysis",
                    "subcaption": "Current Data Status of " + component,
                    "lowerLimit": "0",
                    "upperLimit": "100",
                    "numberSuffix": "%",
                    "chartBottomMargin": "40",
                    "valueFontSize": "11",
                    "valueFontBold": "1",
                    "valueFontColor": "#000000",
                    "baseFontSize": 15,
                    "exportEnabled": "1",
                },
                "colorRange": {
                    "color": [
                        {
                            "minValue": "0",
                            "maxValue": "40",
                            "label": "Low",
                            "code": "#cc0000",
                        },
                        {
                            "minValue": "40",
                            "maxValue": "60",
                            "label": "Moderate",
                            "code": "#ffba00",
                        },
                        {
                            "minValue": "60",
                            "maxValue": "100",
                            "label": "High",
                            "code": "#228b22",
                        },
                    ],
                },
                "value": value,
                "pointers": {
                    "pointer": [
                            {
                                "value": value,
                            },
                    ],
                },
                "annotations": {
                    "origw": "400",
                    "origh": "190",
                    "autoscale": "1",
                    "groups": [
                        {
                            "id": "range",
                            "items": [
                                {
                                    "id": "rangeBg",
                                    "type": "rectangle",
                                    "x": "$chartCenterX-115",
                                    "y": "$chartEndY-35",
                                    "tox": "$chartCenterX +115",
                                    "toy": "$chartEndY-15",
                                    "fillcolor": "#0075c2",
                                },
                                {
                                    "id": "rangeText",
                                    "type": "Text",
                                    "fontSize": "15",
                                    "fillcolor": "#ffffff",
                                    "text": "Recommended Data Status : >40%",
                                    "x": "$chartCenterX",
                                    "y": "$chartEndY-25",
                                },
                            ],
                        },
                    ],
                },
            },
        }
