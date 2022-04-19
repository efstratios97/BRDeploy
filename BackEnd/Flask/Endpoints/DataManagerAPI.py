# Project Athena
'''
Owner: Efstratios Pahis
Contributors:
Description: Endpoints for DataManager
'''

import flask as fl
import pandas as pd
import DataManager.DataManager as dm
import DataManager.DataSet as ds
import DataManager.Label as lab
import UserManager.UserManager as um
import Utils.Settings as st
from datetime import datetime
import pytz


class DataManagerEndpoints:

    def endpoints_exception(self, code, msg):
        fl.abort(fl.make_response(fl.jsonify(message=msg), code))

    def data_set_to_dict(self, dataset: ds.DataSet, data_path=''):
        dict_formatted = {}
        if dataset:
            dict_formatted['dataset_id'] = dataset.get_datasetID()
            dict_formatted['name'] = dataset.get_name()
            dict_formatted['owner'] = dataset.get_owner()
            dict_formatted['size'] = str(
                dataset.get_size())
            dict_formatted['hash_of_dataset'] = dataset.get_hash_of_dataset()
            dict_formatted['cleaned'] = dataset.get_cleaned()
            dict_formatted['access_user_list'] = dataset.get_access_user_list().split(
                ',')
            dict_formatted['access_business_unit_list'] = dataset.get_access_business_unit_list(
            ).split(',')
            dict_formatted['description'] = dataset.get_description()
            dict_formatted['data'] = data_path
            dict_formatted['storage_type'] = dataset.get_storage_type()
            dict_formatted['label'] = dataset.get_label()
            GMT = pytz.timezone("UTC")
            if isinstance(dataset.get_creation_date(), datetime):
                dict_formatted['creation_date'] = dataset.get_creation_date().astimezone(GMT).strftime(
                    "%d %b %Y %H:%M:%S GMT")
            elif isinstance(dataset.get_creation_date(), str):
                dict_formatted['creation_date'] = datetime.strptime(dataset.get_creation_date().astimezone(GMT),
                                                                    '%Y-%m-%d %H:%M:%S')
        return dict_formatted

    def label_to_dict(self, label: lab):
        dict_formatted = {}
        if label:
            dict_formatted['label_id'] = label.get_labelID()
            dict_formatted['name'] = label.get_name()
            dict_formatted['header_list'] = st.make_str_to_list(
                label.get_header_list())
            dict_formatted['operation_list'] = st.make_str_to_list(
                label.get_operation_list())
        return dict_formatted


blueprint = fl.Blueprint('DataManager', __name__)


@blueprint.route('/create_dataset', methods=['POST', 'OPTIONS'])
def post_dataset():
    result = {}
    data = fl.request.files['file']
    name = fl.request.form['name']
    cleaned = fl.request.form['cleaned']
    access_user_list = fl.request.form['access_user_list']
    access_business_unit_list = fl.request.form['access_business_unit_list']
    description = fl.request.form['description']
    storage_type = fl.request.form['storage_type']
    owner = fl.request.args.get('uid')
    if data.filename.lower()[-3:] == 'csv':
        data = pd.read_csv(data)
    elif data.filename.lower()[-4:] == 'xlsx' or data.filename.lower()[-3:] == 'xls':
        data = pd.read_excel(data, engine='openpyxl')
    # Adds to the user_access_list the owner/creator of the dataset by default
    access_business_unit_list, access_user_list = st.determine_bu_and_user_access(
        access_business_unit_list=access_business_unit_list,
        access_user_list=access_user_list, owner=owner)
    dataset = dm.DataManager.create_data_set(dm.DataManager, name=name, owner=owner, data=data, cleaned=cleaned,
                                             access_user_list=access_user_list, access_business_unit_list=access_business_unit_list,
                                             description=description, storage_type=storage_type)
    result.update({"cleaned_dataset": DataManagerEndpoints.data_set_to_dict(
        DataManagerEndpoints, dataset=dataset)})
    return fl.jsonify(result), 200


@blueprint.route('/update_dataset', methods=['POST', 'OPTIONS'])
def update_dataset():
    result = {}
    dataset_id = fl.request.form['dataset_id']
    name = fl.request.form['name']
    cleaned = fl.request.form['cleaned']
    access_user_list = fl.request.form['access_user_list']
    access_business_unit_list = fl.request.form['access_business_unit_list']
    description = fl.request.form['description']
    owner = fl.request.args.get('uid')
    access_business_unit_list, access_user_list = st.determine_bu_and_user_access(
        access_business_unit_list=access_business_unit_list,
        access_user_list=access_user_list, owner=owner)
    dataset = dm.DataManager.get_dataset_by_id(
        dm.DataManager, dataset_id=dataset_id, local=False)
    # Set the new values/changes in the dataset object
    dataset.set_name(name=name)
    dataset.set_description(description=description)
    dataset.set_cleaned(cleaned=cleaned)
    dataset.set_access_business_unit_list(
        access_business_unit_list=access_business_unit_list)
    dataset.set_access_user_list(access_user_list=access_user_list)
    dm.DataManager.update_dataset(
        dm.DataManager, dataset=dataset, local=False)
    result = DataManagerEndpoints.data_set_to_dict(
        DataManagerEndpoints, dataset=dataset)
    return fl.jsonify(result), 200


@blueprint.route('/delete_dataset/<dataset_id>/<storage_type>', methods=['DELETE', 'OPTIONS'])
def delete_dataset(dataset_id, storage_type):
    result = {}
    local = st.enum_storage_type_bool(
        storage_type=storage_type)
    dataset = dm.DataManager.get_dataset_by_id(
        dm.DataManager, dataset_id=dataset_id, local=local)
    try:
        dm.DataManager.delete_dataset(
            dm.DataManager, dataset_id=dataset_id, local=local)
    except:
        print('Deleting Dataset from Dataset table unsuccessful')
    try:
        dm.DataManager.drop_dataset_table(
            dm.DataManager, dataset_id=dataset_id, local=local)
    except:
        print('Droping Dataset data table unsuccessful')
    result = DataManagerEndpoints.data_set_to_dict(
        DataManagerEndpoints, dataset=dataset)
    return fl.jsonify(result), 200


@blueprint.route('/get_dataset/<dataset_id>', methods=['GET', 'OPTIONS'])
def get_dataset(dataset_id):
    result = {}
    dataset_id = dm.DataManager.check_dataset_exists_and_return_alternative_based_on_label(
        dm.DataManager, dataset_id=dataset_id)
    dataset = dm.DataManager.get_dataset_by_id(
        dm.DataManager, dataset_id=dataset_id, local=False)
    if dataset:
        result = DataManagerEndpoints.data_set_to_dict(
            DataManagerEndpoints, dataset=dataset)
    else:
        DataManagerEndpoints.endpoints_exception(
            DataManagerEndpoints, 404, "DATASET_NOT_FOUND")
    return fl.jsonify(result), 200


@blueprint.route('/get_datasets/<user_id>', methods=['GET', 'OPTIONS'])
def get_datasets(user_id):
    result = {}
    result['data'] = []
    try:
        datasets = dm.DataManager.get_all_datasets(
            dm.DataManager, user_id=user_id)
    except:
        datasets = dm.DataManager.get_all_datasets(
            dm.DataManager, user_id=user_id)
    for dataset in datasets:
        result['data'].append(DataManagerEndpoints.data_set_to_dict(
            DataManagerEndpoints, dataset=dataset))
    return fl.jsonify(result), 200


@blueprint.route('/get_datasets_only_id/<user_id>', methods=['GET', 'OPTIONS'])
def get_datasets_only_id(user_id):
    result = {}
    result['data'] = []
    dataset_ids = dm.DataManager.get_all_datasets_only_id(
        dm.DataManager, user_id=user_id)
    result['data'] = dataset_ids
    return fl.jsonify(result), 200


@blueprint.route('/get_datasets_only_name/<user_id>', methods=['GET', 'OPTIONS'])
def get_datasets_only_name(user_id):
    result = {}
    result['data'] = []
    dataset_ids = dm.DataManager.get_all_datasets_only_name(
        dm.DataManager, user_id=user_id)
    result['data'] = dataset_ids
    return fl.jsonify(result), 200


@blueprint.route('/get_dataset_df/<dataset_id>/<storage_type>', methods=['GET', 'OPTIONS'])
def get_table_df(dataset_id, storage_type):
    result = dm.DataManager.get_table_as_df(
        dm.DataManager, table=dataset_id, local=st.
        enum_storage_type_bool(storage_type=storage_type)).to_json()
    return fl.jsonify(result), 200


@blueprint.route('/assign_label/<dataset_id>/<label>', methods=['POST', 'OPTIONS'])
def assign_label_to_dataset(dataset_id, label):
    result = {}
    dataset = dm.DataManager.get_dataset_by_id(
        dm.DataManager, dataset_id=dataset_id, local=False)
    dm.DataManager.create_label(
        dm.DataManager, name=label, header_list=dataset.get_data().columns.values.tolist())
    dm.DataManager.update_dataset_label(
        dm.DataManager, label=label, dataset_id=dataset_id, local=False)
    return fl.jsonify(result), 200


@blueprint.route('/get_all_labels', methods=['GET', 'OPTIONS'])
def get_labels():
    result = []
    labels = dm.DataManager.get_all_labels(
        dm.DataManager)
    for label in labels:
        result.append(DataManagerEndpoints.label_to_dict(
            DataManagerEndpoints, label=label))
    return fl.jsonify(result), 200


@blueprint.route('/get_label_by_name/<name>', methods=['GET', 'OPTIONS'])
def get_label_by_name(name):
    result = []
    label = dm.DataManager.get_label_by_name(
        dm.DataManager, name=name)
    result.append(DataManagerEndpoints.label_to_dict(
        DataManagerEndpoints, label=label))
    return fl.jsonify(result), 200


@blueprint.route('/get_label_by_id/<label_id>', methods=['GET', 'OPTIONS'])
def get_label_by_id(label_id):
    result = []
    label = dm.DataManager.get_label_by_id(
        dm.DataManager, label_id=label_id)
    result.append(DataManagerEndpoints.label_to_dict(
        DataManagerEndpoints, label=label))
    return fl.jsonify(result), 200


@blueprint.route('/get_newest_dataset_replacement_by_dataset_label/<name>', methods=['GET', 'OPTIONS'])
def get_newest_dataset_replacement_by_dataset_label(name):
    result = {}
    dataset = dm.DataManager.get_newest_dataset_replacement_by_dataset_label(
        dm.DataManager, dataset_label=name)
    result = DataManagerEndpoints.data_set_to_dict(
        DataManagerEndpoints, dataset=dataset)
    return fl.jsonify(result), 200
