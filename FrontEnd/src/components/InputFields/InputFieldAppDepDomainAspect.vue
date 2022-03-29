<template>
  <div>
    <Fieldset legend="Select Input" :toggleable="true">
      <div class="p-grid">
        <div class="p-col">
          <div class="p-fluid">
            <input-field-app-dep-dom
              :apps="apps"
              :domains="domains"
              :departments="departments"
              :selected_dataset_id="selected_dataset_id"
              :selected_dataset_label="selected_dataset_label"
              @input-parameter="assign_parameter($event)"
            ></input-field-app-dep-dom>
          </div>
        </div>
        <div class="p-col">
          <div class="p-fluid">
            <input-field-aspect
              :selected_dataset_id="selected_dataset_id"
              :selected_dataset_label="selected_dataset_label"
              @input-aspect="assign_aspect($event)"
            ></input-field-aspect>
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
import InputFieldAppDepDom from "./InputFieldComponents/InputFieldAppDepDom.vue";
import InputAspect from "./InputFieldComponents/InputAspect.vue";
import ApplyButton from "../Plots/ApplyButton.vue";

export default {
  components: {
    "input-field-app-dep-dom": InputFieldAppDepDom,
    "input-field-aspect": InputAspect,
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
    assign_aspect(aspects) {
      this.formdata["aspects"] = JSON.stringify(aspects);
    },
    assign_parameter(parameter) {
      this.formdata["parameter"] = JSON.stringify(parameter);
    },
  },
};
</script>
<style scoped>
</style>