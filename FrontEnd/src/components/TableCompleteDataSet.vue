<template>
  <DataTable
    :value="data"
    dataKey="dataset_id"
    :paginator="true"
    :rows="10"
    paginatorTemplate="FirstPageLink PrevPageLink PageLinks NextPageLink LastPageLink CurrentPageReport RowsPerPageDropdown"
    :rowsPerPageOptions="[10, 25, 50]"
    currentPageReportTemplate="Showing {first} to {last} of {totalRecords} entries"
    responsiveLayout="scroll"
    :globalFilterFields="['Name']"
    showGridlines
    stripedRows
    ref="dt"
    p-dataTable
    csvSeparator=";"
  >
    <template #header>
      <div class="p-d-flex p-jc-between p-ai-center">
        <h5 class="p-m-0">Dataset</h5>
        <div style="text-align: left">
          <Button
            icon="pi pi-external-link"
            label="Export"
            @click="exportCSV($event)"
          />
        </div>
      </div>
    </template>
    <Column
      v-for="col of columns"
      :field="col"
      :header="col"
      :key="col"
      sortable
    ></Column>
  </DataTable>
</template>
<script>
export default {
  props: ["dataset_id", "storage_type"],
  data() {
    this.getTableHeaders();
    return {
      columns: [],
      values: "",
      data: [],
    };
  },
  methods: {
    exportCSV() {
      this.$refs.dt.exportCSV();
    },
    getTableHeaders() {
      this.$axios
        .get("/get_dataset_df/" + this.dataset_id + "/" + this.storage_type)
        .then((res) => {
          const jsondf = JSON.parse(res.data);
          var row = {};
          for (var col in jsondf) {
            this.columns.push(col);
          }
          for (
            let index = 0;
            index < Object.keys(jsondf["Name"]).length;
            index++
          ) {
            row = {};
            this.columns.forEach(function (item) {
              row[item] = jsondf[item][index];
            });
            this.data.push(row);
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