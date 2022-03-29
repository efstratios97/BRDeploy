<template>
  <div v-if="admin === 'true'">
    <div class="banner-head banner-image p-shadow-14"></div>
    <div class="page-background">
      <div class="container-xxl main-page p-shadow-14">
        <h1 style="text-align: left; font-size: 38px">Data Manager</h1>
        <br />
        <br />
        <TabView class="tabview-custom" ref="tabview4">
          <TabPanel>
            <template #header>
              <b-icon-file-earmark-spreadsheet-fill
                style="font-size: 18px; margin: 3px"
              />
              <span><h4>Datasets</h4></span>
            </template>
            <Card class="component-card">
              <template v-slot:title> Datasets </template>
              <template v-slot:subtitle> Manager here your Datasets </template>
              <template v-slot:content>
                <data-set-table
                  :key="componentKey"
                  @view="viewDataset"
                  @update="updateDataset($event)"
                ></data-set-table>
              </template>
            </Card>
            <Card class="component-card">
              <template v-slot:title> Complete Data View </template>
              <template v-slot:subtitle>
                View here your whole dataset
              </template>
              <template v-slot:content>
                <data-set-complete-table
                  :dataset_id="this.selected_dataset_id"
                  :storage_type="this.selected_storage_type"
                  v-if="showAddTableData"
                >
                </data-set-complete-table>
              </template>
            </Card>
          </TabPanel>
          <TabPanel>
            <template #header>
              <i class="pi pi-cog" style="font-size: 18px; margin: 3px"></i>
              <span><h4>DataManager Operations</h4></span>
            </template>
            <Card class="component-card">
              <template v-slot:content>
                <Carousel
                  :value="operations"
                  :numVisible="1"
                  :numScroll="1"
                  :responsiveOptions="responsiveOptions"
                >
                  <template #header>
                    <h1 style="text-align: center">Available Operations</h1>
                  </template>
                  <template #item="operations">
                    <div class="operation-item">
                      <div class="operation-item-content">
                        <div class="p-mb-3">
                          <span style="text-align: center">
                            {{ operations.title
                            }}<b-icon-file-earmark-plus-fill
                              style="font-size: 230px"
                          /></span>
                        </div>
                        <h4>Click to create a new Dataset</h4>
                        <div>
                          <div class="d-grid">
                            <button
                              class="btn btn-primary"
                              type="button"
                              @click="toggleShowAddData"
                            >
                              <span class="btn-label"
                                ><b-icon-file-earmark-plus-fill
                              /></span>
                            </button>
                          </div>
                        </div>
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
      <modal-view v-if="showAddData" @close="toggleShowAddData">
        <template v-slot:header>ADD DATASET</template>
        <template v-slot:body>
          <add-data-set @close="refreshData"> </add-data-set> </template
      ></modal-view>
    </transition>
    <transition class="modal-animation">
      <modal-view v-if="showUpdateData" @close="toggleShowUpdateData">
        <template v-slot:header>UPDATE DATASET</template>
        <template v-slot:body>
          <update-data-set @close="refreshData" :dataset="selected_dataset">
          </update-data-set> </template
      ></modal-view>
    </transition>
  </div>
</template>
<script>
import DataSetTable from "../components/DataSetTable.vue";
import DataSetCompleteTable from "../components/TableCompleteDataSet.vue";
import AddDataSet from "../components/AddDataSet.vue";
import UpdateDataset from "../components/InputForms/UpdateDataset.vue";
import Modal from "../components/Modal.vue";

export default {
  components: {
    "data-set-table": DataSetTable,
    "add-data-set": AddDataSet,
    "update-data-set": UpdateDataset,
    "modal-view": Modal,
    "data-set-complete-table": DataSetCompleteTable,
  },
  data() {
    this.autenticateSession();
    return {
      admin: localStorage.admin,
      showAddData: false,
      showUpdateData: false,
      showAddTableData: false,
      componentKey: 0,
      selected_dataset_id: "",
      selected_storage_type: "",
      selected_dataset: "",
      operations: [{ operation: 0 }],
    };
  },
  methods: {
    toggleShowAddData() {
      this.showAddData = !this.showAddData;
      this.componentKey += 1;
    },
    toggleShowUpdateData() {
      this.showUpdateData = !this.showUpdateData;
      this.componentKey += 1;
    },
    toggleShowAddTableData() {
      this.showAddTableData = !this.showAddTableData;
    },
    refreshData() {
      this.showAddData = false;
      this.showUpdateData = false;
      this.componentKey += 1;
    },
    viewDataset(dataset_id, storage_type) {
      this.selected_dataset_id = dataset_id;
      this.selected_storage_type = storage_type;
      this.toggleShowAddTableData();
    },
    updateDataset(dataset) {
      this.selected_dataset = dataset;
      this.toggleShowUpdateData();
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

<style>
.operation-item .operation-item-content {
  border: 1px solid var(--surface-d);
  border-radius: 10px;
  margin: 0.3rem;
  text-align: center;
  padding: 2rem 0;
}
.product-image {
  width: 50%;
  box-shadow: 0 3px 6px rgba(0, 0, 0, 0.16), 0 3px 6px rgba(0, 0, 0, 0.23);
}

.banner-head {
  min-height: 450px;
  max-height: 500px;
  display: flex;
  background-repeat: round;
  background-size: contain;
  width: calc(100%);
  height: calc(100%);
}

.banner-image {
  background-image: url(~@/assets/DATAMANAGER_BACKGROUND.jpg);
}

.p-card {
  display: table-cell;
  vertical-align: middle;
  text-align: center;
}

.container-xxl {
  min-width: calc(95%);
  overflow: visible;
}

.page-background {
  background-color: #f1f1f1;
  background-attachment: fixed;
  min-height: 80vh;
  overflow: visible;
}
.main-page {
  background-color: white;
  border-radius: 15px;
  position: fixed center;
  transform: translate(0px, -150px);
  min-height: 98vh;
}
.pt-tablecell {
  display: table-cell;
  vertical-align: text-top;
}

.h1_sub {
  color: white;
  text-align: center;
  font-size: bolder;
}

.tablehr {
  background: #0c8cd3;
  height: 28px;
}

button {
  color: white;
  background: #0c8cd3;
  border: 0px solid blue;
  border-radius: 2px;
}

.btn {
  display: inline-block;
  vertical-align: middle;
  -webkit-transform: perspective(1px) translateZ(0);
  transform: perspective(1px) translateZ(0);
  box-shadow: 0 0 1px rgba(0, 0, 0, 0);
  position: relative;
  overflow: hidden;
  width: auto;
}

.btn-label {
  font-size: 25px;
  display: block;
}

.btn:before {
  content: "";
  position: absolute;
  z-index: -1;
  left: 51%;
  right: 51%;
  bottom: 0;
  background: #0c8cd3;
  height: 4px;
  -webkit-transition-property: left, right;
  transition-property: left, right;
  -webkit-transition-duration: 0.3s;
  transition-duration: 0.3s;
  -webkit-transition-timing-function: ease-out;
  transition-timing-function: ease-out;
}
.btn:hover:before,
.btn:focus:before,
.btn:active:before {
  left: 0;
  right: 0;
}

.container-fluid {
  border-right: 1px solid black;
}

.br-sub {
  display: block;
  margin-bottom: 5em;
  line-height: 5em;
}

.v-enter-from {
  opacity: 0;
  transform: translateY(-40px);
}

.v-enter-active {
  transition: all 0.4s ease-out;
}

.v-enter-to {
  opacity: 1;
  transform: translateY(0);
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