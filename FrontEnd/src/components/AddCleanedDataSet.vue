<template>
  <form>
    <div class="p-grid p-fluid">
      <div class="p-col-12 p-md-12">
        <div class="p-inputgroup">
          <span class="p-inputgroup-addon">
            <i class="pi pi-search"></i>
          </span>
          <Dropdown
            v-model="selected_dataset"
            :options="datasets"
            :filter="true"
            optionLabel="dataset"
            placeholder="Choose Dataset"
            filterPlaceholder="Find an Dataset"
            class="multiselect-custom"
            :showClear="true"
          />
          <Button
            label="Find Applicable Cleanser"
            @click="
              toggleShowCleanserSelector();
              updateCleansers();
            "
          />
        </div>
      </div>
    </div>

    <div v-if="showCleanserSelector">
      <div class="p-grid p-fluid">
        <div class="p-col-12 p-md-12">
          <div class="p-inputgroup">
            <span class="p-inputgroup-addon">
              <i class="pi pi-cog"></i>
            </span>
            <Dropdown
              v-model="selected_cleanser"
              :options="suitable_cleansers"
              :filter="true"
              optionLabel="cleanser.name"
              placeholder="Choose Cleanser"
              filterPlaceholder="Find a Cleanser"
              class="multiselect-custom"
              :showClear="true"
            />
          </div>
        </div>
      </div>
    </div>

    <hr />

    <div v-if="selected_cleanser !== ''">
      <h2>Save cleaned Dataset</h2>
      <div class="p-grid p-fluid">
        <div class="p-col-12 p-md-12">
          <div class="p-inputgroup">
            <span class="p-inputgroup-addon">
              <i class="pi pi-file"></i>
            </span>
            <InputText
              placeholder="Dataset's Name"
              v-model="name"
              class="inputfield w-full"
            />
          </div>
        </div>
      </div>

      <div class="p-grid p-fluid">
        <div class="p-col-12 p-md-12">
          <Textarea
            placeholder="Dataset Description"
            v-model="description"
            :autoResize="true"
            rows="5"
            cols="30"
          />
        </div>
      </div>

      <div class="p-grid p-fluid">
        <div class="p-col-12 p-md-12">
          <div class="p-inputgroup">
            <span class="p-inputgroup-addon">
              <i class="pi pi-users"></i>
            </span>
            <MultiSelect
              v-model="selected_users"
              :options="users"
              :filter="true"
              optionLabel="user.email"
              placeholder="Assign Users with Access (Optional)"
              filterPlaceholder="Find Users"
              class="multiselect-custom"
              :showClear="true"
            />
          </div>
        </div>
      </div>

      <div class="p-grid p-fluid">
        <div class="p-col-12 p-md-12">
          <div class="p-inputgroup">
            <span class="p-inputgroup-addon">
              <b-icon-building />
            </span>
            <MultiSelect
              v-model="selected_departments"
              :options="departments"
              :filter="true"
              optionLabel="dep.name"
              placeholder="Assign Departments with Access (Optional)"
              filterPlaceholder="Find Departments"
              class="multiselect-custom"
              :showClear="true"
            />
          </div>
        </div>
      </div>

      <div class="p-grid p-fluid">
        <div class="p-col">
          <div class="card p-align-center">
            <h5>Delete older Versions of Dataset</h5>
            <InputSwitch
              v-model="delete_all_previous_versions"
              v-tooltip="'Datasets can be still recovered from the Archive'"
              @click="listAllDatasets"
            />
          </div>
        </div>
      </div>

      <div class="p-grid p-fluid">
        <div class="p-col-12 p-md-12">
          <Button
            label="Save Cleaned Dataset"
            icon="pi pi-plus-circle"
            iconPos="center"
            @click="createCleanedDataSet"
          />
        </div>
      </div>
      <div v-if="submitted">
        <br />
        <ProgressBar mode="indeterminate" v-if="submitted" />
      </div>
    </div>
  </form>
  <transition class="modal-animation">
    <modal-view v-if="new_label">
      <template v-slot:header>New Dataset Identified</template>
      <template v-slot:body>
        <h3>
          The Dataset you upload seems <b>not</b> to have any predecessors.
          Please label your Dataset with a designated Label. By doing so the
          next time you upload a newer version of Dataset it will automatically
          be assigned to the correct Label.
        </h3>
        <form>
          <div class="p-grid p-fluid">
            <div class="p-col-12 p-md-12">
              <div class="p-inputgroup">
                <span class="p-inputgroup-addon">
                  <i class="pi pi-tag"></i>
                </span>
                <InputText
                  placeholder="Labels's Name"
                  v-model="label_name"
                  class="inputfield w-full"
                  v-tooltip="'Label Name must be unique!'"
                />
              </div>
            </div>
          </div>
          <div class="p-grid p-fluid">
            <div class="p-col-12 p-md-12">
              <Button
                label="Assign Label"
                icon="pi pi-tag"
                iconPos="center"
                @click="assignLabel"
              />
            </div>
          </div>
        </form> </template
    ></modal-view>
  </transition>
  <Dialog
    v-model:visible="cleaned_operation"
    :breakpoints="{ '960px': '75vw', '640px': '100vw' }"
    :style="{ width: '50vw' }"
  >
    <DataTable
      :value="cleaned_rows"
      v-model:selection="selectedCleanedRows"
      dataKey="Name"
      :paginator="true"
      :rows="10"
      filterDisplay="menu"
      paginatorTemplate="FirstPageLink PrevPageLink PageLinks NextPageLink LastPageLink CurrentPageReport RowsPerPageDropdown"
      :rowsPerPageOptions="[10, 25, 50]"
      currentPageReportTemplate="Showing {first} to {last} of {totalRecords} entries"
      responsiveLayout="scroll"
      :rowHover="true"
      showGridlines
      stripedRows
      ref="dt"
      p-dataTable
      csvSeparator=";"
    >
      <template #header>
        <div class="p-d-flex p-jc-between p-ai-center">
          <h5 class="p-m-0">Cleaned Rows</h5>
          <span class="p-input-icon-left">
            <Button
              icon="pi pi-external-link"
              label="Export"
              @click="exportCSV($event)"
            />
          </span>
          <span class="p-input-icon-right">
            <Button
              icon="pi pi-cloud-upload"
              label="Return Rows to Dataset"
              @click="return_rows_to_dataset()"
            />
          </span>
          <span class="p-input-icon-right">
            <Button
              icon="pi pi-chevron-circle-down"
              label="Close"
              @click="close()"
            />
          </span>
        </div>
      </template>
      <template #empty>
        <span v-if="architecture_view_loading">
          Loading Cleaned Rows. Please wait.
          <ProgressBar mode="indeterminate" />
        </span>
        <span v-else> There are no Cleaned Rows. </span>
      </template>
      <template #loading>
        Loading Cleaned Rows. Please wait.
        <ProgressBar mode="indeterminate" />
      </template>
      <Column selectionMode="multiple" style="min-width: 3rem"></Column>
      <Column
        v-for="col of columns"
        :field="col"
        :header="col"
        :key="col"
        sortable
      ></Column>
    </DataTable>
  </Dialog>
</template>

<script>
import Modal from "../components/Modal.vue";
export default {
  components: {
    "modal-view": Modal,
  },
  data() {
    return {
      name: "",
      cleaned: "",
      description: "",
      storageType: true,
      file: "",
      users: this.getUsersOptions(),
      departments: this.getDepartmentsOptions(),
      datasets: this.getDatasetOptions(),
      datasets_all: "",
      suitable_cleansers: [],
      selected_users: "",
      selected_dataset: "",
      selected_departments: "",
      selected_cleanser: "",
      formData: "",
      submitted: false,
      new_label: false,
      cleaned_operation: false,
      selectedCleanedRows: "",
      formData_cleaned_rows: "",
      cleaned_rows: "",
      columns: "",
      showCleanserSelector: false,
      label_name: "",
      delete_all_previous_versions: false,
      new_created_dataset: "",
    };
  },
  methods: {
    toggleShowCleanserSelector() {
      this.showCleanserSelector = !this.showCleanserSelector;
    },
    getUsersOptions() {
      this.$axios.get("/users").then((res) => {
        var users_tmp = [];
        for (let index = 0; index < res.data.length; index++) {
          users_tmp.push({ user: res.data[index] });
        }
        this.users = users_tmp;
      });
    },
    getDepartmentsOptions() {
      this.$axios.get("/departments").then((res) => {
        var departments_tmp = [];
        for (let index = 0; index < res.data.length; index++) {
          departments_tmp.push({ dep: res.data[index] });
        }
        this.departments = departments_tmp;
      });
    },
    toString(dict_key) {
      var key_word = "";
      var object_input = "";
      if (dict_key === "user") {
        key_word = "email";
        object_input = this.selected_users;
      } else if (dict_key === "dep") {
        key_word = "name";
        object_input = this.selected_departments;
      } else if (dict_key === "dataset") {
        object_input = this.selected_datasets;
      } else if (dict_key === "cleanser") {
        object_input = this.suitable_cleansers;
      }
      var updt_list = "";
      if (dict_key === "user" || dict_key === "dep") {
        for (let index = 0; index < object_input.length; index++) {
          updt_list = updt_list.concat(object_input[index][dict_key][key_word]);
          updt_list = updt_list.concat(",");
        }
      } else if (dict_key === "dataset" || dict_key === "cleanser") {
        for (let index = 0; index < object_input.length; index++) {
          var temp_elem = object_input[index][dict_key];
          if (dict_key === "dataset") {
            temp_elem = object_input[index][dict_key].split("ID: ")[1];
          }
          updt_list = updt_list.concat(temp_elem);
          updt_list = updt_list.concat(",");
        }
      }
      return updt_list.slice(0, -1);
    },
    createCleanedDataSet() {
      this.$axios
        .get(
          "/get_cleanser_by_id/" + this.selected_cleanser.cleanser.cleanser_id
        )
        .then((res) => {
          this.submitted = true;
          this.$toast.add({
            severity: "info",
            summary: "The Dataset is being cleaned",
            detail: "Please be aware that this may take few minutes",
            life: 15000,
          });
          this.selected_cleanser = res.data.data[0];
          this.formData = new FormData();
          this.formData.append("name", this.name);
          this.formData.append(
            "cleanser_operation_types",
            this.selected_cleanser.cleanser_operation_types
          );
          this.formData.append("cleaned", this.cleaned);
          this.formData.append("description", this.description);
          this.formData.append(
            "storage_type",
            this.storageType === true ? "cloud" : "local"
          );
          this.formData.append("access_user_list", this.toString("user"));
          this.formData.append(
            "access_business_unit_list",
            this.toString("dep")
          );
          this.$axios
            .post(
              "/create_cleaned_dataset/" +
                this.selected_cleanser.cleanser_id +
                "/" +
                this.selected_dataset["dataset"].split("ID: ")[1] +
                "/" +
                localStorage.loggedUser,
              this.formData
            )
            .then((res) => {
              this.cleaned_rows = JSON.parse(res.data.eliminated_rows);
              this.columns = Object.keys(this.cleaned_rows[0]);
              this.submitted = false;
              this.cleaned_operation = true;
              this.new_created_dataset = res.data; //consists of a cleaned_dataset and a dataset with removed rows
              if (
                this.new_created_dataset.cleaned_dataset["label"] ===
                "NO_LABEL_6aba48df0cb55992803d864977c3aa204520d659"
              ) {
                this.new_label = true;
              }
              if (this.delete_all_previous_versions) {
                this.delete_all_previous_versions_of_datasets();
              }
              this.$toast.add({
                severity: "success",
                summary: "Cleaned Dataset Creation Successful",
                detail: "The cleaned Dataset was created",
                life: 3000,
              });
            })
            .catch(() => {
              this.$toast.add({
                severity: "error",
                summary: "Cleaned Dataset Creation Unsuccessful",
                detail: "The cleaned Dataset could not be created",
                life: 3000,
              });
              this.submitted = false;
            });
        });
    },
    getDatasetOptions() {
      this.$axios
        .get("/get_datasets_only_name/" + localStorage.loggedUser)
        .then((res) => {
          var datasets_tmp = [];
          for (let index = 0; index < res.data.data.length; index++) {
            datasets_tmp.push({
              dataset:
                "NAME: " +
                res.data.data[index]["name"] +
                "   |   " +
                "ID: " +
                res.data.data[index]["dataset_id"],
            });
          }
          this.datasets = datasets_tmp;
        });
    },
    getSuitableCleansersOptions() {
      // if (this.selected_dataset === undefined) {
      //   this.selected_dataset = " ";
      // }
      this.$axios
        .get(
          "/get_suitable_cleansers/" +
            this.selected_dataset["dataset"].split("ID: ")[1]
        )
        .then((res) => {
          var cleanser_tmp = [];
          for (let index = 0; index < res.data.data.length; index++) {
            cleanser_tmp.push({
              cleanser: res.data.data[index],
            });
          }
          this.suitable_cleansers = cleanser_tmp;
          if (cleanser_tmp.length === 0) {
            this.$toast.add({
              severity: "error",
              summary: "No suitable Cleansers available",
              detail: "The Dataset has no suitable cleanser",
              life: 3000,
            });
          }
        })
        .catch(() => {
          this.$toast.add({
            severity: "error",
            summary: "No suitable Cleansers available",
            detail: "The Dataset has no suitable cleanser",
            life: 3000,
          });
        });
    },
    exportCSV() {
      this.$refs.dt.exportCSV();
    },
    close() {
      if (this.new_label) {
        this.cleaned_operation = false;
      } else {
        this.$emit("close");
      }
    },
    assignLabel() {
      this.$axios
        .post(
          "/assign_label/" +
            this.new_created_dataset.cleaned_dataset.dataset_id +
            "/" +
            this.label_name
        )
        .then(() => {
          this.$toast.add({
            severity: "success",
            summary: "Label Creation Successful",
            detail:
              "The Label was created and assigned to your Dataset and will be assigned to any future similar Dataset automatically",
            life: 10000,
          });
          this.new_label = false;
          this.close();
        })
        .catch(() => {
          this.$toast.add({
            severity: "error",
            summary: "Label Creation Unuccessful",
            detail:
              "The Label could not have been assigned! Check if the given Name is unique",
            life: 7000,
          });
        });
    },
    return_rows_to_dataset() {
      this.$toast.add({
        severity: "info",
        summary: "Row Re-Addition is starting",
        detail: "Adding selected Rows will start shortly",
        life: 5000,
      });
      for (let index = 0; index < this.selectedCleanedRows.length; index++) {
        var element = this.selectedCleanedRows[index];
        var jsonString = JSON.stringify(element);
        this.$axios
          .post(
            "/return_to_dataset_cleaned_rows/" +
              this.new_created_dataset.cleaned_dataset.dataset_id,
            jsonString
          )
          .then(() => {
            this.$toast.add({
              severity: "success",
              summary: "Row Re-Addition was Succesul",
              detail:
                "Following Row was added:\n " +
                jsonString.substring(1, 130) +
                "......",
              life: 5000,
            });
          })
          .catch(() => {
            this.$toast.add({
              severity: "error",
              summary: "Row RE-Addition Unsuccessful",
              detail:
                "The selected Row could not be re-added! Check if Row is compatible with dataset",
              life: 3000,
            });
          });
      }
      if (this.selectedCleanedRows.length === 0) {
        this.$toast.add({
          severity: "warn",
          summary: "No Row selected",
          detail: "Please select a Row to re-add to dataset",
          life: 5000,
        });
      } else {
        this.close();
      }
    },
    updateCleansers() {
      this.$axios
        .post("/update_cleansers/" + localStorage.loggedUser)
        .then(() => {
          this.getSuitableCleansersOptions();
        });
    },
    delete_all_previous_versions_of_datasets() {
      var label_of_dataset = this.new_created_dataset.cleaned_dataset.label;
      for (let index = 0; index < this.datasets_all.length; index++) {
        if (label_of_dataset === this.datasets_all[index].label) {
          this.$axios.delete(
            "/delete_dataset/" +
              this.datasets_all[index].dataset_id +
              "/" +
              this.datasets_all[index].storage_type
          );
        }
      }
    },
    listAllDatasets() {
      this.$axios
        .get("/get_datasets/" + localStorage.loggedUser)
        .then((res) => {
          this.datasets_all = res.data.data;
        });
    },
  },
};
</script>
<style scoped>
label {
  display: block;
}

.btn-form {
  color: white;
  background: #0d6efd;
  border: 0px solid blue;
  border-radius: 2px;
}

select {
  color: black;
}

input {
  color: black;
}

textarea {
  color: black;
}
</style>