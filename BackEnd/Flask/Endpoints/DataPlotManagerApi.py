import flask as fl
import pandas as pd
import UserManager.UserManager as um
import ExecutiveDashboardManager.ExecutiveDashboardManager as edm
import ExecutiveDashboardManager.ExecutiveDashboard as ed
import DataPlotManager.DataPlotManager as dpm
import DataPlotManager.Plot as plt
import Utils.Settings as st
from datetime import datetime


class DataPlotManagerEndpoints:

    def plot_to_dict(self, plot: plt.Plot):
        dict_formatted = {}
        if plot:

            dict_formatted['plot_id'] = plot.get_plotID(
            )
            dict_formatted['title'] = plot.get_title()
            dict_formatted['subtitle'] = plot.get_subtitle()
            dict_formatted['legend_show'] = plot.get_legend_show()
            dict_formatted['dataset_id_for_chart'] = plot.get_dataset_id_for_chart()
            dict_formatted['chart_width'] = plot.get_chart_width()
            dict_formatted['chart_height'] = plot.get_chart_height()
            dict_formatted['dataset_label'] = plot.get_dataset_label()
            dict_formatted['chart_type'] = plot.get_chart_type()
            dict_formatted['xaxis_categories'] = plot.get_xaxis_categories()
            dict_formatted['input_fields'] = plot.get_input_fields()
            dict_formatted['input_fields_id'] = plot.get_input_fields_id()
        return dict_formatted

    def endpoints_exception(self, code, msg):
        fl.abort(fl.make_response(fl.jsonify(message=msg), code))


blueprint = fl.Blueprint('DataPlotManager', __name__)


@blueprint.route('/create_plot/<executive_dashboard_id>', methods=['POST', 'OPTIONS'])
def post_plot(executive_dashboard_id):
    result = {}
    title = fl.request.form['title']
    subtitle = fl.request.form['subtitle']
    legend_show = fl.request.form['legend_show']
    dataset_id_for_chart = fl.request.form['dataset_id_for_chart']
    dataset_label = fl.request.form['dataset_label']
    chart_type = fl.request.form['chart_type']
    chart_width = fl.request.form['chart_width']
    chart_height = fl.request.form['chart_height']
    xaxis_categories = fl.request.form['xaxis_categories']
    input_fields = fl.request.form['input_fields']
    input_fields_id = fl.request.form['input_fields_id']
    plot = dpm.DataPlotManager.create_data_plot(dpm.DataPlotManager, plot_title=title, plot_subtitle=subtitle, plot_legend_show=legend_show,
                                                plot_dataset_id_for_chart=dataset_id_for_chart, plot_dataset_label=dataset_label,
                                                plot_chart_type=chart_type, plot_chart_width=chart_width, plot_chart_height=chart_height,
                                                plot_xaxis_categories=xaxis_categories, plot_input_fields=input_fields, plot_input_fields_id=input_fields_id,
                                                executive_dashboard_id=executive_dashboard_id)
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
    plots = edm.ExecutiveDashboardManager.get_plots_from_executive_dashboard(
        edm.ExecutiveDashboardManager, executive_dashboard_id=executive_dashboard_id)
    for plot in plots:
        result['data'].append(DataPlotManagerEndpoints.plot_to_dict(
            DataPlotManagerEndpoints, plot=plot))
    return fl.jsonify(result), 200
