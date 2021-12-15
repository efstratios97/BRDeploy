<template>
  <div>
    <div class="p-grid p-fluid">
      <div class="p-col-12 p-md-12">
        <div class="p-inputgroup">
          <span class="p-inputgroup-addon">
            <b-icon-columns-gap />
          </span>
          <Dropdown
            v-model="selected_aspect"
            :options="aspects"
            :filter="true"
            optionLabel="aspect.name"
            placeholder="Assign Components to an Aspect"
            filterPlaceholder="Find Components"
            class="multiselect-custom"
            :showClear="true"
            :disabled="disabled_component"
          />
        </div>
      </div>
    </div>
    <div v-if="selected_aspect !== ''">
      <span v-if="selected_aspect !== undefined"
        >{{ this.getGaugeValue() }}
      </span>
      <kpi-applicability-gauge
        ref="applicabilityGauge"
        :id="id"
        :selected_component="selected_aspect.aspect.name"
        :gauge_value="gauge_value"
        gauge_type="hlineargauge"
        width="100%"
        height="19%"
      ></kpi-applicability-gauge>
    </div>
    <div class="p-grid p-align-center">
      <div class="p-col-4 p-md-4">
        <h3>Assign weight:</h3>
      </div>
      <div class="p-col-4 p-md-4">
        <Knob
          v-model="selected_weight"
          :min="0"
          :max="10"
          :disabled="disabled_weight"
        />
      </div>
      <div class="p-col-4 p-md-4">
        <Button
          label="Verify Weight"
          icon="pi pi-check"
          iconPos="center"
          class="p-button-success"
          @click="verify_weight()"
          v-tooltip="
            'Verify your weight! Else your Aspect will not be added to KPI'
          "
        />
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
      aspects: this.get_aspects(),
      operation_types: "",
      gauge_value: 75,
      selected_dataset_labels: "",
      selected_aspect: "",
      selected_weight: 0,
      disabled_component: false,
      disabled_weight: false,
      verified_weight: false,
    };
  },
  methods: {
    getGaugeValue() {
      if (this.selected_aspect !== undefined) {
        this.$axios
          .get(
            "/analyze_applicability_kpi_based_on_aspect/" +
              this.selected_aspect.aspect.aspect_id +
              "/" +
              this.selected_dataset_id +
              "/" +
              this.selected_dataset_label
          )
          .then((res) => {
            this.gauge_value = res.data.data;
            this.$refs.applicabilityGauge.update_value(this.gauge_value);
            if (this.selected_aspect !== undefined) {
              this.disabled_component = true;
              if (this.verified_weight === false) {
                this.$toast.add({
                  severity: "warn",
                  summary: "Verify also the Aspect's Weight",
                  detail:
                    "Press the 'Verify Weight' Button to add Aspect to KPI",
                  life: 5000,
                });
              } else {
                this.$emit("selected-aspect-weight", [
                  this.selected_aspect.aspect,
                  this.selected_weight,
                ]);
              }
            }
          });
      }
    },
    get_aspects() {
      this.$axios
        .get("/get_aspects_by_dataset_label/" + this.selected_dataset_label)
        .then((res) => {
          var aspects_tmp = [];
          for (let index = 0; index < res.data.data.length; index++) {
            aspects_tmp.push({ aspect: res.data.data[index] });
          }
          this.aspects = aspects_tmp;
        });
    },
    verify_weight() {
      console.log("verified");
      this.verified_weight = !this.verified_weight;
      console.log(this.verified_weight);
      this.disabled_weight = true;
    },
  },
};
</script>
