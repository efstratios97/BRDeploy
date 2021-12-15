<template>
  <div class="container-...">
    <div class="row row-cols-auto auto-cols-adj">
      <Card class="component-card">
        <template v-slot:title> Department Selection </template>
        <template v-slot:subtitle> Select Department to examine </template>
        <template v-slot:content>
          <div class="p-fluid">
            <Dropdown
              v-model="selected_dep_from_dataset"
              :options="deps_from_dataset"
              optionLabel="dep"
              placeholder="Select a Department"
              :filter="true"
              filterPlaceholder="Find a Department"
              :showClear="true"
            />
          </div>
        </template>
        <template v-slot:footer> </template>
      </Card>
      <Card class="component-card">
        <template v-slot:title> Architecture Views Selection </template>
        <template v-slot:subtitle>
          Select Architecture Views to apply
        </template>
        <template v-slot:content>
          <div class="p-fluid">
            <Dropdown
              v-model="selected_architecture_view"
              :options="architecture_views"
              optionLabel="architecture_view"
              placeholder="Select a Architecture View"
              :filter="true"
              filterPlaceholder="Find a Architecture View"
              :showClear="true"
            />
          </div>
        </template>
        <template v-slot:footer> </template>
      </Card>
    </div>
    <br />
    <div class="p-grid">
      <div class="p-col-4 p-offset-4">
        <div class="p-fluid">
          <Button
            label="Start Applicability Analysis"
            @click="applyArchitectureViewAnalysis()"
          />
        </div>
      </div>
    </div>
    <div class="container-..." v-if="showApplicabilityAnalysis">
      <div class="row row-cols-auto auto-cols-adj">
        <Card class="component-card">
          <template v-slot:title> Applicability Analysis </template>
          <template v-slot:subtitle>
            This Analysis shows the current maintainance level of EAM Data
            regarding the selected Architecture View for the selected Department
          </template>
          <template v-slot:content>
            <div class="p-fluid">
              <div id="chartBarArchitectureView">
                <apexchart
                  type="bar"
                  height="400"
                  width="100%"
                  :options="chartOptionsArchitectureView"
                  :series="architecture_view_bar_data"
                ></apexchart>
              </div>
            </div>
          </template>
          <template v-slot:footer> </template>
        </Card>
      </div>
    </div>
  </div>
</template>
<script>
export default {
  props: ["selected_dataset_id", "selected_dataset_label"],
  data() {
    return {
      deps_from_dataset: this.getDepartmentsFromDataset(),
      architecture_views: this.getArchitectureViews(),
      selected_dep_from_dataset: "",
      selected_architecture_view: "",
      architecture_views_all: "",
      showApplicabilityAnalysis: false,
      architecture_view_bar_data: [
        {
          name: "Initiating",
          data: [1],
        },
      ],
      chartOptionsArchitectureView: {
        chart: {
          type: "bar",
        },
        plotOptions: {
          bar: {
            borderRadius: 10,
            dataLabels: {
              position: "top", // top, center, bottom
            },
          },
        },
        dataLabels: {
          enabled: true,
          formatter: function (val) {
            return Math.round(val) + "%";
          },
          offsetY: -20,
          style: {
            fontSize: "12px",
            colors: ["#304758"],
          },
        },
        stroke: {
          colors: ["transparent"],
          width: 10,
        },
        xaxis: {
          labels: {
            show: false,
          },
          categories: ["Initiating..."],
          position: "bottom",
          axisBorder: {
            show: true,
          },
          axisTicks: {
            show: true,
          },
          crosshairs: {
            fill: {
              type: "gradient",
              gradient: {
                colorFrom: "#D8E3F0",
                colorTo: "#BED1E6",
                stops: [0, 100],
                opacityFrom: 0.4,
                opacityTo: 0.5,
              },
            },
          },
          tooltip: {
            enabled: true,
          },
        },
        yaxis: {
          axisBorder: {
            show: false,
          },
          axisTicks: {
            show: false,
          },
          labels: {
            show: false,
            formatter: function (val) {
              return val + "%";
            },
          },
        },
        title: {
          text: "Applicability Analysis",
          floating: true,
          align: "center",
          style: {
            color: "#444",
            position: "top",
          },
        },
      },
    };
  },
  methods: {
    applyArchitectureViewAnalysis() {
      this.showApplicabilityAnalysis = true;
      var selected_architecture_view = "";
      for (let index = 0; index < this.architecture_views_all.length; index++) {
        if (
          this.architecture_views_all[index].name ===
          this.selected_architecture_view.architecture_view
        ) {
          selected_architecture_view =
            this.architecture_views_all[index].architecture_view_id;
        }
      }
      this.$axios
        .post(
          "/analyze_applicability/" +
            this.selected_dataset_id +
            "/" +
            selected_architecture_view +
            "/" +
            this.selected_dep_from_dataset.dep
        )
        .then((res) => {
          this.architecture_view_bar_data = res.data[0];
          this.updateDataLabelsArchitecureViewBar(res.data[1]);
          this.$toast.add({
            severity: "success",
            summary: "Architecture View Applicability Analysis Successful",
            detail:
              "The Architecture View Applicability Analysis was successful",
            life: 3000,
          });
        })
        .catch(() => {
          this.$toast.add({
            severity: "error",
            summary: "Architecture View Applicability Analysis Unsuccessful",
            detail: "Select Parameters OR  click Back and re-select a dataset!",
            life: 3000,
          });
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
          var data_tmp = [];
          for (let index = 0; index < res.data.data.length; index++) {
            if (res.data.data[index] !== "") {
              data_tmp.push({ dep: res.data.data[index] });
            }
          }
          this.deps_from_dataset = data_tmp;
        });
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