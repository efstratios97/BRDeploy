<template>
  <div>
    <form>
      <div class="p-grid p-fluid">
        <div class="p-col-12 p-md-12">
          <div class="p-inputgroup">
            <span class="p-inputgroup-addon">
              <i class="pi pi-file"></i>
            </span>
            <InputText
              placeholder="KPI's Name"
              v-model="name"
              class="inputfield w-full"
            />
          </div>
        </div>
      </div>

      <div class="p-grid p-fluid">
        <div class="p-col-12 p-md-12">
          <Textarea
            placeholder="Description"
            v-model="description"
            :autoResize="true"
            rows="5"
            cols="30"
          />
        </div>
      </div>

      <div class="p-grid p-fluid">
        <div class="p-col-12 p-md-12">
          <div class="p-inputgroup">
            <span class="p-inputgroup-addon">
              <i class="pi pi-file"></i>
            </span>
            <MultiSelect
              v-model="selected_dataset_labels"
              :options="labels"
              :filter="true"
              optionLabel="label"
              placeholder="Assign applicable Labels"
              filterPlaceholder="Find Labels"
              :showClear="true"
            />
          </div>
        </div>
      </div>

      <div
        v-for="kpi_aspect_weight in initial_kpi_aspects_weights"
        :key="kpi_aspect_weight"
      >
        <update-kpi-helper
          :selected_dataset_id="selected_dataset_id"
          :selected_dataset_label="selected_dataset_label"
          :id="id"
          :kpi_aspect_weight="kpi_aspect_weight"
          @selected-aspect-weight-for-update="update_aspect_weight($event)"
        ></update-kpi-helper>
        <div class="p-grid p-fluid">
          <div class="p-col-12 p-md-12">
            <Button
              label="Remove Further Components"
              icon="pi pi-minus-circle"
              iconPos="center"
              class="p-button-danger"
              @click="remove_aspect(kpi_aspect_weight)"
            />
          </div>
        </div>
      </div>

      <div v-for="number in number_components" :key="number">
        <add-kpi-helper
          :selected_dataset_id="selected_dataset_id"
          :selected_dataset_label="selected_dataset_label"
          :id="id"
          @selected-aspect-weight="add_to_aspect_weight($event)"
        ></add-kpi-helper>
      </div>
      <div class="p-grid p-fluid">
        <div class="p-col-6 p-md-6">
          <Button
            label="Add Further Aspect"
            icon="pi pi-plus-circle"
            iconPos="center"
            class="p-button-success"
            @click="add_further_aspect"
          />
        </div>
        <div class="p-col-6 p-md-6">
          <Button
            label="Remove Further Components"
            icon="pi pi-minus-circle"
            iconPos="center"
            class="p-button-danger"
            @click="remove_further_aspect"
          />
        </div>
      </div>
      <div class="p-grid p-align-center">
        <div class="p-col-6 p-md-6">
          <h3>Assign Threshold:</h3>
        </div>
        <div class="p-col-6 p-md-6">
          <Knob v-model="selected_threshold" :min="0" :max="10" />
        </div>
      </div>

      <div class="p-grid p-fluid">
        <div class="p-col-12 p-md-12">
          <div class="p-inputgroup">
            <span class="p-inputgroup-addon">
              <b-icon-speedometer2 />
            </span>
            <Dropdown
              v-model="selected_color_coding"
              :options="color_codings"
              :filter="true"
              optionLabel="color_coding"
              placeholder="Select the right Logic for the Gauge's Color Coding"
              filterPlaceholder="Find Logic for Color coding"
              class="multiselect-custom"
            >
              <template #value="slotProps">
                <div v-if="slotProps.value">
                  <span
                    v-if="
                      slotProps.value.color_coding === 'the Higher the Better'
                    "
                  >
                    <img
                      src="~@/assets/Gauge_the_higher_the_better.png"
                      class="kpi-image"
                    />
                  </span>
                  <span
                    v-if="
                      slotProps.value.color_coding === 'the Lower the Better'
                    "
                    ><img
                      src="~@/assets/Gauge_the_lower_the_better.png"
                      class="kpi-image"
                  /></span>
                  {{ slotProps.value.color_coding }}
                </div>
              </template>
              <template #option="slotProps">
                <span
                  v-if="
                    slotProps.option.color_coding === 'the Higher the Better'
                  "
                >
                  <img
                    src="~@/assets/Gauge_the_higher_the_better.png"
                    class="kpi-image"
                  />
                </span>
                <span
                  v-if="
                    slotProps.option.color_coding === 'the Lower the Better'
                  "
                  ><img
                    src="~@/assets/Gauge_the_lower_the_better.png"
                    class="kpi-image"
                /></span>

                {{ slotProps.option.color_coding }}
              </template>
            </Dropdown>
          </div>
        </div>
      </div>

      <div class="p-grid p-fluid">
        <div class="p-col-12 p-md-12">
          <div class="p-inputgroup">
            <span class="p-inputgroup-addon">
              <b-icon-calculator />
            </span>
            <Dropdown
              v-model="selected_formula"
              :options="formulas"
              :filter="true"
              optionLabel="formula"
              placeholder="Assign Formula to an Aspect"
              filterPlaceholder="Find Formula"
              class="multiselect-custom"
            />
          </div>
        </div>
      </div>
      <div class="p-grid p-fluid">
        <div class="p-col-12 p-md-12">
          <Button
            label="Update KPI"
            icon="pi pi-refresh"
            iconPos="center"
            @click="update_kpi"
          />
        </div>
      </div>
      <div v-if="submitted">
        <br />
        <ProgressBar mode="indeterminate" v-if="submitted" />
      </div>
    </form>
  </div>
</template>

<script>
import AddKPIHelper from "./HelperComponents/AddKPIHelper.vue";
import UpdateKPIHelper from "./HelperComponents/UpdateKPIHelper.vue";

export default {
  props: ["kpi"],
  components: {
    "add-kpi-helper": AddKPIHelper,
    "update-kpi-helper": UpdateKPIHelper,
  },
  data() {
    return {
      selected_dataset_id: localStorage.selected_dataset_id,
      selected_dataset_label: localStorage.selected_dataset_label,
      name: "",
      description: "",
      datasets: this.getDatasetOptions(),
      labels: this.getLabelsOptions(),
      aspects: this.get_aspects(),
      formulas: this.getFormulas("kpi"),
      selected_dataset_labels: [],
      selected_threshold: 0,
      selected_aspect: "",
      selected_weight: 0,
      selected_aspects_weights: [],
      selected_formula: "",
      initial_kpi_aspects_weights: [],
      number_components: 1,
      formData: "",
      submitted: false,
      selected_color_coding: "",
      color_codings: [
        { color_coding: "the Higher the Better" },
        { color_coding: "the Lower the Better" },
      ],
    };
  },
  created() {
    this.name = this.kpi.name;
    this.description = this.kpi.description;
    this.selected_threshold = this.kpi.threshold;
    this.selected_color_coding = { color_coding: this.kpi.color_coding };
    this.selected_formula = { formula: this.kpi.formula };
    this.initial_kpi_aspects_weights = this.kpi.kpi_aspects_weights;
    for (
      let index = 0;
      index < this.kpi.dataset_labels.split(",").length;
      index++
    ) {
      this.$axios
        .get("/get_label_by_id/" + this.kpi.dataset_labels.split(",")[index])
        .then((res) => {
          this.selected_dataset_labels.push({
            label:
              "NAME: " +
              res.data[0]["name"] +
              "   |   " +
              "ID: " +
              res.data[0]["label_id"],
          });
        });
    }
  },
  methods: {
    containsObject(obj, list) {
      var i;
      for (i = 0; i < list.length; i++) {
        var obj_tmp = JSON.parse(JSON.stringify(list[i]));
        obj = JSON.parse(JSON.stringify(obj));
        if (
          Object.keys(obj_tmp)[0] === Object.keys(obj)[0] &&
          Object.values(obj_tmp)[0] === Object.values(obj)[0]
        ) {
          return true;
        }
      }
      return false;
    },
    add_to_aspect_weight(aspect_weight) {
      var obj_to_push = {};
      obj_to_push[aspect_weight[0].name] = aspect_weight[1];
      if (
        aspect_weight[0].name !== undefined &&
        aspect_weight[1] !== undefined
      ) {
        if (
          this.containsObject(obj_to_push, this.selected_aspects_weights) ===
          false
        ) {
          this.selected_aspects_weights.push(obj_to_push);
        }
      }
    },
    update_aspect_weight(aspect_weight) {
      var obj_to_push = {};
      var obj_to_del = {};
      obj_to_push[aspect_weight[0].name] = aspect_weight[2];
      obj_to_del[aspect_weight[0].name] = aspect_weight[1];
      if (
        aspect_weight[0].name !== undefined &&
        aspect_weight[1] !== undefined
      ) {
        if (
          this.containsObject(obj_to_push, this.initial_kpi_aspects_weights) ===
          false
        ) {
          this.initial_kpi_aspects_weights.push(obj_to_push);
          this.remove_aspect(obj_to_del);
        }
      }
    },
    add_further_aspect() {
      this.number_components = this.number_components + 1;
      this.id = this.id + this.number_components;
    },
    remove_further_aspect() {
      if (this.number_components > 0) {
        this.number_components = this.number_components - 1;
      }
    },
    remove_aspect(aspect) {
      var initial_kpi_aspects_weights_tmp = [];
      this.initial_kpi_aspects_weights.forEach((element) => {
        if (
          Object.keys(element)[0] + Object.values(element)[0] !==
          Object.keys(aspect)[0] + Object.values(aspect)[0]
        ) {
          initial_kpi_aspects_weights_tmp.push(element);
        }
      });
      this.initial_kpi_aspects_weights = initial_kpi_aspects_weights_tmp;
      this.$forceUpdate();
    },
    getDatasetOptions() {
      this.$axios
        .get("/get_datasets_only_name/" + localStorage.loggedUser)
        .then((res) => {
          var datasets_tmp = [];
          for (let index = 0; index < res.data.data.length; index++) {
            datasets_tmp.push({
              dataset:
                "NAME: " +
                res.data.data[index]["name"] +
                "   |   " +
                "ID: " +
                res.data.data[index]["dataset_id"],
            });
          }
          this.datasets = datasets_tmp;
        });
    },
    getLabelsOptions() {
      this.$axios.get("/get_all_labels").then((res) => {
        var labels_tmp = [];
        for (let index = 0; index < res.data.length; index++) {
          labels_tmp.push({
            label:
              "NAME: " +
              res.data[index]["name"] +
              "   |   " +
              "ID: " +
              res.data[index]["label_id"],
          });
        }
        this.labels = labels_tmp;
      });
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
    getFormulas(purpose) {
      this.$axios.get("/get_formulas_by_purpose/" + purpose).then((res) => {
        var formulas_tmp = [];
        for (let index = 0; index < res.data.data.length; index++) {
          formulas_tmp.push({
            formula: res.data.data[index]["name"],
          });
        }
        this.formulas = formulas_tmp;
      });
    },
    update_kpi() {
      this.normalize_dataset_labels_obj();
      this.submitted = true;
      this.formData = new FormData();
      this.formData.append("kpi_id", this.kpi.kpi_id);
      this.formData.append("name", this.name);
      this.formData.append("description", this.description);
      this.formData.append("high_level_kpi_component_kpi_weight", "");
      this.formData.append(
        "kpi_aspects_weights",
        JSON.stringify(
          this.initial_kpi_aspects_weights.concat(this.selected_aspects_weights)
        )
      );
      this.formData.append("threshold", this.selected_threshold);
      this.formData.append("formula", this.selected_formula.formula);
      this.formData.append("dataset_id", this.selected_dataset_id);
      this.formData.append(
        "dataset_labels",
        JSON.stringify(this.selected_dataset_labels)
      );
      this.formData.append("kpi_family", this.selected_kpi_family);
      this.formData.append(
        "color_coding",
        this.selected_color_coding.color_coding
      );
      this.$axios
        .post("/update_KPI", this.formData)
        .then(() => {
          this.$toast.add({
            severity: "success",
            summary: "KPI Update Successful",
            detail: "The KPI was updated",
            life: 3000,
          });
          this.close();
        })
        .catch(() => {
          this.$toast.add({
            severity: "error",
            summary: "KPI Update Unsuccessful",
            detail:
              "Check if KPI Name is duplicate and/or all Input Fields contain values",
            life: 5000,
          });
          this.submitted = false;
        });
    },
    normalize_dataset_labels_obj() {
      var selected_dataset_labels_tmp = [];
      for (
        let index = 0;
        index < this.selected_dataset_labels.length;
        index++
      ) {
        var str_tmp = this.selected_dataset_labels[index].label;
        str_tmp = str_tmp.split("ID: ")[1];
        selected_dataset_labels_tmp.push(str_tmp);
      }
      this.selected_dataset_labels = selected_dataset_labels_tmp;
    },
    close() {
      this.$emit("close");
    },
  },
};
</script>