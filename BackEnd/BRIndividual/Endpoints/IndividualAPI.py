# Project Athena
'''
Owner: Efstratios Pahis
Contributors:
Description: Endpoints for Individualcomponents
'''

import flask as fl
import KPIManager.KPIManager as kpi_m
import BRIndividual.IndividualVisualizationExecutor as vs_exec
import BRIndividual.IndividualGetDataExecutor as gt_dt_exec


class IndividualEndpoints:

    def endpoints_exception(self, code, msg):
        fl.abort(fl.make_response(fl.jsonify(message=msg), code))


blueprint = fl.Blueprint('Individual', __name__)


@blueprint.route('/render_visualizations/<dataset_id>/<dataset_label>/<visualization>', methods=['POST', 'OPTIONS'])
def render_visualizations(dataset_id, dataset_label, visualization):
    results = {}
    formdata = fl.request.form.to_dict(flat=False)
    result = vs_exec.IndividualVisualizationExecutor.execute_visualization(vs_exec.IndividualVisualizationExecutor, formdata=formdata,
                                                                           visualization=visualization, dataset_id=dataset_id,
                                                                           dataset_label=dataset_label)
    results["result"] = result
    return fl.jsonify(results), 200


@blueprint.route('/get_data/<dataset_id>/<dataset_label>/<datatype>', methods=['GET', 'OPTIONS'])
def get_data_apps(dataset_id, dataset_label, datatype):
    result = gt_dt_exec.IndividualGetDataExecutor.execute_get_data_operation(gt_dt_exec.IndividualGetDataExecutor, dataset_id=dataset_id,
                                                                             dataset_label=dataset_label, get_data_operation=datatype)
    return fl.jsonify(result), 200


@blueprint.route('/get_data_special_by_br_hierarchy/<dataset_id>/<dataset_label>/<datatype>/<department>', methods=['GET', 'OPTIONS'])
def get_data_special_by_br_hierarchy(dataset_id, dataset_label, datatype, department):
    result = gt_dt_exec.IndividualGetDataExecutor.execute_get_data_operation(gt_dt_exec.IndividualGetDataExecutor, dataset_id=dataset_id,
                                                                             dataset_label=dataset_label, get_data_operation=datatype, department=department)
    return fl.jsonify(result), 200


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
