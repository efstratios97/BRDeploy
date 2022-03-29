# Project Athena
'''
Owner: Efstratios Pahis
Contributors:
Description: Endpoints for KPIAspectMAnager
'''

from KPIFormulaManager.FormulaManager import FormulaManager
import flask as fl
import Utils.Settings as st
import KPIManager.KPIManager as kpi_m
import KPIAspectManager.Aspect as aspct
import KPIAspectManager.AspectManager as aspct_m
import KPIFormulaManager.FormulaManager as fa_m


class KPIAspectManagerEndpoints:

    def endpoints_exception(self, code, msg):
        fl.abort(fl.make_response(fl.jsonify(message=msg), code))

    def aspect_to_dict(self, aspect: aspct.ASPECT):
        dict_formatted = {}
        if aspect:
            dict_formatted['aspect_id'] = aspect.get_aspectID()
            dict_formatted['name'] = aspect.get_name()
            dict_formatted['description'] = aspect.get_description()
            dict_formatted['raw_components_from_dataset'] = aspect.get_raw_components_from_dataset(
            )
            dict_formatted['skala_size'] = aspect.get_skala_size(
            )
            dict_formatted['weight'] = aspect.get_weight()
            dict_formatted['threshold'] = aspect.get_threshold()
            dict_formatted['operation_type'] = aspect.get_operation_type()
            dict_formatted['formula'] = aspect.get_formula()
            dict_formatted['dataset_id'] = aspect.get_dataset_id()
            dict_formatted['dataset_labels'] = aspect.get_dataset_labels()
            dict_formatted['kpi_family'] = aspect.get_kpi_family()
        return dict_formatted


blueprint = fl.Blueprint('KPIAspectManager', __name__)


@blueprint.route('/create_aspect', methods=['POST', 'OPTIONS'])
def post_aspect():
    result = {}
    name = fl.request.form['name']
    description = fl.request.form['description']
    raw_components_from_dataset = st.string_list_with_string_dict_into_list_dict(fl.request.form[
        'raw_components_from_dataset'])
    skala_size = int(fl.request.form['skala_size'])
    weight = int(fl.request.form['weight'])
    threshold = int(fl.request.form['threshold'])
    operation_type = fl.request.form['operation_type']
    formula = fl.request.form['formula']
    dataset_id = fl.request.form['dataset_id']
    dataset_labels = st.make_list_to_str(st.string_list_to_list(
        fl.request.form['dataset_labels']))
    kpi_family = fl.request.form['kpi_family']
    aspect = aspct_m.AspectManager.create_aspect(aspct_m.AspectManager, name=name, description=description,
                                                 raw_components_from_dataset=raw_components_from_dataset, skala_size=skala_size, weight=weight,
                                                 threshold=threshold, operation_type=operation_type, formula=formula, dataset_id=dataset_id,
                                                 dataset_labels=dataset_labels, kpi_family=kpi_family)
    result = KPIAspectManagerEndpoints.aspect_to_dict(
        KPIAspectManagerEndpoints, aspect=aspect)
    return fl.jsonify(result), 200


@blueprint.route('/update_aspect', methods=['POST', 'OPTIONS'])
def update_aspect():
    result = {}
    aspect_id = fl.request.form['aspect_id']
    name = fl.request.form['name']
    description = fl.request.form['description']
    raw_components_from_dataset = st.string_list_with_string_dict_into_list_dict(fl.request.form[
        'raw_components_from_dataset'])
    skala_size = int(fl.request.form['skala_size'])
    weight = int(fl.request.form['weight'])
    threshold = int(fl.request.form['threshold'])
    operation_type = fl.request.form['operation_type']
    formula = fl.request.form['formula']
    dataset_id = fl.request.form['dataset_id']
    dataset_labels = st.make_list_to_str(st.string_list_to_list(
        fl.request.form['dataset_labels']))
    kpi_family = fl.request.form['kpi_family']
    aspect = aspct_m.AspectManager.get_aspect_by_id(
        aspct_m.AspectManager, aspect_id=aspect_id)
    aspect.set_dataset_id(dataset_id=dataset_id)
    aspect.set_dataset_labels(dataset_labels=dataset_labels)
    aspect.set_description(description=description)
    aspect.set_formula(formula=formula)
    aspect.set_kpi_family(kpi_family=kpi_family)
    aspect.set_operation_type(operation_type=operation_type)
    aspect.set_name(name=name)
    aspect.set_raw_components_from_dataset(
        raw_components_from_dataset=raw_components_from_dataset)
    aspect.set_skala_size(skala_size=skala_size)
    aspect.set_threshold(threshold=threshold)
    aspect.set_weight(weight=weight)
    aspct_m.AspectManager.update_aspect(aspct_m.AspectManager, aspect=aspect)
    result = KPIAspectManagerEndpoints.aspect_to_dict(
        KPIAspectManagerEndpoints, aspect=aspect)
    return fl.jsonify(result), 200


@blueprint.route('/delete_aspect/<aspect_id>', methods=['DELETE', 'OPTIONS'])
def delete_aspect(aspect_id):
    result = {}
    aspect = aspct_m.AspectManager.get_aspect_by_id(
        aspct_m.AspectManager, aspect_id=aspect_id)
    aspct_m.AspectManager.delete_aspect(
        aspct_m.AspectManager, aspect_id=aspect_id)
    result = KPIAspectManagerEndpoints.aspect_to_dict(
        KPIAspectManagerEndpoints, aspect=aspect)
    return fl.jsonify(result), 200


@blueprint.route('/get_aspect/<aspect_id>', methods=['GET', 'OPTIONS'])
def get_aspect(aspect_id):
    result = {}
    aspect = aspct_m.AspectManager.get_aspect_by_id(
        aspct_m.AspectManager, aspect_id=aspect_id)
    if aspect:
        result = KPIAspectManagerEndpoints.aspect_to_dict(
            KPIAspectManagerEndpoints, aspect=aspect)
    else:
        KPIAspectManagerEndpoints(404, "ASPECT_NOT_FOUND")
    return fl.jsonify(result), 200


@blueprint.route('/get_aspects', methods=['GET', 'OPTIONS'])
def get_aspects():
    result = {}
    result['data'] = []
    aspects = aspct_m.AspectManager.get_all_aspects(aspct_m.AspectManager)
    for aspect in aspects:
        result['data'].append(KPIAspectManagerEndpoints.aspect_to_dict(
            KPIAspectManagerEndpoints, aspect=aspect))
    return fl.jsonify(result), 200


@blueprint.route('/get_aspects_by_dataset_label/<dataset_label>', methods=['GET', 'OPTIONS'])
def get_aspects_by_dataset_label(dataset_label):
    result = {}
    result['data'] = []
    aspects = aspct_m.AspectManager.get_all_aspects_by_dataset_label(
        aspct_m.AspectManager, dataset_label=dataset_label)
    for aspect in aspects:
        result['data'].append(KPIAspectManagerEndpoints.aspect_to_dict(
            KPIAspectManagerEndpoints, aspect=aspect))
    return fl.jsonify(result), 200


@blueprint.route('/get_aspect_by_name/<name>', methods=['GET', 'OPTIONS'])
def get_aspect_by_name(name):
    result = {}
    aspect = aspct_m.AspectManager.get_aspect_by_name(
        aspct_m.AspectManager, name=name)
    if aspect:
        result = KPIAspectManagerEndpoints.aspect_to_dict(
            KPIAspectManagerEndpoints, aspect=aspect)
    else:
        KPIAspectManagerEndpoints(404, "ASPECT_NOT_FOUND")
    return fl.jsonify(result), 200


@blueprint.route('/get_all_raw_components/<dataset_id>/<dataset_label>', methods=['GET', 'OPTIONS'])
def get_all_raw_components(dataset_id, dataset_label):
    result = {}
    raw_components = aspct_m.AspectManager.get_raw_components_from_dataset(
        aspct_m.AspectManager, dataset_id=dataset_id, dataset_label=dataset_label)
    result["data"] = raw_components
    return fl.jsonify(result), 200


@blueprint.route('/get_formulas', methods=['GET', 'OPTIONS'])
def get_formulas():
    result = {}
    formulas = fa_m.FormulaManager.get_all_formulas(
        aspct_m.AspectManager)
    result["data"] = formulas
    return fl.jsonify(result), 200


@blueprint.route('/get_aspects_by_kpi_id/<kpi_id>', methods=['GET', 'OPTIONS'])
def get_aspects_by_kpi_id(kpi_id):
    result = {}
    result['data'] = []
    aspects = kpi_m.KPIManager.get_aspects_by_kpi_id(kpi_m.KPIManager, kpi_id)
    for aspect in aspects:
        result['data'].append(KPIAspectManagerEndpoints.aspect_to_dict(
            KPIAspectManagerEndpoints, aspect=aspect))
    return fl.jsonify(result), 200
