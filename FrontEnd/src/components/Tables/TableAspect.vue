<template>
  <DataTable
    :value="aspects"
    v-model:selection="selected_aspects"
    dataKey="aspect.aspect_id"
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
        <h5 class="p-m-0">Aspects</h5>
        <span class="p-input-icon-left">
          <i class="pi pi-search" />
          <InputText placeholder="Keyword Search" />
        </span>
      </div>
    </template>
    <template #empty>
      <span v-if="aspect_loading">
        Loading KPIs. Please wait.
        <ProgressBar mode="indeterminate" />
      </span>
      <span v-else> There are no Aspects. </span>
    </template>
    <template #loading>
      Loading Aspects. Please wait.
      <ProgressBar mode="indeterminate"
    /></template>
    <Column selectionMode="multiple" headerStyle="width: 3em"></Column>
    <Column
      field="aspect.aspect_id"
      header="ID"
      sortable
      style="min-width: auto"
    >
    </Column>
    <Column field="aspect.name" header="Name" sortable style="min-width: auto">
    </Column>
    <Column
      field="aspect.description"
      header="Description"
      sortable
      style="min-width: auto"
    >
    </Column>
    <Column
      field="aspect.raw_components_from_dataset"
      header="Raw Components - Operation Type"
      headerStyle="min-width: 4rem; text-align: center"
      bodyStyle="text-align: center; overflow: visible; color:black"
    >
      <template #body="slotProps">
        <Dropdown
          :options="slotProps.data.aspect.raw_components_from_dataset"
          placeholder="Raw Components - Operation Type"
        />
      </template>
    </Column>
    <Column
      field="aspect.skala_size"
      header="Scale"
      sortable
      style="min-width: auto"
    >
    </Column>
    <Column
      field="aspect.formula"
      header="Formula"
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
        <ProgressBar mode="indeterminate" v-if="aspects_operating" />
      </template>
    </Column>
  </DataTable>
</template>
 
<script>
export default {
  props: ["selected_dataset_id", "selected_dataset_label"],
  data() {
    return {
      aspects: this.get_aspects(),
      selected_aspects: "",
      aspect_loading: true,
      aspects_operating: false,
    };
  },
  methods: {
    deleteSelected() {
      for (let index = 0; index < this.selected_aspects.length; index++) {
        this.deleteAspect(this.selected_aspects[index].aspect.aspect_id);
      }
      this.$emit("delete");
    },
    deleteAspect(aspect_id) {
      if (aspect_id === undefined) {
        this.$toast.add({
          severity: "warn",
          summary: "No Aspect selected",
          detail: "Please select Aspect first",
          life: 3000,
        });
      } else {
        this.aspects_operating = true;
      }
      this.$axios
        .delete("/delete_aspect/" + aspect_id)
        .then(() => {
          if (this.aspects_operating == true) {
            this.$toast.add({
              severity: "success",
              summary: "Aspect Deletion Successful",
              detail: "The selected Aspect was deleted",
              life: 3000,
            });
          }
          this.aspects_operating = false;
          this.selected_aspects = "";
          this.get_aspects();
        })
        .catch(() => {
          this.aspects_operating = false;
          this.$toast.add({
            severity: "error",
            summary: "Aspect Deletion Unsuccessful",
            detail: "The selected Aspect could not be deleted",
            life: 3000,
          });
          this.selected_aspects = "";
        });
      this.get_aspects();
    },
    UpdateSelectedKPI(aspect_id) {
      if (aspect_id === undefined) {
        this.$toast.add({
          severity: "warn",
          summary: "No Aspect selected",
          detail: "Please select Aspect first",
          life: 3000,
        });
      }
      //TODO
    },
    get_aspects() {
      this.aspect_loading = true;
      this.$axios
        .get("/get_aspects_by_dataset_label/" + this.selected_dataset_label)
        .then((res) => {
          var aspects_tmp = [];
          for (let index = 0; index < res.data.data.length; index++) {
            aspects_tmp.push({ aspect: res.data.data[index] });
          }
          this.aspects = aspects_tmp;
          this.aspect_loading = false;
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