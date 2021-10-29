<template>
  <div>
    <div class="container-...">
      <div class="row row-cols-auto auto-cols-adj">
        <Card class="component-card">
          <template v-slot:title> Architecture Views </template>
          <template v-slot:subtitle>
            Table with all available Architecture Views
          </template>
          <template v-slot:content>
            <div class="p-fluid" @deleted="getArchitectureViews()">
              <table-architecture-views
                :key="componentKey"
                @close="emitClose"
              ></table-architecture-views>
            </div>
          </template>
          <template v-slot:footer> </template>
        </Card>
        <Card class="component-card">
          <template v-slot:title> Create Architecture View </template>
          <template v-slot:subtitle>
            Create individual Architecture Views based on your needs
          </template>
          <template v-slot:content>
            <form>
              <div class="p-fluid">
                <div class="p-inputgroup">
                  <span class="p-inputgroup-addon">
                    <b-icon-upc />
                  </span>
                  <InputText
                    placeholder="Name"
                    v-model="create_architecture_view_name"
                  />
                </div>
                <br />
                <div class="p-inputgroup">
                  <span class="p-inputgroup-addon">
                    <b-icon-journal-text />
                  </span>
                  <InputText
                    placeholder="Description"
                    v-model="create_architecture_view_description"
                  />
                </div>
                <br />
                <MultiSelect
                  v-model="selected_architecture_view_components"
                  :options="architecture_view_components"
                  optionLabel="architecture_view_component"
                  placeholder="Select a Architecture View Component"
                  :filter="true"
                  filterPlaceholder="Find a Architecture View Component"
                  class="multiselect-custom"
                />
                <br />

                <div class="p-grid p-nogutter p-justify-between">
                  <Button
                    label="Create Architecture View"
                    @click="createArchitectureView()"
                  />
                </div>
              </div>
            </form>
          </template>
          <template v-slot:footer> </template>
        </Card>
      </div>
    </div>
  </div>
</template>
<script>
import TableArchitectureViews from "../TableArchitectureViews.vue";

export default {
  props: ["selected_dataset"],
  components: { "table-architecture-views": TableArchitectureViews },
  data() {
    return {
      componentKey: 0,
      selected_architecture_view_components: "",
      selected_architecture_view: "",
      create_architecture_view_description: "",
      create_architecture_view_name: "",
      architecture_views_all: "",
      deps_from_dataset: this.getDepartmentsFromDataset(),
      architecture_views: this.getArchitectureViews(),
      architecture_view_components: this.getComponents(),
    };
  },
  methods: {
    createArchitectureView() {
      this.submitted = true;
      this.formData = new FormData();
      this.formData.append("name", this.create_architecture_view_name);
      this.formData.append(
        "description",
        this.create_architecture_view_description
      );
      var components_string = "";
      for (
        let index = 0;
        index < this.selected_architecture_view_components.length;
        index++
      ) {
        components_string += this.selected_architecture_view_components[index]
          .architecture_view_component;
        if (index < this.selected_architecture_view_components.length - 1) {
          components_string += ",";
        }
      }
      this.formData.append("components", components_string);
      this.$axios
        .post("/create_architecture_view", this.formData)
        .then(() => {
          this.$toast.add({
            severity: "success",
            summary: "Architecture View Creation Successful",
            detail: "The selected Architecture View was created",
            life: 3000,
          });
          this.getArchitectureViews();
          this.componentKey += 1;
          this.emitClose();
        })
        .catch(() => {
          this.$toast.add({
            severity: "error",
            summary: "Architecture View Creation Unsuccessful",
            detail: "Check if Architecture View Name already exists",
            life: 3000,
          });
        });
    },
    getArchitectureViews() {
      this.$axios.get("/get_architecture_views").then((res) => {
        this.architecture_views_all = res.data.data;
        var data_tmp = [];
        for (let index = 0; index < res.data.data.length; index++) {
          data_tmp.push({
            architecture_view: res.data.data[index].name,
          });
        }
        this.architecture_views = data_tmp;
      });
    },
    getDepartmentsFromDataset() {
      this.$axios
        .get("/get_departments_from_dataset/" + this.selected_dataset)
        .then((res) => {
          var data_tmp = [{ dep: "All" }];
          for (let index = 0; index < res.data.data.length; index++) {
            if (res.data.data[index] !== null) {
              data_tmp.push({ dep: res.data.data[index] });
            }
          }
          this.deps_from_dataset = data_tmp;
        });
    },
    getComponents() {
      this.$axios
        .get("/get_components/" + this.selected_dataset)
        .then((res) => {
          var data_tmp = [];
          for (let index = 0; index < res.data.data.length; index++) {
            data_tmp.push({
              architecture_view_component: res.data.data[index],
            });
          }
          this.architecture_view_components = data_tmp;
        });
    },
    updateDataLabelsArchitecureViewBar(data) {
      this.chartOptionsArchitectureView = {
        ...this.chartOptionsArchitectureView,
        ...{
          xaxis: {
            categories: data,
          },
        },
      };
    },
    emitClose() {
      this.$emit("close");
    },
  },
};
</script>
<style scoped>
.component-card {
  margin-top: 30px;
  position: relative;
  display: flex;
  flex-grow: 1;
  flex-direction: column;
  min-width: 0;
  word-wrap: break-word;
  background-color: #fff;
  background-clip: border-box;
  border-radius: 0.25rem;
  resize: both;
  overflow: auto;
  margin-right: 10px;
  margin-left: 10px;
}

.centered-chart {
  align-items: center;
}

.p-multiselect {
  max-width: 800px;
}

.p-multiselect-label:not(.p-placeholder) {
  padding-top: 0.25rem;
  padding-bottom: 0.25rem;
}
.selected-item-value {
  padding: 0.25rem 0.5rem;
  border-radius: 3px;
  /* display: inline-block; */
  margin-bottom: 0.5rem;
  background-color: var(--primary-color);
  color: var(--primary-color-text);
}

@media screen and (max-width: 900px) {
  .p-multiselect {
    width: 100%;
  }
}
</style>