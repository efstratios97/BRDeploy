<template>
  <div>
    <TabView class="tabview-custom" ref="tabview4" :key="componentKey">
      <TabPanel>
        <template #header>
          <b-icon-gear-wide-connected style="font-size: 18px; margin: 3px" />
          <span><h4>ExecutiveDashboardManager</h4></span>
        </template>
        <Card class="component-card">
          <template v-slot:title> Executive Dashboards </template>
          <template v-slot:subtitle>
            Manager here your Executive Dashboards
          </template>
          <template v-slot:content>
            <table-executive-dashboard
              @delete="increaseComponentKey"
              @update="update_dashboard($event)"
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
      </TabPanel>
    </TabView>
  </div>
</template>
<script>
import TableExecutiveDashboard from "../Tables/TableExecutiveDashboard.vue";

export default {
  components: {
    "table-executive-dashboard": TableExecutiveDashboard,
  },
  data() {
    return {
      componentKey: 0,
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
    toggleShowAddExecutiveDashboard() {
      this.increaseComponentKey();
      this.$emit("add-executive-dashboard");
    },
    update_dashboard(dashboard) {
      this.increaseComponentKey();
      this.$emit("update", dashboard);
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