import flask as fl
import DataManager.DataManager as dm
import UserManager.UserManager as um
import DataHealthManager.DataHealthManager as dhm
import ExecutiveDashboardManager.ExecutiveDashboardManager as edm
import ExecutiveDashboardManager.ExecutiveDashboard as ed
import ExecutiveDashboardManager.DatsetChoiceRule as dt_ch_rl
import ExecutiveDashboardManager.VisualizationRight as vs_rg
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
            dict_formatted['dataset_id'] = executive_dashboard.get_dataset_id()
            dict_formatted['dataset_label'] = executive_dashboard.get_dataset_label()
            dict_formatted['dataset_choice_rule'] = executive_dashboard.get_dataset_choice_rule(
            )
            dict_formatted['visualization_right'] = executive_dashboard.get_visualization_right(
            )
            if isinstance(executive_dashboard.get_creation_date(), datetime):
                dict_formatted['creation_date'] = executive_dashboard.get_creation_date().strftime(
                    "%Y/%m/%d, %H:%M:%S")
            elif isinstance(executive_dashboard.get_creation_date(), str):
                dict_formatted['creation_date'] = datetime.strptime(executive_dashboard.get_creation_date(),
                                                                    '%Y-%m-%d %H:%M:%S')
        return dict_formatted

    def dataset_choice_rule_to_dict(self, dataset_choice_rule: dt_ch_rl.DatsetChoiceRule):
        dict_formatted = {}
        if dataset_choice_rule:
            dict_formatted['dataset_choice_rule_id'] = dataset_choice_rule.get_dataset_choice_rule_id(
            )
            dict_formatted['name'] = dataset_choice_rule.get_name()
            dict_formatted['description'] = dataset_choice_rule.get_description()
        return dict_formatted

    def visualization_right_to_dict(self, visualization_right: vs_rg.VisualizationRight):
        dict_formatted = {}
        if visualization_right:
            dict_formatted['visualization_right_id'] = visualization_right.get_visualization_right_id(
            )
            dict_formatted['name'] = visualization_right.get_name()
            dict_formatted['description'] = visualization_right.get_description()
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
    dataset_id = fl.request.form['dataset_id']
    dataset_label = fl.request.form['dataset_label']
    dataset_choice_rule = fl.request.form['dataset_choice_rule']
    visualization_right = fl.request.form['visualization_right']
    owner = fl.request.args.get('uid')
    # Adds to the user_access_list the owner/creator of the dataset by default
    access_business_unit_list, access_user_list = st.determine_bu_and_user_access(
        access_business_unit_list=access_business_unit_list, access_user_list=access_user_list, owner=owner)
    executive_dashboard = edm.ExecutiveDashboardManager.create_executive_dashboard(
        edm.ExecutiveDashboardManager, name=name, description=description,
        access_user_list=access_user_list, access_business_unit_list=access_business_unit_list,
        plots=plots, dataset_id=dataset_id, dataset_label=dataset_label,
        dataset_choice_rule=dataset_choice_rule, visualization_right=visualization_right)
    result = ExecutiveDashboardEndpoints.executive_dashboard_to_dict(
        ExecutiveDashboardEndpoints, executive_dashboard=executive_dashboard)
    return fl.jsonify(result), 200


@blueprint.route('/update_executive_dashboard', methods=['POST', 'OPTIONS'])
def update_executive_dashboard():
    result = {}
    executive_dashboard_id = fl.request.form['executive_dashboard_id']
    name = fl.request.form['name']
    description = fl.request.form['description']
    access_user_list = fl.request.form['access_user_list']
    access_business_unit_list = fl.request.form['access_business_unit_list']
    dataset_id = fl.request.form['dataset_id']
    dataset_label = fl.request.form['dataset_label']
    dataset_choice_rule = fl.request.form['dataset_choice_rule']
    owner = fl.request.args.get('uid')
    # Adds to the user_access_list the owner/creator of the dataset by default
    access_business_unit_list, access_user_list = st.determine_bu_and_user_access(
        access_business_unit_list=access_business_unit_list, access_user_list=access_user_list, owner=owner)
    executive_dashboard = edm.ExecutiveDashboardManager.get_executive_dashboard_by_id(
        edm.ExecutiveDashboardManager, executive_dashboard_id=executive_dashboard_id)
    executive_dashboard.set_name(name=name)
    executive_dashboard.set_description(description=description)
    executive_dashboard.set_dataset_id(dataset_id=dataset_id)
    executive_dashboard.set_dataset_label(dataset_label=dataset_label)
    executive_dashboard.set_dataset_choice_rule(
        dataset_choice_rule=dataset_choice_rule)
    executive_dashboard.set_access_business_unit_list(
        access_business_unit_list=access_business_unit_list)
    executive_dashboard.set_access_user_list(access_user_list=access_user_list)
    edm.ExecutiveDashboardManager.update_executive_dashboard(
        edm.ExecutiveDashboardManager, executive_dashboard=executive_dashboard)
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


@blueprint.route('/get_dataset_choice_rules', methods=['GET', 'OPTIONS'])
def get_dataset_choice_rules():
    result = []
    dataset_choice_rules = edm.ExecutiveDashboardManager.get_dataset_choice_rules(
        edm.ExecutiveDashboardManager)
    for dataset_choice_rule in dataset_choice_rules:
        result.append(ExecutiveDashboardEndpoints.dataset_choice_rule_to_dict(
            ExecutiveDashboardEndpoints, dataset_choice_rule=dataset_choice_rule))
    return fl.jsonify(result), 200


@blueprint.route('/get_visualization_rights', methods=['GET', 'OPTIONS'])
def get_visualization_rights():
    result = []
    visualization_rights = edm.ExecutiveDashboardManager.get_visualization_rights(
        edm.ExecutiveDashboardManager)
    for visualization_right in visualization_rights:
        result.append(ExecutiveDashboardEndpoints.visualization_right_to_dict(
            ExecutiveDashboardEndpoints, visualization_right=visualization_right))
    return fl.jsonify(result), 200


@blueprint.route('/get_executive_dashboards_by_user/<user_id>', methods=['GET', 'OPTIONS'])
def get_executive_dashboards_by_user(user_id):
    result = {}
    result['data'] = []
    executive_dashboards = edm.ExecutiveDashboardManager.get_all_executive_dashboards_by_user(
        edm.ExecutiveDashboardManager, user_id=user_id)
    for executive_dashboard in executive_dashboards:
        result['data'].append(ExecutiveDashboardEndpoints.executive_dashboard_to_dict(
            ExecutiveDashboardEndpoints, executive_dashboard=executive_dashboard))
    return fl.jsonify(result), 200
