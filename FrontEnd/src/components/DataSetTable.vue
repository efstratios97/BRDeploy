<template>
  <DataTable
    :value="datasets"
    v-model:selection="selected_dataset"
    dataKey="dataset_id"
    :paginator="true"
    :rows="10"
    filterDisplay="menu"
    paginatorTemplate="FirstPageLink PrevPageLink PageLinks NextPageLink LastPageLink CurrentPageReport RowsPerPageDropdown"
    :rowsPerPageOptions="[10, 25, 50]"
    currentPageReportTemplate="Showing {first} to {last} of {totalRecords} entries"
    responsiveLayout="scroll"
    sortMode="multiple"
  >
    <template #header>
      <div class="p-d-flex p-jc-between p-ai-center">
        <h5 class="p-m-0">Datasets</h5>
        <span class="p-input-icon-left">
          <i class="pi pi-search" />
          <InputText placeholder="Keyword Search" />
        </span>
      </div>
    </template>
    <template #empty>
      <span v-if="dataset_loading">
        Loading Datasets. Please wait.
        <ProgressBar mode="indeterminate" />
      </span>
      <span v-else> There are no datasets. </span>
    </template>
    <template #loading>
      Loading Datasets. Please wait. <ProgressBar mode="indeterminate"
    /></template>
    <Column selectionMode="multiple" headerStyle="width: 3em"></Column>
    <Column field="dataset_id" header="ID" sortable style="min-width: auto">
    </Column>
    <Column field="name" header="Name" sortable style="min-width: auto">
    </Column>
    <Column
      field="description"
      header="Description"
      sortable
      style="min-width: auto"
    >
    </Column>
    <Column field="cleaned" header="Cleaned" sortable style="min-width: auto">
    </Column>
    <Column field="owner" header="Owner" sortable style="min-width: auto">
    </Column>
    <Column field="label" header="Label" sortable style="min-width: auto">
    </Column>
    <Column
      field="access_user_list"
      header="Access Users"
      headerStyle="min-width: 4rem; text-align: center"
      bodyStyle="text-align: center; overflow: visible; color:black"
    >
      <template #body="slotProps">
        <Dropdown
          :options="slotProps.data.access_user_list"
          placeholder="Users"
        />
      </template>
    </Column>
    <Column
      field="access_business_unit_list"
      header="Access BUs"
      style="min-width: auto"
    >
      <template #body="slotProps">
        <Dropdown
          :options="slotProps.data.access_business_unit_list"
          placeholder="BUs"
        />
      </template>
    </Column>

    <Column
      field="creation_date"
      header="Timestamp"
      sortable
      style="min-width: auto"
    >
    </Column>
    <Column header="Ad hoc Operations" style="min-width: auto">
      <template #body>
        <div>
          <SpeedDial
            :model="items"
            :radius="50"
            direction="right"
            type="right"
            buttonClass="p-button-secondary"
            style="position: relative"
          />
        </div>
        <ProgressBar mode="indeterminate" v-if="dataset_operating" />
      </template>
    </Column>
  </DataTable>
</template>
 
<script>
export default {
  data() {
    return {
      users: this.listUsers(),
      datasets: this.listDatasets(),
      selected_dataset: "",
      dataset_loading: true,
      dataset_operating: false,
      items: [
        {
          label: "Delete",
          icon: "pi pi-trash",
          command: () => {
            this.deleteSelected();
          },
        },
        {
          label: "Show",
          icon: "pi pi-eye",
          command: () => {
            this.viewSelected();
          },
        },
        {
          label: "Update",
          icon: "pi pi-refresh",
          command: () => {
            this.getSelectedToUpdate();
          },
        },
      ],
    };
  },
  methods: {
    getSelectedToUpdate() {
      if (
        this.selected_dataset.length === 1 &&
        this.selected_dataset.length !== 0
      ) {
        this.$emit("update", this.selected_dataset[0]);
      } else {
        this.$toast.add({
          severity: "warn",
          summary: "None or More than 1 Dataset selected",
          detail: "Please select only one Dataset to display",
          life: 4000,
        });
      }
    },
    deleteSelected() {
      if (this.selected_dataset.length === 0) {
        this.$toast.add({
          severity: "warn",
          summary: "No Dataset selected",
          detail: "Please select Dataset first",
          life: 3000,
        });
      } else {
        for (let index = 0; index < this.selected_dataset.length; index++) {
          this.deleteDataSet(
            this.selected_dataset[index].dataset_id,
            this.selected_dataset[index].storage_type
          );
        }
      }
    },
    viewSelected() {
      if (
        this.selected_dataset.length === 1 &&
        this.selected_dataset.length !== 0
      ) {
        this.viewDataset(
          this.selected_dataset[0].dataset_id,
          this.selected_dataset[0].storage_type
        );
      } else {
        this.$toast.add({
          severity: "warn",
          summary: "None or More than 1 Dataset selected",
          detail: "Please select only one Dataset to display",
          life: 4000,
        });
      }
    },
    normalize_datasets(datasets) {
      for (let index = 0; index < datasets.length; index++) {
        for (var key in datasets[index]) {
          if (key === "owner") {
            datasets[index][key] = this.enumOwner(datasets[index][key]);
          }
          if (key === "user") {
            datasets[index][key] = this.enumUser(datasets[index][key]);
          }
          if (key === "access_user_list") {
            var tmp_list = [];
            for (let i = 0; i < datasets[index][key].length; i++) {
              tmp_list.push(this.enumUser(datasets[index][key][i]));
            }
            datasets[index][key] = tmp_list;
          }
          if (key === "access_business_unit_list") {
            tmp_list = [];
            for (let i = 0; i < datasets[index][key].length; i++) {
              tmp_list.push(this.enumUser(datasets[index][key][i]));
            }
            datasets[index][key] = tmp_list;
          }
        }
      }
      return datasets;
    },
    enumOwner(owner) {
      for (let i = 0; i < this.users.length; i++) {
        if (this.users[i]["user_id"] === owner) {
          return this.users[i]["email"];
        }
      }
      return owner;
    },
    enumUser(user) {
      for (let i = 0; i < this.users.length; i++) {
        if (this.users[i]["user_id"] === user) {
          return this.users[i]["email"];
        }
      }
      return user;
    },
    deleteDataSet(dataset_id, storageType) {
      if (dataset_id === undefined) {
        this.$toast.add({
          severity: "warn",
          summary: "No Dataset selected",
          detail: "Please select Dataset first",
          life: 3000,
        });
      } else {
        this.dataset_operating = true;
      }
      this.$axios
        .delete("/delete_dataset/" + dataset_id + "/" + storageType)
        .then(() => {
          this.listDatasets();
          if (this.dataset_operating == true) {
            this.$toast.add({
              severity: "success",
              summary: "Dataset Deletion Successful",
              detail: "The selected Dataset was deleted",
              life: 3000,
            });
          }
          this.dataset_operating = false;
          this.selected_dataset = "";
        })
        .catch(() => {
          this.dataset_operating = false;
          this.$toast.add({
            severity: "error",
            summary: "Dataset Deletion Unsuccessful",
            detail: "The selected Dataset could not be deleted",
            life: 3000,
          });
          this.selected_dataset = "";
        });
    },
    viewDataset(dataset_id, storage_type) {
      if (dataset_id === undefined) {
        this.$toast.add({
          severity: "warn",
          summary: "No Dataset selected",
          detail: "Please select Dataset first",
          life: 3000,
        });
      }
      this.$emit("view", dataset_id, storage_type);
    },
    listDatasets() {
      this.$axios
        .get("/get_datasets/" + localStorage.loggedUser)
        .then((res) => {
          this.datasets = this.normalize_datasets(res.data.data);
          if (this.datasets.length === 0) {
            this.dataset_loading = false;
          }
        });
    },
    listUsers() {
      this.$axios.get("/users").then((res) => {
        this.users = res.data;
      });
    },
  },
};
</script>

<style>
.btn-align-td {
  display: inline-block;
  margin: 2px;
}

.speed-dial-td {
  display: inline-block;
  margin: 2px;
}
</style>