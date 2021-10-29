<template>
  <div>
    <div v-if="this.excecutive_dashboard !== undefined">
      <span v-if="alreadyRendered === false">
        {{ this.getDeparmtentApplicationRankingData() }}
      </span>
      <div class="p-fluid">
        <div id="chart-bar">
          <apexchart
            type="bar"
            height="350"
            :options="chartOptionsInternal"
            :series="deparmtentApplicationRankingDataInternal"
          ></apexchart>
        </div>
      </div>
    </div>
    <div v-else>
      <div class="p-fluid">
        <div id="chart-bar">
          <apexchart
            type="bar"
            height="350"
            :options="chartOptions"
            :series="deparmtentApplicationRankingData"
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
    "deparmtentApplicationRankingData",
    "chartOptions",
    "excecutive_dashboard",
  ],
  data() {
    return {
      alreadyRendered: false,
      deparmtentApplicationRankingDataInternal: [
        {
          data: [{ x: "Initiating...", y: 1 }],
        },
      ],
      chartOptionsInternal: {
        legend: {
          show: false,
        },
        title: {
          text: "Departments by # of Applications",
        },
      },
    };
  },
  methods: {
    getDeparmtentApplicationRankingData() {
      this.$axios
        .get("/get_data_for_app_dep_ranking/" + this.selected_dataset)
        .then((res) => {
          this.deparmtentApplicationRankingDataInternal = [{ data: res.data }];
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
  },
};
</script>