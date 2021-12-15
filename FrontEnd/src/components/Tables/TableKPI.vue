<template>
  <DataTable
    :value="kpis"
    v-model:selection="selected_kpis"
    dataKey="kpi.kpi_id"
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
        <h5 class="p-m-0">KPIs</h5>
        <span class="p-input-icon-left">
          <i class="pi pi-search" />
          <InputText placeholder="Keyword Search" />
        </span>
      </div>
    </template>
    <template #empty>
      <span v-if="kpis_loading">
        Loading KPIs. Please wait.
        <ProgressBar mode="indeterminate" />
      </span>
      <span v-else> There are no KPIs. </span>
    </template>
    <template #loading>
      Loading KPIs. Please wait.
      <ProgressBar mode="indeterminate"
    /></template>
    <Column selectionMode="multiple" headerStyle="width: 3em"></Column>
    <Column field="kpi.kpi_id" header="ID" sortable style="min-width: auto">
    </Column>
    <Column field="kpi.name" header="Name" sortable style="min-width: auto">
    </Column>
    <Column
      field="kpi.description"
      header="Description"
      sortable
      style="min-width: auto"
    >
    </Column>
    <Column
      field="kpi.kpi_aspects_weights"
      header="Aspects - Weights"
      headerStyle="min-width: 4rem; text-align: center"
      bodyStyle="text-align: center; overflow: visible; color:black"
    >
      <template #body="slotProps">
        <Dropdown
          :options="slotProps.data.kpi.kpi_aspects_weights"
          placeholder="Aspects - Weights"
        />
      </template>
    </Column>
    <Column
      field="kpi.threshold"
      header="Threshold"
      sortable
      style="min-width: auto"
    >
    </Column>
    <Column
      field="kpi.formula"
      header="Formula"
      sortable
      style="min-width: auto"
    >
    </Column>
    <Column
      field="kpi.color_coding"
      header="Color Coding"
      sortable
      style="min-width: auto"
    >
    </Column>
    <Column header="Ad hoc Operations" style="min-width: auto">
      <template #body>
        <div class="btn-align-td">
          <button
            v-on:click="UpdateSelectedKPI()"
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
        <ProgressBar mode="indeterminate" v-if="kpis_operating" />
      </template>
    </Column>
  </DataTable>
</template>
 
<script>
export default {
  props: ["selected_dataset_id", "selected_dataset_label"],
  data() {
    return {
      kpis: this.get_kpis(),
      selected_kpis: "",
      kpis_loading: true,
      kpis_operating: false,
    };
  },
  methods: {
    deleteSelected() {
      for (let index = 0; index < this.selected_kpis.length; index++) {
        this.deleteKPI(this.selected_kpis[index].kpi.kpi_id);
      }
      this.$emit("delete");
    },
    deleteKPI(kpi_id) {
      if (kpi_id === undefined) {
        this.$toast.add({
          severity: "warn",
          summary: "No KPI selected",
          detail: "Please select KPI first",
          life: 3000,
        });
      } else {
        this.kpis_operating = true;
      }
      this.$axios
        .delete("/delete_kpi/" + kpi_id)
        .then(() => {
          if (this.kpis_operating == true) {
            this.$toast.add({
              severity: "success",
              summary: "KPI Deletion Successful",
              detail: "The selected KPI was deleted",
              life: 3000,
            });
          }
          this.kpis_operating = false;
          this.selected_kpis = "";
          this.get_kpis();
        })
        .catch(() => {
          this.kpis_operating = false;
          this.$toast.add({
            severity: "error",
            summary: "KPI Deletion Unsuccessful",
            detail: "The selected KPI could not be deleted",
            life: 3000,
          });
          this.selected_kpis = "";
        });
      this.get_kpis();
    },
    UpdateSelectedKPI(kpi_id) {
      if (kpi_id === undefined) {
        this.$toast.add({
          severity: "warn",
          summary: "No KPI selected",
          detail: "Please select KPI first",
          life: 3000,
        });
      }
      //TODO
    },
    get_kpis() {
      this.kpis_loading = true;
      this.$axios
        .get("/get_kpis_by_dataset_label/" + this.selected_dataset_label)
        .then((res) => {
          var kpis_tmp = [];
          for (let index = 0; index < res.data.data.length; index++) {
            kpis_tmp.push({ kpi: res.data.data[index] });
          }
          this.kpis = kpis_tmp;
          this.kpis_loading = false;
        });
    },
    close() {
      this.$emit("close");
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