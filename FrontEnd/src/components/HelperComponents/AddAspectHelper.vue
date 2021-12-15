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
            placeholder="Assign Components to an Aspect"
            filterPlaceholder="Find Components"
            class="multiselect-custom"
            :showClear="true"
            :disabled="disabled_component"
            v-tooltip="
              'Once chosen please click Remove Component enable choice again!'
            "
          />
        </div>
      </div>
    </div>
    <div v-if="selected_raw_component !== ''">
      <span v-if="selected_raw_component !== undefined"
        >{{ this.getGaugeValue() }}
      </span>
      <kpi-applicability-gauge
        ref="applicabilityGauge"
        :id="id"
        :selected_component="selected_raw_component.raw_component"
        :gauge_value="gauge_value"
        gauge_type="hlineargauge"
        width="100%"
        height="19%"
      ></kpi-applicability-gauge>
    </div>
    <!-- <div class="p-grid p-align-center">
        <div class="p-col-6 p-md-6">
          <h3>Assign weight:</h3>
        </div>
        <div class="p-col-6 p-md-6">
          <Knob v-model="selected_weight" :min="0" :max="10" />
        </div>
      </div> -->
    <div class="p-grid p-fluid">
      <div class="p-col-12 p-md-12">
        <div class="p-inputgroup">
          <span class="p-inputgroup-addon">
            <b-icon-tag />
          </span>
          <Dropdown
            v-model="selected_operation_type"
            :options="operation_types"
            :filter="true"
            optionLabel="operation_type"
            placeholder="Assign Category to an Aspect"
            filterPlaceholder="Find Category"
            class="multiselect-custom"
            :showClear="true"
            :disabled="disabled_type"
            v-tooltip="
              'Once chosen please click Remove Component enable choice again!'
            "
          />
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import KPIApplicabilityGauge from "../Plots/KPIApplicabilityGauge.vue";

export default {
  components: {
    "kpi-applicability-gauge": KPIApplicabilityGauge,
  },
  props: ["id", "selected_dataset_id", "selected_dataset_label"],
  data() {
    return {
      raw_components: this.getRawComponentsOptions(),
      operation_types: this.getKPICategoryTypesOptions(),
      gauge_value: 75,
      selected_dataset_labels: "",
      selected_raw_component: "",
      selected_operation_type: "",
      selected_raw_component_tmp: "1",
      disabled_component: false,
      disabled_type: false,
    };
  },
  methods: {
    getGaugeValue() {
      if (this.selected_raw_component !== undefined) {
        this.$axios
          .get(
            "/analyze_applicability/" +
              this.selected_raw_component.raw_component +
              "/" +
              this.selected_dataset_id +
              "/" +
              this.selected_dataset_label
          )
          .then((res) => {
            this.gauge_value = res.data.data;
            this.selected_raw_component_tmp =
              this.selected_raw_component.raw_component;
            this.$refs.applicabilityGauge.update_value(this.gauge_value);
            this.$emit("selected-raw-component-operation-type", [
              this.selected_raw_component.raw_component,
              this.selected_operation_type.operation_type,
            ]);
            if (this.selected_raw_component !== undefined) {
              this.disabled_component = true;
              this.getKPICategoryTypesOptions();
            }
            if (this.selected_operation_type !== "") {
              this.disabled_type = true;
            }
          });
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
            this.selected_raw_component_tmp +
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
        });
    },
  },
};
</script>
