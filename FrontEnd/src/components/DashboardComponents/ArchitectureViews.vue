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
                @update="update_architecture_view($event)"
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
            <add-architecture-view
              :selected_dataset_id="selected_dataset_id"
              :selected_dataset_label="selected_dataset_label"
            ></add-architecture-view> </template
        ></Card>
      </div>
    </div>
  </div>
</template>
<script>
import TableArchitectureViews from "../TableArchitectureViews.vue";
import AddArchitectureView from "../InputForms/AddArchitectureView.vue";

export default {
  props: ["selected_dataset_id", "selected_dataset_label"],
  components: {
    "table-architecture-views": TableArchitectureViews,
    "add-architecture-view": AddArchitectureView,
  },
  data() {
    return {
      componentKey: 0,
      architecture_views_all: "",
      deps_from_dataset: this.getDepartmentsFromDataset(),
      architecture_views: this.getArchitectureViews(),
    };
  },
  methods: {
    update_architecture_view(architecture_view) {
      this.$emit("update", architecture_view);
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
        .get(
          "/get_departments_from_dataset/" +
            this.selected_dataset_id +
            "/" +
            this.selected_dataset_label
        )
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