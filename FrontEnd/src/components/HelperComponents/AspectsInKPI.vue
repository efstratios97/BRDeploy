<template>
  <div>
    <div class="p-grid">
      <div class="p-col">
        <div class="p-fluid">
          <Button
            label="KPI composition"
            @click="toggleShowAspectsComposition(kpi_id, selected_parameter)"
            icon="pi pi-check"
            iconPos="right"
          />
        </div>
      </div>
      <div class="p-col">
        <div class="p-fluid">
          <Button
            label="KPI Applicability App"
            @click="toggleShowKPIAppApplicability()"
            icon="pi pi-check"
            iconPos="right"
          />
        </div>
      </div>
    </div>
    <div v-if="show_aspects">
      <div class="container-..." v-if="triggered_rendering">
        <h1>Rendering Aspects from {{ kpi_name }}</h1>
        <h3>Please wait...</h3>
        <ProgressBar mode="indeterminate" />
      </div>
      <div v-if="rendered_graph_aspects">
        <aspect-app-analysis
          :id="kpi_id"
          :data="data[0].data"
          :caption="selected_parameter"
          :subCaption="subCaption"
        ></aspect-app-analysis>
      </div>
    </div>
    <div v-if="show_kpi_app_applicability">
      <show-applicability-kpi
        :id="selected_parameter[Object.keys(selected_parameter)[0]] + kpi_id"
        :selected_dataset_id="selected_dataset_id"
        :selected_dataset_label="selected_dataset_label"
        :selected_kpi="selected_kpi"
        :selected_parameter="selected_parameter"
        gauge_type="bulb"
      ></show-applicability-kpi>
    </div>
  </div>
</template>
<script>
import AspectAppAnalysis from "../Plots/AspectAppAnalysis.vue";
import ShowApplicabilityKPI from "../HelperComponents/ShowApplicabilityKPI.vue";

export default {
  components: {
    "aspect-app-analysis": AspectAppAnalysis,
    "show-applicability-kpi": ShowApplicabilityKPI,
  },
  props: [
    "kpi_id",
    "selected_parameter",
    "kpi_name",
    "selected_dataset_id",
    "selected_dataset_label",
    "aspects_weights",
  ],
  data() {
    return {
      rendered_graph_aspects: false,
      subCaption: "",
      triggered_rendering: true,
      data: [],
      show_aspects: false,
      show_kpi_app_applicability: false,
      selected_kpi: "",
      gauge_value: "",
    };
  },
  methods: {
    toggleShowAspectsComposition(kpi_id, selected_parameter) {
      this.show_aspects = !this.show_aspects;
      this.get_aspects_by_kpi_id(kpi_id, selected_parameter);
    },
    toggleShowKPIAppApplicability() {
      this.selected_kpi = { kpi: { name: this.kpi_name, kpi_id: this.kpi_id } };
      this.show_kpi_app_applicability = !this.show_kpi_app_applicability;
    },
    get_aspects_by_kpi_id(kpi_id, selected_parameter) {
      this.$axios.get("/get_aspects_by_kpi_id/" + kpi_id).then((res) => {
        var aspects_tmp = [];
        for (let index = 0; index < res.data.data.length; index++) {
          aspects_tmp.push({ aspect: res.data.data[index] });
        }
        this.render_aspects(aspects_tmp, selected_parameter);
      });
    },
    render_aspects(aspects, selected_parameter) {
      this.triggered_rendering = true;
      this.rendered_graph_aspects = false;
      this.data = [];
      this.$toast.add({
        severity: "info",
        summary: "Rendering Aspect Visualization initiated...",
        detail: "This make take some time.. Please wait",
        life: 15000,
      });
      var formData = new FormData();
      formData.append("parameter", JSON.stringify(selected_parameter));
      formData.append("aspects", JSON.stringify(aspects));
      this.$axios
        .post(
          "/calculate_aspects/" +
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
              var data_tmp = [];
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
                data_tmp.push({
                  label:
                    res.data[this.selected_parameter[index].parameter][index_2]
                      .aspect_name,
                  value:
                    res.data[this.selected_parameter[index].parameter][index_2]
                      .result,
                });
              }
              this.data.push({
                parameter: this.selected_parameter[index].parameter,
                data: data_tmp,
              });
              delete Object.assign(this.selected_parameter[index], {
                [oldKey]: this.selected_parameter[index][newKey],
              })[newKey];
            }
          } else {
            var key = Object.keys(this.selected_parameter)[0];
            data_tmp = [];
            for (
              let index_3 = 0;
              index_3 < res.data[this.selected_parameter[key]].length;
              index_3++
            ) {
              data_tmp.push({
                label:
                  res.data[this.selected_parameter[key]][index_3].aspect_name,
                value: res.data[this.selected_parameter[key]][index_3].result,
              });
            }
            this.data.push({
              parameter: this.selected_parameter,
              data: data_tmp,
            });
          }
          var aspect_weight_tmp = "";
          var aspects_weights = this.aspects_weights;
          for (let index = 0; index < this.aspects_weights.length; index++) {
            aspect_weight_tmp = JSON.stringify(this.aspects_weights[index]);
            aspects_weights[index] = aspect_weight_tmp
              .replace("{", "Weighting")
              .replace("}", "");
          }
          this.subCaption = aspects_weights
            .toString()
            .replaceAll('"', " ")
            .replaceAll(":", " : ")
            .replaceAll(",", " , ");
          this.triggered_rendering = false;
          this.rendered_graph_aspects = true;
        })
        .catch(() => {
          this.$toast.add({
            severity: "error",
            summary: "Aspect Analysis Unsuccessful",
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