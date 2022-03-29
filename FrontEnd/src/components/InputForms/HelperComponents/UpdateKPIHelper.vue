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
            @change="render_visualization()"
          />
        </div>
      </div>
    </div>
    <div v-if="rendered">
      <fusion-chart :data="data"></fusion-chart>
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
  </div>
</template>
<script>
import FusionChart from "../../Plots/FusionChart.vue";

export default {
  components: {
    "fusion-chart": FusionChart,
  },
  props: [
    "id",
    "selected_dataset_id",
    "selected_dataset_label",
    "kpi_aspect_weight",
  ],
  data() {
    return {
      aspects: this.get_aspects(),
      operation_types: "",
      data: [],
      rendered: false,
      selected_aspect: "",
      selected_weight: 0,
      disabled_component: false,
      disabled_weight: false,
      verified_weight: false,
    };
  },
  created() {
    this.selected_aspect = {
      aspect: Object.keys(this.kpi_aspect_weight)[0],
    };
    this.selected_weight = Object.values(this.kpi_aspect_weight)[0];
    this.$axios
      .get("/get_aspect_by_name/" + Object.keys(this.kpi_aspect_weight)[0])
      .then((res) => {
        this.selected_aspect = { aspect: res.data };
      })
      .then(() => {
        this.render_visualization();
      });
  },
  methods: {
    render_visualization() {
      this.rendered = false;
      if (this.selected_aspect !== undefined) {
        var formdata = new FormData();
        formdata.append("aspect_id", this.selected_aspect.aspect.aspect_id);
        this.$axios
          .post(
            "/render_visualizations/" +
              this.selected_dataset_id +
              "/" +
              this.selected_dataset_label +
              "/" +
              "analyze_applicability_kpi_based_on_aspect",
            formdata
          )
          .then((res) => {
            this.data = res.data.result[0];
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
              }
            }
            this.rendered = true;
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
      this.verified_weight = !this.verified_weight;
      this.disabled_weight = true;
      if (this.selected_aspect !== undefined) {
        this.$emit("selected-aspect-weight-for-update", [
          this.selected_aspect.aspect,
          Object.values(this.kpi_aspect_weight)[0],
          this.selected_weight,
        ]);
      }
    },
  },
};
</script>
