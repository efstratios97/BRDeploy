<template>
  <div>
    <TabView class="tabview-custom" ref="tabview4">
      <TabPanel>
        <template #header>
          <b-icon-pie-chart style="font-size: 18px; margin: 3px" />
          <span
            ><h4>{{ "KPI Dashboard Präsentation 11.01.2022" }}</h4></span
          >
        </template>
        <div
          class="p-col p-d-flex p-ai-center p-jc-center"
          v-if="dataset_not_selected"
        >
          <!-- <div class="overflow-auto"> -->
          <selector-dataset @next-page="next($event)"></selector-dataset>
          <!-- </div> -->
          <!-- </div> -->
        </div>
        <div v-else>
          <Splitter layout="vertical">
            <SplitterPanel
              style="margin: 25px"
              class="p-d-flex p-ai-center p-jc-center"
            >
              <h1 style="font-family: 'Roboto', sans-serif">KPI Analysis</h1>
            </SplitterPanel>
            <SplitterPanel>
              <render-kpis
                :selected_dataset_id="selected_dataset_id"
                :selected_dataset_label="selected_dataset_label"
                :apps="apps"
                :domains="domains"
                :departments="departments"
              ></render-kpis>
            </SplitterPanel>
            <SplitterPanel
              style="margin: 25px"
              class="p-d-flex p-ai-center p-jc-center"
            >
              <h1 style="font-family: 'Roboto', sans-serif">
                KPI Application Landscape Analysis
              </h1>
            </SplitterPanel>
            <SplitterPanel>
              <render-app-landscape
                :selected_dataset_id="selected_dataset_id"
                :selected_dataset_label="selected_dataset_label"
                :apps="apps"
                :domains="domains"
                :departments="departments"
              ></render-app-landscape>
            </SplitterPanel>
            <SplitterPanel
              style="margin: 25px"
              class="p-d-flex p-ai-center p-jc-center"
            >
              <h1 style="font-family: 'Roboto', sans-serif">
                KPI Application Life Cycle Analysis
              </h1>
            </SplitterPanel>
            <SplitterPanel>
              <render-life-cycle-kpi
                :selected_dataset_id="selected_dataset_id"
                :selected_dataset_label="selected_dataset_label"
                :apps="apps"
                :domains="domains"
                :departments="departments"
              ></render-life-cycle-kpi>
            </SplitterPanel>
            <SplitterPanel
              style="margin: 25px; margin-top: 100px"
              class="p-d-flex p-ai-center p-jc-center"
            >
              <h1 style="font-family: 'Roboto', sans-serif">MOCKUP!!</h1>
            </SplitterPanel>
            <SplitterPanel>
              <img
                src="~@/assets/MOCKUP.png"
                alt="Mockup"
                style="height: 550px; width: 100%"
              />
            </SplitterPanel>
          </Splitter>
        </div>
      </TabPanel>
    </TabView>
  </div>
</template>
<script>
import SelectorDataset from "../SelectorDataset.vue";
import RenderKPIs from "../HelperComponents/RenderKPIs.vue";
import RenderAppLandscape from "../HelperComponents/RenderAppLandscape.vue";
import RenderLifeCycleKPI from "../HelperComponents/RenderLifeCycleKPI.vue";
export default {
  components: {
    "render-kpis": RenderKPIs,
    "render-app-landscape": RenderAppLandscape,
    "render-life-cycle-kpi": RenderLifeCycleKPI,
    "selector-dataset": SelectorDataset,
  },
  data() {
    return {
      dataset_not_selected: true,
      selected_dataset_id: "",
      selected_dataset_label: "",
      apps: "",
      departments: "",
      domains: "",
    };
  },
  methods: {
    next(dataset) {
      this.dataset_not_selected = false;
      console.log(dataset.selected_dataset.dataset_id);
      this.selected_dataset_id = dataset.selected_dataset.dataset_id;
      this.selected_dataset_label = dataset.selected_dataset.dataset_label;
      this.getApps();
      this.getDatasetDepartmentOptions();
      this.getDomainsOptions();
    },
    toggleShowAddExecutiveDashboard() {
      this.increaseComponentKey();
      this.$emit("add-executive-dashboard");
    },
    prevPage() {
      this.$emit("prev-page", { pageIndex: 1 });
    },
    increaseComponentKey() {
      this.componentKey += 1;
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
    getDatasetDepartmentOptions() {
      this.$axios
        .get(
          "/get_departments_from_dataset/" +
            this.selected_dataset_id +
            "/" +
            this.selected_dataset_label
        )
        .then((res) => {
          var departments_tmp = [];
          for (let index = 0; index < res.data.data.length; index++) {
            departments_tmp.push({ dep: res.data.data[index] });
          }
          this.departments = departments_tmp;
        });
    },
    getDomainsOptions() {
      this.$axios
        .get(
          "/get_domains_from_dataset/" +
            this.selected_dataset_id +
            "/" +
            this.selected_dataset_label
        )
        .then((res) => {
          var domains_tmp = [];
          for (let index = 0; index < res.data.data.length; index++) {
            domains_tmp.push({ domain: res.data.data[index] });
          }
          this.domains = domains_tmp;
        });
    },
  },
};
</script>
<style scoped>
@import url("https://fonts.googleapis.com/css?family=Roboto+Condensed");

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

.component-card-table {
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