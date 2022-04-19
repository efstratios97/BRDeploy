<template>
  <div>
    <Card class="component-card-rendering" v-if="triggered_rendering">
      <template v-slot:content>
        <div class="p-fluid">
          <div class="container-...">
            <h1>Rendering your Visualization...</h1>
            <h3>Please wait...</h3>
            <ProgressBar mode="indeterminate" />
          </div>
        </div>
      </template>
    </Card>
    <!-- grouped graphs will render correctly seperately -->
    <span v-if="separated_display">
      <div v-for="data_point in data" :key="data_point">
        <div class="container-..." v-if="rendered_visualization">
          <div class="row row-cols-auto auto-cols-adj">
            <Card class="component-card">
              <template v-slot:content>
                <div class="p-fluid">
                  <fusion-chart :data="data_point"></fusion-chart>
                </div>
              </template>
              <template v-slot:footer v-if="executive_dashboard !== true">
                <save-to-dashboard-button
                  @show_add_to_dashboard="showAddToDashboard()"
                ></save-to-dashboard-button>
              </template>
            </Card>
          </div>
        </div>
      </div>
    </span>
    <span v-else-if="data.length > 1">
      <span v-if="grouped === 'true' || grouped">
        <div class="container-..." v-if="rendered_visualization">
          <div class="row row-cols-auto auto-cols-adj">
            <Card class="component-card">
              <template v-slot:content>
                <div class="p-fluid">
                  <div v-for="data_point in data" :key="data_point">
                    <fusion-chart :data="data_point"></fusion-chart>
                  </div>
                </div>
              </template>
              <template v-slot:footer v-if="executive_dashboard !== true">
                <save-to-dashboard-button
                  @show_add_to_dashboard="showAddToDashboard()"
                ></save-to-dashboard-button>
              </template>
            </Card>
          </div>
        </div>
      </span>
      <span v-else>
        <div class="container-..." v-if="rendered_visualization">
          <div class="row row-cols-auto auto-cols-adj">
            <div v-for="data_point in data" :key="data_point">
              <Card class="component-card">
                <template v-slot:content>
                  <div class="p-fluid">
                    <fusion-chart :data="data_point"></fusion-chart>
                  </div>
                </template>
                <template v-slot:footer v-if="executive_dashboard !== true">
                  <save-to-dashboard-button
                    @show_add_to_dashboard="showAddToDashboard()"
                  ></save-to-dashboard-button>
                </template>
              </Card>
            </div>
          </div>
        </div>
      </span>
    </span>
    <span v-else>
      <div v-for="data_point in data" :key="data_point">
        <div class="container-..." v-if="rendered_visualization">
          <div class="row row-cols-auto auto-cols-adj">
            <Card class="component-card">
              <template v-slot:content>
                <div class="p-fluid">
                  <fusion-chart :data="data_point"></fusion-chart>
                </div>
              </template>
              <template v-slot:footer v-if="executive_dashboard !== true">
                <save-to-dashboard-button
                  @show_add_to_dashboard="showAddToDashboard()"
                ></save-to-dashboard-button>
              </template>
            </Card>
          </div>
        </div>
      </div>
    </span>
    <br />
    <div v-if="show_add_to_dashboard">
      <modal-view @close="showAddToDashboard()">
        <template v-slot:body>
          <add-plot-to-executive-dashboard
            :formdata="formdata"
            :visualization="visualization"
            :grouped="grouped"
            :component_name="component_name"
            :separated_display="separated_display"
            @close="showAddToDashboard()"
          ></add-plot-to-executive-dashboard>
        </template>
      </modal-view>
    </div>
  </div>
</template>

<script>
import FusionChart from "./FusionChart.vue";
import SaveToDashboardButton from "./SaveToDashboardButton.vue";
import AddPlotToExecutiveDashboards from "../InputForms/AddPlotToExecutiveDashboards.vue";
import Modal from "../Modal.vue";

export default {
  components: {
    "fusion-chart": FusionChart,
    "save-to-dashboard-button": SaveToDashboardButton,
    "add-plot-to-executive-dashboard": AddPlotToExecutiveDashboards,
    "modal-view": Modal,
  },
  props: [
    "selected_dataset_id",
    "selected_dataset_label",
    "formdata",
    "visualization",
    "grouped",
    "component_name",
    "executive_dashboard", //Is it called by executive dashboard --> no `Save to Dashboard´ else yes
    "separated_display", //grouped graphs will render correctly seperately
  ],
  data() {
    return {
      data: [],
      rendered_visualization: false,
      triggered_rendering: false,
      show_add_to_dashboard: false,
    };
  },
  mounted() {
    this.render_visualization(this.formdata, this.visualization);
  },
  methods: {
    showAddToDashboard() {
      window.scrollTo(1500, 1250);
      this.show_add_to_dashboard = !this.show_add_to_dashboard;
    },
    render_visualization(formdata, visualization) {
      this.triggered_rendering = true;
      this.rendered_visualization = false;
      this.data = [];
      this.$toast.add({
        severity: "info",
        summary: "Rendering Visualization initiated...",
        detail: "This make take some time.. Please wait",
        life: 3000,
      });
      var formData = new FormData();
      for (const [key, value] of Object.entries(formdata)) {
        formData.append(key, value);
      }
      this.$axios
        .post(
          "/render_visualizations/" +
            this.selected_dataset_id +
            "/" +
            this.selected_dataset_label +
            "/" +
            visualization,
          formData
        )
        .then((res) => {
          this.data = res.data.result;
          this.triggered_rendering = false;
          this.rendered_visualization = true;
        })
        .catch(() => {
          this.$toast.add({
            severity: "error",
            summary: "Visualization Rendereing Unsuccessful",
            detail: "Please make sure you selected all input fields",
            life: 5000,
          });
          this.triggered_rendering = false;
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
  word-wrap: break-word;
  background-color: #fff;
  background-clip: border-box;
  border-radius: 0.25rem;
  resize: both;
  overflow: auto;
  margin-right: 10px;
  margin-left: 10px;
  max-width: 100%;
}

.component-card-rendering {
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
}
</style>