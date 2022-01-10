<template>
  <div>
    <Card class="component-card-rendering">
      <template v-slot:content>
        <div class="p-grid">
          <div class="p-col">
            <input-field-dep-dom
              :selected_dataset_label="selected_dataset_label"
              :selected_dataset_id="selected_dataset_id"
              :departments="departments"
              :domains="domains"
              @input-parameter="assign_parameter($event)"
            ></input-field-dep-dom>
          </div>
          <div class="p-col">
            <input-field-kpi
              :selected_dataset_id="selected_dataset_id"
              :selected_dataset_label="selected_dataset_label"
              @input-kpis="assign_kpi($event)"
            >
            </input-field-kpi>
          </div>
          <!-- <div class="p-col-4">
            <input-field-calendar @input-date="assign_date($event)">
            </input-field-calendar>
          </div> -->
        </div>
      </template>
      <template v-slot:footer>
        <div class="p-grid">
          <div class="p-col-4 p-offset-4">
            <div class="p-fluid">
              <Button
                label="Apply"
                @click="
                  render_app_life_cycle();
                  render_spline_chart();
                "
                icon="pi pi-check"
                iconPos="right"
              />
            </div>
          </div>
        </div>
      </template>
    </Card>
    <Card class="component-card-rendering" v-if="triggered_rendering">
      <template v-slot:content>
        <div class="p-fluid">
          <div class="p-col-12">
            <h1>Rendering KPIs...</h1>
            <h3>Please wait...</h3>
            <ProgressBar mode="indeterminate" />
          </div>
        </div>
      </template>
    </Card>
    <div class="container-..." v-if="rendered_graph_kpis">
      <Card class="component-card">
        <template v-slot:content>
          <div class="p-fluid">
            <span v-if="rendered_graph_spline_chart">
              <spline-chart
                id="spline-chart"
                :data="data_spline_chart"
                :subCaption="subCaption"
              ></spline-chart>
            </span>
          </div>
        </template>
      </Card>
    </div>
    <div class="container-..." v-if="rendered_graph_kpis">
      <Card class="component-card">
        <template v-slot:content>
          <div class="p-fluid">
            <gantt-chart :data="data" :id="id"></gantt-chart>
          </div>
        </template>
      </Card>
    </div>
  </div>
</template>
<script>
import InputFieldDepDom from "../InputFields/InputFieldDepDom.vue";
import InputFieldKPI from "../InputFields/InputFieldKPI.vue";
// import InputFieldCalendar from "../InputFields/InputFieldCalendar.vue";
import GanttChart from "../Plots/GanttChart.vue";
import SplineChart from "../Plots/SplineChart.vue";
export default {
  components: {
    "gantt-chart": GanttChart,
    "input-field-dep-dom": InputFieldDepDom,
    "input-field-kpi": InputFieldKPI,
    "spline-chart": SplineChart,
    // "input-field-calendar": InputFieldCalendar,
  },
  props: [
    "selected_dataset_id",
    "selected_dataset_label",
    "departments",
    "domains",
  ],
  data() {
    return {
      selected_parameter: "",
      selected_kpis: "",
      selected_date: "",
      data: [],
      data_spline_chart: [],
      rendered_graph_kpis: false,
      rendered_graph_spline_chart: false,
      rendered_graph_aspects: false,
      subCaption: "",
      id: "lifecycle",
      triggered_rendering: false,
      input_field_selected: false,
    };
  },
  methods: {
    assign_parameter(parameter) {
      this.selected_parameter = parameter;
    },
    assign_kpi(kpis) {
      this.selected_kpis = kpis;
    },
    assign_date(date) {
      this.selected_date = date;
    },
    render_spline_chart() {
      this.rendered_graph_spline_chart = false;
      this.data_spline_chart = [];
      var formData = new FormData();
      formData.append("parameter", JSON.stringify(this.selected_parameter));
      formData.append("time_horizon", JSON.stringify(this.selected_date));
      formData.append("kpis", JSON.stringify(this.selected_kpis));
      this.$axios
        .post(
          "/render_life_cycle_development/" +
            this.selected_dataset_id +
            "/" +
            this.selected_dataset_label,
          formData
        )
        .then((res) => {
          this.data_spline_chart = res.data.result;
          this.rendered_graph_spline_chart = true;
        });
    },
    render_app_life_cycle() {
      if (this.selected_parameter === "" || this.selected_kpis === "") {
        this.$toast.add({
          severity: "warn",
          summary: "No Parameter and/or KPI chosen",
          detail:
            "Please select first the Parameter & KPI in both of the input fields",
          life: 8000,
        });
      } else {
        this.triggered_rendering = true;
        this.rendered_graph_kpis = false;
        this.data = [];
        this.$toast.add({
          severity: "info",
          summary: "Rendering KPIs Visualization initiated...",
          detail: "This make take some time.. Please wait",
          life: 15000,
        });
        var formData = new FormData();
        formData.append("parameter", JSON.stringify(this.selected_parameter));
        formData.append("time_horizon", JSON.stringify(this.selected_date));
        formData.append("kpis", JSON.stringify(this.selected_kpis));
        this.$axios
          .post(
            "/render_app_life_cycle/" +
              this.selected_dataset_id +
              "/" +
              this.selected_dataset_label,
            formData
          )
          .then((res) => {
            console.log(res.data.result);
            this.data = res.data.result;
            this.triggered_rendering = false;
            this.rendered_graph_kpis = true;
          });
      }
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