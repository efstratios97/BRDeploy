<template>
  <div v-if="admin === 'true'">
    <div class="banner-head banner-image p-shadow-14"></div>
    <div class="page-background">
      <div class="container-xxl main-page p-shadow-14">
        <h1 style="text-align: left; font-size: 38px">Data Health</h1>
        <div class="component-card">
          <!-- <Steps :model="items" :readonly="true" /> -->
          <router-view
            v-slot="{ Component }"
            :selected_dataset_id="selected_dataset_id"
            :selected_dataset_label="selected_dataset_label"
            @prev-page="prevPage($event)"
            @next-page="nextPage($event)"
            @update="update_architecture_view($event)"
            :key="componentKey"
          >
            <keep-alive>
              <div class="component-card">
                <component :is="Component" />
              </div>
            </keep-alive>
          </router-view>
        </div>
      </div>
    </div>
    <transition class="modal-animation">
      <modal-view v-if="showUpdateArchitectureView" @close="refreshData()">
        <template v-slot:header>Update Architecture View</template>
        <template v-slot:body>
          <update-architecture-view
            :architecture_view="selected_architecture_view"
            :selected_dataset_id="selected_dataset_id"
            :selected_dataset_label="selected_dataset_label"
            @close="refreshData()"
          >
          </update-architecture-view>
        </template>
      </modal-view>
    </transition>
  </div>
</template>
<script>
import UpdateArchitectureView from "../components/InputForms/UpdateArchitectureView.vue";
import Modal from "../components/Modal.vue";

export default {
  components: {
    "modal-view": Modal,
    "update-architecture-view": UpdateArchitectureView,
  },
  data() {
    return {
      admin: localStorage.admin,
      selected_dataset: "",
      selected_architecture_view: "",
      componentKey: 0,
      showUpdateArchitectureView: false,
      items: [
        {
          label: "Select Dataset",
          to: "/datahealthmanager",
        },
        {
          label: "Analyze DataHealth",
          to: "/datahealthmanager/dashboard",
        },
      ],
    };
  },
  methods: {
    nextPage(event) {
      this.selected_dataset_id = event.selected_dataset.dataset_id;
      this.selected_dataset_label = event.selected_dataset.dataset_label;
      this.$router.push(this.items[event.pageIndex + 1].to);
    },
    prevPage(event) {
      this.$router.push(this.items[event.pageIndex - 1].to);
    },
    toggleShowAnalyzerSelector() {
      this.showAnalyzerSelector = !this.showAnalyzerSelector;
    },
    toggleShowUpdateArchitectureView() {
      this.showUpdateArchitectureView = !this.showUpdateArchitectureView;
    },
    update_architecture_view(architecture_view) {
      this.selected_architecture_view = architecture_view;
      this.toggleShowUpdateArchitectureView();
    },
    refreshData() {
      this.componentKey += 1;
      this.showUpdateArchitectureView = false;
    },
    updateSelectedDataset(value) {
      this.selected_dataset = value;
      this.datasetSelected = true;
      this.componentKey++;
      this.toggleShowAnalyzerSelector();
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
  background-image: url(~@/assets/DATAHEALTH_BACKGROUND.png);
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
      