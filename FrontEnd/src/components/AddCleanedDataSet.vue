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
      <div class="mb-3">
        <label> <b-icon-shield-lock-fill /> Choose Datasets</label>
        <select
          v-model="selected_dataset"
          @click="getSuitableCleansersOptions()"
        >
          <option
            v-for="dataset in datasets"
            v-bind:value="dataset"
            :key="dataset"
          >
            {{ dataset }}
          </option>
        </select>
      </div>

      <div v-if="selected_dataset !== ''" class="mb-3">
        <label> <b-icon-shield-lock-fill /> Suitable Cleansers</label>
        <select
          v-model="selected_cleanser"
          @click="getSuitableCleansersOptions()"
        >
          <option
            v-for="cleanser in suitable_cleansers"
            v-bind:value="cleanser.cleanser_id"
            :key="cleanser.cleanser_id"
          >
            {{ cleanser.name }}
          </option>
        </select>
      </div>
      <hr />

      <div v-if="selected_cleanser !== ''">
        <h1>Save cleaned Dataset</h1>
        <hr />

        <div class="mb-3">
          <label for="DatasetName" class="form-label">
            <b-icon-archive-fill /> Name:</label
          >
          <input
            class="input100"
            id="DatasetName"
            type="text"
            v-model="name"
            placeholder="Data Set Name"
          />
        </div>

        <div class="mb-3">
          <label for="description" class="form-label" id="description">
            <b-icon-pencil-fill /> Description:
          </label>
          <textarea
            class="input100"
            v-model="description"
            placeholder="Description"
            id="description"
          ></textarea>
        </div>

        <div class="mb-3">
          <label for="storage">
            <b-icon-cloud-check-fill /> Stored in Cloud
          </label>
          <input
            class="input200"
            type="checkbox"
            v-model="storageType"
            id="storage"
          />
        </div>

        <div class="mb-3">
          <label> <b-icon-shield-lock-fill /> Users with Access</label>
          <select v-model="selected_users" multiple>
            <option
              v-for="user in users"
              v-bind:value="user.email"
              :key="user.email"
            >
              {{ user.email }}
            </option>
          </select>
        </div>

        <div class="mb-3">
          <label> <b-icon-shield-lock-fill /> Departments with Access</label>
          <select v-model="selected_departments" multiple>
            <option
              v-for="department in departments"
              v-bind:value="department.name"
              :key="department.name"
            >
              {{ department.name }}
            </option>
          </select>
        </div>
        <button class="btn-form" @click="createCleanedDataSet">
          <b-icon-upload />
          <b> Apply Cleanser & Save cleaned Dataset</b>
        </button>
        <span v-if="submitted">
          <br />
          <br />
          <ProgressBar mode="indeterminate" v-if="submitted" />
        </span>
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
      storageType: "",
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
    };
  },
  methods: {
    getUsersOptions() {
      this.users = this.$axios.get("/users").then((res) => {
        this.users = res.data;
      });
    },
    getDepartmentsOptions() {
      this.users = this.$axios.get("/departments").then((res) => {
        this.departments = res.data;
      });
    },
    createCleanedDataSet() {
      this.$axios
        .get("/get_cleanser_by_id/" + this.selected_cleanser)
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
          this.formData.append("access_user_list", this.selected_users);
          this.formData.append(
            "access_business_unit_list",
            this.selected_departments
          );
          this.$axios
            .post(
              "/create_cleaned_dataset/" +
                this.selected_cleanser.cleanser_id +
                "/" +
                this.selected_dataset.split("ID: ")[1] +
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
            datasets_tmp.push(
              "NAME: " +
                res.data.data[index]["name"] +
                "   |   " +
                "ID: " +
                res.data.data[index]["dataset_id"]
            );
          }
          this.datasets = datasets_tmp;
        });
    },
    getSuitableCleansersOptions() {
      if (this.selected_dataset === undefined) {
        this.selected_dataset = " ";
      }
      this.$axios
        .get(
          "/get_suitable_cleansers/" + this.selected_dataset.split("ID: ")[1]
        )
        .then((res) => {
          this.suitable_cleansers = res.data.data;
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