<template>
  <div>
    <span v-if="alreadyRendered === false">
      {{ this.getDeparmtentApplicationRankingData() }}
    </span>
    <div class="p-fluid">
      <div id="chart-pie">
        <apexchart
          :type="chart_type"
          :options="chartOptions"
          :series="data_for_chart"
        ></apexchart>
      </div>
    </div>
  </div>
</template>
<script>
export default {
  props: ["selected_dataset_id", "selected_dataset_label"],
  data() {
    return {
      alreadyRendered: false,
      title_chart: "Departments by # of Applications",
      subtitle_chart: "",
      legend_show_chart: true,
      data_for_chart: [],
      chart_type: "pie",
      chart_width: "800",
      chart_height: "800",
      xaxis_categories: [],
      input_fields_id: "",
      input_fields: false,
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
        labels: ["Initiating..."],
        // responsive: [
        //   {
        //     breakpoint: 480,
        //     options: {
        //       chart: {},
        //       legend: {
        //         position: "bottom",
        //       },
        //     },
        //   },
        // ],
      },
      deparmtentApplicationRankingDataInternal: [],
      chartOptionsPieChartInternal: {
        chart: {
          type: "pie",
          width: "800",
        },
        labels: ["Initiating..."],
        // responsive: [
        //   {
        //     breakpoint: 480,
        //     options: {
        //       chart: {},
        //       legend: {
        //         position: "bottom",
        //       },
        //     },
        //   },
        // ],
      },
    };
  },
  methods: {
    // normalize_selected_dataset() {
    //   this.selected_dataset_id = this.selected_dataset.dataset_id;
    //   this.selected_dataset_label = this.selected_dataset.dataset_label;
    // },
    create_plot_and_save_to_executive_dashboard() {
      var formData = {};
      formData["title"] = this.title_chart;
      formData["subtitle"] = this.subtitle_chart;
      formData["legend_show"] = this.legend_show_chart;
      formData["dataset_id_for_chart"] = this.selected_dataset_id;
      formData["dataset_label"] = this.selected_dataset_label;
      formData["chart_type"] = this.chart_type;
      formData["chart_width"] = this.chart_width;
      formData["chart_height"] = this.chart_height;
      formData["xaxis_categories"] = this.xaxis_categories;
      formData["input_fields"] = this.input_fields;
      formData["input_fields_id"] = this.input_fields_id;
      console.log(formData);
      this.$emit("plotDataAsForm", formData);
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
      this.alreadyRendered = true;
    },
    getDeparmtentApplicationRankingData() {
      this.$axios
        .get("/get_data_for_app_dep_ranking/" + this.selected_dataset_id)
        .then((res) => {
          this.updateDataLabels(res.data);
          this.getDeparmtentApplicationRankingDataPieChart(res.data);
          this.updateChartOptions();
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
        this.data_for_chart.push(data[key]["y"]);
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