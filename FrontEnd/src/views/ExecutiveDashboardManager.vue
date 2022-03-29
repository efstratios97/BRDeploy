<template>
  <div v-if="admin === 'true'">
    <div class="banner-head banner-image p-shadow-14"></div>
    <div class="page-background">
      <div class="container-xxl main-page p-shadow-14">
        <h1 style="text-align: left; font-size: 38px">Executive Dashboard</h1>
        <div class="component-card">
          <router-view
            v-slot="{ Component }"
            @add-executive-dashboard="toggleShowAddExecutiveDashboard"
            @update="update_dashboard($event)"
            :key="componentKey"
          >
            <keep-alive>
              <div class="component-card">
                <component :is="Component" :key="componentKey" />
              </div>
            </keep-alive>
          </router-view>
        </div>
      </div>
    </div>
    <transition class="modal-animation">
      <modal-view v-if="showAddExecutiveDashboard" @close="refreshData()">
        <template v-slot:header>Add Executive Dashboard</template>
        <template v-slot:body>
          <add-executive-dashboards @close="refreshData()">
          </add-executive-dashboards> </template
      ></modal-view>
    </transition>
    <transition class="modal-animation">
      <modal-view v-if="showUpdateExecutiveDashboard" @close="refreshData()">
        <template v-slot:header>Update Executive Dashboard</template>
        <template v-slot:body>
          <update-executive-dashboards
            :dashboard="selected_dashboard"
            @close="refreshData()"
          >
          </update-executive-dashboards> </template
      ></modal-view>
    </transition>
  </div>
</template>
<script>
import AddExecutiveDashboards from "../components/InputForms/AddExecutiveDashboards.vue";
import UpdateExecutiveDashboard from "../components/InputForms/UpdateExecutiveDashboard.vue";
import Modal from "../components/Modal.vue";

export default {
  components: {
    "add-executive-dashboards": AddExecutiveDashboards,
    "update-executive-dashboards": UpdateExecutiveDashboard,
    "modal-view": Modal,
  },
  data() {
    this.autenticateSession();
    return {
      admin: localStorage.admin,
      showAddExecutiveDashboard: false,
      showUpdateExecutiveDashboard: false,
      selected_dashboard: "",
      componentKey: 0,
    };
  },
  methods: {
    update_dashboard(dashboard) {
      this.selected_dashboard = dashboard;
      this.toggleShowUpdateExecutiveDashboard();
    },
    toggleShowAddExecutiveDashboard() {
      this.showAddExecutiveDashboard = !this.showAddExecutiveDashboard;
    },
    toggleShowUpdateExecutiveDashboard() {
      this.showUpdateExecutiveDashboard = !this.showUpdateExecutiveDashboard;
    },
    refreshData() {
      this.componentKey += 1;
      this.showUpdateExecutiveDashboard = false;
      this.showAddExecutiveDashboard = false;
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
  background-image: url(~@/assets/EXECUTIVEDASHBOARD_BACKGROUND.jpg);
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
      