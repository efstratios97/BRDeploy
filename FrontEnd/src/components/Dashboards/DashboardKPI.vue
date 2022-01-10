<template>
  <div>
    <TabView class="tabview-custom" ref="tabview4" :key="componentKey">
      <TabPanel :disabled="disabled">
        <template #header>
          <b-icon-gear-wide-connected style="font-size: 18px; margin: 3px" />
          <span><h4>KPIDashboardManager</h4></span>
        </template>
        <span v-if="admin">
          <div class="p-grid">
            <div class="p-col">
              <Card class="component-card">
                <template v-slot:title> KPIs </template>
                <template v-slot:subtitle> Manager here your KPIs </template>
                <template v-slot:content>
                  <table-kpi
                    @delete="increaseComponentKey"
                    :selected_dataset_id="selected_dataset_id"
                    :selected_dataset_label="selected_dataset_label"
                  ></table-kpi>
                </template>
              </Card>
            </div>
            <div class="p-col">
              <Card class="component-card">
                <template v-slot:title> Aspects </template>
                <template v-slot:subtitle> Manager here your Aspects </template>
                <template v-slot:content>
                  <table-aspect
                    @delete="increaseComponentKey"
                    :selected_dataset_id="selected_dataset_id"
                    :selected_dataset_label="selected_dataset_label"
                  ></table-aspect>
                </template>
              </Card>
            </div>
          </div>
          <Card class="component-card">
            <template v-slot:content>
              <Carousel
                :value="operationsItems"
                :numVisible="2"
                :numScroll="2"
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
                        @click.capture="toggleShowAddKPI()"
                        v-if="slotProps.data.operation === 'add_kpi'"
                      ></div>
                      <div
                        v-html="slotProps.data.operation_button"
                        @click.capture="toggleShowAddAspect()"
                        v-if="slotProps.data.operation === 'add_aspect'"
                      ></div>
                    </div>
                  </div>
                </template>
              </Carousel>
            </template>
          </Card>
        </span>
      </TabPanel>
      <TabPanel>
        <template #header>
          <b-icon-bar-chart-line style="font-size: 18px; margin: 3px" />
          <span><h4>Aspects Dashboard</h4></span>
        </template>
        <render-aspects
          :selected_dataset_id="selected_dataset_id"
          :selected_dataset_label="selected_dataset_label"
          :apps="apps"
          :departments="departments"
          :domains="domains"
          selected_apps_aspects=""
          selected_aspects=""
        ></render-aspects>
      </TabPanel>
      <TabPanel>
        <template #header>
          <b-icon-speedometer style="font-size: 18px; margin: 3px" />
          <span><h4>KPI Dashboard</h4></span>
        </template>
        <render-kpis
          :selected_dataset_id="selected_dataset_id"
          :selected_dataset_label="selected_dataset_label"
          :apps="apps"
          :domains="domains"
          :departments="departments"
        ></render-kpis>
      </TabPanel>
      <TabPanel>
        <template #header>
          <b-icon-columns style="font-size: 18px; margin: 3px" />
          <span><h4>KPI Landscape</h4></span>
        </template>
        <render-app-landscape
          :selected_dataset_id="selected_dataset_id"
          :selected_dataset_label="selected_dataset_label"
          :apps="apps"
          :domains="domains"
          :departments="departments"
        ></render-app-landscape>
      </TabPanel>
      <TabPanel>
        <template #header>
          <b-icon-columns style="font-size: 18px; margin: 3px" />
          <span><h4>KPI Application Lifecyle</h4></span>
        </template>
        <render-life-cycle-kpi
          :selected_dataset_id="selected_dataset_id"
          :selected_dataset_label="selected_dataset_label"
          :domains="domains"
          :departments="departments"
        ></render-life-cycle-kpi>
      </TabPanel>
      <TabPanel>
        <template #header>
          <b-icon-speedometer style="font-size: 18px; margin: 3px" />
          <span><h4>DEMO</h4></span>
        </template>
        <demo-sankey> </demo-sankey>
        <demo-sankey-vertical></demo-sankey-vertical>
        <demo-drag-node></demo-drag-node>
      </TabPanel>
    </TabView>
    <div class="p-grid p-nogutter p-justify-between">
      <Button label="Back" @click="prevPage()" icon="pi pi-angle-left" />
    </div>
  </div>
</template>
<script>
import RenderKPIs from "../HelperComponents/RenderKPIs.vue";
import RenderAspects from "../HelperComponents/RenderAspects.vue";
import RenderAppLandscape from "../HelperComponents/RenderAppLandscape.vue";
import RenderLifeCycleKPI from "../HelperComponents/RenderLifeCycleKPI.vue";
import TableKPI from "../Tables/TableKPI.vue";
import TableAspect from "../Tables/TableAspect.vue";
//Demo
import DemoSankey from "../Plots/DemoSankey.vue";
import DemoSankeyVertical from "../Plots/DemoSankeyVertical.vue";
import DemoDragNode from "../Plots/DemoDragNode.vue";

export default {
  components: {
    "render-kpis": RenderKPIs,
    "render-aspects": RenderAspects,
    "render-app-landscape": RenderAppLandscape,
    "render-life-cycle-kpi": RenderLifeCycleKPI,
    "table-kpi": TableKPI,
    "table-aspect": TableAspect,
    "demo-sankey": DemoSankey,
    "demo-sankey-vertical": DemoSankeyVertical,
    "demo-drag-node": DemoDragNode,
  },
  props: ["selected_dataset_id", "selected_dataset_label"],
  data() {
    return {
      componentKey: 0,
      disabled: true,
      admin: this.check_user_admin(),
      apps: this.getApps(),
      departments: this.getDatasetDepartmentOptions(),
      domains: this.getDomainsOptions(),
      operationsItems: [
        {
          operation: "add_kpi",
          operation_img:
            "<i class='pi pi-plus-circle' style='font-size: 230px'></i>",
          operation_desc: "Build your KPI",
          operation_button:
            '<div class="d-grid"><button class="btn btn-primary" ' +
            'type="button" @click="toggleShowAddKPI"> <span class="btn-label"> <i class="pi pi-plus-circle" style="font-size: 23px"></i>' +
            " </button>   </div>",
        },
        {
          operation: "add_aspect",
          operation_img:
            "<i class='pi pi-plus-circle' style='font-size: 230px'></i>",
          operation_desc: "Build your Aspect",
          operation_button:
            '<div class="d-grid"><button class="btn btn-primary" ' +
            'type="button" @click="toggleShowAddAspect"> <span class="btn-label"> <i class="pi pi-plus-circle" style="font-size: 23px"></i>' +
            " </button>   </div>",
        },
      ],
    };
  },
  methods: {
    getApps() {
      this.$axios
        .get("/get_applications/" + this.selected_dataset_id)
        .then((res) => {
          var apps_tmp = [];
          for (let index = 0; index < res.data.length; index++) {
            apps_tmp.push({ app: res.data[index] });
          }
          this.apps = apps_tmp;
        });
    },
    getDatasetDepartmentOptions() {
      this.$axios
        .get(
          "/get_departments_from_dataset/" +
            this.selected_dataset_id +
            "/" +
            this.selected_dataset_label
        )
        .then((res) => {
          var departments_tmp = [];
          for (let index = 0; index < res.data.data.length; index++) {
            departments_tmp.push({ dep: res.data.data[index] });
          }
          this.departments = departments_tmp;
        });
    },
    getDomainsOptions() {
      this.$axios
        .get(
          "/get_domains_from_dataset/" +
            this.selected_dataset_id +
            "/" +
            this.selected_dataset_label
        )
        .then((res) => {
          var domains_tmp = [];
          for (let index = 0; index < res.data.data.length; index++) {
            domains_tmp.push({ domain: res.data.data[index] });
          }
          this.domains = domains_tmp;
        });
    },
    toggleShowAddAspect() {
      this.increaseComponentKey();
      this.$emit("add-aspect");
    },
    toggleShowAddKPI() {
      this.increaseComponentKey();
      this.$emit("add-kpi");
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
    prevPage() {
      this.$emit("prev-page", { pageIndex: 1 });
    },
    increaseComponentKey() {
      this.componentKey += 1;
    },
  },
};
</script>
<style scoped>
.component-card {
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
  /* min-width: 100%; */
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