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
              placeholder="Aspect's Name"
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
      <div v-for="number in number_components" :key="number">
        <add-aspect-helper
          :selected_dataset_id="selected_dataset_id"
          :selected_dataset_label="selected_dataset_label"
          :id="id"
          @selected-raw-component-operation-type="
            add_to_raw_components_operation_types($event)
          "
        ></add-aspect-helper>
      </div>
      <div class="p-grid p-fluid">
        <div class="p-col-6 p-md-6">
          <Button
            label="Add Further Component"
            icon="pi pi-plus-circle"
            iconPos="center"
            class="p-button-success"
            @click="add_further_component"
          />
        </div>
        <div class="p-col-6 p-md-6">
          <Button
            label="Remove Component"
            icon="pi pi-minus-circle"
            iconPos="center"
            class="p-button-danger"
            @click="remove_further_component"
          />
        </div>
      </div>
      <div class="p-grid p-align-center">
        <div class="p-col-6 p-md-6">
          <h3>Assign Scale Size:</h3>
        </div>
        <div class="p-col-6 p-md-6">
          <Knob v-model="selected_skala_size" :min="0" :max="10" />
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
              :showClear="true"
            />
          </div>
        </div>
      </div>
      <div class="p-grid p-fluid">
        <div class="p-col-12 p-md-12">
          <Button
            label="Create Aspect"
            icon="pi pi-plus-circle"
            iconPos="center"
            @click="create_aspect"
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
import AddAspectHelper from "./HelperComponents/AddAspectHelper.vue";
export default {
  components: {
    "add-aspect-helper": AddAspectHelper,
  },
  data() {
    return {
      selected_dataset_id: localStorage.selected_dataset_id,
      selected_dataset_label: localStorage.selected_dataset_label,
      name: "",
      description: "",
      datasets: this.getDatasetOptions(),
      labels: this.getLabelsOptions(),
      formulas: this.getFormulas("aspect"),
      selected_dataset_labels: "",
      selected_raw_components_operation_types: [],
      selected_skala_size: 10,
      selected_threshold: 0,
      selected_weight: 0,
      id: "gauge_",
      selected_formula: "",
      selected_kpi_family: "",
      number_components: 1,
      formData: "",
      submitted: false,
    };
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
    add_to_raw_components_operation_types(raw_component_operation_types) {
      var obj_to_push = {};
      obj_to_push[raw_component_operation_types[0]] =
        raw_component_operation_types[1];
      if (
        raw_component_operation_types[1] !== undefined &&
        raw_component_operation_types[0] !== undefined
      ) {
        if (
          this.containsObject(
            obj_to_push,
            this.selected_raw_components_operation_types
          ) === false
        ) {
          this.selected_raw_components_operation_types.push(obj_to_push);
        }
      }
    },
    add_further_component() {
      this.number_components = this.number_components + 1;
      this.id = this.id + this.number_components;
    },
    remove_further_component() {
      if (this.number_components > 0) {
        this.number_components = this.number_components - 1;
      }
      this.selected_raw_components_operation_types.pop();
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
    create_aspect() {
      this.normalize_dataset_labels_obj();
      this.submitted = true;
      this.formData = new FormData();
      this.formData.append("name", this.name);
      this.formData.append("description", this.description);
      this.formData.append(
        "raw_components_from_dataset",
        JSON.stringify(this.selected_raw_components_operation_types)
      );
      this.formData.append("skala_size", this.selected_skala_size);
      this.formData.append("weight", this.selected_weight);
      this.formData.append("threshold", this.selected_threshold);
      this.formData.append("operation_type", this.selected_operation_type);
      this.formData.append("formula", this.selected_formula.formula);
      this.formData.append("dataset_id", this.selected_dataset_id);
      this.formData.append(
        "dataset_labels",
        JSON.stringify(this.selected_dataset_labels)
      );
      this.formData.append("kpi_family", this.selected_kpi_family);

      this.$axios
        .post("/create_aspect", this.formData)
        .then(() => {
          this.$toast.add({
            severity: "success",
            summary: "Aspect Creation Successful",
            detail: "The Aspect was created",
            life: 3000,
          });
          this.close();
        })
        .catch(() => {
          this.$toast.add({
            severity: "error",
            summary: "Aspect Creation Unsuccessful",
            detail:
              "Check if Aspect Name is duplicate and/or all Input Fields contain values",
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

<style>
.grouped_inputs {
  text-align: center;
  margin: 5px;
}

label {
  margin-top: 5px;
  display: block;
}

.p-checkbox-icon {
  margin: 5px;
}

.p-field-checkbox {
  margin-top: 6px;
}

.p-grid {
  margin-top: 15px;
}

.visuallyhidden {
  border: 0;
  clip: rect(0 0 0 0);
  height: 1px;
  margin: -1px;
  overflow: hidden;
  padding: 0;
  position: absolute;
  width: 1px;
}

body {
  font-family: "Open Sans", sans-serif;
  color: #1a1a1a;
  background-color: #f0f0f0;
}

h2 {
  color: #111;
  font-family: "Open Sans Condensed", sans-serif;
  font-size: 28x;
  font-weight: 700;
  line-height: 28px;
  margin: 0 0 5px;
  padding: 0 5px;
  text-align: center;
  text-transform: uppercase;
}

h1 {
  color: #111;
  font-family: "Open Sans Condensed", sans-serif;
  font-size: 30x;
  font-weight: 700;
  line-height: 35px;
  margin: 0 0 5px;
  padding: 0 5px;
  text-align: center;
  text-transform: uppercase;
}

.button {
  color: #ffffff;
  background-color: #24cf5f;
  margin-top: 10px;

  padding: 12px 25px;
  font-size: 12px;
  letter-spacing: 1px;
  text-transform: uppercase;
  border: 0;
  border-radius: 2px;
  outline: 0;
  box-shadow: 3px 3px 20px rgba(0, 0, 0, 0.2);
  transition: all 0.2s;
}
.button:hover,
.button:active,
.button:focus {
  -ms-transform: scale(1.1);
  transform: scale(1.1);
}

input {
  width: calc(100% - 10px);
  min-height: 30px;
  padding-left: 5px;
  padding-right: 5px;
  letter-spacing: 0.5px;
  border: 0;
  border-bottom: 2px solid #f0f0f0;
}
input:valid {
  border-color: #24cf5f;
}
input:focus {
  outline: none;
  border-color: #fbcf34;
}

.form-list {
  padding-left: 0;
  list-style: none;
}
.form-list__row {
  margin-bottom: 25px;
}
.form-list__row label {
  position: relative;
  display: block;
  text-transform: uppercase;
  font-weight: 600;
  font-size: 11px;
  letter-spacing: 0.5px;
  color: #939393;
}
.form-list__row--inline {
  display: -ms-flexbox;
  display: flex;
  -ms-flex-pack: justify;
  justify-content: space-between;
}
.form-list__row--inline > :first-child {
  -ms-flex: 2;
  flex: 2;
  padding-right: 20px;
}
.form-list__row--inline > :nth-child(2n) {
  -ms-flex: 1;
  flex: 1;
}
.form-list__input-inline {
  display: -ms-flexbox;
  display: flex;
  -ms-flex-pack: justify;
  justify-content: space-between;
}
.form-list__input-inline > * {
  width: calc(50% - 10px - 10px);
}
.form-list__row--agree {
  margin-top: 10px;
  margin-bottom: 10px;
  font-size: 12px;
}
.form-list__row--agree label {
  font-weight: 400;
  text-transform: none;
  color: #676767;
}
.form-list__row--agree input {
  width: auto;
  margin-right: 5px;
}

#input--cc {
  position: relative;
  padding-top: 6px;
}
#input--cc input {
  padding-left: 46px;
  width: calc(100% - 46px);
}
#input--cc:before {
  content: "";
  position: absolute;
  left: 0;
  top: 50%;
  width: 36px;
  height: 45px;
  background-image: url("data:image/svg+xml;utf8,%3Csvg%20class%3D%22nc-icon%20glyph%22%20xmlns%3D%22http%3A//www.w3.org/2000/svg%22%20xmlns%3Axlink%3D%22http%3A//www.w3.org/1999/xlink%22%20x%3D%220px%22%20y%3D%220px%22%20width%3D%2248px%22%20height%3D%2248px%22%20viewBox%3D%220%200%2048%2048%22%3E%3Cg%3E%20%3Cpath%20data-color%3D%22color-2%22%20fill%3D%22%238c8c8c%22%20d%3D%22M47%2C16V9c0-1.105-0.895-2-2-2H3C1.895%2C7%2C1%2C7.895%2C1%2C9v7H47z%22%3E%3C/path%3E%20%3Cpath%20fill%3D%22%238c8c8c%22%20d%3D%22M1%2C22v17c0%2C1.105%2C0.895%2C2%2C2%2C2h42c1.105%2C0%2C2-0.895%2C2-2V22H1z%20M18%2C33H8c-0.552%2C0-1-0.448-1-1s0.448-1%2C1-1h10%20c0.552%2C0%2C1%2C0.448%2C1%2C1S18.552%2C33%2C18%2C33z%20M40%2C33h-5c-0.552%2C0-1-0.448-1-1s0.448-1%2C1-1h5c0.552%2C0%2C1%2C0.448%2C1%2C1S40.552%2C33%2C40%2C33z%22%3E%3C/path%3E%20%3C/g%3E%3C/svg%3E");
  background-position: center;
  background-repeat: no-repeat;
  background-size: 36px;
  -ms-transform: translateY(-50%);
  transform: translateY(-50%);
}

footer p {
  margin: 10px 0;
}

footer i {
  color: red;
}

footer a {
  color: #3c97bf;
  text-decoration: none;
}
</style>