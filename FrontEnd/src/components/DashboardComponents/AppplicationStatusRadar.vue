<template>
  <div>
    <input-field-app-dep-domain-architecture-view
      :selected_dataset_id="selected_datset_id"
      :selected_dataset_label="selected_dataset_label"
      :departments="departments"
      :domains="domains"
      :apps="apps"
      :showArchitectureViewInfo="true"
      :multiple_dep="true"
      :multiple_dom="true"
      @render="render_graphs($event)"
    ></input-field-app-dep-domain-architecture-view>
    <render-visualization
      v-if="render"
      :selected_dataset_id="selected_dataset_id"
      :selected_dataset_label="selected_dataset_label"
      :formdata="formdata"
      visualization="analyze_application_status_radar"
      ref="myApplicationStatusAnalysis"
      separated_display="true"
    ></render-visualization>
  </div>
</template>

<script>
import InputFieldAppDepDomainArchitectureView from "../InputFields/InputFieldAppDepDomainArchitectureView.vue";
import RenderVisualization from "../Plots/RenderVisualization.vue";

export default {
  props: ["selected_datset_id", "selected_dataset_label"],
  components: {
    "input-field-app-dep-domain-architecture-view":
      InputFieldAppDepDomainArchitectureView,
    "render-visualization": RenderVisualization,
  },
  data() {
    return {
      apps: [],
      departments: [],
      domains: [],
      render: false,
    };
  },
  created() {
    this.getDatasetDepartmentOptions();
    this.getDomainsOptions();
    this.getApps();
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
          res.data.data.forEach((department) =>
            this.departments.push({ dep: department })
          );
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
          res.data.data.forEach((domain) => {
            this.domains.push({ domain: domain });
          });
        });
    },
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
          res.data.data.forEach((app) => {
            this.apps.push({ app: app });
          });
        });
    },
    render_graphs(options) {
      this.formdata = options.formdata;
      this.render = true;
      this.$refs.myApplicationStatusAnalysis.render_visualization(
        options.formdata,
        "analyze_application_status_radar"
      );
    },
  },
};
</script>