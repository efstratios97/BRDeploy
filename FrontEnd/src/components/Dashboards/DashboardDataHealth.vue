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
                  :selected_dataset_id="selected_dataset_id"
                  :selected_dataset_label="selected_dataset_label"
                  ref="myTreeMapChart"
                  @plotDataAsForm="get_plot_data_as_form($event)"
                ></tree-map>
              </template>
              <template v-slot:footer>
                <div>
                  <Button
                    label="Assign Plot to Dashboard"
                    icon="pi pi-tag"
                    iconPos="center"
                    @click="toggleShowAddPlotToExecutiveDashboards('treemap')"
                  />
                </div>
              </template>
            </Card>
            <Card class="component-card">
              <template v-slot:title> BarChart </template>
              <template v-slot:subtitle>
                Departments by # of Applications as BarChart representation
              </template>
              <template v-slot:content>
                <bar-chart
                  :selected_dataset_id="selected_dataset_id"
                  :selected_dataset_label="selected_dataset_label"
                  ref="myBarChart"
                  @plotDataAsForm="get_plot_data_as_form($event)"
                ></bar-chart>
              </template>
              <template v-slot:footer>
                <div>
                  <Button
                    label="Assign Plot to Dashboard"
                    icon="pi pi-tag"
                    iconPos="center"
                    @click="toggleShowAddPlotToExecutiveDashboards('bar')"
                  />
                </div>
              </template>
            </Card>
            <Card class="component-card centered-chart">
              <template v-slot:title> PieChart </template>
              <template v-slot:subtitle>
                Departments by # of Applications as PieChart representation
              </template>
              <template v-slot:content>
                <pie-chart
                  :selected_dataset_id="selected_dataset_id"
                  :selected_dataset_label="selected_dataset_label"
                  ref="myPieChart"
                  @plotDataAsForm="get_plot_data_as_form($event)"
                ></pie-chart>
              </template>
              <template v-slot:footer>
                <div>
                  <Button
                    label="Assign Plot to Dashboard"
                    icon="pi pi-tag"
                    iconPos="center"
                    @click="toggleShowAddPlotToExecutiveDashboards('pie')"
                  />
                </div>
              </template>
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
                  :selected_dataset_id="selected_dataset_id"
                  :selected_dataset_label="selected_dataset_label"
                  ref="myApplicationRadar"
                  @plotDataAsForm="get_plot_data_as_form($event)"
                ></application-radar>
              </template>
              <template v-slot:footer>
                <div>
                  <Button
                    label="Assign Plot to Dashboard"
                    icon="pi pi-tag"
                    iconPos="center"
                    @click="toggleShowAddPlotToExecutiveDashboards('appradar')"
                  />
                </div>
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
          :selected_dataset_id="selected_dataset_id"
          :selected_dataset_label="selected_dataset_label"
          :key="componentKey"
        ></architecture-views-applicability-analysis>
      </TabPanel>
      <TabPanel>
        <template #header>
          <b-icon-upc style="font-size: 18px; margin: 3px" />
          <span><h4>Architecture Views</h4></span>
        </template>
        <architecture-views
          :selected_dataset_id="selected_dataset_id"
          :selected_dataset_label="selected_dataset_label"
          @close="increaseComponentKey"
        ></architecture-views>
      </TabPanel>
    </TabView>
    <div class="p-grid p-nogutter p-justify-between">
      <Button label="Back" @click="prevPage()" icon="pi pi-angle-left" />
    </div>
    <transition class="modal-animation">
      <modal-view
        v-if="showAddPlotToExecutiveDashboards"
        @close="toggleShowAddPlotToExecutiveDashboards('close')"
      >
        <template v-slot:header>ADD PLOT TO DASHBOARD</template>
        <template v-slot:body>
          <add-plot-to-executive-dashboards
            @selected_executive_dashboards="
              create_plot_and_save_to_executive_dashboard($event)
            "
          >
          </add-plot-to-executive-dashboards>
        </template>
      </modal-view>
    </transition>
  </div>
</template>
<script>
// import Chart from "../Plots/Chart.vue";
import PieChart from "../Plots/PieChart.vue";
import TreeMap from "../Plots/TreeMap.vue";
import BarChart from "../Plots/BarChart.vue";
import ApplicationRadar from "../Plots/ApplicationRadar.vue";
import ArchitectureViews from "../DashboardComponents/ArchitectureViews.vue";
import ArchitectureViewApplicabilityAnalysis from "../Plots/ArchitectureViewApplicabilityAnalysis.vue";
import AddPlotToExecutiveDashboards from "../InputForms/AddPlotToExecutiveDashboards.vue";
import Modal from "../Modal.vue";

export default {
  props: ["selected_dataset_id", "selected_dataset_label"],
  components: {
    // chart: Chart,
    "pie-chart": PieChart,
    "tree-map": TreeMap,
    "bar-chart": BarChart,
    "application-radar": ApplicationRadar,
    "architecture-views": ArchitectureViews,
    "architecture-views-applicability-analysis":
      ArchitectureViewApplicabilityAnalysis,
    "add-plot-to-executive-dashboards": AddPlotToExecutiveDashboards,
    "modal-view": Modal,
  },
  data() {
    return {
      componentKey: 0,
      showAddPlotToExecutiveDashboards: false,
      formData: "",
    };
  },
  methods: {
    get_plot_data_as_form(formData) {
      console.log(formData);

      this.formData = new FormData();
      for (var key in formData) {
        this.formData.append(key, formData[key]);
      }
      console.log(this.formData);
    },
    toggleShowAddPlotToExecutiveDashboards(chart_type) {
      this.showAddPlotToExecutiveDashboards =
        !this.showAddPlotToExecutiveDashboards;
      if (chart_type === "bar") {
        this.$refs.myBarChart.create_plot_and_save_to_executive_dashboard();
      } else if (chart_type === "pie") {
        this.$refs.myPieChart.create_plot_and_save_to_executive_dashboard();
      } else if (chart_type === "treemap") {
        this.$refs.myTreeMapChart.create_plot_and_save_to_executive_dashboard();
      } else if (chart_type === "appradar") {
        this.$refs.myApplicationRadar.create_plot_and_save_to_executive_dashboard();
      }
    },
    create_plot_and_save_to_executive_dashboard(selected_executive_dashboards) {
      for (
        let index = 0;
        index < selected_executive_dashboards.length;
        index++
      ) {
        console.log(this.formData);
        var executive_dashboard_id =
          selected_executive_dashboards[index].executive_dashboard
            .executive_dashboard_id;
        this.$axios
          .post("/create_plot/" + executive_dashboard_id, this.formData)
          .then(() => {
            this.$toast.add({
              severity: "success",
              summary: "Plot Creation Successful",
              detail: "The Plot was created",
              life: 3000,
            });
          })
          .catch(() => {
            this.$toast.add({
              severity: "error",
              summary: "Plot Creation Unsuccessful",
              detail: "The Plot Creation was Unsuccessful",
              life: 3000,
            });
            this.submitted = false;
          });
        this.toggleShowAddPlotToExecutiveDashboards();
      }
    },
    prevPage() {
      this.$emit("prev-page", { pageIndex: 1 });
    },
    increaseComponentKey() {
      this.componentKey += 1;
    },
  },
};
</script>
<style scoped>
.component-card {
  margin-top: 30px;
  position: relative;
  /* display: flex; */
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
  /* min-width: 100%; */
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