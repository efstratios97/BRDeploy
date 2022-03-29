<template>
  <div>
    <TabView class="tabview-custom" ref="tabview4" :key="componentKey">
      <TabPanel>
        <template #header>
          <b-icon-gear-wide-connected style="font-size: 18px; margin: 3px" />
          <span><h4>KPIDashboardManager</h4></span>
        </template>
        <div class="p-grid">
          <div class="p-col overflow-auto">
            <Card class="component-card">
              <template v-slot:title> KPIs </template>
              <template v-slot:subtitle> Manager here your KPIs </template>
              <template v-slot:content>
                <table-kpi
                  @update="updateKPI($event)"
                  @delete="increaseComponentKey"
                  :selected_dataset_id="selected_dataset_id"
                  :selected_dataset_label="selected_dataset_label"
                ></table-kpi>
              </template>
            </Card>
          </div>
          <div class="p-col overflow-auto">
            <Card class="component-card">
              <template v-slot:title> Aspects </template>
              <template v-slot:subtitle> Manager here your Aspects </template>
              <template v-slot:content>
                <table-aspect
                  @update="updateAspect($event)"
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
      </TabPanel>
      <TabPanel>
        <template #header>
          <b-icon-bar-chart-line style="font-size: 18px; margin: 3px" />
          <span><h4>Aspects Dashboard</h4></span>
        </template>
        <kpi-aspects
          :selected_dataset_id="selected_dataset_id"
          :selected_dataset_label="selected_dataset_label"
        ></kpi-aspects>
      </TabPanel>
      <TabPanel>
        <template #header>
          <b-icon-speedometer style="font-size: 18px; margin: 3px" />
          <span><h4>KPI Dashboard</h4></span>
        </template>
        <kpis
          :selected_dataset_id="selected_dataset_id"
          :selected_dataset_label="selected_dataset_label"
        ></kpis>
      </TabPanel>
      <TabPanel>
        <template #header>
          <b-icon-columns style="font-size: 18px; margin: 3px" />
          <span><h4>KPI Landscape</h4></span>
        </template>
        <kpi-app-landscape
          :selected_dataset_id="selected_dataset_id"
          :selected_dataset_label="selected_dataset_label"
        ></kpi-app-landscape>
      </TabPanel>
      <TabPanel>
        <template #header>
          <b-icon-columns style="font-size: 18px; margin: 3px" />
          <span><h4>KPI Application Lifecyle</h4></span>
        </template>
        <kpi-life-cycle
          :selected_dataset_id="selected_dataset_id"
          :selected_dataset_label="selected_dataset_label"
        ></kpi-life-cycle>
      </TabPanel>
    </TabView>
    <customazible-button
      @button-click="prevPage()"
      altLabel="Back"
      altStyle="margin-top: 10px; margin-bottom: 20px"
    ></customazible-button>
  </div>
</template>
<script>
import KPIAppLandscape from "../DashboardComponents/KPIAppLandscape.vue";
import KPILifeCycle from "../DashboardComponents/KPILifeCycle.vue";
import KPIAspects from "../DashboardComponents/KPIAspects.vue";
import KPI from "../DashboardComponents/KPI.vue";
import TableKPI from "../Tables/TableKPI.vue";
import TableAspect from "../Tables/TableAspect.vue";
import CustomazibleButton from "../HelperComponents/CustomazibleButton.vue";

export default {
  components: {
    kpis: KPI,
    "kpi-aspects": KPIAspects,
    "kpi-app-landscape": KPIAppLandscape,
    "kpi-life-cycle": KPILifeCycle,
    "table-kpi": TableKPI,
    "table-aspect": TableAspect,
    "customazible-button": CustomazibleButton,
  },
  data() {
    return {
      selected_dataset_id: localStorage.selected_dataset_id,
      selected_dataset_label: localStorage.selected_dataset_label,
      componentKey: 0,
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
    updateAspect(aspect) {
      this.$emit("update-aspect", aspect);
    },
    updateKPI(kpi) {
      this.$emit("update-kpi", kpi);
    },
    toggleShowAddAspect() {
      this.increaseComponentKey();
      this.$emit("add-aspect");
    },
    toggleShowAddKPI() {
      this.increaseComponentKey();
      this.$emit("add-kpi");
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