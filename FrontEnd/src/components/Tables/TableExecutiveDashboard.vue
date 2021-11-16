<template>
  <DataTable
    :value="executive_dashboards"
    v-model:selection="selected_executive_dashboard"
    dataKey="executive_dashboard_id"
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
        <h5 class="p-m-0">Executive Dashboards</h5>
        <span class="p-input-icon-left">
          <i class="pi pi-search" />
          <InputText placeholder="Keyword Search" />
        </span>
      </div>
    </template>
    <template #empty>
      <span v-if="executive_dashboard_loading">
        Loading Executive Dashboards. Please wait.
        <ProgressBar mode="indeterminate" />
      </span>
      <span v-else> There are no executive Dashboards. </span>
    </template>
    <template #loading>
      Loading Executive Dashboards. Please wait.
      <ProgressBar mode="indeterminate"
    /></template>
    <Column selectionMode="multiple" headerStyle="width: 3em"></Column>
    <Column
      field="executive_dashboard_id"
      header="ID"
      sortable
      style="min-width: auto"
    >
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
        <div class="btn-align-td">
          <button
            v-on:click="UpdateSelectedExecutiveDashboard()"
            class="btn btn-secondary"
            v-tooltip="'Select Dataset first'"
          >
            <b-icon-pencil-square></b-icon-pencil-square>
          </button>
        </div>
        <div class="btn-align-td">
          <button
            v-on:click="deleteSelected()"
            class="btn btn-secondary"
            v-tooltip="'Select Dataset first'"
          >
            <b-icon-trash-fill />
          </button>
        </div>
        <ProgressBar
          mode="indeterminate"
          v-if="executive_dashboard_operating"
        />
      </template>
    </Column>
  </DataTable>
</template>
 
<script>
export default {
  data() {
    return {
      users: this.listUsers(),
      executive_dashboards: this.listAllExecutiveDashboards(),
      selected_executive_dashboard: "",
      executive_dashboard_loading: true,
      executive_dashboard_operating: false,
    };
  },
  methods: {
    deleteSelected() {
      for (
        let index = 0;
        index < this.selected_executive_dashboard.length;
        index++
      ) {
        this.deleteExecutiveDashboard(
          this.selected_executive_dashboard[index].executive_dashboard_id
        );
      }
      this.$emit("delete");
    },
    normalize_executive_dashboards(executive_dashboards) {
      for (let index = 0; index < executive_dashboards.length; index++) {
        for (var key in executive_dashboards[index]) {
          if (key === "user") {
            executive_dashboards[index][key] = this.enumUser(
              executive_dashboards[index][key]
            );
          }
          if (key === "access_user_list") {
            var tmp_list = [];
            for (let i = 0; i < executive_dashboards[index][key].length; i++) {
              tmp_list.push(this.enumUser(executive_dashboards[index][key][i]));
            }
            executive_dashboards[index][key] = tmp_list;
          }
          if (key === "access_business_unit_list") {
            tmp_list = [];
            for (let i = 0; i < executive_dashboards[index][key].length; i++) {
              tmp_list.push(this.enumUser(executive_dashboards[index][key][i]));
            }
            executive_dashboards[index][key] = tmp_list;
          }
        }
      }
      return executive_dashboards;
    },
    enumUser(user) {
      for (let i = 0; i < this.users.length; i++) {
        if (this.users[i]["user_id"] === user) {
          return this.users[i]["email"];
        }
      }
      return user;
    },
    deleteExecutiveDashboard(executive_dashboard_id) {
      if (executive_dashboard_id === undefined) {
        this.$toast.add({
          severity: "warn",
          summary: "No Executive Dashboard selected",
          detail: "Please select Executive Dashboard first",
          life: 3000,
        });
      } else {
        this.executive_dashboard_operating = true;
      }
      this.$axios
        .delete("/delete_executive_dashboard/" + executive_dashboard_id)
        .then(() => {
          this.listAllExecutiveDashboards();
          if (this.executive_dashboard_operating == true) {
            this.$toast.add({
              severity: "success",
              summary: "Executive Dashboard Deletion Successful",
              detail: "The selected Executive Dashboard was deleted",
              life: 3000,
            });
          }
          this.executive_dashboard_operating = false;
          this.selected_executive_dashboard = "";
        })
        .catch(() => {
          this.executive_dashboard_operating = false;
          this.$toast.add({
            severity: "error",
            summary: "Executive Dashboard Deletion Unsuccessful",
            detail: "The selected Executive Dashboard could not be deleted",
            life: 3000,
          });
          this.selected_executive_dashboard = "";
        });
    },
    UpdateSelectedExecutiveDashboard(executive_dashboard_id) {
      if (executive_dashboard_id === undefined) {
        this.$toast.add({
          severity: "warn",
          summary: "No Executive Dashboard selected",
          detail: "Please select Executive Dashboard first",
          life: 3000,
        });
      }
      //TODO
    },
    listUsers() {
      this.$axios.get("/users").then((res) => {
        this.users = res.data;
      });
    },
    listAllExecutiveDashboards() {
      this.$axios.get("/get_executive_dashboards").then((res) => {
        this.executive_dashboards = this.normalize_executive_dashboards(
          res.data.data
        );
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
</style>