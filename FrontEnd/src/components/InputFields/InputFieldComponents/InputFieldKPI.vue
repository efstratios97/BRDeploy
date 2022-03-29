<template>
  <div>
    <Card class="component-card">
      <template v-slot:title> KPI </template>
      <template v-slot:subtitle> Select KPIs </template>
      <template v-slot:content>
        <form class="overflow-auto">
          <Dropdown
            v-model="selected_kpis"
            :options="kpis"
            :filter="true"
            optionLabel="kpi.name"
            placeholder="Select KPI"
            filterPlaceholder="Find a KPI"
            @change="send_kpi"
          />
        </form>
      </template>
    </Card>
  </div>
</template>
<script>
export default {
  props: ["selected_dataset_id", "selected_dataset_label"],
  data() {
    return {
      kpis: this.get_kpis(),
      selected_kpis: "",
    };
  },
  methods: {
    send_kpi() {
      this.$emit("input-kpis", this.selected_kpis);
    },
    get_kpis() {
      this.$axios
        .get("/get_kpis_by_dataset_label/" + this.selected_dataset_label)
        .then((res) => {
          var kpis_tmp = [];
          for (let index = 0; index < res.data.data.length; index++) {
            kpis_tmp.push({ kpi: res.data.data[index] });
          }
          this.kpis = kpis_tmp;
        });
    },
  },
};
</script>
<style scoped>
.component-card {
  margin-top: 30px;
  position: relative;
  display: flex;
  table-layout: fixed;
  flex-grow: 1;
  flex-direction: column;
  min-width: 0;
  word-wrap: break-word;
  background-color: #fff;
  background-clip: border-box;
  border-radius: 0.25rem;
  resize: both;
  overflow: auto;
  margin-right: 10px;
  margin-left: 10px;
  min-width: 100%;
  min-height: 175px;
}
</style>