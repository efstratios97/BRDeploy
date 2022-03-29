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
      field="dataset_choice_rule"
      header="Dataset Choice Rule"
      sortable
      style="min-width: auto"
    >
    </Column>
    <Column
      field="dataset_label"
      header="Associated Dataset Label"
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
      items: [
        {
          label: "Add",
          icon: "pi pi-trash",
          command: () => {
            this.deleteSelected();
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
        this.selected_executive_dashboard.length === 1 &&
        this.selected_executive_dashboard.length !== 0
      ) {
        this.$emit("update", this.selected_executive_dashboard[0]);
      } else {
        this.$toast.add({
          severity: "warn",
          summary: "None or More than 1 Executive Dashboard selected",
          detail: "Please select only one Executive Dashboard to display",
          life: 4000,
        });
      }
    },
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
      if (executive_dashboards === undefined) {
        this.listAllExecutiveDashboards();
      }
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
      this.executive_dashboard_loading = false;
      return executive_dashboards;
    },
    enumUser(user) {
      if (this.users === undefined) {
        this.listUsers();
      } else {
        for (let i = 0; i < this.users.length; i++) {
          if (this.users[i]["user_id"] === user) {
            return this.users[i]["email"];
          }
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
          this.executive_dashboard_loading = false;
          this.$emit("delete");
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
        this.executive_dashboard_loading = false;
      });
    },
  },
};
</script>

<style scoped>
.btn-align-td {
  display: inline-block;
  margin: 2px;
}
</style>