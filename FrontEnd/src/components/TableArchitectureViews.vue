<template>
  <DataTable
    :value="architecture_views"
    v-model:selection="selected_architecture_view"
    dataKey="architecture_view_id"
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
        <h5 class="p-m-0">Architecture Views</h5>
        <span class="p-input-icon-left">
          <i class="pi pi-search" />
          <InputText placeholder="Keyword Search" />
        </span>
      </div>
    </template>
    <template #empty>
      <span v-if="architecture_view_loading">
        Loading Architecture Views. Please wait.
        <ProgressBar mode="indeterminate" />
      </span>
      <span v-else> There are no Architecture Views. </span>
    </template>
    <template #loading>
      Loading Architecture Views. Please wait.
      <ProgressBar mode="indeterminate" />
    </template>
    <Column selectionMode="single" style="min-width: 3rem"></Column>
    <Column
      field="architecture_view_id"
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
      field="components"
      header="Architecture Views Components"
      style="min-width: auto"
    >
      <template #body="slotProps">
        <Dropdown
          :options="slotProps.data.components"
          placeholder="Components"
        />
      </template>
    </Column>

    <Column header="Ad hoc Operations" style="min-width: auto">
      <template #body>
        <div class="btn-align-td">
          <button
            v-on:click="
              deleteArchitectureView(
                this.selected_architecture_view.architecture_view_id
              )
            "
            class="btn btn-secondary"
            v-tooltip="'Select Architecture View first'"
          >
            <b-icon-trash-fill />
          </button>
        </div>
        <ProgressBar mode="indeterminate" v-if="architecture_view_operating" />
      </template>
    </Column>
  </DataTable>
</template>
 
<script>
export default {
  data() {
    this.listArchitectureViews();
    return {
      architecture_views: "",
      selected_architecture_view: "",
      architecture_view_loading: true,
      architecture_view_operating: false,
    };
  },
  methods: {
    normalizeArchitectureViews() {
      for (let index = 0; index < this.architecture_views.length; index++) {
        for (var key in this.architecture_views[index]) {
          if (key === "components") {
            this.architecture_views[index][key] = this.architecture_views[
              index
            ][key].split(",");
          }
        }
      }
    },
    deleteArchitectureView(architecture_view_id) {
      if (architecture_view_id === undefined) {
        this.$toast.add({
          severity: "warn",
          summary: "No Architecture View selected",
          detail: "Please select Architecture View first",
          life: 3000,
        });
      } else {
        this.architecture_view_operating = true;
      }
      this.$axios
        .delete("/delete_architecture_view/" + architecture_view_id)
        .then(() => {
          if (this.architecture_view_operating == true) {
            this.$toast.add({
              severity: "success",
              summary: "Architecture View successfully deleted",
              detail: "Architecture View was successfully deleted",
              life: 3000,
            });
          }
          this.architecture_view_operating = false;
          this.selected_architecture_view = "";
          this.listArchitectureViews();
          this.$emit("close");
        })
        .catch(() => {
          this.architecture_view_operating = false;
          this.$toast.add({
            severity: "error",
            summary: "Architecture View Deletion Unsuccessful",
            detail: "The selected Architecture View could not be deleted",
            life: 3000,
          });
          this.selected_architecture_view = "";
        });
    },
    strToList(strings) {
      const list_string = strings.split(",");
      return list_string;
    },
    listArchitectureViews() {
      this.$axios.get("/get_architecture_views").then((res) => {
        this.architecture_views = res.data.data;
        this.normalizeArchitectureViews();
        if (this.architecture_views.length === 0) {
          this.architecture_view_loading = false;
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