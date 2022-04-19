<template>
  <div>
    <Fieldset legend="Select Input" :toggleable="true">
      <div class="p-grid">
        <div class="p-col">
          <div class="p-fluid">
            <input-field-app-dep-dom
              :apps="apps"
              :departments="departments"
              :domains="domains"
              :selected_dataset_id="selected_dataset_id"
              :selected_dataset_label="selected_dataset_label"
              :multiple_dep="multiple_dep"
              :multiple_dom="multiple_dom"
              @input-parameter="assign_parameter($event)"
            ></input-field-app-dep-dom>
          </div>
        </div>
        <div class="p-col">
          <div class="p-fluid">
            <input-field-architecture-view
              :selected_dataset_id="selected_dataset_id"
              :selected_dataset_label="selected_dataset_label"
              :showArchitectureViewInfo="showArchitectureViewInfo"
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
import InputFieldAppDepDom from "./InputFieldComponents/InputFieldAppDepDom.vue";
import InputFieldArchitectureView from "./InputFieldComponents/InputFieldArchitectureView.vue";
import ApplyButton from "../Plots/ApplyButton.vue";

export default {
  components: {
    "input-field-app-dep-dom": InputFieldAppDepDom,
    "input-field-architecture-view": InputFieldArchitectureView,
    "apply-button": ApplyButton,
  },
  props: [
    "apps",
    "departments",
    "domains",
    "selected_dataset_id",
    "selected_dataset_label",
    "showArchitectureViewInfo",
    "multiple_dep",
    "multiple_dom",
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