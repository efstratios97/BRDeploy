import flask as fl
import DataPlotManager.DataPlotManager as dpm
import DataPlotManager.Plot as plt
import json


class DataPlotManagerEndpoints:

    def plot_to_dict(self, plot: plt.Plot):
        dict_formatted = {}
        if plot:
            dict_formatted['plot_id'] = plot.get_plotID(
            )
            dict_formatted['formdata'] = plot.get_formdata()
            dict_formatted['grouped'] = plot.get_grouped()
            dict_formatted['visualization_type'] = plot.get_visualization_type()
            dict_formatted['visualization_right'] = plot.get_visualization_right()
            dict_formatted['component_name'] = plot.get_component_name()
            dict_formatted['separated_display'] = plot.get_separated_display()
            dict_formatted['dataset_id'] = plot.get_dataset_id()
            dict_formatted['dataset_label'] = plot.get_dataset_label()
        return dict_formatted

    def endpoints_exception(self, code, msg):
        fl.abort(fl.make_response(fl.jsonify(message=msg), code))


blueprint = fl.Blueprint('DataPlotManager', __name__)


@blueprint.route('/create_plot/<executive_dashboard_id>', methods=['POST', 'OPTIONS'])
def post_plot(executive_dashboard_id):
    result = {}
    formdata = json.dumps(
        fl.request.form['formdata'], ensure_ascii=False)
    grouped = fl.request.form['grouped']
    visualization_type = fl.request.form['visualization_type']
    visualization_right = fl.request.form['visualization_right']
    component_name = fl.request.form['component_name']
    separated_display = fl.request.form['separated_display']
    plot = dpm.DataPlotManager.create_data_plot(dpm.DataPlotManager, formdata=formdata, grouped=grouped, visualization_type=visualization_type,
                                                visualization_right=visualization_right, component_name=component_name, separated_display=separated_display, executive_dashboard_id=executive_dashboard_id)
    result = DataPlotManagerEndpoints.plot_to_dict(
        DataPlotManagerEndpoints, plot=plot)
    return fl.jsonify(result), 200


@blueprint.route('/get_plot/<plot_id>', methods=['GET', 'OPTIONS'])
def get_plot(plot_id):
    result = {}
    plot = dpm.DataPlotManager.get_plot_by_id(
        dpm.DataPlotManager, plot_id=plot_id)
    if plot:
        result = DataPlotManagerEndpoints.plot_to_dict(
            DataPlotManagerEndpoints, plot=plot)
    else:
        DataPlotManagerEndpoints(404, "PLOT_NOT_FOUND")
    return fl.jsonify(result), 200


@blueprint.route('/get_plots_from_executive_dashboards/<executive_dashboard_id>', methods=['GET', 'OPTIONS'])
def get_plots_from_executive_dashboards(executive_dashboard_id):
    result = {}
    result['data'] = []
    plots = dpm.DataPlotManager.get_plots_from_executive_dashboard(
        dpm.DataPlotManager, executive_dashboard_id=executive_dashboard_id)
    for plot in plots:
        result['data'].append(DataPlotManagerEndpoints.plot_to_dict(
            DataPlotManagerEndpoints, plot=plot))
    return fl.jsonify(result), 200
