<template>
  <div>
    <div class="p-grid p-fluid">
      <div class="p-col-12 p-md-12">
        <div class="p-inputgroup">
          <span class="p-inputgroup-addon">
            <b-icon-columns-gap />
          </span>
          <Dropdown
            v-model="selected_raw_component"
            :options="raw_components"
            :filter="true"
            optionLabel="raw_component"
            :placeholder="selected_raw_component_placeholder"
            filterPlaceholder="Find Components"
            class="multiselect-custom"
            :showClear="true"
            :disabled="disabled_component"
            v-tooltip="
              'Once chosen please click Remove Component enable choice again!'
            "
            @change="render_raw_component_applicability()"
          />
        </div>
      </div>
    </div>
    <div v-if="rendered">
      <fusion-chart :data="data"> </fusion-chart>
    </div>
    <update-aspect-helper-category
      v-if="show_operation_types"
      :selected_dataset_id="selected_dataset_id"
      :selected_dataset_label="selected_dataset_label"
      :operation_types="operation_types"
      :operation_type="selected_operation_type"
      @input-operation-type="assign_operation_type($event)"
    ></update-aspect-helper-category>
  </div>
</template>
<script>
import FusionChart from "../../Plots/FusionChart.vue";
import UpdateAspectHelperCategory from "./UpdateAspectHelperCategory.vue";

export default {
  components: {
    "update-aspect-helper-category": UpdateAspectHelperCategory,
    "fusion-chart": FusionChart,
  },
  props: [
    "id",
    "selected_dataset_id",
    "selected_dataset_label",
    "raw_component",
  ],
  data() {
    return {
      raw_components: this.getRawComponentsOptions(),
      operation_types: "",
      rendered: false,
      show_operation_types: false,
      selected_raw_component: "",
      selected_operation_type: "",
      selected_raw_component_placeholder: "",
      disabled_component: false,
      data: [],
    };
  },
  created() {
    this.selected_raw_component = {
      raw_component: Object.keys(this.raw_component)[0],
    };
    this.selected_raw_component_placeholder = Object.keys(
      this.raw_component
    )[0];
    this.selected_operation_type = {
      operation_type: Object.values(this.raw_component)[0],
    };
    this.render_raw_component_applicability();
  },
  methods: {
    render_raw_component_applicability() {
      this.rendered = false;
      var formdata = new FormData();
      formdata.append(
        "raw_component",
        JSON.stringify(this.selected_raw_component)
      );
      this.$axios
        .post(
          "/render_visualizations/" +
            this.selected_dataset_id +
            "/" +
            this.selected_dataset_label +
            "/" +
            "analyze_applicability_raw_component",
          formdata
        )
        .then((res) => {
          this.data = res.data.result[0];
          this.rendered = true;
          if (
            this.selected_raw_component !== undefined &&
            this.disabled_component !== true
          ) {
            this.disabled_component = true;
            this.getKPICategoryTypesOptions();
          }
        });
    },
    assign_operation_type(selected_operation_type) {
      this.selected_operation_type = selected_operation_type;
      if (this.selected_operation_type !== "") {
        this.disabled_type = true;
      }
      if (
        this.selected_raw_component.raw_component !== undefined &&
        this.selected_operation_type !== undefined
      ) {
        this.$emit("selected-raw-component-operation-type", [
          this.selected_raw_component.raw_component,
          this.selected_operation_type,
        ]);
      }
    },
    getRawComponentsOptions() {
      this.$axios
        .get(
          "/get_all_raw_components/" +
            this.selected_dataset_id +
            "/" +
            this.selected_dataset_label
        )
        .then((res) => {
          var raw_components_tmp = [];
          for (let index = 0; index < res.data.data.length; index++) {
            raw_components_tmp.push({ raw_component: res.data.data[index] });
          }
          this.raw_components = raw_components_tmp;
        });
    },
    getKPICategoryTypesOptions() {
      this.$axios
        .get(
          "/get_suitable_kpi_category_types/" +
            this.selected_raw_component.raw_component +
            "/" +
            this.selected_dataset_id +
            "/" +
            this.selected_dataset_label
        )
        .then((res) => {
          var operation_type_tmp = [];
          for (let index = 0; index < res.data.data.length; index++) {
            operation_type_tmp.push({
              operation_type: res.data.data[index]["name"],
            });
          }
          this.operation_types = operation_type_tmp;
          this.show_operation_types = true;
        });
    },
  },
};
</script>
