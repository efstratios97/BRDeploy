<template>
  <div v-if="admin === 'true'">
    <div class="banner-head banner-image p-shadow-14"></div>
    <div class="page-background">
      <div class="container-xxl main-page p-shadow-14">
        <h1 style="text-align: left; font-size: 38px">Data Cleanser</h1>
        <br />
        <br />
        <TabView class="tabview-custom" ref="tabview4">
          <TabPanel>
            <template #header>
              <b-icon-funnel-fill style="font-size: 18px; margin: 3px" />
              <span><h4>Cleansers</h4></span>
            </template>
            <Card class="component-card">
              <template v-slot:title> Data Cleansers </template>
              <template v-slot:subtitle>
                Manager here your Data Cleansers
              </template>
              <template v-slot:content>
                <cleanser-table
                  :key="componentKey"
                  @update="update_cleanser($event)"
                ></cleanser-table>
              </template>
            </Card>
          </TabPanel>
          <TabPanel>
            <template #header>
              <i class="pi pi-cog" style="font-size: 18px; margin: 3px"></i>
              <span><h4>DataCleanser Operations</h4></span>
            </template>
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
                          @click.capture="toggleShowAddCleanser"
                          v-if="slotProps.data.operation === 'add_cleanser'"
                        ></div>
                        <div
                          v-html="slotProps.data.operation_button"
                          @click.capture="toggleShowApplyCleanser"
                          v-if="slotProps.data.operation === 'apply_cleanser'"
                        ></div>
                        <div
                          v-html="slotProps.data.operation_button"
                          @click.capture="toggleShowUpdateCleanser"
                          v-if="slotProps.data.operation === 'update_cleanser'"
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
    </div>
    <transition class="modal-animation">
      <modal-view v-if="showAddCleanser" @close="toggleShowAddCleanser">
        <template v-slot:header>Add Cleanser</template>
        <template v-slot:body>
          <add-cleanser @close="refreshData"> </add-cleanser> </template
      ></modal-view>
    </transition>
    <transition class="modal-animation">
      <modal-view v-if="showUpdateCleanser" @close="toggleShowUpdateCleanser">
        <template v-slot:header>Update Cleanser</template>
        <template v-slot:body>
          <ProgressBar mode="indeterminate" />
          <h1>Please wait while updating</h1>
          <h1>This can take some minutes</h1>
        </template>
      </modal-view>
    </transition>
    <transition class="modal-animation">
      <modal-view v-if="showApplyCleanser" @close="toggleShowApplyCleanser">
        <template v-slot:header>Apply Cleanser</template>
        <template v-slot:body>
          <add-cleaned-data-set @close="refreshData"></add-cleaned-data-set>
        </template>
      </modal-view>
    </transition>
    <transition class="modal-animation">
      <modal-view
        v-if="showUpdateCleanserObject"
        @close="toggleShowUpdateCleanserObject"
      >
        <template v-slot:header>Update Cleanser</template>
        <template v-slot:body>
          <update-cleanser
            @close="refreshData"
            :cleanser="selected_cleanser"
          ></update-cleanser>
        </template>
      </modal-view>
    </transition>
  </div>
</template>
<script>
import CleanserTable from "../components/TableCleanser.vue";
import AddCleanser from "../components/AddCleanser.vue";
import AddCleanedDataSet from "../components/AddCleanedDataSet.vue";
import UpdateCleanser from "../components/InputForms/UpdateCleanser.vue";
import Modal from "../components/Modal.vue";

export default {
  components: {
    "cleanser-table": CleanserTable,
    "add-cleanser": AddCleanser,
    "modal-view": Modal,
    "add-cleaned-data-set": AddCleanedDataSet,
    "update-cleanser": UpdateCleanser,
  },
  data() {
    this.autenticateSession();
    return {
      admin: localStorage.admin,
      showAddCleanser: false,
      showUpdateCleanser: false,
      showApplyCleanser: false,
      showUpdateCleanserObject: false,
      componentKey: 0,
      selected_cleanser: "",
      operationsItems: [
        {
          operation: "add_cleanser",
          operation_img:
            "<i class='pi pi-plus-circle' style='font-size: 230px'></i>",
          operation_desc: "Click here to create new Cleanser",
          operation_button:
            '<div class="d-grid"><button class="btn btn-primary" ' +
            'type="button" @click="toggleShowAddData"> <span class="btn-label"> <i class="pi pi-plus-circle" style="font-size: 23px"></i>' +
            " </button>   </div>",
        },
        {
          operation: "apply_cleanser",
          operation_img:
            "<i class='pi pi-filter' style='font-size: 230px'></i>",
          operation_desc: "Click here to apply Cleanser",
          operation_button:
            '<div class="d-grid"> <button class="btn btn-primary" type="button" @click="toggleShowApplyCleanser()" >' +
            '<span class="btn-label"><i class="pi pi-filter" style="font-size: 23px"></i></span> </button>  </div>',
        },
        {
          operation: "update_cleanser",
          operation_img:
            "<i class='pi pi-spin pi-spinner' style='font-size: 230px'></i>",
          operation_desc:
            "Click here to update Cleanser!" +
            " This will automatically scan all your datasets to find and assign applicable Cleansers",
          operation_button:
            '<div class="d-grid"> <button class="btn btn-primary" ' +
            'type="button" @click="updateCleansers"> <span class="btn-label"> <i class="pi pi-spinner" style="font-size: 23px"></i>' +
            " </button>  </div>",
        },
      ],
    };
  },
  methods: {
    toggleShowAddCleanser() {
      this.showAddCleanser = !this.showAddCleanser;
    },
    toggleShowApplyCleanser() {
      this.showApplyCleanser = !this.showApplyCleanser;
    },
    toggleShowUpdateCleanser() {
      this.showUpdateCleanser = !this.showUpdateCleanser;
      this.updateCleansers();
    },
    toggleShowUpdateCleanserObject() {
      this.showUpdateCleanserObject = !this.showUpdateCleanserObject;
    },
    update_cleanser(cleanser) {
      this.selected_cleanser = cleanser;
      this.toggleShowUpdateCleanserObject();
    },
    refreshData() {
      this.componentKey += 1;
      this.showAddCleanser = false;
      this.showUpdateCleanser = false;
      this.showAddTableData = false;
      this.showApplyCleanser = false;
      this.showUpdateCleanserObject = false;
    },
    updateCleansers() {
      this.$axios
        .post("/update_cleansers/" + localStorage.loggedUser)
        .then(() => {
          this.$toast.add({
            severity: "success",
            summary: "Updating Cleansers Successful",
            detail:
              "All your Cleanser are updated!\nSuitable datasets were assigned to the applicable Cleansers",
            life: 8000,
          });
          this.refreshData();
        });
    },
    autenticateSession() {
      if (localStorage.loggedUser && localStorage.token) {
        this.$axios
          .get("/user/validatetoken?token=" + localStorage.token)
          .then(() => {
            this.selected_user = localStorage.loggedUser;
            this.$axios.get("/user/" + this.selected_user).then((res) => {
              this.$store.state.loggedUser = res.data;
            });
          })
          .catch(() => {
            this.$router.push("/");
          });
      } else {
        this.$router.push("/");
      }
    },
  },
};
</script>
<style scoped>
.banner-image {
  background-image: url(~@/assets/CLEANSER_BACKGROUND.jpg);
}
.component-card {
  margin-top: 30px;
  position: relative;
  display: flex;
  flex-direction: column;
  min-width: 0;
  word-wrap: break-word;
  background-color: #fff;
  background-clip: border-box;
  border-radius: 0.25rem;
  /* min-width: 100%; */
}
</style>