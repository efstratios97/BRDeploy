# Project Athena
'''
Owner: Efstratios Pahis
Contributors:
Description: Implements main functionality of the KPIManager
'''

import KPIManager.KPIManager as kpi_m
import DataManager.DataManager as dm
import KPIFormulaManager.FormulaManager as fa_m
import KPIFormulaManager.FormulaExecutor as fa_e
import KPIAspectManager.AspectManager as aspct_m
import Utils.Settings as st
import BRIndividual.Utils.SettingsBR as st_br
import BRIndividual.IndividualMethods.GetData as gt_dt
import pandas as pd
import datetime


class KPIVisualizations:

    def render_application_landscape_kpi(self, kpi, parameter, dataset_id, dataset_label):
        threshold = kpi.get_threshold()
        formula = kpi_m.KPIManager.get_suitable_formula(
            kpi_m.KPIManager, kpi_id=kpi.get_KPIID())
        formula = fa_m.FormulaManager.get_formula_by_id(
            fa_m.FormulaManager, formula_id=formula.get_formulaID())
        departments_from_dataset = gt_dt.GetData.get_departments_from_dataset(
            gt_dt.GetData, dataset_id=dataset_id, dataset_label=dataset_label)
        departments_br = gt_dt.GetData.get_departments_by_department_hierarchy_br(
            gt_dt.GetData, department=parameter["department"], dataset_id=dataset_id, dataset_label=dataset_label)
        results = {"label": "Application Landscape of Department: {department}".format(department=parameter["department"]),
                   "fillcolor": "595f5d",
                   "data": []}
        dataset_id = dm.DataManager.check_dataset_exists_and_return_alternative_based_on_label(
            dm.DataManager, dataset_id=dataset_id, dataset_label=dataset_label)
        data = dm.DataManager.get_table_as_df(dm.DataManager, table=dataset_id)
        if not parameter["department"] == "":
            if parameter["department"] == st.ALL_VALUES_INPUT_FIELD:
                for department_br in departments_br:
                    if any(department_br in string for string in departments_from_dataset) or department_br.startswith("HA "):
                        if not any(department_br in string for string in departments_from_dataset):
                            departments_from_dataset.append(department_br)
                        if department_br in list(st_br.departments_bayerischer_rundfunk["Hauptabteilungen"].keys()):
                            haupt_abteilung = self.__find_hauptabteilung_br(
                                KPIVisualizations, dep_br=department_br, departments_from_dataset=departments_from_dataset, data=data, formula=formula, kpi=kpi.get_KPIID(), dataset_id=dataset_id, dataset_label=dataset_label)
                            for abteilung_br in list(st_br.departments_bayerischer_rundfunk["Hauptabteilungen"][department_br]["Abteilungen"].keys()):
                                if any(abteilung_br in string for string in departments_from_dataset):
                                    new_abteilung_br = self.__find_abteilung_br(
                                        KPIVisualizations, dep_br=abteilung_br, departments_from_dataset=departments_from_dataset, data=data, formula=formula, kpi=kpi.get_KPIID(), dataset_id=dataset_id, dataset_label=dataset_label)
                                    if new_abteilung_br != False:
                                        for fg_br in list(st_br.departments_bayerischer_rundfunk["Hauptabteilungen"][department_br]["Abteilungen"][abteilung_br].values())[0]:
                                            if any(fg_br in string for string in departments_from_dataset):
                                                new_fg_br = self.__find_fg_br(
                                                    KPIVisualizations, dep_br=fg_br, departments_from_dataset=departments_from_dataset, data=data, formula=formula, kpi=kpi.get_KPIID(), dataset_id=dataset_id, dataset_label=dataset_label)
                                                if new_fg_br != False:
                                                    new_abteilung_br["data"].append(
                                                        new_fg_br)
                                        haupt_abteilung["data"].append(
                                            new_abteilung_br)
                            results["data"].append(haupt_abteilung)
            elif parameter["department"] == st.NO_ENTRY_INPUT_FIELD:
                department_br = "Undefined"
                results["data"].append(self.__create_json_dep_apps_kpi_app_landscape(
                    KPIVisualizations, dep_br=department_br, department_dataset="", data=data, formula=formula, kpi=kpi.get_KPIID(), dataset_id=dataset_id, dataset_label=dataset_label))
            elif parameter["department"].startswith("HA "):
                department_br = st_br.clean_department_from_dataset(
                    parameter["department"])
                department_dataset = [
                    val for val in departments_from_dataset if parameter["department"] in val][0]
                haupt_abteilung = self.__create_json_dep_apps_kpi_app_landscape(
                    KPIVisualizations, dep_br=department_br, department_dataset=department_dataset, data=data, formula=formula, kpi=kpi.get_KPIID(), dataset_id=dataset_id, dataset_label=dataset_label, fillcolor="#898686")
                try:
                    for abteilung_br in list(st_br.departments_bayerischer_rundfunk["Hauptabteilungen"][department_br]["Abteilungen"].keys()):
                        if any(abteilung_br in string for string in departments_from_dataset):
                            new_abteilung_br = self.__find_abteilung_br(
                                KPIVisualizations, dep_br=abteilung_br, departments_from_dataset=departments_from_dataset, data=data, formula=formula, kpi=kpi.get_KPIID(), dataset_id=dataset_id, dataset_label=dataset_label)
                            if new_abteilung_br != False:
                                for fg_br in list(st_br.departments_bayerischer_rundfunk["Hauptabteilungen"][department_br]["Abteilungen"][abteilung_br].values())[0]:
                                    if any(fg_br in string for string in departments_from_dataset):
                                        new_fg_br = self.__find_fg_br(
                                            KPIVisualizations, dep_br=fg_br, departments_from_dataset=departments_from_dataset, data=data, formula=formula, kpi=kpi.get_KPIID(), dataset_id=dataset_id, dataset_label=dataset_label)
                                        if new_fg_br != False:
                                            new_abteilung_br["data"].append(
                                                new_fg_br)
                    haupt_abteilung["data"].append(
                        new_abteilung_br)
                except:
                    print("only HA available")
                results["data"].append(haupt_abteilung)
            elif parameter["department"].startswith("Abt. "):
                department_br = st_br.clean_department_from_dataset(
                    parameter["department"])
                ha_abteilungen = list(
                    st_br.departments_bayerischer_rundfunk["Hauptabteilungen"].keys())
                current_ha_abteilung = ""
                for ha_abteilung in ha_abteilungen:
                    for abteilung_br in list(st_br.departments_bayerischer_rundfunk["Hauptabteilungen"][ha_abteilung]["Abteilungen"].keys()):
                        if department_br in abteilung_br:
                            current_ha_abteilung = ha_abteilung
                            break
                    if current_ha_abteilung != "":
                        break
                if not "," in parameter["department"]:
                    department_dataset = [
                        val for val in departments_from_dataset if department_br in val and not "," in val and "abt. " in val.lower()][0]
                else:
                    department_dataset = parameter["department"]
                new_abteilung_br = self.__create_json_dep_apps_kpi_app_landscape(
                    KPIVisualizations, dep_br=department_br, department_dataset=department_dataset, data=data, formula=formula, kpi=kpi.get_KPIID(), dataset_id=dataset_id, dataset_label=dataset_label, fillcolor="#9a9999")
                try:
                    for fg_br in list(st_br.departments_bayerischer_rundfunk["Hauptabteilungen"][current_ha_abteilung]["Abteilungen"][department_br].values())[0]:
                        if any(fg_br in string for string in departments_from_dataset):
                            new_fg_br = self.__find_fg_br(
                                KPIVisualizations, dep_br=fg_br, departments_from_dataset=departments_from_dataset, data=data, formula=formula, kpi=kpi.get_KPIID(), dataset_id=dataset_id, dataset_label=dataset_label)
                            if new_fg_br != False:
                                new_abteilung_br["data"].append(
                                    new_fg_br)
                    results["data"].append(new_abteilung_br)
                except:
                    print("somethin wrong")
                    results["data"].append(new_abteilung_br)
            else:
                department_br = st_br.clean_department_from_dataset(
                    parameter["department"])
                all_failed = False
                try:
                    department_dataset = [
                        val for val in departments_from_dataset if parameter["department"] in val and not "," in val][0]
                except:
                    try:
                        department_dataset = [
                            val for val in departments_from_dataset if parameter["department"] in val and "," in val][0]
                    except:
                        department_dataset = ""
                        all_failed = True
                if not all_failed:
                    new_fg_br = self.__create_json_dep_apps_kpi_app_landscape(
                        KPIVisualizations, dep_br=department_br, department_dataset=department_dataset, data=data, formula=formula, kpi=kpi.get_KPIID(), dataset_id=dataset_id, dataset_label=dataset_label)
                    results["data"].append(new_fg_br)
        result = {
            "id": st.create_id(),
            "type": "treemap",
            "width": "100%",
            "height": "550%",
            "dataFormat": "json",
            "dataSource": {
                "chart": {
                    "animation": "0",
                    "hideTitle": "1",
                    "plotToolText": "<div><b>$label</b><br/><b> KPI " + kpi.get_KPI_name() + " : </b>$value</div>",
                    "horizontalPadding": "0",
                    "verticalPadding": "0",
                    "plotborderthickness": ".5",
                    "plotbordercolor": "ffffff",
                    "chartBottomMargin": "0",
                    "labelGlow": "0",
                    "labelFontColor": "ffffff",
                    "showLegend": "1",
                    "legendpadding": "0",
                    "legendItemFontSize": "10",
                    "legendItemFontBold": "1",
                    "legendPointerWidth": "8",
                    "legenditemfontcolor": "3d5c5c",
                    "legendScaleLineThickness": "0",
                    "legendCaptionFontSize": "10",
                    "algorithm": "squarified",
                    "caption": "KPI Landscape " + kpi.get_KPI_name(),
                    "theme": "fusion",
                    "subcaption": "",
                    "showChildLabels": "1",
                    "exportEnabled": "1",
                },
                "data": [results],
                "colorrange": {
                    "mapbypercent": "0",
                    "gradient": "1",
                    "minvalue": "0",
                    "maxvalue": threshold,
                    "code": "6baa01",
                    "startlabel": "Ideal",
                    "endlabel": "Alarming",
                    "color": [
                        {
                            "code": "#ffba00",
                            "minvalue": threshold,
                            "maxvalue": threshold,
                            "label": "Threshold",
                        },
                        {
                            "code": "#cc0000",
                            "minvalue": threshold + 0.5,
                            "maxvalue": "10",
                            "label": "AVERAGE",
                        },
                    ],
                },
            },
        }
        return [result]

    def __find_hauptabteilung_br(self, dep_br, departments_from_dataset,  data, formula, kpi, dataset_id, dataset_label, fillcolor="#898686"):
        try:
            department_dataset = [
                val for val in departments_from_dataset if dep_br in val and not "," in val and "HA " in val][0]
            if len(st_br.clean_department_from_dataset(department_dataset).split(" ")) != len(dep_br.split(" ")):
                department_dataset = [
                    val for val in departments_from_dataset if dep_br in val and not "," in val and "HA " in val and len(st_br.clean_department_from_dataset(val).split(" ")) == len(dep_br.split(" "))][0]
            return self.__create_json_dep_apps_kpi_app_landscape(KPIVisualizations, dep_br=dep_br, department_dataset=department_dataset, data=data, formula=formula, kpi=kpi, dataset_id=dataset_id, dataset_label=dataset_label, fillcolor=fillcolor)
        except:
            print(dep_br + " not in dep from dataset")
            return False

    def __find_abteilung_br(self, dep_br, departments_from_dataset, data, formula, kpi, dataset_id, dataset_label, fillcolor="#9a9999"):
        try:
            department_dataset = [
                val for val in departments_from_dataset if dep_br in val and not "," in val and "abt. " in val.lower()][0]
            if len(st_br.clean_department_from_dataset(department_dataset).split(" ")) != len(dep_br.split(" ")) and not "(SEP)" in dep_br:
                department_dataset = [
                    val for val in departments_from_dataset if dep_br in val and not "," in val and "abt. " in val.lower() and len(st_br.clean_department_from_dataset(val).split(" ")) == len(dep_br.split(" "))][0]
            return self.__create_json_dep_apps_kpi_app_landscape(KPIVisualizations, dep_br=dep_br, department_dataset=department_dataset, data=data, formula=formula, kpi=kpi, dataset_id=dataset_id, dataset_label=dataset_label, fillcolor=fillcolor)
        except:
            print(dep_br + " not in dep from dataset")
            return False

    def __find_fg_br(self, dep_br, departments_from_dataset,  data, formula, kpi, dataset_id, dataset_label, fillcolor="bcbcbc"):
        try:
            department_dataset = [
                val for val in departments_from_dataset if dep_br in val and not "," in val and "fg " in val.lower()][0]
            if len(st_br.clean_department_from_dataset(department_dataset).split(" ")) != len(dep_br.split(" ")):
                department_dataset = [
                    val for val in departments_from_dataset if dep_br in val and not "," in val and "fg " in val.lower() and len(st_br.clean_department_from_dataset(val).split(" ")) == len(dep_br.split(" "))][0]
            return self.__create_json_dep_apps_kpi_app_landscape(KPIVisualizations, dep_br=dep_br, department_dataset=department_dataset, data=data, formula=formula, kpi=kpi, dataset_id=dataset_id, dataset_label=dataset_label, fillcolor=fillcolor)
        except:
            print(dep_br + " not in dep from dataset")
            return False

    def __create_json_dep_apps_kpi_app_landscape(self, dep_br, department_dataset, data, formula, kpi, dataset_id, dataset_label, fillcolor="#bcbcbc"):
        new_dep_br = {"label": dep_br,
                      "fillcolor": fillcolor,
                      "data": []}
        apps = data[data["Verantwortliche Organisationseinheit"]
                    == department_dataset]["Name"].to_list()
        for app in apps:
            val = self.__calc_kpi_value_for_kpi(
                KPIVisualizations, app=app, data=data, formula=formula, kpi=kpi, dataset_id=dataset_id, dataset_label=dataset_label)
            if val == 0.0:
                val = 0.01
            new_dep_br["data"].append(
                {"label": app,
                    "value": val,
                    "sValue": val,
                 }
            )
        return new_dep_br

    def render_app_life_cycle(self, parameter, kpi, dataset_id, dataset_label):
        dataset_id = dm.DataManager.check_dataset_exists_and_return_alternative_based_on_label(
            dm.DataManager, dataset_id=dataset_id, dataset_label=dataset_label)
        data = dm.DataManager.get_table_as_df(dm.DataManager, table=dataset_id)
        formula = kpi_m.KPIManager.get_suitable_formula(
            kpi_m.KPIManager, kpi_id=kpi.get_KPIID())
        formula = fa_m.FormulaManager.get_formula_by_id(
            fa_m.FormulaManager, formula_id=formula.get_formulaID())
        apps_data_set = st_br.get_apps_df_by_parameter(
            parameter=parameter, dataset_data=data, dataset_id=dataset_id, return_apps=False)
        apps_data_set.drop(apps_data_set[(apps_data_set[st_br.life_cycle_end] ==
                           '-') & (apps_data_set[st_br.life_cycle_start] == '-')].index, inplace=True)
        if apps_data_set.empty:
            return {}
        all_apps = apps_data_set["Name"].to_list()
        apps_kpis = [self.__calc_kpi_value_for_kpi(
            KPIVisualizations, app=val, data=data, formula=formula, kpi=kpi.get_KPIID(), dataset_id=dataset_id, dataset_label=dataset_label) for val in all_apps]
        apps_data_set["KPI Value"] = apps_kpis
        apps_data_set.sort_values(
            by=["KPI Value"], ascending=False, inplace=True)
        apps_data_set = apps_data_set.apply(
            lambda x: st_br.date_handler(x), axis=1)
        datatable = {}
        datatable.update({"headervalign": "bottom"})
        app_names = []
        [app_names.append(
            {"label": app}) for app in apps_data_set["Name"]]
        processes = {
            "headertext": "Applications",
            "headervalign": "bottom",
            "headeralign": "left",
            "align": "left",
            "process": app_names}
        kpi_values = []
        [kpi_values.append({"label": str(round(val, 2))})
         for val in apps_data_set["KPI Value"]]
        datacolumn = [
            {
                "headertext": kpi.get_KPI_name(),
                "headervalign": "bottom",
                "headeralign": "left",
                "align": "left",
                "text": kpi_values}]
        datatable.update({"datacolumn": datacolumn})
        tasks = {}
        time_horizons = []
        [time_horizons.append({"start": start, "end": end, "color": color_coding}) for start, end, color_coding in zip(
            apps_data_set[st_br.life_cycle_start], apps_data_set[st_br.life_cycle_end], apps_data_set["color_coding"])]
        tasks.update({"task": time_horizons})
        apps_data_set[st_br.life_cycle_end] = pd.to_datetime(
            apps_data_set[st_br.life_cycle_end], errors='coerce')
        apps_data_set[st_br.life_cycle_end].fillna(datetime.datetime.now().replace(
            year=datetime.datetime.now().year + 10), inplace=True)
        apps_data_set[st_br.life_cycle_end] = apps_data_set[st_br.life_cycle_end].dt.strftime(
            '%d/%m/%Y')
        start_date = max(pd.to_datetime(
            apps_data_set[st_br.life_cycle_start], errors='coerce')).to_pydatetime().strftime(
            '%d/%m/%Y')
        end_date = max(pd.to_datetime(
            apps_data_set[st_br.life_cycle_end], errors='coerce')).to_pydatetime().strftime('%d/%m/%Y')
        category_quarters = st_br.get_quarter_by_time_span_formatted_by_operation(
            start_date=start_date, end_date=end_date, data=apps_data_set, gantt_chart=True)
        category_quarters.append({"start": category_quarters[-1]["end"], "end": end_date,
                                  "label": "LQ " + str(datetime.datetime.strptime(end_date, '%d/%m/%Y').strftime('%Y'))})
        categories = [{"category": [{"start": category_quarters[0]["start"],
                                     "end": end_date, "label": "Application LifeCycle"}]}]
        categories.append({"category": category_quarters})
        kpi_name = kpi.get_KPI_name()
        parameter = st_br.get_parameter_as_string_from_parameter_dict(
            parameter)
        subcaption = parameter + " & " + kpi_name
        height = self.__calc_height_gantt_chart(
            KPIVisualizations, dataset_size=len(apps_data_set))
        result = {
            "id": parameter+kpi_name + st.create_id(),
            "type": "gantt",
            "width": "100%",
            "height": height,
            "dataFormat": "json",
            "dataSource": {
                "chart": {
                    "dateformat": "dd/mm/yyyy",
                    "theme": "fusion",
                    "useverticalscrolling": "0",
                    "caption": "Application Lifecycles",
                    "subcaption": subcaption,
                    "canvasborderalpha": "40",
                    "ganttlinealpha": "50",
                    "exportEnabled": "1",
                },
                "processes": processes,
                "datatable": datatable,
                "tasks": tasks,
                "categories": categories}
        }
        return [result]

    def __calc_height_gantt_chart(self, dataset_size):
        height_basis = 600
        if dataset_size <= 5:
            return 300
        elif dataset_size <= 30:
            return 500
        elif dataset_size <= 75:
            return 1000
        elif dataset_size <= 100:
            return 1500
        elif dataset_size <= 150:
            return 1850
        elif dataset_size > 150:
            return height_basis * (dataset_size/50)

    def render_life_cycle_development(self, parameter, kpi, dataset_id, dataset_label):
        dataset_id = dm.DataManager.check_dataset_exists_and_return_alternative_based_on_label(
            dm.DataManager, dataset_id=dataset_id, dataset_label=dataset_label)
        data = dm.DataManager.get_table_as_df(dm.DataManager, table=dataset_id)
        formula = kpi_m.KPIManager.get_suitable_formula(
            kpi_m.KPIManager, kpi_id=kpi.get_KPIID())
        formula = fa_m.FormulaManager.get_formula_by_id(
            fa_m.FormulaManager, formula_id=formula.get_formulaID())
        apps_data_set = st_br.get_apps_df_by_parameter(
            parameter=parameter, dataset_data=data, dataset_id=dataset_id, return_apps=False)
        apps_data_set.drop(apps_data_set[(apps_data_set[st_br.life_cycle_end] ==
                           '-') & (apps_data_set[st_br.life_cycle_start] == '-')].index, inplace=True)
        if apps_data_set.empty:
            return {}
        apps_data_set = apps_data_set.apply(
            lambda x: st_br.date_handler(x), axis=1)
        apps_data_set[st_br.life_cycle_end] = pd.to_datetime(
            apps_data_set[st_br.life_cycle_end], errors='coerce')
        apps_data_set[st_br.life_cycle_end].fillna(datetime.datetime.now().replace(
            year=datetime.datetime.now().year + 10), inplace=True)
        start_date = max(pd.to_datetime(
            apps_data_set[st_br.life_cycle_start], errors='coerce')).to_pydatetime().strftime(
            '%d/%m/%Y')
        end_date = max(pd.to_datetime(
            apps_data_set[st_br.life_cycle_end], errors='coerce')).to_pydatetime().strftime('%d/%m/%Y')
        kpi_name = kpi.get_KPI_name()
        parameter = st_br.get_parameter_as_string_from_parameter_dict(
            parameter)
        subcaption = parameter + " & " + kpi_name
        return [{
            "id": st.create_id(),
            "type": "line",
            "width": "100%",
            "height": "300",
            "dataFormat": "json",
            "dataSource":
            {
                "chart": {
                    "caption": "Applications Lifecycle Overview",
                    "subcaption": subcaption,
                    "yaxisname": "# of Application to Shut-Down",
                    "anchorradius": "3",
                    "plottooltext": "# App shut-Downs in $label is <b>$dataValue</b>",
                    "showhovereffect": "1",
                    "showvalues": "0",
                    "theme": "fusion",
                    "anchorbgcolor": "#72D7B2",
                    "palettecolors": "#72D7B2",
                    "yAxisMinValue": 0,
                    "exportEnabled": 1,
                },
                "data": st_br.get_quarter_by_time_span_formatted_by_operation(
                    start_date=start_date, end_date=end_date, data=apps_data_set, line_chart=True)
            }
        }]

    def render_kpi(self, parameters, kpi, dataset_id, dataset_label, fast=True):
        results = []
        if fast:
            dataset_id = dm.DataManager.check_dataset_exists_and_return_alternative_based_on_label(
                dm.DataManager, dataset_id=dataset_id, dataset_label=dataset_label)
            data = dm.DataManager.get_table_as_df(
                dm.DataManager, table=dataset_id)
        for param in parameters:
            formula = kpi_m.KPIManager.get_suitable_formula(
                kpi_m.KPIManager, kpi_id=kpi.get_KPIID())
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
                operation=formula_operation, purpose=formula.get_purpose(), kpi_id=kpi.get_KPIID(),
                dataset_id=dataset_id, dataset_label=dataset_label, parameter=parameter, dataset_data=data, fast=fast)
            if result["color_coding"] == "the Higher the Better":
                color_coding = [
                    {
                        "minValue": "0",
                        "maxValue": result["threshold"] - 0.5,
                        "code": "#cc0000",
                    },
                    {
                        "minValue": result["threshold"] - 0.5,
                        "maxValue": result["threshold"] + 0.5,
                        "code": "#ffba00",
                    },
                    {
                        "minValue": result["threshold"] + 0.5,
                        "maxValue": "10",
                        "code": "#6baa01",
                    },
                ]
            else:
                color_coding = [
                    {
                        "minValue": "0",
                        "maxValue":  result["threshold"] - 0.5,
                        "code": "#6baa01",
                    },
                    {
                        "minValue":  result["threshold"] - 0.5,
                        "maxValue":  result["threshold"] + 0.5,
                        "code": "#ffba00",
                    },
                    {
                        "minValue":  result["threshold"] + 0.5,
                        "maxValue": "10",
                        "code": "#cc0000",
                    },
                ]
            result_fusion = {
                "id":  st.create_id(),
                "type": "angulargauge",
                "width": "616",
                "height": "300",
                "dataFormat": "json",
                "dataSource": {
                        "chart": {
                            "plotToolText": "Current Score: $value",
                            "theme": "fusion",
                            "caption": st_br.get_parameter_as_string_from_parameter_dict(parameter),
                            "subcaption": "KPI Analysis",
                            "lowerLimit": "0",
                            "upperLimit": "10",
                            "chartBottomMargin": "40",
                            "valueFontSize": "11",
                            "valueFontBold": "1",
                            "valueFontColor": "#000000",
                            "baseFontSize": 15,
                            "exportEnabled": "1",
                            "showValue": "1",
                        },
                    "colorRange": {
                            "color": color_coding,
                            },
                    "dials": {
                            "dial": [
                                {
                                    "value": result["result"],
                                    "showValue": 1,
                                },
                            ],
                            },
                    "trendpoints": {
                            "point": [
                                {
                                    "startValue": result["threshold"],
                                    "displayValue": "Threshold: " + str(result["threshold"]),
                                    "color": "#0075c2",
                                    "thickness": "2",
                                    "radius": "180",
                                    "innerRadius": "82",
                                    "alpha": "100",
                                    "valueInside": "1",
                                    "dashed": "0",
                                    "dashLen": "2",
                                    "dashGap": "1",
                                    "trendValueDistance": "3",
                                    "useMarker": "1",
                                    "markerColor": "#F1f1f1",
                                    "markerBorderColor": "#666666",
                                    "markerRadius": "10",
                                    "markerTooltext": "Threshold: " + str(result["threshold"]),
                                },
                            ],
                            },
                }
            }
            results.append(result_fusion)
        return results

    def __calc_kpi_value_for_kpi(self, app, data, formula, kpi, dataset_id, dataset_label):
        return fa_e.FormulaExecutor.execute_formula(
            operation=formula.get_operation(), purpose=formula.get_purpose(), kpi_id=kpi,
            dataset_id=dataset_id, dataset_label=dataset_label, parameter={"app": app, "department": "", "domain": ""}, fast=True, dataset_data=data)["result"]

    def render_aspects(self, parameters, aspects, dataset_id, dataset_label, fast=True, subcaption="Aspect Analysis"):
        results = []
        if fast:
            dataset_id = dm.DataManager.check_dataset_exists_and_return_alternative_based_on_label(
                dm.DataManager, dataset_id=dataset_id, dataset_label=dataset_label)
            dataset_data = dm.DataManager.get_table_as_df(
                dm.DataManager, table=dataset_id)
        for param in parameters:
            data = []
            scales = []
            res_to_add_data = []
            for aspect_dict in aspects:
                aspect = aspct_m.AspectManager.get_aspect_by_id(
                    aspct_m.AspectManager, aspect_id=aspect_dict['aspect']['aspect_id'])
                formula = aspct_m.AspectManager.get_suitable_formula(
                    aspct_m.AspectManager, aspect_id=aspect.get_aspectID())
                formula = fa_m.FormulaManager.get_formula_by_id(
                    fa_m.FormulaManager, formula_id=formula.get_formulaID())
                formula_operation = formula.get_operation()
                parameter = ""
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
                    operation=formula_operation, purpose=formula.get_purpose(), aspect_id=aspect.get_aspectID(),
                    dataset_id=dataset_id, dataset_label=dataset_label, parameter=parameter, dataset_data=dataset_data, fast=fast)
                scales.append(result["scale"])
                if result == False:
                    return result
                res_to_add_data.append(
                    {"result": result["result"], "aspect_name": aspect.get_name(), "scale": str(result["scale"])})
            for data_to_add in res_to_add_data:
                if len(set(scales)) > 1:
                    data.append({"label": data_to_add["aspect_name"] + " with max score: " + data_to_add["scale"],
                                 "value": data_to_add["result"]})
                else:
                    data.append({"label": data_to_add["aspect_name"],
                                 "value": data_to_add["result"]})
            result = {
                "id":  st.create_id(),
                "type": "column2d",
                "width": "616",
                "height": "300",
                "dataFormat": "json",
                "dataSource": {
                        "chart": {
                            "caption": st_br.get_parameter_as_string_from_parameter_dict(parameter),
                            "subCaption": subcaption,
                            "xAxisName": "Aspect",
                            "yAxisName": "Score",
                            "numberSuffix": "",
                            "theme": "fusion",
                            "yAxisMaxValue": max(scales),
                            "yAxisMinValue": "0",
                            "exportEnabled": "1",
                        },
                    "data": data,
                },
            }
            results.append(result)
        return results
