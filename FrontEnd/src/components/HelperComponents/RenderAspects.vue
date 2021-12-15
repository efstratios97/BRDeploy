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
          <template v-slot:title> Aspects </template>
          <template v-slot:subtitle>
            Select Aspects to perform Aspect Analysis
          </template>
          <template v-slot:content>
            <form class="overflow-auto">
              <MultiSelect
                v-model="selected_aspects"
                :options="aspects"
                :filter="true"
                optionLabel="aspect.name"
                placeholder="Select Aspect"
                filterPlaceholder="Find an Aspect"
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
              @click="render_aspects()"
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
          <!-- <div class="container-..."> -->
          <h1>Rendering Aspects...</h1>
          <h3>Please wait...</h3>
          <ProgressBar mode="indeterminate" />
          <!-- </div> -->
        </div>
      </template>
    </Card>
    <div class="container-..." v-if="rendered_graph_aspects">
      <div class="row row-cols-auto auto-cols-adj">
        <div v-for="data_point in data" :key="data_point.app">
          <Card class="component-card">
            <template v-slot:content>
              <div class="p-fluid">
                <aspect-app-analysis
                  :id="data_point.parameter"
                  :data="data_point.data"
                  :caption="data_point.parameter"
                  :subCaption="subCaption"
                ></aspect-app-analysis>
              </div>
            </template>
          </Card>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import AspectAppAnalysis from "../Plots/AspectAppAnalysis.vue";
import InputFieldAppDepDom from "../InputFields/InputFieldAppDepDom.vue";

export default {
  components: {
    "aspect-app-analysis": AspectAppAnalysis,
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
      data: [],
      subCaption: "",
      aspects: this.get_aspects(),
      rendered_graph_aspects: false,
      triggered_rendering: false,
      selected_aspects: "",
    };
  },
  methods: {
    assign_parameter(parameter) {
      this.selected_parameter = parameter;
    },
    get_aspects() {
      this.$axios
        .get("/get_aspects_by_dataset_label/" + this.selected_dataset_label)
        .then((res) => {
          var aspects_tmp = [];
          for (let index = 0; index < res.data.data.length; index++) {
            aspects_tmp.push({ aspect: res.data.data[index] });
          }
          this.aspects = aspects_tmp;
        });
    },
    render_aspects() {
      if (this.selected_parameter === "" || this.selected_aspects === "") {
        this.$toast.add({
          severity: "warn",
          summary: "No Parameter and/or Aspect chosen",
          detail:
            "Please select first the Parameter & Aspect in both of the input fields",
          life: 8000,
        });
      } else {
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
        formData.append("parameter", JSON.stringify(this.selected_parameter));
        formData.append("aspects", JSON.stringify(this.selected_aspects));
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
                      res.data[this.selected_parameter[index].parameter][
                        index_2
                      ].aspect_name,
                    value:
                      res.data[this.selected_parameter[index].parameter][
                        index_2
                      ].result,
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
              newKey = "parameter";
              oldKey = Object.keys(this.selected_parameter);
              delete Object.assign(this.selected_parameter, {
                [newKey]: this.selected_parameter[oldKey],
              })[oldKey];
              data_tmp = [];
              for (
                let index_3 = 0;
                index_3 < res.data[this.selected_parameter[newKey]].length;
                index_3++
              ) {
                data_tmp.push({
                  label:
                    res.data[this.selected_parameter[newKey]][index_3]
                      .aspect_name,
                  value:
                    res.data[this.selected_parameter[newKey]][index_3].result,
                });
              }
              this.data.push({
                parameter: this.selected_parameter.parameter,
                data: data_tmp,
              });
              delete Object.assign(this.selected_parameter, {
                [oldKey]: this.selected_parameter[newKey],
              })[newKey];
            }
            this.subCaption = "Aspect Analysis per Application";
            this.triggered_rendering = false;
            this.rendered_graph_aspects = true;
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