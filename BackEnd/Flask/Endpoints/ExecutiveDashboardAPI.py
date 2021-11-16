import flask as fl
import pandas as pd
import DataManager.DataManager as dm
import DataManager.DataSet as ds
import UserManager.UserManager as um
import DataHealthManager.DataHealthManager as dhm
import ExecutiveDashboardManager.ExecutiveDashboardManager as edm
import ExecutiveDashboardManager.ExecutiveDashboard as ed
import Utils.Settings as st
from datetime import datetime


class ExecutiveDashboardEndpoints:

    def executive_dashboard_to_dict(self, executive_dashboard: ed.ExecutiveDashboard):
        dict_formatted = {}
        if executive_dashboard:
            dict_formatted['executive_dashboard_id'] = executive_dashboard.get_executive_dashboardID(
            )
            dict_formatted['name'] = executive_dashboard.get_name()
            dict_formatted['description'] = executive_dashboard.get_description()
            dict_formatted['access_user_list'] = executive_dashboard.get_access_user_list().split(
                ',')
            dict_formatted['access_business_unit_list'] = executive_dashboard.get_access_business_unit_list(
            ).split(',')
            dict_formatted['plots'] = executive_dashboard.get_plots().split(
                ',')
            dict_formatted['dataset'] = executive_dashboard.get_dataset()
            if isinstance(executive_dashboard.get_creation_date(), datetime):
                dict_formatted['creation_date'] = executive_dashboard.get_creation_date().strftime(
                    "%Y/%m/%d, %H:%M:%S")
            elif isinstance(executive_dashboard.get_creation_date(), str):
                dict_formatted['creation_date'] = datetime.strptime(executive_dashboard.get_creation_date(),
                                                                    '%Y-%m-%d %H:%M:%S')
        return dict_formatted

    def endpoints_exception(self, code, msg):
        fl.abort(fl.make_response(fl.jsonify(message=msg), code))


blueprint = fl.Blueprint('ExecutiveDashboard', __name__)


@blueprint.route('/create_executive_dashboard', methods=['POST', 'OPTIONS'])
def post_create_executive_dashboard():
    result = {}
    name = fl.request.form['name']
    description = fl.request.form['description']
    access_user_list = fl.request.form['access_user_list']
    access_business_unit_list = fl.request.form['access_business_unit_list']
    plots = fl.request.form['plots']
    datasets = fl.request.form['dataset']
    owner = fl.request.args.get('uid')
    # Adds to the user_access_list the owner/creator of the dataset by default
    access_user_list_ids = ""
    if access_business_unit_list == "":
        access_business_unit_list = st.DEPARTMENT_GENESIS
    if access_user_list == "":
        access_user_list = owner
    else:
        for user_mail in access_user_list.split(','):
            user = um.UserManager.get_user_by_email(um.UserManager, user_mail)
            access_user_list_ids += user.get_userID() + ","
        access_user_list = access_user_list_ids[:-1]
    if not owner in access_user_list.split(','):
        access_user_list += "," + owner
    executive_dashboard = edm.ExecutiveDashboardManager.create_executive_dashboard(
        edm.ExecutiveDashboardManager, name=name, description=description,
        access_user_list=access_user_list, access_business_unit_list=access_business_unit_list,
        dataset=datasets, plots=plots)
    result = ExecutiveDashboardEndpoints.executive_dashboard_to_dict(
        ExecutiveDashboardEndpoints, executive_dashboard=executive_dashboard)
    return fl.jsonify(result), 200


@blueprint.route('/get_data_for_view/<dataset_id>/<label>/<view_type>/', methods=['GET', 'OPTIONS'])
def get_data_for_view(dataset_id, label, view_type):
    try:
        result = {}
        if view_type in st.STANDARD_VIEW_TYPES:
            result = dhm.DataHealthManager.treemap_ranking_by_applications(
                dhm.DataHealthManager, dataset_id)
        else:
            data, labels = dhm.DataHealthManager.get_data_for_radar_description(
                dhm.DataHealthManager, dataset_id, "test")
            data = [str(val) for val in data]
            result = [{"data": data}, {"labels": labels}]
        if not result:
            ExecutiveDashboardEndpoints(404, "DATASET_NOT_FOUND")
    except:
        print("TODO")
    return fl.jsonify(result), 200


@blueprint.route('/delete_executive_dashboard/<executive_dashboard_id>', methods=['DELETE', 'OPTIONS'])
def delete_executive_dashboard(executive_dashboard_id):
    result = {}
    executive_dashboard = edm.ExecutiveDashboardManager.get_executive_dashboard_by_id(
        edm.ExecutiveDashboardManager, executive_dashboard_id=executive_dashboard_id)
    try:
        edm.ExecutiveDashboardManager.delete_executive_dashboard(
            edm.ExecutiveDashboardManager, executive_dashboard_id=executive_dashboard_id)
    except:
        print('Deleting Executive Dashboard from Executive Dashboard table unsuccessful')
    result = ExecutiveDashboardEndpoints.executive_dashboard_to_dict(
        ExecutiveDashboardEndpoints, executive_dashboard=executive_dashboard)
    return fl.jsonify(result), 200


@blueprint.route('/get_executive_dashboard_by_id/<executive_dashboard_id>', methods=['GET', 'OPTIONS'])
def get_executive_dashboard_by_id(executive_dashboard_id):
    result = {}
    executive_dashboard = edm.ExecutiveDashboardManager.get_executive_dashboard_by_id(
        edm.ExecutiveDashboardManager, executive_dashboard_id=executive_dashboard_id)
    if executive_dashboard:
        result = ExecutiveDashboardEndpoints.executive_dashboard_to_dict(
            ExecutiveDashboardEndpoints, executive_dashboard=executive_dashboard)
    else:
        ExecutiveDashboardEndpoints(404, "EXECUTIVE_DASHBOARD_NOT_FOUND")
    return fl.jsonify(result), 200


@blueprint.route('/get_executive_dashboards', methods=['GET', 'OPTIONS'])
def get_executive_dashboards():
    result = {}
    result['data'] = []
    executive_dashboards = edm.ExecutiveDashboardManager.get_all_executive_dashboards(
        edm.ExecutiveDashboardManager)
    for executive_dashboard in executive_dashboards:
        result['data'].append(ExecutiveDashboardEndpoints.executive_dashboard_to_dict(
            ExecutiveDashboardEndpoints, executive_dashboard=executive_dashboard))
    return fl.jsonify(result), 200
