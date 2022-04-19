# Project Athena
'''
Owner: Efstratios Pahis
Contributors:
Description: Implements main functionality of the KPIManager
'''


import BRIndividual.IndividualVisualizations.KPIVisualizations as kpi_v
import BRIndividual.IndividualVisualizations.DataHealthVisualizations as dt_ht_v
import BRIndividual.IndividualVisualizations.ApplicabilityVisualizations as apl_v
import KPIManager.KPIManager as kpi_m
import KPIAspectManager.AspectManager as aspct_m
import BRIndividual.Utils.SettingsBR as st_br
import Utils.Settings as st
import Flask.Endpoints.KPIAspectManagerAPI as aspct_api
import json


class IndividualVisualizationExecutor:

    def __init__(self):
        self.execution_switch = {
            'aspects': self.__render_aspects,
            'analyze_kpi_applicability': self.__analyze_applicability_kpi,
            'analyze_kpi_applicability_bulb': self.__analyze_kpi_applicability_bulb,
            'analyze_applicability_raw_component': self.__analyze_applicability_raw_component,
            'analyze_applicability_kpi_based_on_aspect': self.__analyze_applicability_kpi_based_on_aspect,
            'render_aspect_based_kpi': self.__render_aspect_based_kpi,
            'kpi': self.__render_kpis,
            'kpi_complete_view': self.__render_kpi_complete_view,
            'kpi_landscape': self.__render_application_landscape_kpi,
            'kpi_lifecycle': self.__render_app_life_cycle,
            'kpi_lifecycle_development': self.__render_life_cycle_development,
            'analyze_architecture_view': self.__analyze_architecture_view,
            'architecture_view_analysis_complete_conditional': self.__analyze_architecture_view_complete_conditional,
            'analyze_application_status_radar': self.__analyze_application_status_radar
        }

    def execute_visualization(self, formdata, visualization, dataset_id="", dataset_label=""):
        self.__init__(IndividualVisualizationExecutor)
        result = self.execution_switch[visualization](
            IndividualVisualizationExecutor, formdata, dataset_id, dataset_label)
        return result

    def __render_application_landscape_kpi(self, formdata, dataset_id, dataset_label):
        kpis = st.string_list_with_nested_string_dict_into_list_dict(formdata[
            'kpis'])
        try:
            parameters = st.string_list_with_nested_string_dict_into_list_dict(formdata[
                'parameter'])
        except:
            parameters = formdata[
                'parameter']
        parameter = st_br.get_parameters_from_input(parameters)
        for kpi in kpis:
            kpi = kpi_m.KPIManager.get_kpi_by_id(
                kpi_m.KPIManager, kpi_id=kpi["kpi"]["kpi_id"])
            result = kpi_v.KPIVisualizations.render_application_landscape_kpi(
                kpi_v.KPIVisualizations, kpi=kpi, parameter=parameter,
                dataset_id=dataset_id, dataset_label=dataset_label)
        return result

    def __render_kpi_complete_view(self, formdata, dataset_id, dataset_label):
        results = []
        results.append(self.__render_kpis(
            IndividualVisualizationExecutor, formdata=formdata.copy(), dataset_id=dataset_id, dataset_label=dataset_label)[0])
        results.append(self.__render_aspect_based_kpi(
            IndividualVisualizationExecutor, formdata=formdata.copy(), dataset_id=dataset_id, dataset_label=dataset_label)[0])
        results.append(self.__analyze_kpi_applicability_bulb(
            IndividualVisualizationExecutor, formdata=formdata.copy(), dataset_id=dataset_id, dataset_label=dataset_label)[0])
        return results

    def __render_kpis(self, formdata, dataset_id, dataset_label):
        kpis = st.string_list_with_nested_string_dict_into_list_dict(formdata[
            'kpis'])
        try:
            parameters = st.string_list_with_nested_string_dict_into_list_dict(formdata[
                'parameter'])
        except:
            parameters = formdata[
                'parameter']
        for kpi in kpis:
            kpi = kpi_m.KPIManager.get_kpi_by_id(
                kpi_m.KPIManager, kpi_id=kpi["kpi"]["kpi_id"])
        result = kpi_v.KPIVisualizations.render_kpi(
            kpi_v.KPIVisualizations, parameters=parameters, kpi=kpi,
            dataset_id=dataset_id, dataset_label=dataset_label, fast=True)
        return result

    def __render_app_life_cycle(self, formdata, dataset_id, dataset_label):
        kpis = st.string_list_with_nested_string_dict_into_list_dict(formdata[
            'kpis'])
        try:
            parameters = st.string_list_with_nested_string_dict_into_list_dict(formdata[
                'parameter'])
        except:
            parameters = formdata[
                'parameter']
        parameter = st_br.get_parameters_from_input(parameters)
        for kpi in kpis:
            kpi = kpi_m.KPIManager.get_kpi_by_id(
                kpi_m.KPIManager, kpi_id=kpi["kpi"]["kpi_id"])
        result = kpi_v.KPIVisualizations.render_app_life_cycle(
            kpi_v.KPIVisualizations, kpi=kpi, parameter=parameter, dataset_id=dataset_id, dataset_label=dataset_label)
        return result

    def __render_life_cycle_development(self, formdata, dataset_id, dataset_label):
        kpis = st.string_list_with_nested_string_dict_into_list_dict(formdata[
            'kpis'])
        try:
            parameters = st.string_list_with_nested_string_dict_into_list_dict(formdata[
                'parameter'])
        except:
            parameters = formdata[
                'parameter']
        parameter = st_br.get_parameters_from_input(parameters)
        for kpi in kpis:
            kpi = kpi_m.KPIManager.get_kpi_by_id(
                kpi_m.KPIManager, kpi_id=kpi["kpi"]["kpi_id"])
        result = kpi_v.KPIVisualizations.render_life_cycle_development(
            kpi_v.KPIVisualizations, kpi=kpi, parameter=parameter, dataset_id=dataset_id, dataset_label=dataset_label)
        return result

    def __analyze_applicability_kpi_based_on_aspect(self, formdata, dataset_id, dataset_label):
        try:
            aspect_name = formdata["aspect_name"][0]
            aspect = aspct_m.AspectManager.get_aspect_by_name(
                aspct_m.AspectManager, name=aspect_name)
            aspect_id = aspect.get_aspectID()
        except:
            aspect_id = formdata["aspect_id"][0]
        result = apl_v.ApplicabilityVisualizations.analyze_applicability_kpi_based_on_aspect(apl_v.ApplicabilityVisualizations,
                                                                                             aspect_id=aspect_id,
                                                                                             dataset_id=dataset_id,
                                                                                             dataset_label=dataset_label)
        return result

    def __analyze_applicability_kpi(self, formdata, dataset_id, dataset_label, gauge_type="hlineargauge"):
        kpis = st.string_list_with_nested_string_dict_into_list_dict(formdata[
            'kpis'])
        try:
            parameters = st.string_list_with_nested_string_dict_into_list_dict(formdata[
                'parameter'])
        except:
            parameters = formdata[
                'parameter']
        for kpi in kpis:
            kpi = kpi_m.KPIManager.get_kpi_by_id(
                kpi_m.KPIManager, kpi_id=kpi["kpi"]["kpi_id"])
        result = apl_v.ApplicabilityVisualizations.analyze_applicability_kpi(apl_v.ApplicabilityVisualizations,
                                                                             kpi=kpi,
                                                                             dataset_id=dataset_id,
                                                                             dataset_label=dataset_label,
                                                                             parameters=parameters, gauge_type=gauge_type)
        return result

    def __analyze_kpi_applicability_bulb(self, formdata, dataset_id, dataset_label):
        return self.__analyze_applicability_kpi(IndividualVisualizationExecutor, formdata=formdata, dataset_id=dataset_id,
                                                dataset_label=dataset_label, gauge_type="bulb")

    def __render_aspect_based_kpi(self, formdata, dataset_id, dataset_label):
        kpis = st.string_list_with_nested_string_dict_into_list_dict(formdata[
            'kpis'])
        for kpi in kpis:
            aspects = kpi_m.KPIManager.get_aspects_by_kpi_id(
                kpi_m.KPIManager, kpi_id=kpi["kpi"]["kpi_id"])
            kpi = kpi_m.KPIManager.get_kpi_by_id(
                kpi_m.KPIManager, kpi_id=kpi["kpi"]["kpi_id"])
            subcaption = "Weights ==> " + str(kpi.get_kpi_aspects_weights()).replace(
                '[', "").replace(']', "").replace("'", "")
        formdata.pop("kpis", None)
        formdata["aspects"] = []
        for aspect in aspects:
            aspect_dict = aspct_api.KPIAspectManagerEndpoints.aspect_to_dict(
                aspct_api.KPIAspectManagerEndpoints, aspect=aspect)
            formdata["aspects"].append({"aspect": aspect_dict})
        formdata["aspects"] = [json.dumps(formdata["aspects"])]
        return self.__render_aspects(IndividualVisualizationExecutor,
                                     formdata, dataset_id, dataset_label, subcaption=subcaption)

    def __render_aspects(self, formdata, dataset_id, dataset_label, subcaption="Aspect Analysis"):
        if isinstance(formdata, list):
            aspects = st.string_list_with_nested_string_dict_into_list_dict(formdata[
                'aspects'][0])
        else:
            aspects = st.string_list_with_nested_string_dict_into_list_dict(formdata[
                'aspects'])
        try:
            parameters = st.string_list_with_nested_string_dict_into_list_dict(
                formdata['parameter'])
        except:
            parameters = formdata[
                'parameter']
        result = kpi_v.KPIVisualizations.render_aspects(
            kpi_v.KPIVisualizations, parameters=parameters, aspects=aspects,
            dataset_id=dataset_id, dataset_label=dataset_label, subcaption=subcaption, fast=True)
        return result

    def __analyze_applicability_raw_component(self, formdata, dataset_id, dataset_label):
        raw_component = st.string_dict_to_dict(
            formdata["raw_component"][0])["raw_component"]
        result = apl_v.ApplicabilityVisualizations.analyze_applicability_by_raw_component(apl_v.ApplicabilityVisualizations,
                                                                                          raw_component=raw_component,
                                                                                          dataset_id=dataset_id,
                                                                                          dataset_label=dataset_label)
        return result

    def __analyze_architecture_view(self, formdata, dataset_id, dataset_label):
        if isinstance(formdata, list):
            architecture_view = st.string_list_with_nested_string_dict_into_list_dict(formdata[
                'architecture_view'][0])
        else:
            architecture_view = st.string_list_with_nested_string_dict_into_list_dict(formdata[
                'architecture_view'])
        try:
            parameters = st.string_list_with_nested_string_dict_into_list_dict(formdata[
                'parameter'])
        except:
            parameters = formdata[
                'parameter']
        parameter = st_br.get_parameters_from_input(parameters)
        result = dt_ht_v.DataHealthVisualizations.architecture_view_analysis(dt_ht_v.DataHealthVisualizations,
                                                                             parameter=parameter,
                                                                             architecture_view=architecture_view,
                                                                             dataset_id=dataset_id,
                                                                             dataset_label=dataset_label)
        return result

    def __analyze_architecture_view_complete_conditional(self, formdata, dataset_id, dataset_label):
        if isinstance(formdata, list):
            architecture_view = st.string_list_with_nested_string_dict_into_list_dict(formdata[
                'architecture_view'][0])
        else:
            architecture_view = st.string_list_with_nested_string_dict_into_list_dict(formdata[
                'architecture_view'])
        try:
            parameters = st.string_list_with_nested_string_dict_into_list_dict(formdata[
                'parameter'])
        except:
            parameters = formdata[
                'parameter']
        parameter = st_br.get_parameters_from_input(parameters)
        result = dt_ht_v.DataHealthVisualizations.architecture_view_analysis_complete_conditional(dt_ht_v.DataHealthVisualizations,
                                                                                                  parameter=parameter,
                                                                                                  architecture_view=architecture_view,
                                                                                                  dataset_id=dataset_id,
                                                                                                  dataset_label=dataset_label)
        return result

    def __analyze_application_status_radar(self, formdata, dataset_id, dataset_label):
        if isinstance(formdata, list):
            architecture_view = st.string_list_with_nested_string_dict_into_list_dict(formdata[
                'architecture_view'][0])
        else:
            architecture_view = st.string_list_with_nested_string_dict_into_list_dict(formdata[
                'architecture_view'])
        try:
            parameters = st.string_list_with_nested_string_dict_into_list_dict(formdata[
                'parameter'])
        except:
            parameters = formdata[
                'parameter']
        result = dt_ht_v.DataHealthVisualizations.application_status_radar(dt_ht_v.DataHealthVisualizations,
                                                                           parameters=parameters,
                                                                           architecture_view=architecture_view,
                                                                           dataset_id=dataset_id,
                                                                           dataset_label=dataset_label)
        return result
