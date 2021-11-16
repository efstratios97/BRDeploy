<template>
  <div>
    <span v-if="alreadyRendered === false">
      <!-- {{ this.getDataForView() }} -->
    </span>
    <div class="p-fluid">
      <div>
        <apexchart :options="chartOptions" :series="data_chart"></apexchart>
      </div>
    </div>
  </div>
</template>
<script>
export default {
  props: ["selected_dataset_id", "selected_dataset_label"],
  data() {
    return {
      // selected_dataset_id: "",
      // selected_dataset_label: "",
      alreadyRendered: false,
      title_chart: "Rendering Data....",
      subtitle_chart: "Please wait...",
      legend_show_chart: false,
      data_for_chart: [{ x: "Initiating...", y: 1 }],
      chart_type: "bar",
      chart_width: "150%",
      chart_height: "150%",
      xaxis_categories: [],
      data_chart: [
        {
          data: this.data_for_chart,
        },
      ],
      chartOptions: {
        chart: {
          type: this.chart_type,
          width: this.chart_width,
          height: this.chart_height,
        },
        legend: {
          show: this.legend_show_chart,
        },
        xaxis: {
          categories: this.xaxis_categories,
        },
      },
    };
  },
  methods: {
    getDataForView() {
      this.$axios
        .get(
          "/get_data_for_view/" +
            this.selected_dataset_id +
            "/" +
            this.selected_dataset_label +
            "/" +
            "bar"
        )
        .then((res) => {
          this.data_chart = [{ data: res.data }];
          console.log(this.data_chart);
          this.$toast.add({
            severity: "success",
            summary: "Departments by # of Application Analysis Successful",
            detail:
              "The Departments by # of Application Analysis was successful",
            life: 3000,
          });
          this.updateChartOptions();
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
    updateChartOptions() {
      this.chartOptions = {
        ...this.chartOptions,
        ...{
          chart: {
            type: this.chart_type,
            width: this.chart_width,
            height: this.chart_height,
          },
          legend: {
            show: this.legend_show_chart,
          },
          xaxis: {
            categories: this.xaxis_categories,
          },
        },
      };
      this.retrievingGraph = false;
    },
  },
};
</script>
