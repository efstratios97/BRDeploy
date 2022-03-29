<template>
  <div>
    <TabView class="tabview-custom" ref="tabview4" :key="componentKey">
      <TabPanel
        v-for="executive_dashboard in suitable_dashboards"
        :key="executive_dashboard.executive_dashboard_id"
      >
        <template #header>
          <b-icon-pie-chart style="font-size: 18px; margin: 3px" />
          <span
            ><h4>{{ executive_dashboard.name }}</h4></span
          >
        </template>
        <div
          v-if="
            showDatasetSelection[executive_dashboard.executive_dashboard_id]
          "
        >
          <Card
            class="component-card"
            style="margin-left: auto; margin-right: auto"
          >
            <template v-slot:title> Select your dataset to analyze </template>
            <template v-slot:content>
              <div class="p-grid p-fluid">
                <div class="p-col-8 p-offset-4">
                  <select-dataset-choice-rule-specific
                    @input-dataset="
                      assign_dataset_specific(
                        $event,
                        executive_dashboard.executive_dashboard_id
                      )
                    "
                  ></select-dataset-choice-rule-specific>
                </div>
              </div>
            </template>
          </Card>
        </div>

        <div class="container-...">
          <div class="row row-cols-auto auto-cols-adj">
            <div
              v-for="plot in plots_from_dashboard[
                executive_dashboard.executive_dashboard_id
              ]"
              :key="plot"
            >
              <div
                v-if="
                  plot.visualization_right ===
                  'No option for own Analysis - Plain Visualization'
                "
              >
                <br />
                <Fieldset
                  :legend="
                    JSON.stringify(plot.formdata.parameter)
                      .substring(
                        JSON.stringify(plot.formdata.parameter).indexOf('\:') +
                          3
                      )
                      .slice(0, -4)
                  "
                  :toggleable="true"
                  :style="select_style_field_set_plain(plot.visualization_type)"
                >
                  <render-visualization
                    :formdata="plot.formdata"
                    :visualization="plot.visualization_type"
                    :grouped="plot.grouped"
                    :selected_dataset_id="
                      selected_dataset_id[
                        executive_dashboard.executive_dashboard_id
                      ]
                    "
                    :selected_dataset_label="
                      selected_dataset_label[
                        executive_dashboard.executive_dashboard_id
                      ]
                    "
                    :executive_dashboard="true"
                  ></render-visualization>
                </Fieldset>
                <br />
              </div>
              <div v-else>
                <br />
                <Fieldset
                  :legend="plot.component_name"
                  :toggleable="true"
                  style="width: 92vw"
                >
                  <component
                    :is="comp(plot.component_name)"
                    :selected_dataset_id="
                      selected_dataset_id[
                        executive_dashboard.executive_dashboard_id
                      ]
                    "
                    :selected_dataset_label="
                      selected_dataset_label[
                        executive_dashboard.executive_dashboard_id
                      ]
                    "
                  ></component>
                </Fieldset>
                <br />
              </div>
            </div>
          </div>
        </div> </TabPanel
    ></TabView>
  </div>
</template>

<script>
import RenderVisualization from "../Plots/RenderVisualization.vue";
import SelectDatasetChoiceRuleSpecific from "../InputForms/HelperComponents/SelectDatasetChoiceRuleSpecific.vue";
import { defineAsyncComponent } from "vue";

export default {
  components: {
    "render-visualization": RenderVisualization,
    "select-dataset-choice-rule-specific": SelectDatasetChoiceRuleSpecific,
  },
  data() {
    return {
      componentKey: 0,
      suitable_dashboards: this.get_suitable_dashboards(),
      plots_from_dashboard: [],
      showAddExecutiveDashboard: false,
      showDatasetSelection: {},
      selected_dataset_id: {},
      selected_dataset_label: {},
    };
  },
  watch: {},
  computed: {},
  methods: {
    select_style_field_set_plain(visualization_type) {
      var style_field_set_plain = "";
      if (
        visualization_type === "kpi_lifecycle" ||
        visualization_type === "kpi_lifecycle_development"
      ) {
        style_field_set_plain =
          "min-width : 92vw; margin-left: auto; margin-right: auto";
      } else {
        style_field_set_plain =
          "min-width : 29vw; margin-left: auto; margin-right: auto";
      }
      return style_field_set_plain;
    },
    comp(component_name) {
      return defineAsyncComponent(() =>
        import(`../DashboardComponents/${component_name}.vue`)
      );
    },
    seperate_dashboards_plots_by_right(current_ed_id) {
      var plots_from_dashboard_own_analysis = [],
        plots_from_dashboard_plain = [];
      for (
        let i = 0;
        i < this.plots_from_dashboard[current_ed_id].length;
        i++
      ) {
        if (
          this.plots_from_dashboard[current_ed_id][i].visualization_right ===
          "No option for own Analysis - Plain Visualization"
        ) {
          plots_from_dashboard_plain.push(
            this.plots_from_dashboard[current_ed_id][i]
          );
        } else {
          plots_from_dashboard_own_analysis.push(
            this.plots_from_dashboard[current_ed_id][i]
          );
        }
      }
      this.plots_from_dashboard[current_ed_id] =
        plots_from_dashboard_plain.concat(plots_from_dashboard_own_analysis);
    },
    assign_dataset_specific(selected_dataset, executive_dashboard_id) {
      this.selected_dataset_id[executive_dashboard_id] =
        selected_dataset.dataset_id;
      this.selected_dataset_label[executive_dashboard_id] =
        selected_dataset.dataset_label;
      this.$axios
        .get("/get_plots_from_executive_dashboards/" + executive_dashboard_id)
        .then((res) => {
          var current_ed_id = executive_dashboard_id;
          this.plots_from_dashboard[current_ed_id] = [];
          for (let index_2 = 0; index_2 < res.data.data.length; index_2++) {
            this.plots_from_dashboard[current_ed_id].push(
              res.data.data[index_2]
            );
            this.plots_from_dashboard[current_ed_id].sort(function (
              plot_1,
              plot_2
            ) {
              var x = plot_1.visualization_type;
              var y = plot_2.visualization_type;
              return y < x ? -1 : y > x ? 1 : 0;
            });
          }
          this.seperate_dashboards_plots_by_right(current_ed_id);
        });
    },
    increaseComponentKey() {
      this.componentKey += 1;
    },
    get_suitable_dashboards() {
      this.$axios
        .get("/get_executive_dashboards_by_user/" + localStorage.loggedUser)
        .then((res) => {
          var dashboards_tmp = [];
          for (let index = 0; index < res.data.data.length; index++) {
            dashboards_tmp.push(res.data.data[index]);
            this.increaseComponentKey();
          }
          this.suitable_dashboards = dashboards_tmp;
          for (
            let index = 0;
            index < this.suitable_dashboards.length;
            index++
          ) {
            var executive_dashboard_id =
              this.suitable_dashboards[index].executive_dashboard_id;
            this.increaseComponentKey();
            if (
              this.suitable_dashboards[index].dataset_choice_rule ===
              "User's Choice"
            ) {
              this.showDatasetSelection[executive_dashboard_id] = true;
            }
            this.$axios
              .get(
                "/get_plots_from_executive_dashboards/" + executive_dashboard_id
              )
              .then((res) => {
                let current_ed_id =
                  this.suitable_dashboards[index].executive_dashboard_id;
                if (this.showDatasetSelection[current_ed_id] !== true) {
                  this.plots_from_dashboard[current_ed_id] = [];
                  for (
                    let index_2 = 0;
                    index_2 < res.data.data.length;
                    index_2++
                  ) {
                    this.selected_dataset_id[current_ed_id] =
                      res.data.data[index_2].dataset_id;
                    this.selected_dataset_label[current_ed_id] =
                      res.data.data[index_2].dataset_label;
                    this.plots_from_dashboard[current_ed_id].push(
                      res.data.data[index_2]
                    );
                    this.plots_from_dashboard[current_ed_id].sort(function (
                      plot_1,
                      plot_2
                    ) {
                      var x = plot_1.visualization_type;
                      var y = plot_2.visualization_type;
                      return y < x ? -1 : y > x ? 1 : 0;
                    });
                  }
                  this.seperate_dashboards_plots_by_right(current_ed_id);
                }
              });
          }
        });
    },
  },
};
</script>
<style scoped>
.flex-container {
  display: -webkit-box; /* OLD - iOS 6-, Safari 3.1-6, BB7 */
  display: -ms-flexbox; /* TWEENER - IE 10 */
  display: -webkit-flex; /* NEW - Safari 6.1+. iOS 7.1+, BB10 */
  display: flex; /* NEW, Spec - Firefox, Chrome, Opera */

  justify-content: center;
  align-items: center;
}
.fieldset p {
  line-height: 1.5;
  margin: 0;
}

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
</style>