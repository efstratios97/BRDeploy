<template>
  <div>
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
                getSuitableCleansersOptions();
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
  </div>
</template>

<script>
export default {
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
      suitable_cleansers: [],
      selected_users: "",
      selected_dataset: "",
      selected_departments: "",
      selected_cleanser: "",
      formData: "",
      submitted: false,
      cleaned_operation: false,
      selectedCleanedRows: "",
      cleaned_rows: "",
      columns: "",
      showCleanserSelector: false,
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
              this.cleaned_rows = JSON.parse(res.data);
              this.columns = Object.keys(this.cleaned_rows[0]);
              this.submitted = false;
              this.cleaned_operation = true;
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
      this.$emit("close");
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