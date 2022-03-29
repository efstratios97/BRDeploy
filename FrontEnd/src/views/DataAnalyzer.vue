<template>
  <div v-if="admin === 'true'">
    <div class="banner-head banner-image p-shadow-14"></div>
    <div class="page-background">
      <div class="container-xxl main-page p-shadow-14">
        <h1 style="text-align: left; font-size: 38px">Data Analyzer</h1>
        <div class="component-card">
          <!-- <Steps :model="items" :readonly="true" /> -->
          <router-view
            v-slot="{ Component }"
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
  </div>
</template>

<script>
import SelectorAnalyzerDataset from "../components/SelectorDataset.vue";
import Modal from "../components/Modal.vue";

export default {
  components: {
    "modal-view": Modal,
    "selector-analyzer-dataset": SelectorAnalyzerDataset,
  },
  data() {
    this.autenticateSession();
    return {
      admin: localStorage.admin,
      showAnalyzerSelector: false,
      showFurtherHeatMaps: false,
      showFurtherSimpleStatistics: false,
      selected_dataset: "",
      datasetSelected: false,
      componentKey: 0,
      items: [
        {
          label: "Select Dataset",
          to: "/dataanalyzer",
        },
        {
          label: "Analyze Dataset",
          to: "/dataanalyzer/dashboard",
        },
      ],
    };
  },
  methods: {
    nextPage(event) {
      this.selected_dataset = event.selected_dataset;
      this.selected_dataset_id = event.selected_dataset.dataset_id;
      this.selected_dataset_label = event.selected_dataset.dataset_label;
      this.$router.push(this.items[event.pageIndex + 1].to);
    },
    prevPage(event) {
      this.$router.push(this.items[event.pageIndex - 1].to);
    },
    toggleShowFurtherSimpleStatistics() {
      this.showFurtherSimpleStatistics = !this.showFurtherSimpleStatistics;
    },
    toggleShowFurtherHeatMaps() {
      this.showFurtherHeatMaps = !this.showFurtherHeatMaps;
    },
    toggleShowAnalyzerSelector() {
      this.showAnalyzerSelector = !this.showAnalyzerSelector;
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
  background-image: url("~@/assets/DATAANALYZER_BACKGROUND.png");
}
.bokeh-graph {
  resize: both;
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
}
</style>