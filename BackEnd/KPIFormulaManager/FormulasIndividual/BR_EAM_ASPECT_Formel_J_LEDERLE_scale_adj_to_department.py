import sys
# sys.path.insert(0, '/root/BRDeploy/BackEnd')
# sys.path.insert(0,  '/root/brapp/bin')
import DataManager.DataManager as dm
import KPIFormulaManager.Result as res
import KPIAspectManager.AspectManager as aspct_m
import json
import Utils.Settings as st
import numpy
from numpy import NaN
import datetime
import BRIndividual.IndividualMethods.GetData as gt_dt


def aspect_calculation(parameter="", aspect_id="", dataset_data="", dataset_id="", fast=False):
    result = {}
    if not fast:
        aspect_id = sys.argv[1]
        dataset_id = sys.argv[2]
        parameter = json.loads(sys.argv[3])
        db_location = sys.argv[4]
        dataset_data = dm.DataManager.get_table_as_df(
            dm.DataManager, dataset_id)
    else:
        parameter = json.loads(parameter)
    aspect = aspct_m.AspectManager.get_aspect_by_id(
        aspct_m.AspectManager, aspect_id=aspect_id)
    raw_components_from_datasets = aspect.get_raw_components_from_dataset()
    scale = aspect.get_skala_size()
    threshold = aspect.get_threshold()
    aspect_nominal = 0
    max_val_scale = 0
    aspect_value = 0
    app = parameter["app"]
    department = parameter["department"]
    domain = parameter["domain"]
    if not app == "":
        parameter = app
        dataset_data_dep = dataset_data.copy()
        department_tmp = dataset_data_dep[dataset_data_dep["Name"]
                                          == app]["Verantwortliche Organisationseinheit"].iloc[0]
        departments = gt_dt.GetData.get_departments_by_department_hierarchy_br(
            gt_dt.GetData, department=department_tmp, dataset_id=dataset_id)
        dataset_data_dep["Verantwortliche Organisationseinheit"] = dataset_data["Verantwortliche Organisationseinheit"].apply(
            lambda x: x if x in departments else NaN)
        dataset_data_dep.dropna(inplace=True, subset=[
            'Verantwortliche Organisationseinheit'])
        apps = [app]
    if not department == "":
        parameter = department
        if not department == st.ALL_VALUES_INPUT_FIELD:
            if department == st.NO_ENTRY_INPUT_FIELD:
                department = ""
            departments = gt_dt.GetData.get_departments_by_department_hierarchy_br(
                gt_dt.GetData, department=department, dataset_id=dataset_id)
            dataset_data_dep = dataset_data.copy()
            dataset_data_dep["Verantwortliche Organisationseinheit"] = dataset_data["Verantwortliche Organisationseinheit"].apply(
                lambda x: x if x in departments else NaN)
            dataset_data_dep.dropna(inplace=True, subset=[
                                    'Verantwortliche Organisationseinheit'])
            apps = dataset_data_dep["Name"].to_list()
        else:
            apps = dataset_data["Name"].to_list()
    if not domain == "":
        parameter = domain
        dataset_data_domain = dataset_data.copy()
        dataset_data_domain["Zugeordnete Dom??ne"] = dataset_data["Zugeordnete Dom??ne"].apply(
            lambda x: x if domain in x else NaN)
        dataset_data_domain.dropna(inplace=True, subset=[
            'Zugeordnete Dom??ne'])
        apps = dataset_data_domain["Name"].to_list()
    for app in apps:
        app_data = dataset_data[dataset_data["Name"] == app][:1]
        for raw_components_from_dataset in raw_components_from_datasets:
            raw_component = list(raw_components_from_dataset.keys())[0]
            try:
                if st.ASPECT_OPERATION_TYPE_COUNT in list(raw_components_from_dataset.values())[0]:
                    if not raw_component == "Name":
                        if not isinstance(app_data[raw_component].iloc[0], numpy.int64):
                            app_data[raw_component] = app_data[raw_component].apply(
                                lambda x: len(x.split(",")) if not x == "" else 0)
                        if not department == "":
                            if not isinstance(dataset_data_dep[raw_component].iloc[0], numpy.int64):
                                dataset_data_dep[raw_component] = dataset_data_dep[raw_component].apply(
                                    lambda x: len(x.split(",")) if not x == "" else 0)
                            max_val_scale += max(
                                list(set(dataset_data_dep[raw_component].values.tolist())))

                        elif not domain == "":
                            if not isinstance(dataset_data_domain[raw_component].iloc[0], numpy.int64):
                                dataset_data_domain[raw_component] = dataset_data_domain[raw_component].apply(
                                    lambda x: len(x.split(",")) if not x == "" else 0)
                            max_val_scale += max(
                                list(set(dataset_data_domain[raw_component].values.tolist())))
                        else:
                            if not isinstance(dataset_data[raw_component].iloc[0], numpy.int64):
                                dataset_data[raw_component] = dataset_data[raw_component].apply(
                                    lambda x: len(x.split(",")) if not x == "" else 0)
                            max_val_scale += max(
                                list(set(dataset_data[raw_component].values.tolist())))
                    else:
                        aspect_nominal += 0
                        scale += 0
                        max_val_scale += 1
                    aspect_nominal += app_data[raw_component].iloc[0]
                elif st.ASPECT_OPERATION_TYPE_CATEGORICAL_3_SCALE in list(raw_components_from_dataset.values())[0]:
                    def define_scale_categorical_3(x):
                        if x == "Niedrig":
                            return 3
                        elif x == "Mittel":
                            return 6
                        elif x == "Hoch":
                            return 10
                        else:
                            return 0
                    app_data[raw_component] = app_data[raw_component].apply(
                        lambda x: define_scale_categorical_3(x))
                    max_val_scale += 10
                    aspect_nominal += app_data[raw_component].iloc[0]
                elif st.ASPECT_OPERATION_TYPE_CATEGORICAL_5_SCALE in list(raw_components_from_dataset.values())[0]:
                    def define_scale_categorical_5(x):
                        if x == "Sehr Niedrig":
                            return 1
                        elif x == "Niedrig":
                            return 3
                        elif x == "Mittel":
                            return 5
                        elif x == "Hoch":
                            return 7
                        elif x == "Sehr Hoch":
                            return 10
                        else:
                            return 0
                    app_data[raw_component] = app_data[raw_component].apply(
                        lambda x: define_scale_categorical_5(x))
                    max_val_scale += 10
                    aspect_nominal += app_data[raw_component].iloc[0]
                elif st.ASPECT_OPERATION_TYPE_CATEGORICAL_LIFE_CYCLE_END:
                    def define_scale_categorical_life_cycle_end(x):
                        if x == "-":
                            return 0
                        elif (datetime.datetime.strptime(x, '%Y-%m-%d %H:%M:%S') - datetime.datetime.now()).days < 2*365:
                            return 10
                        elif (datetime.datetime.strptime(x, '%Y-%m-%d %H:%M:%S') - datetime.datetime.now()).days < 5*365:
                            return 6
                        elif (datetime.datetime.strptime(x, '%Y-%m-%d %H:%M:%S') - datetime.datetime.now()).days >= 5*365:
                            return 3
                    app_data[raw_component] = app_data[raw_component].apply(
                        lambda x: define_scale_categorical_life_cycle_end(x))
                    max_val_scale += 10
                    aspect_nominal += app_data[raw_component].iloc[0]
                else:
                    aspect_nominal += 0
                    scale += 0
                    max_val_scale += 1
            except:
                print("error_aspect_calc" + app)
                aspect_nominal = 0
                scale = 0
                max_val_scale = 1
        aspect_value += aspect_nominal * (scale/max_val_scale)
    aspect_value = aspect_value / len(apps)
    result['result'] = aspect_value
    result['threshold'] = threshold
    result['aspect_id'] = aspect_id
    result['aspect_name'] = aspect.get_name()
    result['scale'] = scale
    result['parameter'] = parameter
    if fast:
        return result
    else:
        sys.argv = []
        res.Result.save_result(res.Result, result=result,
                               table_name=db_location)


if __name__ == "__main__":
    aspect_calculation()
