<template>
  <div>
    <TabView class="tabview-custom" ref="tabview4">
      <TabPanel>
        <template #header>
          <b-icon-thermometer-half style="font-size: 18px; margin: 3px" />
          <span><h4>Heatmap Analysis</h4></span>
        </template>
        <div class="bokeh-graph">
          <plotter-bubble
            :selected_dataset_id="selected_dataset_id"
            :key="componentKey"
          ></plotter-bubble>
        </div>
        <br />
        <div class="row justify-content-center pb-5 pt-2">
          <div class="col-...">
            <h1 class="h1_sub" v-if="showFurtherHeatMaps">
              Remove Additional Heatmap Analyzer
            </h1>
            <h1 class="h1_sub" v-else>Add Additional Heatmap Analyzer</h1>
            <div class="d-grid">
              <button
                class="btn btn-secondary"
                type="button"
                @click="toggleShowFurtherHeatMaps"
              >
                <span class="btn-label"
                  ><b-icon-dash-square-fill
                    v-if="showFurtherHeatMaps" /><b-icon-plus-square-fill
                    v-else
                /></span>
              </button>
            </div>
          </div>
        </div>
        <div class="row" v-if="showFurtherHeatMaps">
          <div class="col-6">
            <plotter-bubble
              :selected_dataset_id="selected_dataset_id"
              :key="componentKey"
              style="resize: both; overflow: auto"
            ></plotter-bubble>
          </div>
          <div class="col-6">
            <plotter-bubble
              :selected_dataset_id="selected_dataset_id"
              :key="componentKey"
              style="resize: both; overflow: auto"
            ></plotter-bubble>
          </div>
        </div>
      </TabPanel>
      <TabPanel>
        <template #header>
          <b-icon-bar-chart-line-fill style="font-size: 18px; margin: 3px" />
          <span><h4>Statistics Analysis</h4></span>
        </template>
        <div class="bokeh-graph">
          <plotter-simple-statistics
            :selected_dataset_id="selected_dataset_id"
            :key="componentKey"
          ></plotter-simple-statistics>
        </div>
        <br />
        <div class="row justify-content-center pb-5 pt-2">
          <br />
          <br />
          <div class="col-...">
            <h1 class="h1_sub" v-if="showFurtherSimpleStatistics">
              Remove Additional Statistics Analyzer
            </h1>
            <h1 class="h1_sub" v-else>Add Additional Statistics Analyzer</h1>
            <div class="d-grid">
              <button
                class="btn btn-secondary"
                type="button"
                @click="toggleShowFurtherSimpleStatistics"
              >
                <span class="btn-label"
                  ><b-icon-dash-square-fill
                    v-if="
                      showFurtherSimpleStatistics
                    " /><b-icon-plus-square-fill v-else
                /></span>
              </button>
            </div>
          </div>
          <div class="row" v-if="showFurtherSimpleStatistics">
            <br />
            <div class="col-6">
              <plotter-simple-statistics
                :selected_dataset_id="selected_dataset_id"
                :key="componentKey"
                class="overflow-auto"
              ></plotter-simple-statistics>
            </div>
            <div class="col-6">
              <plotter-simple-statistics
                :selected_dataset_id="selected_dataset_id"
                :key="componentKey"
                class="overflow-auto"
              ></plotter-simple-statistics>
            </div>
          </div>
        </div>
      </TabPanel>
    </TabView>
    <div class="p-grid p-nogutter p-justify-between">
      <Button label="Back" @click="prevPage()" icon="pi pi-angle-left" />
    </div>
    <br />
  </div>
</template>

<script>
import BubblePlotter from "../Plots/PlotterBubble.vue";
import PlotterSimpleStatistics from "../Plots/PlotterSimpleStatistics.vue";

export default {
  components: {
    "plotter-bubble": BubblePlotter,
    "plotter-simple-statistics": PlotterSimpleStatistics,
  },
  props: ["selected_dataset_id", "selected_dataset_label"],
  data() {
    this.autenticateSession();
    return {
      showAnalyzerSelector: false,
      showFurtherHeatMaps: false,
      showFurtherSimpleStatistics: false,
      componentKey: 0,
    };
  },
  methods: {
    prevPage() {
      this.$emit("prev-page", { pageIndex: 1 });
    },
    toggleShowFurtherSimpleStatistics() {
      this.showFurtherSimpleStatistics = !this.showFurtherSimpleStatistics;
    },
    toggleShowFurtherHeatMaps() {
      this.showFurtherHeatMaps = !this.showFurtherHeatMaps;
    },
    autenticateSession() {
      if (localStorage.loggedUser && localStorage.token) {
        this.$axios
          .get("/user/validatetoken?token=" + localStorage.token)
          .then(() => {
            this.selected_user = localStorage.loggedUser;
            this.$axios.get("/user/" + this.selected_user).then((res) => {
              this.$store.state.loggedUser = res.data;
            });
          })
          .catch(() => {
            this.$router.push("/");
          });
      } else {
        this.$router.push("/");
      }
    },
  },
};
</script>

<style scoped>
.bg-img {
  background-image: url("~@/assets/DATAANALYZER_BACKGROUND.png");
}
.bokeh-graph {
  resize: both;
}
</style>