<template>
  <div>
    <input-field-dep-kpi
      :selected_dataset_id="selected_dataset_id"
      :selected_dataset_label="selected_dataset_label"
      :departments="departments"
      @render="render_graphs"
    ></input-field-dep-kpi>
    <render-visualization
      v-if="render"
      :selected_dataset_id="selected_dataset_id"
      :selected_dataset_label="selected_dataset_label"
      :formdata="formdata"
      :component_name="component_name"
      visualization="kpi_landscape"
      ref="myApplicationlandscape"
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
import InputFieldDepKPI from "../InputFields/InputFieldDepKPI.vue";
import RenderVisualization from "../Plots/RenderVisualization.vue";

export default {
  components: {
    "input-field-dep-kpi": InputFieldDepKPI,
    "render-visualization": RenderVisualization,
  },
  props: ["selected_dataset_id", "selected_dataset_label"],
  data() {
    return {
      component_name: "KPIAppLandscape",
      formdata: "",
      render: false,
      departments: this.getDatasetDepartmentOptions(),
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
    render_graphs(options) {
      this.formdata = options.formdata;
      this.render = true;
      this.$refs.myApplicationlandscape.render_visualization(
        options.formdata,
        "kpi_landscape"
      );
      this.$refs.myKPIApplicabilityAnalysis.render_visualization(
        options.formdata,
        "analyze_kpi_applicability"
      );
    },
  },
};
</script>