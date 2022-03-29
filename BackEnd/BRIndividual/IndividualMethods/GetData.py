# Project Athena
'''
Owner: Efstratios Pahis
Contributors:
Description: Implements main functionality of the kpi_m.KPIManager
'''

import DataManager.DataManager as dm
import Utils.Settings as st
import BRIndividual.Utils.SettingsBR as st_br


class GetData:

    def get_departments_by_department_hierarchy_br(self, department: str, dataset_id="", dataset_label=""):
        departments = []
        departments_in_dataset = self.get_departments_from_dataset(
            GetData, dataset_id=dataset_id, dataset_label=dataset_label)
        haupt_abteilung_tmp = department.replace(
            " (Organisationseinheit)", "")
        abteilung_tmp = department.replace(
            " (Organisationseinheit)", "").replace("Abt. ", "")
        if department == st.ALL_VALUES_INPUT_FIELD:
            departments = st_br.get_departments_bayerischer_rundfunk_list()
            return departments
        elif department.startswith("HA "):
            for ha_abt in list(st_br.departments_bayerischer_rundfunk["Hauptabteilungen"].keys()):
                if ha_abt in haupt_abteilung_tmp:
                    departments.append(department)
                    for abteilung in st_br.departments_bayerischer_rundfunk["Hauptabteilungen"][ha_abt]["Abteilungen"]:
                        abteilung_to_list = [
                            val for val in departments_in_dataset if abteilung in val and val.startswith("Abt. ")]
                        if len(abteilung_to_list) == 1:
                            departments.append(abteilung_to_list[0])
                        elif len(abteilung_to_list) > 1:
                            abteilung_to_list = [
                                val for val in abteilung_to_list if not "," in val or not "\n" in val]
                            departments.append(abteilung_to_list[0])
                        for fachgruppe in st_br.departments_bayerischer_rundfunk["Hauptabteilungen"][ha_abt]["Abteilungen"][abteilung]["Fachgruppen"]:
                            fachgruppe_to_list = [
                                val for val in departments_in_dataset if fachgruppe in val]
                            if len(fachgruppe_to_list) == 1:
                                departments.append(fachgruppe_to_list[0])
                            elif len(fachgruppe_to_list) > 1:
                                fachgruppe_to_list = [
                                    val for val in fachgruppe_to_list if not "," in val or not "\n" in val]
                                departments.append(fachgruppe_to_list[0])
                    return departments
        elif department.startswith("Abt. "):
            for ha_abt in list(st_br.departments_bayerischer_rundfunk["Hauptabteilungen"].keys()):
                if abteilung_tmp in list(st_br.departments_bayerischer_rundfunk["Hauptabteilungen"][ha_abt]["Abteilungen"]):
                    departments.append(department)
                    dept_in_settings = [
                        val for val in departments_in_dataset if department in val][0].replace(
                        " (Organisationseinheit)", "").replace("Abt. ", "")
                    try:
                        for fachgruppe in st_br.departments_bayerischer_rundfunk["Hauptabteilungen"][ha_abt]["Abteilungen"][dept_in_settings]["Fachgruppen"]:
                            fachgruppe_to_list = [
                                val for val in departments_in_dataset if fachgruppe in val]
                            if len(fachgruppe_to_list) == 1:
                                departments.append(fachgruppe_to_list[0])
                            elif len(fachgruppe_to_list) > 1:
                                fachgruppe_to_list = [
                                    val for val in fachgruppe_to_list if not "," in val or not "\n" in val]
                                departments.append(fachgruppe_to_list[0])
                    except:
                        print("list_dep" + dept_in_settings)
                    return departments
        elif department.startswith("FG "):
            departments.append(department)
            return departments
        if len(departments) == 0:
            departments.append(department)
            return departments

    def get_departments_from_dataset(self, dataset_id="", dataset_label=""):
        dataset_id = dm.DataManager.check_dataset_exists_and_return_alternative_based_on_label(
            dm.DataManager, dataset_id=dataset_id, dataset_label=dataset_label)
        data = dm.DataManager.get_table_as_df(
            dm.DataManager, dataset_id)
        departments = st.prepend_elem_to_list(st.prepend_elem_to_list(list(filter(None, list(
            set(data['Verantwortliche Organisationseinheit'].to_list())))), st.NO_ENTRY_INPUT_FIELD), st.ALL_VALUES_INPUT_FIELD)
        return departments

    def get_apps_from_dataset(self, dataset_id="", dataset_label=""):
        dataset_id = dm.DataManager.check_dataset_exists_and_return_alternative_based_on_label(
            dm.DataManager, dataset_id=dataset_id, dataset_label=dataset_label)
        data = dm.DataManager.get_table_as_df(
            dm.DataManager, dataset_id)
        apps = list(
            set(data['Name'].to_list()))
        return apps

    def get_domains_from_dataset(self, dataset_id="", dataset_label=""):
        dataset_id = dm.DataManager.check_dataset_exists_and_return_alternative_based_on_label(
            dm.DataManager, dataset_id=dataset_id, dataset_label=dataset_label)
        data = dm.DataManager.get_table_as_df(
            dm.DataManager, dataset_id)
        domains = list(
            set(list(filter(None, " ".join(str(data['Zugeordnete Domäne'].to_list()).strip('][')
                                           .replace(" \\n", "").replace("'',", "").replace("'", "")
                                           .split()).split(",")))))
        domains = [val.strip() for val in domains]
        return list(set(domains))
