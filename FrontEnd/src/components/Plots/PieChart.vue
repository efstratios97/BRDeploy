<template>
  <div>
    <div v-if="this.excecutive_dashboard !== undefined">
      <span v-if="alreadyRendered === false">
        {{ this.getDeparmtentApplicationRankingData() }}
      </span>
      <div class="p-fluid">
        <div id="chart-pie">
          <apexchart
            type="pie"
            width="800"
            :options="chartOptionsPieChartInternal"
            :series="deparmtentApplicationRankingDataInternal"
          ></apexchart>
        </div>
      </div>
    </div>
    <div v-else>
      <div class="p-fluid">
        <div id="chart-pie">
          <apexchart
            type="pie"
            width="800"
            :options="chartOptionsPieChart"
            :series="deparmtentApplicationRankingDataPieChart"
          ></apexchart>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
export default {
  props: [
    "selected_dataset",
    "deparmtentApplicationRankingDataPieChart",
    "chartOptionsPieChart",
    "excecutive_dashboard",
  ],
  data() {
    return {
      alreadyRendered: false,
      deparmtentApplicationRankingDataInternal: [],
      chartOptionsPieChartInternal: {
        chart: {
          type: "pie",
        },
        labels: ["Initiating..."],
        responsive: [
          {
            breakpoint: 480,
            options: {
              chart: {},
              legend: {
                position: "bottom",
              },
            },
          },
        ],
      },
    };
  },
  methods: {
    getDeparmtentApplicationRankingData() {
      this.$axios
        .get("/get_data_for_app_dep_ranking/" + this.selected_dataset)
        .then((res) => {
          this.updateDataLabels(res.data);
          this.getDeparmtentApplicationRankingDataPieChart(res.data);
          this.$toast.add({
            severity: "success",
            summary: "Departments by # of Application Analysis Successful",
            detail:
              "The Departments by # of Application Analysis was successful",
            life: 3000,
          });
          this.alreadyRendered = true;
        })
        .catch(() => {
          this.$toast.add({
            severity: "error",
            summary: "Departments by # of Application Analysis Unsuccessful",
            detail: "Please click Back and re-select a dataset!",
            life: 8000,
          });
        });
    },
    getDeparmtentApplicationRankingDataPieChart(data) {
      for (const key of Object.keys(data)) {
        this.deparmtentApplicationRankingDataInternal.push(data[key]["y"]);
      }
    },
    updateDataLabels(data) {
      var labels = [];
      for (const key of Object.keys(data)) {
        labels.push(data[key]["x"]);
      }
      this.chartOptionsPieChartInternal = {
        ...this.chartOptionsPieChartInternal,
        ...{
          labels: labels,
        },
      };
    },
  },
};
</script>