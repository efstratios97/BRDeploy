# Project Athena
'''
Owner: Efstratios Pahis
Contributors:
Description: Endpoints for KPIMAnager
'''

from ast import copy_location
from KPIFormulaManager.FormulaManager import FormulaManager
import flask as fl
import pandas as pd
import Utils.Settings as st
from datetime import datetime
import KPIManager.KPIManager as kpi_m
import KPIManager.KPI as kpi_obj
import KPIManager.KPI_Category_Type as kpi_c_t
import KPIFormulaManager.FormulaManager as fa_m
import KPIFormulaManager.FormulaExecutor as fa_e
import KPIFormulaManager.Formula as fa
import DataManager.DataManager as dm


class KPIManagerEndpoints:

    def endpoints_exception(self, code, msg):
        fl.abort(fl.make_response(fl.jsonify(message=msg), code))

    def kpi_to_dict(self, kpi: kpi_obj.KPI):
        dict_formatted = {}
        if kpi:
            dict_formatted['kpi_id'] = kpi.get_KPIID()
            dict_formatted['name'] = kpi.get_KPI_name()
            dict_formatted['description'] = kpi.get_description()
            dict_formatted['high_level_kpi_component_kpi_weight'] = kpi.get_high_level_kpi_component_kpi_weight()
            dict_formatted['kpi_aspects_weights'] = kpi.get_kpi_aspects_weights(
            )
            dict_formatted['threshold'] = kpi.get_threshold()
            dict_formatted['formula'] = kpi.get_formula()
            dict_formatted['dataset_id'] = kpi.get_dataset_id()
            dict_formatted['dataset_labels'] = kpi.get_dataset_labels()
            dict_formatted['color_coding'] = kpi.get_color_coding()
            dict_formatted['kpi_family'] = kpi.get_kpi_family()
        return dict_formatted

    def formula_to_dict(self, formula: fa.Formula):
        dict_formatted = {}
        if formula:
            dict_formatted['formula_id'] = formula.get_formulaID()
            dict_formatted['name'] = formula.get_formula_name()
            dict_formatted['description'] = formula.get_description()
            dict_formatted['operation'] = formula.get_operation()
            dict_formatted['purpose'] = formula.get_purpose()
            dict_formatted['kpi_families'] = formula.get_kpi_families()
        return dict_formatted

    def kpi_category_type_to_dict(self, kpi_category_type: kpi_c_t.KPI_CATEGORY_TYPE):
        dict_formatted = {}
        if kpi_category_type:
            dict_formatted['kpi_category_type_id'] = kpi_category_type.get_kpi_category_type_id(
            )
            dict_formatted['name'] = kpi_category_type.get_name()
        return dict_formatted


blueprint = fl.Blueprint('KPIManager', __name__)


@blueprint.route('/create_KPI', methods=['POST', 'OPTIONS'])
def post_kpi():
    result = {}
    name = fl.request.form['name']
    description = fl.request.form['description']
    high_level_kpi_component_kpi_weight = fl.request.form['high_level_kpi_component_kpi_weight']
    kpi_aspects_weights = st.string_list_with_string_dict_into_list_dict(
        fl.request.form['kpi_aspects_weights'])
    threshold = fl.request.form['threshold']
    formula = fl.request.form['formula']
    dataset_id = fl.request.form['dataset_id']
    dataset_labels = st.make_list_to_str(st.string_list_to_list(
        fl.request.form['dataset_labels']))
    kpi_family = fl.request.form['kpi_family']
    color_coding = fl.request.form['color_coding']
    kpi = kpi_m.KPIManager.create_kpi(kpi_m.KPIManager, name=name, description=description,
                                      high_level_kpi_component_kpi_weight=high_level_kpi_component_kpi_weight,
                                      kpi_aspects_weights=kpi_aspects_weights, threshold=threshold,
                                      formula=formula, dataset_id=dataset_id, dataset_labels=dataset_labels,
                                      kpi_family=kpi_family, color_coding=color_coding)

    result = KPIManagerEndpoints.kpi_to_dict(
        KPIManagerEndpoints, kpi=kpi)
    return fl.jsonify(result), 200


@blueprint.route('/update_kpi/<attribute>/<value>/<kpi_id>', methods=['POST', 'OPTIONS'])
def update_kpi(attribute, value, kpi_id):
    result = {}
    if attribute == "name":
        kpi_m.KPIManager.update_kpi_name(
            kpi_m.KPIManager, name=value, kpi_id=kpi_id)
    if attribute == "formula":
        kpi_m.KPIManager.update_kpi_formula(
            kpi_m.KPIManager, formula=value, kpi_id=kpi_id)
    if attribute == "dataset_label":
        kpi_m.KPIManager.update_kpi_dataset_labels(
            kpi_m.KPIManager, dataset_labels=value, kpi_id=kpi_id)
    if attribute == "kpi_family":
        kpi_m.KPIManager.update_kpi_family(
            kpi_m.KPIManager, kpi_family=value, kpi_id=kpi_id)
    if attribute == "high_level_kpi_component_kpi_weight":
        kpi_m.KPIManager.update_high_level_kpi_component_kpi_weight(
            kpi_m.KPIManager, high_level_kpi_component_kpi_weight=value, kpi_id=kpi_id)
    if attribute == "kpi_aspects_weights":
        kpi_m.KPIManager.update_kpi_aspect(
            kpi_m.KPIManager, kpi_aspects_weights=value, kpi_id=kpi_id)
    kpi = kpi_m.KPIManager.get_kpi_by_id(kpi_m.KPIManager, kpi_id=kpi_id)
    result = KPIManagerEndpoints.kpi_to_dict(
        KPIManagerEndpoints, kpi=kpi)
    return fl.jsonify(result), 200


@blueprint.route('/delete_kpi/<kpi_id>', methods=['DELETE', 'OPTIONS'])
def delete_kpi(kpi_id):
    result = {}
    kpi = kpi_m.KPIManager.get_kpi_by_id(kpi_m.KPIManager, kpi_id=kpi_id)
    kpi_m.KPIManager.delete_kpi(kpi_m.KPIManager, kpi_id=kpi_id)
    result = KPIManagerEndpoints.kpi_to_dict(
        KPIManagerEndpoints, kpi=kpi)
    return fl.jsonify(result), 200


@blueprint.route('/get_kpi/<kpi_id>', methods=['GET', 'OPTIONS'])
def get_kpi(kpi_id):
    result = {}
    kpi = kpi_m.KPIManager.get_kpi_by_id(kpi_m.KPIManager, kpi_id=kpi_id)
    if kpi:
        result = KPIManagerEndpoints.kpi_to_dict(
            KPIManagerEndpoints, kpi=kpi)
    else:
        KPIManagerEndpoints(404, "DATASET_NOT_FOUND")
    return fl.jsonify(result), 200


@blueprint.route('/get_kpis', methods=['GET', 'OPTIONS'])
def get_kpis():
    result = {}
    result['data'] = []
    kpis = kpi_m.KPIManager.get_all_kpis(kpi_m.KPIManager)
    for kpi in kpis:
        result['data'].append(KPIManagerEndpoints.kpi_to_dict(
            KPIManagerEndpoints, kpi=kpi))
    return fl.jsonify(result), 200


@blueprint.route('/get_kpis_by_dataset_label/<dataset_label>', methods=['GET', 'OPTIONS'])
def get_kpis_by_dataset_label(dataset_label):
    result = {}
    result['data'] = []
    kpis = kpi_m.KPIManager.get_all_kpis_by_dataset_label(
        kpi_m.KPIManager, dataset_label=dataset_label)
    for kpi in kpis:
        result['data'].append(KPIManagerEndpoints.kpi_to_dict(
            KPIManagerEndpoints, kpi=kpi))
    return fl.jsonify(result), 200


@blueprint.route('/get_kpi_by_name/<name>', methods=['GET', 'OPTIONS'])
def get_kpi_by_name(name):
    result = {}
    kpi = kpi_m.KPIManager.get_kpi_by_name(kpi_m.KPIManager, name=name)
    if kpi:
        result = KPIManagerEndpoints.kpi_to_dict(
            KPIManagerEndpoints, kpi=kpi)
    else:
        KPIManagerEndpoints(404, "DATASET_NOT_FOUND")
    return fl.jsonify(result), 200


@blueprint.route('/calculate_kpi/<kpi_id>/<dataset_id>/<dataset_label>', methods=['GET', 'OPTIONS'])
def calculate_kpi(kpi_id, dataset_id, dataset_label):
    result = {}
    formula_id = kpi_m.KPIManager.get_suitable_formula(
        kpi_m.KPIManager, kpi_id=kpi_id)
    formula = fa_m.FormulaManager.get_formula_by_id(
        fa_m.FormulaManager, formula_id=formula_id)
    formula_operation = formula.get_operation()
    fa_e.FormulaExecutor.execute_formula(
        fa_e.FormulaExecutor, operation=formula_operation, purpose=formula.get_purpose(),
        kpi_id=kpi_id, dataset_id=dataset_id, dataset_label=dataset_label)
    return fl.jsonify(result), 200


@blueprint.route('/calculate_kpis/<dataset_id>/<dataset_label>', methods=['POST', 'OPTIONS'])
def calculate_kpis(dataset_id, dataset_label):
    results = {}
    kpis = st.string_list_with_nested_string_dict_into_list_dict(fl.request.form[
        'kpis'])
    try:
        parameters = st.string_list_with_nested_string_dict_into_list_dict(fl.request.form[
            'parameter'])
    except:
        parameters = fl.request.form[
            'parameter']
    fast = True
    if fast:
        dataset_id = dm.DataManager.check_dataset_exists_and_return_alternative_based_on_label(
            dm.DataManager, dataset_id=dataset_id, dataset_label=dataset_label)
        data = dm.DataManager.get_table_as_df(dm.DataManager, table=dataset_id)
    for param in parameters:
        for kpi in kpis:
            formula = kpi_m.KPIManager.get_suitable_formula(
                kpi_m.KPIManager, kpi_id=kpi['kpi']['kpi_id'])
            formula = fa_m.FormulaManager.get_formula_by_id(
                fa_m.FormulaManager, formula_id=formula.get_formulaID())
            formula_operation = formula.get_operation()
            if "dep" in list(param.keys()):
                parameter = {"app": "",
                             "department": param["dep"], "domain": ""}
            if "app" in list(param.keys()):
                parameter = {"app": param['app'],
                             "department": "", "domain": ""}
            if "domain" in list(param.keys()):
                parameter = {"app": "",
                             "department": "", "domain": param['domain']}
            result = fa_e.FormulaExecutor.execute_formula(
                operation=formula_operation, purpose=formula.get_purpose(), kpi_id=kpi['kpi']['kpi_id'],
                dataset_id=dataset_id, dataset_label=dataset_label, parameter=parameter, dataset_data=data, fast=fast)
            if not result['parameter'] in list(results.keys()):
                results[result['parameter']] = []
            results[result['parameter']].append(result)
    return fl.jsonify(results), 200


@blueprint.route('/render_application_landscape_kpi/<dataset_id>/<dataset_label>', methods=['POST', 'OPTIONS'])
def render_application_landscape_kpi(dataset_id, dataset_label):
    results = {}
    kpis = st.string_list_with_nested_string_dict_into_list_dict(fl.request.form[
        'kpis'])
    try:
        parameters = st.string_list_with_nested_string_dict_into_list_dict(fl.request.form[
            'parameter'])
    except:
        parameters = fl.request.form[
            'parameter']
    for param in parameters:
        if "dep" in list(param.keys()):
            parameter = {"app": "",
                         "department": param["dep"], "domain": ""}
        if "app" in list(param.keys()):
            parameter = {"app": param['app'],
                         "department": "", "domain": ""}
        if "domain" in list(param.keys()):
            parameter = {"app": "",
                         "department": "", "domain": param['domain']}
    for kpi in kpis:
        kpi = kpi_m.KPIManager.get_kpi_by_id(
            kpi_m.KPIManager, kpi_id=kpi["kpi"]["kpi_id"])
        result = kpi_m.KPIManager.render_application_landscape_kpi(
            kpi_m.KPIManager, kpi=kpi.get_KPIID(), parameter=parameter, dataset_id=dataset_id, dataset_label=dataset_label)
        threshold = kpi.get_threshold()
    results["result"] = result
    results["threshold"] = threshold
    return fl.jsonify(results), 200


@blueprint.route('/analyze_applicability_kpi_based_on_aspect/<aspect_id>/<dataset_id>/<dataset_label>', methods=['GET', 'OPTIONS'])
def analyze_applicability_kpi_based_on_aspect(aspect_id, dataset_id, dataset_label):
    result = {}
    data = kpi_m.KPIManager.analyze_applicability_kpi_based_on_aspect(kpi_m.KPIManager,
                                                                      aspect_id=aspect_id,
                                                                      dataset_id=dataset_id,
                                                                      dataset_label=dataset_label)
    result["data"] = data
    return fl.jsonify(result), 200


@blueprint.route('/analyze_applicability_kpi/<kpi_id>/<dataset_id>/<dataset_label>/<parameters>', methods=['GET', 'OPTIONS'])
def analyze_applicability_kpi(kpi_id, dataset_id, dataset_label, parameters):
    result = {}
    data = kpi_m.KPIManager.analyze_applicability_kpi(kpi_m.KPIManager,
                                                      kpi_id=kpi_id,
                                                      dataset_id=dataset_id,
                                                      dataset_label=dataset_label,
                                                      parameters=parameters)
    result["data"] = data
    return fl.jsonify(result), 200


@blueprint.route('/get_formulas', methods=['GET', 'OPTIONS'])
def get_formulas():
    result = {}
    result['data'] = []
    formulas = fa_m.FormulaManager.get_all_formulas(fa_m.FormulaManager)
    for formula in formulas:
        result['data'].append(KPIManagerEndpoints.formula_to_dict(
            KPIManagerEndpoints, formula=formula))
    return fl.jsonify(result), 200


@blueprint.route('/get_formulas_by_purpose/<purpose>', methods=['GET', 'OPTIONS'])
def get_formulas_by_purpose(purpose):
    result = {}
    result['data'] = []
    formulas = fa_m.FormulaManager.get_all_formulas_by_purpose(
        fa_m.FormulaManager, purpose=purpose)
    for formula in formulas:
        result['data'].append(KPIManagerEndpoints.formula_to_dict(
            KPIManagerEndpoints, formula=formula))
    return fl.jsonify(result), 200


@blueprint.route('/get_all_kpi_category_types', methods=['GET', 'OPTIONS'])
def get_all_kpi_category_types():
    result = {}
    result['data'] = []
    kpi_category_types = kpi_m.KPIManager.get_all_kpi_category_types(
        kpi_m.KPIManager)
    for kpi_category_type in kpi_category_types:
        result['data'].append(KPIManagerEndpoints.kpi_category_type_to_dict(
            KPIManagerEndpoints, kpi_category_type=kpi_category_type))
    return fl.jsonify(result), 200


@blueprint.route('/get_suitable_kpi_category_types/<raw_component>/<dataset_id>/<dataset_label>', methods=['GET', 'OPTIONS'])
def get_suitable_kpi_category_types(raw_component, dataset_id, dataset_label):
    result = {}
    result['data'] = []
    kpi_category_types = kpi_m.KPIManager.get_suitable_kpi_category_types(
        kpi_m.KPIManager, raw_component=raw_component, dataset_id=dataset_id, dataset_label=dataset_label)
    for kpi_category_type in kpi_category_types:
        result['data'].append(KPIManagerEndpoints.kpi_category_type_to_dict(
            KPIManagerEndpoints, kpi_category_type=kpi_category_type))
    return fl.jsonify(result), 200
