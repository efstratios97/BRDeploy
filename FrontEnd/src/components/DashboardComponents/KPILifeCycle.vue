<template>
  <div>
    <input-field-dep-domain-kpi
      :selected_dataset_id="selected_dataset_id"
      :selected_dataset_label="selected_dataset_label"
      :domains="domains"
      :departments="departments"
      @render="render_graphs"
    ></input-field-dep-domain-kpi>
    <render-visualization
      v-if="render"
      :selected_dataset_id="selected_dataset_id"
      :selected_dataset_label="selected_dataset_label"
      :formdata="formdata"
      :component_name="component_name"
      visualization="kpi_lifecycle_development"
      ref="myKPILifecycleDev"
    ></render-visualization>
    <render-visualization
      v-if="render"
      :selected_dataset_id="selected_dataset_id"
      :selected_dataset_label="selected_dataset_label"
      :formdata="formdata"
      :component_name="component_name"
      visualization="kpi_lifecycle"
      ref="myKPILifecycle"
    ></render-visualization>
    <render-visualization
      v-if="render"
      :selected_dataset_id="selected_dataset_id"
      :selected_dataset_label="selected_dataset_label"
      :formdata="formdata"
      :component_name="component_name"
      visualization="analyze_kpi_applicability"
      ref="myKPIApplicabilityAnalysis"
    ></render-visualization>
  </div>
</template>
<script>
import InputFieldDepDomainKPI from "../InputFields/InputFieldDepDomainKPI.vue";
import RenderVisualization from "../Plots/RenderVisualization.vue";

export default {
  components: {
    "input-field-dep-domain-kpi": InputFieldDepDomainKPI,
    "render-visualization": RenderVisualization,
  },
  props: ["selected_dataset_id", "selected_dataset_label"],
  data() {
    return {
      component_name: "KPILifeCycle",
      formdata: "",
      render: false,
      departments: this.getDatasetDepartmentOptions(),
      domains: this.getDomainsOptions(),
    };
  },
  methods: {
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
      this.formdata = options.formdata;
      this.render = true;
      this.$refs.myKPILifecycleDev.render_visualization(
        options.formdata,
        "kpi_lifecycle_development"
      );
      this.$refs.myKPILifecycle.render_visualization(
        options.formdata,
        "kpi_lifecycle"
      );
      this.$refs.myKPIApplicabilityAnalysis.render_visualization(
        options.formdata,
        "analyze_kpi_applicability"
      );
    },
  },
};
</script>