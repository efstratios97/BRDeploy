<template>
  <div v-if="admin === 'true'">
    <div class="banner-head banner-image p-shadow-14"></div>
    <div class="page-background">
      <div class="container-xxl main-page p-shadow-14">
        <h1 style="text-align: left; font-size: 38px">KPI Manager</h1>
        <div class="component-card">
          <!-- <Steps :model="items" :readonly="true" /> -->
          <router-view
            v-slot="{ Component }"
            @add-kpi="toggleShowAddKPI"
            @add-aspect="toggleShowAddAspect"
            @update-kpi="updateKPI($event)"
            @update-aspect="updateAspect($event)"
            :key="componentKey"
            :selected_dataset_id="selected_dataset_id"
            :selected_dataset_label="selected_dataset_label"
            @prev-page="prevPage($event)"
            @next-page="nextPage($event)"
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
      <modal-view v-if="showAddKPI" @close="toggleShowAddKPI()">
        <template v-slot:header>BUILD YOUR KPI</template>
        <template v-slot:body>
          <add-kpi
            :selected_dataset_id="selected_dataset_id"
            :selected_dataset_label="selected_dataset_label"
            @close="toggleShowAddKPI()"
          >
          </add-kpi>
        </template>
      </modal-view>
    </transition>
    <transition class="modal-animation">
      <modal-view v-if="showAddAspect" @close="toggleShowAddAspect()">
        <template v-slot:header>BUILD YOUR ASPECT</template>
        <template v-slot:body>
          <add-aspect
            :selected_dataset_id="selected_dataset_id"
            :selected_dataset_label="selected_dataset_label"
            @close="toggleShowAddAspect()"
          >
          </add-aspect>
        </template>
      </modal-view>
    </transition>
    <transition class="modal-animation">
      <modal-view v-if="showUpdateAspect" @close="toggleShowUpdateAspect()">
        <template v-slot:header>Update your Aspect</template>
        <template v-slot:body>
          <update-aspect
            :aspect="selected_aspect"
            @close="toggleShowUpdateAspect()"
          >
          </update-aspect>
        </template>
      </modal-view>
    </transition>
    <transition class="modal-animation">
      <modal-view v-if="showUpdateKPI" @close="toggleShowUpdateKPI()">
        <template v-slot:header>Update your KPI</template>
        <template v-slot:body>
          <update-kpi :kpi="selected_kpi" @close="toggleShowUpdateKPI()">
          </update-kpi>
        </template>
      </modal-view>
    </transition>
  </div>
</template>
<script>
import Modal from "../components/Modal.vue";
import AddKPI from "../components/InputForms/AddKPI.vue";
import AddAspect from "../components/InputForms/AddAspect.vue";
import UpdateKPI from "../components/InputForms/UpdateKPI.vue";
import UpdateAspect from "../components/InputForms/UpdateAspect.vue";

export default {
  components: {
    "modal-view": Modal,
    "add-kpi": AddKPI,
    "add-aspect": AddAspect,
    "update-kpi": UpdateKPI,
    "update-aspect": UpdateAspect,
  },
  data() {
    this.autenticateSession();
    return {
      admin: localStorage.admin,
      selected_dataset: "",
      selected_kpi: "",
      selected_aspect: "",
      componentKey: 0,
      showAddKPI: false,
      showAddAspect: false,
      showUpdateKPI: false,
      showUpdateAspect: false,
      items: [
        {
          label: "Select Dataset",
          to: "/kpimanager",
        },
        {
          label: "Analyze DataHealth",
          to: "/kpimanager/dashboard",
        },
      ],
    };
  },
  methods: {
    toggleShowAddKPI() {
      this.showAddKPI = !this.showAddKPI;
      this.increaseComponentKey();
    },
    toggleShowAddAspect() {
      this.showAddAspect = !this.showAddAspect;
      this.increaseComponentKey();
    },
    toggleShowUpdateAspect() {
      this.showUpdateAspect = !this.showUpdateAspect;
      this.increaseComponentKey();
    },
    toggleShowUpdateKPI() {
      this.showUpdateKPI = !this.showUpdateKPI;
      this.increaseComponentKey();
    },
    updateKPI(kpi) {
      this.selected_kpi = kpi;
      this.toggleShowUpdateKPI();
    },
    updateAspect(aspect) {
      this.selected_aspect = aspect;
      this.toggleShowUpdateAspect();
    },
    nextPage(event) {
      this.selected_dataset_id = event.selected_dataset.dataset_id;
      this.selected_dataset_label = event.selected_dataset.dataset_label;
      this.$router.push(this.items[event.pageIndex + 1].to);
    },
    prevPage(event) {
      this.$router.push(this.items[event.pageIndex - 1].to);
    },
    increaseComponentKey() {
      this.componentKey += 1;
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
  background-image: url(~@/assets/KPIMANAGER_BACKGROUND_1.jpg);
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
      