<template>
  <div>
    <Fieldset legend="Select Input" :toggleable="true">
      <div class="p-grid">
        <div class="p-col">
          <div class="p-fluid">
            <input-field-dep-dom
              :departments="departments"
              :domains="domains"
              :selected_dataset_id="selected_dataset_id"
              :selected_dataset_label="selected_dataset_label"
              @input-parameter="assign_parameter($event)"
            ></input-field-dep-dom>
          </div>
        </div>
        <div class="p-col">
          <div class="p-fluid">
            <input-field-architecture-view
              :selected_dataset_id="selected_dataset_id"
              :selected_dataset_label="selected_dataset_label"
              @input-architecture-view="assign_architecture_view($event)"
            ></input-field-architecture-view>
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
import InputFieldDepDom from "./InputFieldComponents/InputFieldDepDom.vue";
import InputFieldArchitectureView from "./InputFieldComponents/InputFieldArchitectureView.vue";
import ApplyButton from "../Plots/ApplyButton.vue";

export default {
  components: {
    "input-field-dep-dom": InputFieldDepDom,
    "input-field-architecture-view": InputFieldArchitectureView,
    "apply-button": ApplyButton,
  },
  props: [
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
    assign_architecture_view(architecture_view) {
      this.formdata["architecture_view"] = JSON.stringify(architecture_view);
    },
    assign_parameter(parameter) {
      this.formdata["parameter"] = JSON.stringify(parameter);
    },
  },
};
</script>