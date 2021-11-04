<template>
  <DataTable
    :value="cleansers"
    v-model:selection="selected_cleanser"
    dataKey="cleanser_id"
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
        <h5 class="p-m-0">Cleansers</h5>
        <span class="p-input-icon-left">
          <i class="pi pi-search" />
          <InputText placeholder="Keyword Search" />
        </span>
      </div>
    </template>
    <template #empty>
      <span v-if="cleansers_loading">
        Loading Cleansers. Please wait.
        <ProgressBar mode="indeterminate" />
      </span>
      <span v-else> There are no cleansers. </span>
    </template>
    <template #loading>
      Loading Cleansers. Please wait. <ProgressBar mode="indeterminate" />
    </template>
    <Column selectionMode="multiple" style="min-width: 3rem"></Column>
    <Column field="cleanser_id" header="ID" sortable style="min-width: auto">
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
      field="datasets"
      header="Supporting Datasets"
      style="min-width: auto"
    >
      <template #body="slotProps">
        <Dropdown :options="slotProps.data.datasets" placeholder="Datasets" />
      </template>
    </Column>

    <Column header="Supporting Headers" style="min-width: auto">
      <template #body="slotProps">
        <Dropdown :options="slotProps.data.header_list" placeholder="Headers" />
      </template>
    </Column>
    <Column
      field="cleanser_operation_types"
      header="Supporting Cleansing Operations"
      style="min-width: auto"
    >
      <template #body="slotProps">
        <Dropdown
          :options="slotProps.data.cleanser_operation_types"
          placeholder="Operations"
        />
      </template>
    </Column>
    <Column header="Ad hoc Operations" style="min-width: auto">
      <template #body>
        <div class="btn-align-td">
          <button
            v-on:click="deleteSelected()"
            class="btn btn-secondary"
            v-tooltip="'Select Cleanser first'"
          >
            <b-icon-trash-fill />
          </button>
        </div>
        <ProgressBar mode="indeterminate" v-if="cleanser_operating" />
      </template>
    </Column>
  </DataTable>
</template>
 
<script>
export default {
  data() {
    return {
      cleansers: this.listCleansers(),
      selected_cleanser: "",
      cleansers_loading: true,
      cleanser_operating: false,
    };
  },
  methods: {
    normalizeCleanser() {
      for (let index = 0; index < this.cleansers.length; index++) {
        for (var key in this.cleansers[index]) {
          if (key === "header_list") {
            this.cleansers[index][key] = this.cleansers[index][key].split(",");
          }
          if (key === "datasets") {
            this.cleansers[index][key] = this.cleansers[index][key].split(",");
          }
          if (key === "cleanser_operation_types") {
            this.cleansers[index][key] = this.cleansers[index][key].split(",");
          }
        }
      }
    },
    deleteSelected() {
      for (let index = 0; index < this.selected_cleanser.length; index++) {
        this.deleteCleanser(this.selected_cleanser[index].cleanser_id);
      }
    },
    deleteCleanser(cleanser_id) {
      if (cleanser_id === undefined) {
        this.$toast.add({
          severity: "warn",
          summary: "No Cleanser selected",
          detail: "Please select Cleanser first",
          life: 3000,
        });
      } else {
        this.cleanser_operating = true;
      }
      this.$axios
        .delete("/delete_cleanser/" + cleanser_id)
        .then(() => {
          this.listCleansers();
          if (this.cleanser_operating == true) {
            this.$toast.add({
              severity: "success",
              summary: "Cleanser successfully deleted",
              detail: "Cleanser was successfully deleted",
              life: 3000,
            });
          }
          this.cleanser_operating = false;
          this.selected_cleanser = "";
        })
        .catch(() => {
          this.cleanser_operating = false;
          this.$toast.add({
            severity: "error",
            summary: "Cleanser Deletion Unsuccessful",
            detail: "The selected Cleanser could not be deleted",
            life: 3000,
          });
          this.selected_cleanser = "";
        });
    },
    strToList(strings) {
      const list_string = strings.split(",");
      return list_string;
    },
    listCleansers() {
      this.$axios.get("/get_cleansers").then((res) => {
        this.cleansers = res.data.data;
        this.normalizeCleanser();
        if (this.cleansers.length === 0) {
          this.cleansers_loading = false;
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