<template>
  <div>
    <input-field-dep-domain-architecture-view
      :selected_dataset_id="selected_datset_id"
      :selected_dataset_label="selected_dataset_label"
      :departments="departments"
      :domains="domains"
      @render="render_graphs($event)"
    ></input-field-dep-domain-architecture-view>
    <render-visualization
      v-if="render"
      :selected_dataset_id="selected_dataset_id"
      :selected_dataset_label="selected_dataset_label"
      :formdata="formdata"
      visualization="architecture_view_analysis_complete_conditional"
      ref="myArchitectureViewAnalysis"
      separated_display="true"
    ></render-visualization>
  </div>
</template>

<script>
import InputFieldDepDomainArchitectureView from "../InputFields/InputFieldDepDomainArchitectureView.vue";
import RenderVisualization from "../Plots/RenderVisualization.vue";

export default {
  props: ["selected_datset_id", "selected_dataset_label"],
  components: {
    "input-field-dep-domain-architecture-view":
      InputFieldDepDomainArchitectureView,
    "render-visualization": RenderVisualization,
  },
  data() {
    return {
      departments: [],
      domains: [],
      render: false,
    };
  },
  created() {
    this.getDatasetDepartmentOptions();
    this.getDomainsOptions();
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
    render_graphs(options) {
      this.formdata = options.formdata;
      this.render = true;
      this.$refs.myArchitectureViewAnalysis.render_visualization(
        options.formdata,
        "architecture_view_analysis_complete_conditional"
      );
    },
  },
};
</script>