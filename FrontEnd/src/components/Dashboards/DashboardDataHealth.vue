<template>
  <div>
    <TabView class="tabview-custom" ref="tabview4" style="margin-bottom: 50px">
      <TabPanel>
        <template #header>
          <b-icon-upc style="font-size: 18px; margin: 3px" />
          <span><h4>Architecture Views</h4></span>
        </template>
        <architecture-views
          :selected_dataset_id="selected_dataset_id"
          :selected_dataset_label="selected_dataset_label"
          :key="componentKey"
          @close="increaseComponentKey"
          @update="update_architecture_view($event)"
        ></architecture-views>
      </TabPanel>
      <TabPanel>
        <template #header>
          <b-icon-compass style="font-size: 18px; margin: 3px" />
          <span><h4>Examine Application Status</h4></span>
        </template>
        <application-status-radar
          :selected_dataset_id="selected_dataset_id"
          :selected_dataset_label="selected_dataset_label"
        ></application-status-radar>
      </TabPanel>
      <TabPanel>
        <template #header>
          <b-icon-columns style="font-size: 18px; margin: 3px" />
          <span><h4>Analyze Architecture Views Applicability</h4></span>
        </template>
        <architecture-view-analysis
          :selected_dataset_label="selected_dataset_label"
          :selected_datset_id="selected_dataset_id"
        ></architecture-view-analysis>
      </TabPanel>
    </TabView>
    <customazible-button
      @button-click="prevPage()"
      altLabel="Back"
      altButtonClass="p-button-rounded"
      altClass=""
      altStyle="position: fixed;
                left: 50%;
                bottom: 5px;
                transform: translate(-50%, -50%);
                margin-top: 20px;"
    ></customazible-button>
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
import AppplicationStatusRadar from "../DashboardComponents/AppplicationStatusRadar.vue";
import ArchitectureViews from "../DashboardComponents/ArchitectureViews.vue";
import ArchitectureViewAnalysis from "../DashboardComponents/ArchitectureViewAnalysis.vue";
import AddPlotToExecutiveDashboards from "../InputForms/AddPlotToExecutiveDashboards.vue";
import Modal from "../Modal.vue";
import CustomazibleButton from "../HelperComponents/CustomazibleButton.vue";

export default {
  components: {
    "application-status-radar": AppplicationStatusRadar,
    "architecture-views": ArchitectureViews,
    "add-plot-to-executive-dashboards": AddPlotToExecutiveDashboards,
    "modal-view": Modal,
    "customazible-button": CustomazibleButton,
    "architecture-view-analysis": ArchitectureViewAnalysis,
  },
  data() {
    return {
      componentKey: 0,
      formData: "",
      selected_dataset_id: localStorage.selected_dataset_id,
      selected_dataset_label: localStorage.selected_dataset_label,
    };
  },
  methods: {
    update_architecture_view(architecture_view) {
      this.increaseComponentKey();
      this.$emit("update", architecture_view);
    },
    create_plot_and_save_to_executive_dashboard(selected_executive_dashboards) {
      for (
        let index = 0;
        index < selected_executive_dashboards.length;
        index++
      ) {
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