<template>
  <div>
    <div class="banner-head banner-image p-shadow-14"></div>
    <div class="page-background">
      <div class="container-xxl main-page p-shadow-14">
        <h1 style="text-align: left; font-size: 38px">Executive Dashboard</h1>
        <div class="component-card">
          <router-view
            v-slot="{ Component }"
            @add-executive-dashboard="toggleShowAddExecutiveDashboard"
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
      <modal-view
        v-if="showAddExecutiveDashboard"
        @close="toggleShowAddExecutiveDashboard"
      >
        <template v-slot:header>Add Executive Dashboard</template>
        <template v-slot:body>
          <add-executive-dashboards @close="toggleShowAddExecutiveDashboard()">
          </add-executive-dashboards> </template
      ></modal-view>
    </transition>
  </div>
</template>
<script>
import AddExecutiveDashboards from "../components/InputForms/AddExecutiveDashboards.vue";
import Modal from "../components/Modal.vue";

export default {
  components: {
    "add-executive-dashboards": AddExecutiveDashboards,
    "modal-view": Modal,
  },
  data() {
    return {
      showAddExecutiveDashboard: false,
      componentKey: 0,
    };
  },
  methods: {
    toggleShowAddExecutiveDashboard() {
      this.showAddExecutiveDashboard = !this.showAddExecutiveDashboard;
      this.refreshData();
    },
    refreshData() {
      this.componentKey += 1;
    },
    autenticateSession() {
      this.refreshData();

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
  background-image: url("https://www.br.de/unternehmen/inhalt/veranstaltungen/bayern-1-ballon-taschen-122~_v-img__16__9__xl_-d31c35f8186ebeb80b0cd843a7c267a0e0c81647.png?version=a7b23");
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
      