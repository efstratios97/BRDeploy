<template>
  <div>
    <input-field-app-dep-domain-kpi
      :selected_dataset_id="selected_dataset_id"
      :selected_dataset_label="selected_dataset_label"
      :apps="apps"
      :domains="domains"
      :departments="departments"
      @render="render_graphs"
    ></input-field-app-dep-domain-kpi>
    <br />
    <span v-if="render">
      <div class="container-...">
        <div class="row row-cols-auto auto-cols-adj">
          <div v-for="fd in formdatas" :key="fd">
            <Fieldset :toggleable="true" :legend="JSON.parse(fd.parameter).app">
              <br />
              <render-visualization
                v-if="render"
                :selected_dataset_id="selected_dataset_id"
                :selected_dataset_label="selected_dataset_label"
                :formdata="fd"
                :component_name="component_name"
                visualization="kpi_complete_view"
                :ref="fd.parameter"
                grouped="true"
              ></render-visualization>
              <br />
            </Fieldset>
            <br />
          </div>
        </div>
      </div>
    </span>
  </div>
</template>
<script>
import InputFieldAppDepDomainKPI from "../InputFields/InputFieldAppDepDomainKPI.vue";
import RenderVisualization from "../Plots/RenderVisualization.vue";

export default {
  components: {
    "input-field-app-dep-domain-kpi": InputFieldAppDepDomainKPI,
    "render-visualization": RenderVisualization,
  },
  props: ["selected_dataset_id", "selected_dataset_label"],
  data() {
    return {
      component_name: "KPI",
      render: false,
      show_aspects: false,
      show_kpi_applicability: false,
      parameters: "",
      formdatas: [],
      apps: this.getApps(),
      departments: this.getDatasetDepartmentOptions(),
      domains: this.getDomainsOptions(),
    };
  },
  methods: {
    getApps() {
      this.$axios
        .get(
          "/get_data/" +
            this.selected_dataset_id +
            "/" +
            this.selected_dataset_label +
            "/" +
            "get_apps_from_dataset"
        )
        .then((res) => {
          var apps_tmp = [];
          for (let index = 0; index < res.data.data.length; index++) {
            apps_tmp.push({ app: res.data.data[index] });
          }
          this.apps = apps_tmp;
        });
    },
    getDatasetDepartmentOptions() {
      this.$axios
        .get(
          "/get_data/" +
            this.selected_dataset_id +
            "/" +
            this.selected_dataset_label +
            "/" +
            "get_departments_from_dataset"
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
          "/get_data/" +
            this.selected_dataset_id +
            "/" +
            this.selected_dataset_label +
            "/" +
            "get_domains_from_dataset"
        )
        .then((res) => {
          var domains_tmp = [];
          for (let index = 0; index < res.data.data.length; index++) {
            domains_tmp.push({ domain: res.data.data[index] });
          }
          this.domains = domains_tmp;
        });
    },
    render_graphs(options) {
      this.formdatas = [];
      var parameter = JSON.parse(options.formdata.parameter);
      if (parameter instanceof Array === false) {
        parameter = [parameter];
      }
      var formdatas_tmp = [];
      var kpis = options.formdata.kpis;
      for (let index = 0; index < parameter.length; index++) {
        let formdata_tmp = {
          kpis: kpis,
          parameter: JSON.stringify(parameter[index]),
        };
        formdatas_tmp.push(formdata_tmp);
      }
      this.formdatas = formdatas_tmp;
      this.render = true;
      for (let index = 0; index < this.formdatas.length; index++) {
        this.$refs.this.formdatas[
          index
        ].formdata.parameter.render_visualization(
          this.formdatas[index].formdata,
          "kpi_complete_view"
        );
      }
    },
  },
};
</script>
<style scoped>
</style>