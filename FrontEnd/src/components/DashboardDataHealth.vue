<template>
  <div>
    <TabView class="tabview-custom" ref="tabview4">
      <TabPanel>
        <template #header>
          <b-icon-pie-chart style="font-size: 18px; margin: 3px" />
          <span><h4>Departments by # of Applications</h4></span>
        </template>
        <div class="container-...">
          <div class="row row-cols-auto auto-cols-adj">
            <Card class="component-card">
              <template v-slot:title> Treemap </template>
              <template v-slot:subtitle>
                Departments by # of Applications as Treemap representation
              </template>
              <template v-slot:content>
                <tree-map
                  :selected_dataset="selected_dataset"
                  :deparmtentApplicationRankingData="
                    deparmtentApplicationRankingData
                  "
                  :chartOptions="chartOptions"
                ></tree-map>
              </template>
              <template v-slot:footer> </template>
            </Card>
            <Card class="component-card">
              <template v-slot:title> BarChart </template>
              <template v-slot:subtitle>
                Departments by # of Applications as BarChart representation
              </template>
              <template v-slot:content>
                <bar-chart
                  :selected_dataset="selected_dataset"
                  :deparmtentApplicationRankingData="
                    deparmtentApplicationRankingData
                  "
                  :chartOptions="chartOptions"
                ></bar-chart>
              </template>
              <template v-slot:footer> </template>
            </Card>
            <Card class="component-card centered-chart">
              <template v-slot:title> PieChart </template>
              <template v-slot:subtitle>
                Departments by # of Applications as PieChart representation
              </template>
              <template v-slot:content>
                <pie-chart
                  :selected_dataset="selected_dataset"
                  :deparmtentApplicationRankingDataPieChart="
                    deparmtentApplicationRankingDataPieChart
                  "
                  :chartOptionsPieChart="chartOptionsPieChart"
                ></pie-chart>
              </template>
              <template v-slot:footer> </template>
            </Card>
          </div>
        </div>
      </TabPanel>
      <TabPanel>
        <template #header>
          <b-icon-compass style="font-size: 18px; margin: 3px" />
          <span><h4>Examine Application Status</h4></span>
        </template>
        <div class="container-...">
          <div class="row row-cols-auto auto-cols-adj">
            <Card class="component-card centered-chart">
              <template v-slot:title> ApplicationRadar </template>
              <template v-slot:subtitle>
                # of Key Characteristics of multiple Apps
              </template>
              <template v-slot:content>
                <application-radar
                  :selected_dataset="selected_dataset"
                ></application-radar>
              </template>
            </Card>
          </div>
        </div>
      </TabPanel>
      <TabPanel>
        <template #header>
          <b-icon-columns style="font-size: 18px; margin: 3px" />
          <span><h4>Analyze Architecture Views Applicability</h4></span>
        </template>
        <architecture-views-applicability-analysis
          :selected_dataset="selected_dataset"
          :key="componentKey"
        ></architecture-views-applicability-analysis>
      </TabPanel>
      <TabPanel>
        <template #header>
          <b-icon-upc style="font-size: 18px; margin: 3px" />
          <span><h4>Architecture Views</h4></span>
        </template>
        <architecture-views
          :selected_dataset="selected_dataset"
          @close="increaseComponentKey"
        ></architecture-views>
      </TabPanel>
    </TabView>
    <div class="p-grid p-nogutter p-justify-between">
      <Button label="Back" @click="prevPage()" icon="pi pi-angle-left" />
    </div>
    <br />
  </div>
</template>
<script>
import PieChart from "../components/Plots/PieChart.vue";
import TreeMap from "../components/Plots/TreeMap.vue";
import BarChart from "../components/Plots/BarChart.vue";
import ApplicationRadar from "../components/Plots/ApplicationRadar.vue";
import ArchitectureViews from "../components/DashboardComponents/ArchitectureViews.vue";
import ArchitectureViewApplicabilityAnalysis from "../components/Plots/ArchitectureViewApplicabilityAnalysis.vue";

export default {
  props: ["selected_dataset"],
  components: {
    "pie-chart": PieChart,
    "tree-map": TreeMap,
    "bar-chart": BarChart,
    "application-radar": ApplicationRadar,
    "architecture-views": ArchitectureViews,
    "architecture-views-applicability-analysis": ArchitectureViewApplicabilityAnalysis,
  },
  data() {
    this.getDeparmtentApplicationRankingData();
    return {
      componentKey: 0,
      deparmtentApplicationRankingData: [
        {
          data: [{ x: "Initiating...", y: 1 }],
        },
      ],
      chartOptions: {
        legend: {
          show: false,
        },
        title: {
          text: "Departments by # of Applications",
        },
      },
      deparmtentApplicationRankingDataPieChart: [],
      chartOptionsPieChart: {
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
    prevPage() {
      this.$emit("prev-page", { pageIndex: 1 });
    },
    increaseComponentKey() {
      console.log("hi");
      this.componentKey += 1;
    },
    getDeparmtentApplicationRankingData() {
      console.log(this.selected_dataset);
      this.$axios
        .get("/get_data_for_app_dep_ranking/" + this.selected_dataset)
        .then((res) => {
          this.deparmtentApplicationRankingData = [{ data: res.data }];
          this.updateDataLabels(res.data);
          this.getDeparmtentApplicationRankingDataPieChart(res.data);
          this.$toast.add({
            severity: "success",
            summary: "Departments by # of Application Analysis Successful",
            detail:
              "The Departments by # of Application Analysis was successful",
            life: 3000,
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
    getDeparmtentApplicationRankingDataPieChart(data) {
      for (const key of Object.keys(data)) {
        this.deparmtentApplicationRankingDataPieChart.push(data[key]["y"]);
      }
    },
    updateDataLabels(data) {
      var labels = [];
      for (const key of Object.keys(data)) {
        labels.push(data[key]["x"]);
      }
      this.chartOptionsPieChart = {
        ...this.chartOptionsPieChart,
        ...{
          labels: labels,
        },
      };
    },
  },
};
</script>
<style scoped>
.component-card {
  margin-top: 30px;
  position: relative;
  display: flex;
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
}

.centered-chart {
  align-items: center;
}

.p-multiselect {
  max-width: 800px;
}

.p-multiselect-label:not(.p-placeholder) {
  padding-top: 0.25rem;
  padding-bottom: 0.25rem;
}
.selected-item-value {
  padding: 0.25rem 0.5rem;
  border-radius: 3px;
  /* display: inline-block; */
  margin-bottom: 0.5rem;
  background-color: var(--primary-color);
  color: var(--primary-color-text);
}

@media screen and (max-width: 900px) {
  .p-multiselect {
    width: 100%;
  }
}
</style>