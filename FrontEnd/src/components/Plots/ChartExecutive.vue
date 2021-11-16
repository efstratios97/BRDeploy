<template>
  <div>
    <span v-if="alreadyRendered === false">
      {{ this.get_plot_chart_options() }}
    </span>
    <div class="p-fluid">
      <div>
        <apexchart
          :type="chart_type"
          :options="chartOptions"
          :series="data_chart"
        ></apexchart>
      </div>
    </div>
  </div>
</template>
<script>
export default {
  props: ["plot_id"],
  data() {
    return {
      alreadyRendered: false,
      title_chart: "Rendering Data....",
      subtitle_chart: "Please wait...",
      legend_show_chart: true,
      data_for_chart: [{ x: "Initiating...", y: 1 }],
      chart_type: "bar",
      chart_width: "400",
      chart_height: "400",
      xaxis_categories: [],
      dataset_id_for_chart: "",
      dataset_label: "",
      input_fields: false,
      input_fields_id: "",
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
    get_plot_chart_options() {
      this.$axios
        .get("/get_plot/" + this.plot_id.plot_id)
        .then((res) => {
          // this.chart_height = res.data.chart_height;
          // this.chart_width = res.data.chart_width;
          this.chart_type = res.data.chart_type;
          // this.legend_show_chart = res.data.legend_show_chart;
          this.dataset_id_for_chart = res.data.dataset_id_for_chart;
          this.dataset_label = res.data.dataset_label;
          this.subtitle_chart = res.data.subtitle;
          this.title_chart = res.data.title;
          this.xaxis_categories = res.data.xaxis_categories;
          this.getDataForView();
          // this.updateChartOptions();
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
    getDataForView() {
      this.$axios
        .get(
          "/get_data_for_view/" +
            this.dataset_id_for_chart +
            "/" +
            this.dataset_label +
            "/" +
            this.chart_type +
            "/" +
            "none"
        )
        .then((res) => {
          if (this.chart_type === "pie") {
            this.data_chart = [];
            this.updateDataLabels(res.data);
            this.getDeparmtentApplicationRankingDataPieChart(res.data);
          } else {
            this.data_chart = [{ data: res.data }];
          }
          this.updateChartOptions();
          this.alreadyRendered = true;
          this.$emit("title_change", {
            subtitle_chart: this.subtitle_chart,
            title_chart: this.title_chart,
          });
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
            // width: this.chart_width,
            // height: this.chart_height,
          },
          legend: {
            show: true,
            position: "bottom",
          },
          xaxis: {
            categories: this.xaxis_categories,
          },
        },
      };
      this.retrievingGraph = false;
    },
    getDeparmtentApplicationRankingDataPieChart(data) {
      for (const key of Object.keys(data)) {
        this.data_chart.push(data[key]["y"]);
      }
    },
    updateDataLabels(data) {
      var labels = [];
      for (const key of Object.keys(data)) {
        labels.push(data[key]["x"]);
      }
      this.chartOptions = {
        ...this.chartOptions,
        ...{
          labels: labels,
        },
      };
    },
  },
};
</script>