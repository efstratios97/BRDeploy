<template>
  <div>
    <div class="container-...">
      <div class="row row-cols-auto auto-cols-adj">
        <input-field-dep
          :departments="departments"
          :selected_dataset_id="selected_dataset_id"
          :selected_dataset_label="selected_dataset_label"
          @input-parameter="assign_parameter($event)"
        ></input-field-dep>
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
              @click="render_kpi_landscape()"
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
          <div class="container-...">
            <h1>Rendering KPI Landscape...</h1>
            <h3>Please wait...</h3>
            <ProgressBar mode="indeterminate" />
          </div>
        </div>
      </template>
    </Card>
    <div class="container-..." v-if="rendered_kpi_landscape">
      <div class="row row-cols-auto auto-cols-adj">
        <Card class="component-card">
          <template v-slot:content>
            <div class="p-fluid">
              <application-landscape
                :id="selected_parameter.dep + selected_kpis.kpi.kpi_id"
                :data="data"
                :caption="caption"
                :subCaption="subCaption"
                :threshold="threshold"
              ></application-landscape>
            </div>
          </template>
          <template #footer>
            <show-applicability-kpi
              :id="selected_kpis.kpi.kpi_id + selected_kpis.kpi.name"
              :selected_dataset_id="selected_dataset_id"
              :selected_dataset_label="selected_dataset_label"
              :selected_kpi="selected_kpis"
              selected_parameter="all"
              gauge_type="hlineargauge"
            ></show-applicability-kpi>
          </template>
        </Card>
      </div>
    </div>
  </div>
</template>
<script>
import ShowApplicabilityKPI from "../HelperComponents/ShowApplicabilityKPI.vue";
import InputFieldDep from "../InputFields/InputFieldDep.vue";
import ApplicationLandscape from "../Plots/ApplicationLandscape.vue";

export default {
  components: {
    "show-applicability-kpi": ShowApplicabilityKPI,
    "input-field-dep": InputFieldDep,
    "application-landscape": ApplicationLandscape,
  },
  props: ["selected_dataset_id", "selected_dataset_label", "departments"],
  data() {
    return {
      selected_parameter: "",
      data: [{ label: "hi", value: 2 }],
      rendered_kpi_landscape: false,
      subCaption: "",
      triggered_rendering: false,
      kpis: this.get_kpis(),
      selected_kpis: "",
      caption: "",
      threshold: "",
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
    render_kpi_landscape() {
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
        this.rendered_kpi_landscape = false;
        this.data = [];
        this.$toast.add({
          severity: "info",
          summary: "Rendering KPI Landscape initiated...",
          detail: "This make take some time.. Please wait",
          life: 15000,
        });
        var formData = new FormData();
        formData.append("parameter", JSON.stringify(this.selected_parameter));
        formData.append("kpis", JSON.stringify(this.selected_kpis));
        this.$axios
          .post(
            "/render_application_landscape_kpi/" +
              this.selected_dataset_id +
              "/" +
              this.selected_dataset_label,
            formData
          )
          .then((res) => {
            this.data = [res.data["result"]];
            this.threshold = res.data["threshold"];
            this.subCaption = "";
            this.caption = "KPI Landscape";
            this.triggered_rendering = false;
            this.rendered_kpi_landscape = true;
          })
          .catch(() => {
            this.$toast.add({
              severity: "error",
              summary: "KPI Landscape Analysis Unsuccessful",
              detail: "Please make sure you selected all input fields",
              life: 5000,
            });
            this.triggered_rendering = false;
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