<template>
  <div>
    <Fieldset legend="Select Input" :toggleable="true">
      <div class="p-grid">
        <div class="p-col">
          <div class="p-fluid">
            <input-field-dep
              :departments="departments"
              :selected_dataset_id="selected_dataset_id"
              :selected_dataset_label="selected_dataset_label"
              @input-parameter="assign_parameter($event)"
            ></input-field-dep>
          </div>
        </div>
        <div class="p-col">
          <div class="p-fluid">
            <input-field-kpi
              :selected_dataset_id="selected_dataset_id"
              :selected_dataset_label="selected_dataset_label"
              @input-kpis="assign_kpis($event)"
            ></input-field-kpi>
          </div>
        </div>
      </div>
      <apply-button
        :formdata="formdata"
        :inputfields_filled_count="inputfields_filled_count"
        :inputfields_number="inputfields_number"
        @render="render_visualization($event)"
      ></apply-button>
    </Fieldset>
  </div>
</template>
<script>
import InputFieldDep from "./InputFieldComponents/InputFieldDep.vue";
import InputFieldKPI from "./InputFieldComponents/InputFieldKPI.vue";
import ApplyButton from "../Plots/ApplyButton.vue";

export default {
  components: {
    "input-field-dep": InputFieldDep,
    "input-field-kpi": InputFieldKPI,
    "apply-button": ApplyButton,
  },
  props: [
    "apps",
    "departments",
    "domains",
    "selected_dataset_id",
    "selected_dataset_label",
  ],
  data() {
    return {
      formdata: {},
      inputfields_number: 2,
    };
  },
  methods: {
    render_visualization(options) {
      this.$emit("render", options);
    },
    assign_kpis(kpis) {
      this.formdata["kpis"] = JSON.stringify(kpis);
    },
    assign_parameter(parameter) {
      this.formdata["parameter"] = JSON.stringify(parameter);
    },
  },
};
</script>
<style scoped>
</style>