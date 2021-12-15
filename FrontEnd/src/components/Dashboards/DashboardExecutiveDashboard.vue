<template>
  <div>
    <TabView class="tabview-custom" ref="tabview4" :key="componentKey">
      <TabPanel :disabled="disabled">
        <template #header>
          <b-icon-gear-wide-connected style="font-size: 18px; margin: 3px" />
          <span><h4>ExecutiveDashboardManager</h4></span>
        </template>
        <span v-if="admin">
          <Card class="component-card">
            <template v-slot:title> Executive Dashboards </template>
            <template v-slot:subtitle>
              Manager here your Executive Dashboards
            </template>
            <template v-slot:content>
              <table-executive-dashboard
                @delete="increaseComponentKey"
              ></table-executive-dashboard>
            </template>
          </Card>
          <Card class="component-card">
            <template v-slot:content>
              <Carousel
                :value="operationsItems"
                :numVisible="1"
                :numScroll="1"
                :responsiveOptions="responsiveOptions"
              >
                <template #header>
                  <h1 style="text-align: center">Available Operations</h1>
                </template>
                <template #item="slotProps">
                  <div class="operation-item">
                    <div class="operation-item-content">
                      <div class="p-mb-3">
                        <span style="text-align: center">
                          <span v-html="slotProps.data.operation_img"></span
                        ></span>
                      </div>
                      <h4>{{ slotProps.data.operation_desc }}</h4>
                      <div
                        v-html="slotProps.data.operation_button"
                        @click.capture="toggleShowAddExecutiveDashboard"
                        v-if="
                          slotProps.data.operation === 'add_executive_dashboard'
                        "
                      ></div>
                    </div>
                  </div>
                </template>
              </Carousel>
            </template>
          </Card>
        </span>
      </TabPanel>
      <TabPanel
        v-for="executive_dashboard in suitable_dashboards"
        :key="executive_dashboard.executive_dashboard_id"
      >
        <template #header>
          <b-icon-pie-chart style="font-size: 18px; margin: 3px" />
          <span
            ><h4>{{ executive_dashboard.name }}</h4></span
          >
        </template>
        <div class="container-...">
          <div class="row row-cols-auto auto-cols-adj">
            <template
              v-for="plot_id in plots_from_dashboard[
                executive_dashboard.executive_dashboard_id
              ]"
              :key="plot_id"
            >
              <Card class="component-card">
                <template v-slot:title> {{ title_chart }} </template>
                <template v-slot:subtitle>
                  {{ subtitle_chart }}
                </template>
                <template v-slot:content>
                  <chart-executive
                    :plot_id="plot_id"
                    @title_change="change_titles_chart($event)"
                  >
                  </chart-executive>
                </template>
              </Card>
            </template>
          </div>
        </div>
      </TabPanel>
    </TabView>
  </div>
</template>
<script>
import ChartExecutive from "../Plots/ChartExecutive.vue";
import TableExecutiveDashboard from "../Tables/TableExecutiveDashboard.vue";

export default {
  components: {
    "chart-executive": ChartExecutive,
    "table-executive-dashboard": TableExecutiveDashboard,
  },
  data() {
    return {
      title_chart: "Rendering Data....",
      subtitle_chart: "Please wait...",
      componentKey: 0,
      admin: this.check_user_admin(),
      suitable_dashboards: this.get_suitable_dashboards(),
      plots_from_dashboard: [],
      disabled: true,
      user: "",
      showAddExecutiveDashboard: false,
      operationsItems: [
        {
          operation: "add_executive_dashboard",
          operation_img:
            "<i class='pi pi-plus-circle' style='font-size: 230px'></i>",
          operation_desc: "Click here to create new Executive Dashboard",
          operation_button:
            '<div class="d-grid"><button class="btn btn-primary" ' +
            'type="button" @click="toggleShowAddExecutiveDashboard"> <span class="btn-label"> <i class="pi pi-plus-circle" style="font-size: 23px"></i>' +
            " </button>   </div>",
        },
      ],
    };
  },
  methods: {
    change_titles_chart(titles) {
      this.title_chart = titles.title_chart;
      this.subtitle_chart = titles.subtitle_chart;
    },
    toggleShowAddExecutiveDashboard() {
      this.increaseComponentKey();
      this.$emit("add-executive-dashboard");
    },
    prevPage() {
      this.$emit("prev-page", { pageIndex: 1 });
    },
    increaseComponentKey() {
      this.componentKey += 1;
    },
    check_user_admin() {
      this.$axios.get("/user/" + localStorage.loggedUser).then((res) => {
        this.user = res.data;
        if (res.data.admin == 1) {
          this.admin = true;
          this.disabled = false;
        } else {
          this.admin = false;
          this.disabled = true;
        }
      });
    },
    get_suitable_dashboards() {
      this.$axios.get("/get_executive_dashboards").then((res) => {
        var dashboards_tmp = [];
        for (let index = 0; index < res.data.data.length; index++) {
          if (
            res.data.data[index].access_user_list.includes(this.user.user_id) ||
            res.data.data[index].access_business_unit_list.includes(
              this.user.business_unit
            )
          ) {
            dashboards_tmp.push(res.data.data[index]);
            this.increaseComponentKey();
          }
        }
        this.suitable_dashboards = dashboards_tmp;
        for (let index = 0; index < this.suitable_dashboards.length; index++) {
          var executive_dashboard_id =
            this.suitable_dashboards[index].executive_dashboard_id;
          this.increaseComponentKey();
          this.$axios
            .get(
              "/get_plots_from_executive_dashboards/" + executive_dashboard_id
            )
            .then((res) => {
              this.plots_from_dashboard[
                this.suitable_dashboards[index].executive_dashboard_id
              ] = [];
              for (let index_2 = 0; index_2 < res.data.data.length; index_2++) {
                this.plots_from_dashboard[
                  this.suitable_dashboards[index].executive_dashboard_id
                ].push({
                  plot_id: res.data.data[index_2].plot_id,
                });
              }
              this.increaseComponentKey();
            });
          this.increaseComponentKey();
        }
      });
      this.increaseComponentKey();
    },
  },
};
</script>
<style scoped>
.component-card {
  margin-top: 30px;
  position: relative;
  /* display: flex; */
  display: flex;
  table-layout: fixed;
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
  /* min-width: 100%; */
}

.component-card-table {
  margin-top: 30px;
  position: relative;
  display: flex;
  table-layout: fixed;
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
  min-width: 100%;
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