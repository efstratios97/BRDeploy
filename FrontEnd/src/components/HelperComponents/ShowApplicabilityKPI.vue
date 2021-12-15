<template>
  <div>
    <kpi-applicability-gauge
      ref="applicabilityGauge"
      :id="id"
      :selected_component="selected_kpi.kpi.name"
      :gauge_value="gauge_value"
      :gauge_type="gauge_type"
      width="450"
      height="300"
    ></kpi-applicability-gauge>
  </div>
</template>
<script>
import KPIApplicabilityGauge from "../Plots/KPIApplicabilityGauge.vue";

export default {
  //If MultiSelect selected_kpi.kpi.name; seleceted_kpi.kpi.kpi_id
  components: {
    "kpi-applicability-gauge": KPIApplicabilityGauge,
  },
  props: [
    "id",
    "selected_kpi",
    "selected_dataset_id",
    "selected_dataset_label",
    "selected_parameter",
    "gauge_type",
  ],
  data() {
    return {
      gauge_value: this.getGaugeValue(),
    };
  },
  methods: {
    getGaugeValue() {
      var selected_parameter = "";
      if (
        typeof this.selected_parameter === "string" ||
        this.selected_parameter instanceof String
      ) {
        selected_parameter = this.selected_parameter;
      } else {
        selected_parameter = JSON.stringify(this.selected_parameter);
      }
      if (this.selected_kpi !== undefined) {
        this.$axios
          .get(
            "/analyze_applicability_kpi/" +
              this.selected_kpi.kpi.kpi_id +
              "/" +
              this.selected_dataset_id +
              "/" +
              this.selected_dataset_label +
              "/" +
              selected_parameter
          )
          .then((res) => {
            this.gauge_value = res.data.data;
            this.$refs.applicabilityGauge.update_value(this.gauge_value);
          })
          .catch(() => {
            this.$toast.add({
              severity: "error",
              summary: "Applicability Analysis Unsuccessful",
              detail: "Please retry",
              life: 5000,
            });
          });
      }
    },
  },
};
</script>
