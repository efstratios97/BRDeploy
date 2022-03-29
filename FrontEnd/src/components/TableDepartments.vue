<template>
  <DataTable
    :value="departments"
    v-model:selection="selected_department"
    dataKey="department_id"
    :paginator="true"
    :rows="10"
    filterDisplay="menu"
    paginatorTemplate="FirstPageLink PrevPageLink PageLinks NextPageLink LastPageLink CurrentPageReport RowsPerPageDropdown"
    :rowsPerPageOptions="[10, 25, 50]"
    currentPageReportTemplate="Showing {first} to {last} of {totalRecords} entries"
    responsiveLayout="scroll"
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
      <span v-if="departments_loading">
        Loading Departments. Please wait.
        <ProgressBar mode="indeterminate" />
      </span>
      <span v-else> There are no departmens. </span>
    </template>
    <template #loading>
      Loading Departments. Please wait.
      <ProgressBar mode="indeterminate" />
    </template>
    <Column selectionMode="single" headerStyle="width: 3em"></Column>
    <Column field="department_id" header="ID" sortable style="min-width: auto">
    </Column>
    <Column field="name" header="Name" sortable style="min-width: auto">
    </Column>
    <Column header="Ad hoc Operations" style="min-width: auto">
      <template #body>
        <div class="btn-align-td">
          <button
            v-on:click="deleteDep(this.selected_department.name)"
            class="btn btn-secondary"
            v-tooltip="'Select Department first'"
          >
            <b-icon-trash-fill />
          </button>
        </div>
      </template>
    </Column>
  </DataTable>
</template>
 
<script>
export default {
  data() {
    return {
      departments: this.listDepartments(),
      selected_department: "",
      departments_loading: true,
      dep_operations: false,
    };
  },
  methods: {
    deleteDep(dep_name) {
      if (dep_name === undefined) {
        this.$toast.add({
          severity: "warn",
          summary: "No Department selected",
          detail: "Please select Department first",
          life: 3000,
        });
      } else {
        this.dep_operations = true;
      }
      this.$axios
        .delete(
          "/delete_department/" + dep_name + "/" + localStorage.loggedUser
        )
        .then(() => {
          this.listDepartments();
          if (this.dep_operations === true) {
            this.$toast.add({
              severity: "success",
              summary: "Department Deletion Successful",
              detail: "The selected Department: " + dep_name + " was deleted",
              life: 3000,
            });
          }
        })
        .catch(() => {
          this.dataset_operating = false;
          this.$toast.add({
            severity: "error",
            summary: "Department Deletion Unsuccessful",
            detail:
              "The selected Department: " +
              dep_name +
              " could not be deleted!\n Check if you have admin rights",
            life: 3000,
          });
        });
    },
    listDepartments() {
      this.$axios.get("/departments").then((res) => {
        this.departments = res.data;
        if (this.departments.length === 0) {
          this.departments_loading = false;
        }
      });
    },
  },
};
</script>
<style>
button {
  color: white;
  background: #0c8cd3;
  border: 0px solid blue;
  border-radius: 2px;
}
</style>