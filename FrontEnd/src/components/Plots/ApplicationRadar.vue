<template>
  <span v-if="retrievingGraph == false">
    <form class="overflow-auto">
      <MultiSelect
        v-model="selected_apps"
        :options="apps"
        :filter="true"
        optionLabel="app"
        placeholder="Select Applications"
        filterPlaceholder="Find an Application"
        class="multiselect-custom"
        :showClear="true"
      />

      <Button
        label="Apply"
        @click="getRadarDataMultiple"
        icon="pi pi-check"
        iconPos="right"
      />
    </form>
    <div class="p-fluid">
      <div>
        <apexchart
          :type="radar"
          width="1200"
          :options="chartOptionsRadarMultiple"
          :series="radarDataMultiple"
        ></apexchart>
      </div>
    </div>
  </span>
  <span v-else>
    <ProgressBar mode="indeterminate" />
  </span>
</template>
<script>
export default {
  props: ["selected_dataset_id", "selected_dataset_label"],
  data() {
    this.getApps();
    return {
      retrievingGraph: false,
      selected_apps: "",
      apps: "",
      radarDataMultiple: [{ data: [1, 1, 1] }],
      chartOptionsRadarMultiple: {
        chart: {
          type: "radar",
          width: "250%",
        },
        title: { text: "" },
        xaxis: {
          categories: ["Initiating...", "Initiating...", "Initiating..."],
        },
      },
    };
  },
  methods: {
    getRadarDataMultiple() {
      this.radarDataMultiple = [];
      this.retrievingGraph = true;
      for (let index = 0; index < this.selected_apps.length; index++) {
        var selected_app = this.selected_apps[index].app;
        this.$axios
          .get(
            "/get_data_for_radar_app/" +
              this.selected_dataset_id +
              "/" +
              selected_app
          )
          .then((res) => {
            var data = res.data[0].data.map(function (x) {
              return parseInt(x);
            });
            this.radarDataMultiple.push({
              data: data,
              name: this.selected_apps[index].app,
            });
            this.updateChartOptionsRadarMultiple(res.data[1].labels);
            this.$toast.add({
              severity: "success",
              summary: "ApplicationRadar Analysis Successful",
              detail: "The ApplicationRadar Analysis was successful",
              life: 3000,
            });
          })
          .catch(() => {
            this.$toast.add({
              severity: "error",
              summary: "ApplicationRadar Analysis Unsuccessful",
              detail:
                "Select Parameters OR  click Back and re-select a dataset!",
              life: 3000,
            });
          });
      }
    },
    updateChartOptionsRadarMultiple(data) {
      this.chartOptionsRadarMultiple = {
        ...this.chartOptionsRadarMultiple,
        ...{
          xaxis: {
            categories: data,
          },
        },
      };
      this.retrievingGraph = false;
    },
    getApps() {
      this.$axios
        .get("/get_applications/" + this.selected_dataset_id)
        .then((res) => {
          var apps_tmp = [];
          for (let index = 0; index < res.data.length; index++) {
            apps_tmp.push({ app: res.data[index] });
          }
          this.apps = apps_tmp;
        });
    },
  },
};
</script>
