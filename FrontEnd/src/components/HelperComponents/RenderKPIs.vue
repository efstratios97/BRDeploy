<template>
  <div>
    <div class="container-...">
      <div class="row row-cols-auto auto-cols-adj">
        <input-field-app-dep-dom
          :apps="apps"
          :departments="departments"
          :domains="domains"
          :selected_dataset_id="selected_dataset_id"
          :selected_dataset_label="selected_dataset_label"
          @input-parameter="assign_parameter($event)"
        ></input-field-app-dep-dom>
        <Card class="component-card">
          <template v-slot:title> KPI </template>
          <template v-slot:subtitle>
            Select KPIs to perform KPI Analysis
          </template>
          <template v-slot:content>
            <form class="overflow-auto">
              <Dropdown
                v-model="selected_kpis"
                :options="kpis"
                :filter="true"
                optionLabel="kpi.name"
                placeholder="Select KPI"
                filterPlaceholder="Find a KPI"
              />
            </form>
          </template>
        </Card>
      </div>
      <br />
      <div class="p-grid">
        <div class="p-col-4 p-offset-4">
          <div class="p-fluid">
            <Button
              label="Apply"
              @click="render_kpis()"
              icon="pi pi-check"
              iconPos="right"
            />
          </div>
        </div>
      </div>
    </div>
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
      <div class="row row-cols-auto auto-cols-adj">
        <div v-for="data_point in data" :key="data_point.parameter">
          <Card class="component-card">
            <template v-slot:content>
              <div class="p-fluid">
                <kpi-gauge
                  :id="data_point.parameter"
                  :data="data_point.data"
                  :caption="data_point.parameter"
                  :subCaption="subCaption"
                  :threshold="data_point.threshold"
                  :color_coding="data_point.color_coding"
                ></kpi-gauge>
              </div>
            </template>
            <template #footer>
              <aspects-in-kpi
                :selected_parameter="data_point.original_parameters"
                :kpi_id="data_point.kpi_id"
                :kpi_name="data_point.kpi_name"
                :selected_dataset_id="selected_dataset_id"
                :selected_dataset_label="selected_dataset_label"
                :aspects_weights="data_point.aspects_weights"
              ></aspects-in-kpi>
            </template>
          </Card>
        </div>
        <Card class="component-card">
          <template v-slot:content>
            <div class="p-fluid">
              <show-applicability-kpi
                :id="selected_kpis.kpi.name + selected_kpis.kpi.kpi_id"
                :selected_dataset_id="selected_dataset_id"
                :selected_dataset_label="selected_dataset_label"
                :selected_kpi="selected_kpis"
                selected_parameter="all"
                gauge_type="hlineargauge"
              ></show-applicability-kpi>
            </div>
          </template>
        </Card>
      </div>
    </div>
  </div>
</template>
<script>
import KPIGauge from "../Plots/KPIGauge.vue";
import ShowApplicabilityKPI from "../HelperComponents/ShowApplicabilityKPI.vue";
import AspectsInKPI from "../HelperComponents/AspectsInKPI.vue";
import InputFieldAppDepDom from "../InputFields/InputFieldAppDepDom.vue";

export default {
  components: {
    "kpi-gauge": KPIGauge,
    "show-applicability-kpi": ShowApplicabilityKPI,
    "aspects-in-kpi": AspectsInKPI,
    "input-field-app-dep-dom": InputFieldAppDepDom,
  },
  props: [
    "selected_dataset_id",
    "selected_dataset_label",
    "apps",
    "departments",
    "domains",
  ],
  data() {
    return {
      selected_parameter: "",
      data: [],
      rendered_graph_kpis: false,
      rendered_graph_aspects: false,
      subCaption: "",
      triggered_rendering: false,
      kpis: this.get_kpis(),
      selected_kpis: "",
      input_field_selected: false,
    };
  },
  methods: {
    assign_parameter(parameter) {
      this.selected_parameter = parameter;
    },
    get_kpis() {
      this.$axios
        .get("/get_kpis_by_dataset_label/" + this.selected_dataset_label)
        .then((res) => {
          var kpis_tmp = [];
          for (let index = 0; index < res.data.data.length; index++) {
            kpis_tmp.push({ kpi: res.data.data[index] });
          }
          this.kpis = kpis_tmp;
        });
    },
    render_kpis() {
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
        formData.append("kpis", JSON.stringify(this.selected_kpis));
        this.$axios
          .post(
            "/calculate_kpis/" +
              this.selected_dataset_id +
              "/" +
              this.selected_dataset_label,
            formData
          )
          .then((res) => {
            if (this.selected_parameter.length !== undefined) {
              for (
                let index = 0;
                index < this.selected_parameter.length;
                index++
              ) {
                var data_tmp = 0;
                var threshold_tmp = 0;
                var kpi_id_tmp = "";
                var kpi_name_tmp = "";
                var aspects_weights_tmp = "";
                var color_coding_tmp = "";
                var original_selected_parameters = this.selected_parameter;
                var newKey = "parameter";
                var oldKey = Object.keys(this.selected_parameter[index]);
                delete Object.assign(this.selected_parameter[index], {
                  [newKey]: this.selected_parameter[index][oldKey],
                })[oldKey];
                for (
                  let index_2 = 0;
                  index_2 <
                  res.data[this.selected_parameter[index].parameter].length;
                  index_2++
                ) {
                  data_tmp =
                    res.data[this.selected_parameter[index].parameter][index_2]
                      .result;
                  threshold_tmp =
                    res.data[this.selected_parameter[index].parameter][index_2]
                      .threshold;
                  kpi_id_tmp =
                    res.data[this.selected_parameter[index].parameter][index_2]
                      .kpi_id;
                  kpi_name_tmp =
                    res.data[this.selected_parameter[index].parameter][index_2]
                      .kpi_name;
                  aspects_weights_tmp =
                    res.data[this.selected_parameter[index].parameter][index_2]
                      .aspects_weights;
                  color_coding_tmp =
                    res.data[this.selected_parameter[index].parameter][index_2]
                      .color_coding;
                }
                if (color_coding_tmp === "the Higher the Better") {
                  color_coding_tmp = [
                    {
                      minValue: "0",
                      maxValue: threshold_tmp - 0.5,
                      code: "#cc0000",
                    },
                    {
                      minValue: threshold_tmp - 0.5,
                      maxValue: threshold_tmp + 0.5,
                      code: "#ffba00",
                    },
                    {
                      minValue: threshold_tmp + 0.5,
                      maxValue: "10",
                      code: "#6baa01",
                    },
                  ];
                } else {
                  color_coding_tmp = [
                    {
                      minValue: "0",
                      maxValue: threshold_tmp - 0.5,
                      code: "#6baa01",
                    },
                    {
                      minValue: threshold_tmp - 0.5,
                      maxValue: threshold_tmp + 0.5,
                      code: "#ffba00",
                    },
                    {
                      minValue: threshold_tmp + 0.5,
                      maxValue: "10",
                      code: "#cc0000",
                    },
                  ];
                }
                this.data.push({
                  parameter: this.selected_parameter[index].parameter,
                  data: data_tmp,
                  kpi_id: kpi_id_tmp,
                  kpi_name: kpi_name_tmp,
                  threshold: threshold_tmp,
                  aspects_weights: aspects_weights_tmp,
                  original_parameters: original_selected_parameters[index],
                  color_coding: color_coding_tmp,
                });
                delete Object.assign(this.selected_parameter[index], {
                  [oldKey]: this.selected_parameter[index][newKey],
                })[newKey];
              }
            } else {
              original_selected_parameters = this.selected_parameter;
              newKey = "parameter";
              oldKey = Object.keys(this.selected_parameter);
              delete Object.assign(this.selected_parameter, {
                [newKey]: this.selected_parameter[oldKey],
              })[oldKey];
              var rslt = res.data[this.selected_parameter.parameter][0];
              if (rslt.color_coding === "the Higher the Better") {
                rslt.color_coding = [
                  {
                    minValue: "0",
                    maxValue: rslt.threshold - 0.5,
                    code: "#cc0000",
                  },
                  {
                    minValue: rslt.threshold - 0.5,
                    maxValue: rslt.threshold + 0.5,
                    code: "#ffba00",
                  },
                  {
                    minValue: rslt.threshold + 0.5,
                    maxValue: "10",
                    code: "#6baa01",
                  },
                ];
              } else {
                rslt.color_coding = [
                  {
                    minValue: "0",
                    maxValue: rslt.threshold - 0.5,
                    code: "#6baa01",
                  },
                  {
                    minValue: rslt.threshold - 0.5,
                    maxValue: rslt.threshold + 0.5,
                    code: "#ffba00",
                  },
                  {
                    minValue: rslt.threshold + 0.5,
                    maxValue: "10",
                    code: "#cc0000",
                  },
                ];
              }
              this.data.push({
                parameter: this.selected_parameter.parameter,
                data: rslt.result,
                kpi_id: rslt.kpi_id,
                kpi_name: rslt.kpi_name,
                threshold: rslt.threshold,
                aspects_weights: rslt.aspects_weights,
                original_parameters: original_selected_parameters,
                color_coding: rslt.color_coding,
              });
              delete Object.assign(this.selected_parameter, {
                [oldKey]: this.selected_parameter[newKey],
              })[newKey];
            }
            this.subCaption = "KPI Analysis per Input";
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