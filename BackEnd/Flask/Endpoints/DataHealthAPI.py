import flask as fl
import pandas as pd
import DataManager.DataManager as dm
import DataManager.DataSet as ds
import UserManager.UserManager as um
import DataHealthManager.DataHealthManager as dhm
import Utils.Settings as st


class DataHealthManagerEndpoints:

    def endpoints_exception(self, code, msg):
        fl.abort(fl.make_response(fl.jsonify(message=msg), code))


blueprint = fl.Blueprint('DataHealthManager', __name__)


@blueprint.route('/get_data_for_view/<dataset_id>/<label>/<view_type>/<app_name>', methods=['GET', 'OPTIONS'])
def get_data_for_view(dataset_id, label, view_type, app_name):
    result = {}
    exists = dm.DataManager.check_dataset_exists(
        dm.DataManager, dataset_id=dataset_id, local=False)
    if not exists:
        dataset = dm.DataManager.get_newest_dataset_replacement_by_dataset_label(
            dm.DataManager, dataset_label=label)
        dataset_id = dataset.get_datasetID()
    if view_type in st.STANDARD_VIEW_TYPES:
        result = dhm.DataHealthManager.count_applications_by_department(
            dhm.DataHealthManager, dataset_id)
    else:
        data, labels = dhm.DataHealthManager.get_data_for_radar_description(
            dhm.DataHealthManager, dataset_id, app_name)
        data = [str(val) for val in data]
        result = [{"data": data}, {"labels": labels}]
    if not result:
        DataHealthManagerEndpoints(404, "DATASET_NOT_FOUND")
    return fl.jsonify(result), 200


@blueprint.route('/get_data_for_app_dep_ranking/<dataset_id>', methods=['GET', 'OPTIONS'])
def get_data_for_app_dep_ranking(dataset_id):
    result = {}
    result = dhm.DataHealthManager.count_applications_by_department(
        dhm.DataHealthManager, dataset_id)
    if not result:
        DataHealthManagerEndpoints(404, "DATASET_NOT_FOUND")
    return fl.jsonify(result), 200


@blueprint.route('/get_applications/<dataset_id>', methods=['GET', 'OPTIONS'])
def get_applications(dataset_id):
    result = {}
    result = dhm.DataHealthManager.get_applications(
        dhm.DataHealthManager, dataset_id)
    if not result:
        DataHealthManagerEndpoints(404, "APPLICATIONS_NOT_FOUND")
    return fl.jsonify(result), 200


@blueprint.route('/get_data_for_radar_app/<dataset_id>/<app_name>', methods=['GET', 'OPTIONS'])
def get_data_for_radar_app(dataset_id, app_name):
    result = {}
    data, labels = dhm.DataHealthManager.get_data_for_radar_description(
        dhm.DataHealthManager, dataset_id, app_name)
    data = [str(val) for val in data]
    result = [{"data": data}, {"labels": labels}]
    if not result:
        DataHealthManagerEndpoints(404, "DATASET_NOT_FOUND")
    return fl.jsonify(result), 200
