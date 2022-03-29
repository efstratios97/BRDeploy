<template>
  <div>
    <input-field-app-dep-domain-aspect
      :selected_dataset_id="selected_dataset_id"
      :selected_dataset_label="selected_dataset_label"
      :apps="apps"
      :domains="domains"
      :departments="departments"
      @render="render_graphs"
    ></input-field-app-dep-domain-aspect>
    <render-visualization
      v-if="render"
      :selected_dataset_id="selected_dataset_id"
      :selected_dataset_label="selected_dataset_label"
      :formdata="formdata"
      :component_name="component_name"
      visualization="aspects"
      ref="myAspects"
    ></render-visualization>
  </div>
</template>
<script>
import InputFieldAppDepDomainAspect from "../InputFields/InputFieldAppDepDomainAspect.vue";
import RenderVisualization from "../Plots/RenderVisualization.vue";

export default {
  components: {
    "input-field-app-dep-domain-aspect": InputFieldAppDepDomainAspect,
    "render-visualization": RenderVisualization,
  },
  props: ["selected_dataset_id", "selected_dataset_label"],
  data() {
    return {
      component_name: "KPIAspects",
      formdata: "",
      render: false,
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
      this.formdata = options.formdata;
      this.render = true;
      this.$refs.myAspects.render_visualization(options.formdata, "aspects");
    },
  },
};
</script>
<style scoped>
</style>