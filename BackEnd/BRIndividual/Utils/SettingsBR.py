# Project Athena
'''
Owner: Efstratios Pahis
Contributors:
Description: Various Helpermethods and Attributes specicific to Bayerischer Rundfunk
'''

import re
import numpy as np
import DataManager.DataManager as dm
import Utils.Settings as st
import datetime
import pandas as pd
import ast
import BRIndividual.IndividualMethods.GetData as gt_dt

life_cycle_start = "Datum Produktivsetzung"
life_cycle_end = "Datum Abschaltung"
responsible_unit = "Verantwortliche Organisationseinheit"

departments_bayerischer_rundfunk = {"Hauptabteilungen": {
    "HA IT und Medientechnik": {"Abteilungen": {"IT-Basis und Infrastruktur": {"Fachgruppen": ["Server und Basisdienste", "Hardware und Datenspeicherung", "Netwerk und Systemsicherheit", "Enterprise Workplace Solutions", "Energieanlagetechnik", "Asset & Configuration Management"]},
                                                "Mediensysteme": {"Fachgruppen": ["Außentechnik", "FS-Studios und Systeme", "Zentrale AV-Technik", "Trimediale Studios und Systeme", "Zentrale Mediensysteme", "Regionale Studios und Systeme", "Redaktionssysteme"]},
                                                "Businesssysteme und -lösungen": {"Fachgruppen": ["Planungs- und Standardapplikationen", "Businessapplikationen", "IT Solutions"]},
                                                "Planung Infrastrukturtechnologie": {"Fachgruppen": ["Planung Verbreitungstechnik"]}
                                                }},
    "HA Programmdirektion Information": {"Abteilungen": {"Softwareentwicklung und Plattformen (SEP)": {"Fachgruppen": []},
                                                         }},
    "HA Produktionsservice": {"Abteilungen": {"Veranstaltungsservice": {"Fachgruppen": ["Veranstaltungstechnik", "Veranstaltungssicherheit", "Ausstattungsservice"]},
                                              "Kamera": {"Fachgruppen": ["Kamera 1", "Kamera 2"]},
                                              "Audio/Video Engineering": {"Fachgruppen": ["Audio Engineering", "Video Engineering"]},
                                              "Design - und Editingservice": {"Fachgruppen": ["Video- und Grafikdesign", "Editing", "Sounddesign"]},
                                              "Audio/Video Operating": {"Fachgruppen": ["Audio Operating", "Video Operating", "Multimedia Operating"]}
                                              }},
    "HA Verbreitung und Controlling": {"Abteilungen": {"Controlling": {"Fachgruppen": ["Produktionswirtschaft", "Technisches Controlling und Haushalt"]},
                                                       "Senderbetrieb": {"Fachgruppen": ["Betrieb Terrestrik", "Infrastruktur Senderstandorte"]},
                                                       "Entwicklung Programmverbreitung": {"Fachgruppen": ["Systementwicklung"]},
                                                       "Rundfunkversorgung u. Frequenzmanagement": {"Fachgruppen": ["Rundfunkvertriebssysteme", "Rechnertechnik", "Neue Übertragungstechniken"]},
                                                       "Zentrale Betriebstechnik": {"Fachgruppen": ["Internetverbreitung und Multiplexing", "Netzmanagement", "Leitungsnetze und Richtfunk"]}
                                                       }},
    "HA Personal": {"Abteilungen": {"Kein Eintrag": {"Fachgruppen": []}}},
    "HA Planung": {"Abteilungen": {"Investitionsstrategie": {"Fachgruppen": ["Projektportfoliomanagement"]},
                                   "Planung Produktionstechnologie": {"Fachgruppen": ["Planung Zentrale Broadcastsysteme", "Planung Produktionstechnick"]},
                                   "Planung Systemtechnologie": {"Fachgruppen": ["Enterprise Architecture Management"]},
                                   "Planung Infrastrukturtechnologie": {"Fachgruppen": ["Planung Verbreitungstechnik"]}
                                   }},
    "HA Produktionstechnologie": {"Abteilungen": {"Produktionszentren": {"Fachgruppen": ["MCR / SAW", "Wellenhaus", "Aktualitätenzentrum", "Sendeleitung"]},
                                                  "Audio/Video Editing Infrastruktur": {"Fachgruppen": ["A/V Schnittsysteme", "Grafiksysteme"]},
                                                  "Studios und Mobile Produktion": {"Fachgruppen": ["Studios", "Mobile Produktion", "Materialmanagement"]},
                                                  "Dezentrale Produktionsstandorte": {"Fachgruppen": ["Regionen und Ausland", "Produktionsservice Franken"]}
                                                  }},
}}


def clean_department_from_dataset(department: str):
    return "".join(re.findall(r"(.*?)(?:\(.*?\)|$)", department.replace("Abt. ", "").replace("FG ", "").replace(" (Organisationseinheit)", ""))).rstrip()


def get_departments_bayerischer_rundfunk_list():
    list_tmp = list(__get_departments_bayerischer_rundfunk_list_helper(
        departments_bayerischer_rundfunk))
    return [val for val in ([item for sublist in list_tmp for item in sublist if isinstance(sublist, list)] + [val for val in list_tmp if isinstance(val, str)]) if not val == "Hauptabteilungen" and not val == "Abteilungen" and not val == "Fachgruppen"]


def __get_departments_bayerischer_rundfunk_list_helper(_dict):
    for k, v in _dict.items():
        yield k
        if isinstance(v, dict):
            yield from __get_departments_bayerischer_rundfunk_list_helper(v)
        else:
            yield v


def get_apps_df_by_parameter(parameter, dataset_data, dataset_id, return_apps=True):
    app = parameter["app"]
    department = parameter["department"]
    domain = parameter["domain"]
    if not app == "":
        parameter = app
        dataset_data_app = dataset_data.copy()
        departments = gt_dt.GetData.get_departments_by_department_hierarchy_br(
            gt_dt.GetData, department=department, dataset_id=dataset_id)
        dataset_data_app[responsible_unit] = dataset_data[responsible_unit].apply(
            lambda x: x if x in departments else np.NaN)
        dataset_data_app.dropna(inplace=True, subset=[
            responsible_unit])
        if return_apps:
            apps = [app]
        else:
            apps = dataset_data_app
    if not department == "":
        parameter = department
        if not department == st.ALL_VALUES_INPUT_FIELD:
            if department == st.NO_ENTRY_INPUT_FIELD:
                department = ""
            departments = gt_dt.GetData.get_departments_by_department_hierarchy_br(
                gt_dt.GetData, department=department, dataset_id=dataset_id)
            dataset_data_dep = dataset_data.copy()
            dataset_data_dep[responsible_unit] = dataset_data[responsible_unit].apply(
                lambda x: x if x in departments else np.NaN)
            dataset_data_dep.dropna(inplace=True, subset=[
                                    responsible_unit])
            if return_apps:
                apps = dataset_data_dep["Name"].to_list()
            else:
                apps = dataset_data_dep
        else:
            if return_apps:
                apps = dataset_data["Name"].to_list()
            else:
                apps = dataset_data
    if not domain == "":
        parameter = domain
        dataset_data_domain = dataset_data.copy()
        dataset_data_domain["Zugeordnete Domäne"] = dataset_data["Zugeordnete Domäne"].apply(
            lambda x: x if domain in x else np.NaN)
        dataset_data_domain.dropna(inplace=True, subset=[
            'Zugeordnete Domäne'])
        if return_apps:
            apps = dataset_data_domain["Name"].to_list()
        else:
            apps = dataset_data_domain
    return apps


def get_parameters_from_input(parameters):
    for param in parameters:
        if isinstance(param, str):
            param = ast.literal_eval(param)
        if "dep" in list(param.keys()):
            parameter = {"app": "",
                         "department": param["dep"], "domain": ""}
        if "app" in list(param.keys()):
            parameter = {"app": param['app'],
                         "department": "", "domain": ""}
        if "domain" in list(param.keys()):
            parameter = {"app": "",
                         "department": "", "domain": param['domain']}
    return parameter


def get_parameter_as_string_from_parameter_dict(parameter):
    if not parameter["department"] == "":
        return parameter["department"]
    elif not parameter["app"] == "":
        return parameter["app"]
    elif not parameter["domain"] == "":
        return parameter["domain"]
    else:
        return "Undefined"


def date_handler(x):
    def date_color_coding(x):
        if x[life_cycle_end].year <= datetime.datetime.now().year + 2:
            x["color_coding"] = "#cc0000"
        elif x[life_cycle_end].year < datetime.datetime.now().year + 5:
            x["color_coding"] = "#ffba00"
        else:
            x["color_coding"] = "#6baa01"
        return x

    def datetime_to_string(x):
        date_color_coding(x)
        x[life_cycle_start] = x[life_cycle_start].strftime(
            '%d/%m/%Y')
        x[life_cycle_end] = x[life_cycle_end].strftime(
            '%d/%m/%Y')
        return x
    if not x[life_cycle_start] == "-" and not x[life_cycle_end] == "-":
        x[life_cycle_start] = datetime.datetime.strptime(
            x[life_cycle_start], '%Y-%m-%d %H:%M:%S')
        x[life_cycle_end] = datetime.datetime.strptime(
            x[life_cycle_end], '%Y-%m-%d %H:%M:%S')
        return datetime_to_string(x)
    if not x[life_cycle_start] == "-" and x[life_cycle_end] == "-":
        x[life_cycle_start] = datetime.datetime.strptime(
            x[life_cycle_start], '%Y-%m-%d %H:%M:%S')
        if x[life_cycle_start] <= datetime.datetime.now().replace(year=datetime.datetime.now().year - 5):
            x[life_cycle_end] = x[life_cycle_start].replace(
                year=datetime.datetime.now().year + 5)
        else:
            x[life_cycle_end] = datetime.datetime.now().replace(
                year=x[life_cycle_start].year + 5)
        return datetime_to_string(x)
    if not x[life_cycle_end] == "-" and x[life_cycle_start] == "-":
        x[life_cycle_end] = datetime.datetime.strptime(
            x[life_cycle_end], '%Y-%m-%d %H:%M:%S')
        if x[life_cycle_end] >= datetime.datetime.now().replace(year=datetime.datetime.now().year + 5):
            x[life_cycle_start] = datetime.datetime.now()
        else:
            x[life_cycle_start] = x[life_cycle_end].replace(
                year=x[life_cycle_end].year - 5)


def get_quarter_by_time_span_formatted_by_operation(start_date, end_date, data, gantt_chart=False, line_chart=False, format='%d/%m/%Y'):
    category_quarters = []
    end_date = datetime.datetime.strptime(
        end_date, '%d/%m/%Y').replace(year=datetime.datetime.strptime(
            end_date, '%d/%m/%Y').year + 1, month=3).strftime('%d/%m/%Y')
    quarters_list = [val.to_pydatetime().strftime('%d/%m/%Y')
                     for val in pd.date_range(start_date, end_date, freq='Q')]
    for quarter in quarters_list:
        if "/03/" in quarter:
            if gantt_chart:
                category_quarters = __operation_gantt_chart(
                    category_quarters=category_quarters, quarter=quarter, label=("Q1 " + str(datetime.datetime.strptime(quarter, format).strftime('%Y'))), day=1, month=1)
            elif line_chart:
                category_quarters = __operation_line_chart(
                    category_quarters=category_quarters, quarter=quarter, label=("Q1 " + str(datetime.datetime.strptime(quarter, format).strftime('%Y'))), day=1, month=1, data=data)
        elif "/06/" in quarter:
            if gantt_chart:
                category_quarters = __operation_gantt_chart(
                    category_quarters=category_quarters, quarter=quarter, label=("Q2 " + str(datetime.datetime.strptime(quarter, format).strftime('%Y'))), day=1, month=4)
            elif line_chart:
                category_quarters = __operation_line_chart(
                    category_quarters=category_quarters, quarter=quarter, label=("Q2 " + str(datetime.datetime.strptime(quarter, format).strftime('%Y'))), day=1, month=4, data=data)
        elif "/09/" in quarter:
            if gantt_chart:
                category_quarters = __operation_gantt_chart(
                    category_quarters=category_quarters, quarter=quarter, label=("Q3 " + str(datetime.datetime.strptime(quarter, format).strftime('%Y'))), day=1, month=7)
            elif line_chart:
                category_quarters = __operation_line_chart(
                    category_quarters=category_quarters, quarter=quarter, label=("Q3 " + str(datetime.datetime.strptime(quarter, format).strftime('%Y'))), day=1, month=7, data=data)
        elif "/12/" in quarter:
            if gantt_chart:
                category_quarters = __operation_gantt_chart(
                    category_quarters=category_quarters, quarter=quarter, label=("Q4 " + str(datetime.datetime.strptime(quarter, format).strftime('%Y'))), day=1, month=10)
            elif line_chart:
                category_quarters = __operation_line_chart(
                    category_quarters=category_quarters, quarter=quarter, label=("Q4 " + str(datetime.datetime.strptime(quarter, format).strftime('%Y'))), day=1, month=10, data=data)
    return category_quarters


def __operation_gantt_chart(category_quarters: list, quarter, label, day, month, format='%d/%m/%Y'):
    start = datetime.datetime.strptime(
        quarter, format).replace(day=day, month=month).strftime(format)
    end = datetime.datetime.strptime(
        quarter, format).strftime(format)
    category_quarters.append({"start": start, "end": end,
                              "label": label})
    return category_quarters


def __operation_line_chart(category_quarters: list, quarter, label, data, day, month, format='%d/%m/%Y'):
    start = datetime.datetime.strptime(
        quarter, format).replace(day=day, month=month)
    end = datetime.datetime.strptime(
        quarter, format)
    data[life_cycle_end] = pd.to_datetime(data[life_cycle_end])
    value = len(data[(data[life_cycle_end] >= start) &
                (data[life_cycle_end] <= end)].index)
    category_quarters.append({"label": label, "value": value})
    return category_quarters
