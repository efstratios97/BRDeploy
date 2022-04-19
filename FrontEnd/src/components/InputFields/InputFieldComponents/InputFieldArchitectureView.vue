<template>
  <div>
    <Card class="component-card">
      <template v-slot:title> Architecture View </template>
      <template v-slot:subtitle> Select Architecture View </template>
      <template v-slot:content>
        <form>
          <div class="p-grid">
            <div :class="showArchitectureViewInfo ? 'p-col-11' : 'p-col-12'">
              <Dropdown
                v-model="selected_architecture_views"
                :options="architecture_views"
                :filter="true"
                optionLabel="architecture_view.name"
                placeholder="Select Architecture View"
                filterPlaceholder="Find a Architecture View"
                @change="send_architecture_view"
              />
            </div>
            <div class="p-col-1" v-if="showArchitectureViewInfo">
              <Button
                icon="pi pi-info"
                class="p-button-rounded p-button-info"
                @click="toggleArchitectureViewInfo()"
              />
              <Dialog
                header="Info"
                v-model:visible="architectureViewInfo"
                :style="{ width: '50vw' }"
                :maximizable="true"
                :modal="true"
              >
                <p class="p-m-0">
                  Only components of an ArchitectureView will be taken into
                  account that are meaningful. Others will be omitted in the
                  analysis (An example might be ID).
                </p>
                <template #footer>
                  <Button
                    label="Confirm"
                    icon="pi pi-check"
                    @click="toggleArchitectureViewInfo()"
                    autofocus
                  />
                </template>
              </Dialog>
            </div>
          </div>
        </form>
      </template>
    </Card>
  </div>
</template>
<script>
export default {
  props: [
    "selected_dataset_id",
    "selected_dataset_label",
    "showArchitectureViewInfo",
  ],
  data() {
    return {
      architecture_views: [],
      selected_architecture_views: [],
      architectureViewInfo: false,
    };
  },
  created() {
    this.get_architecture_views();
  },
  methods: {
    send_architecture_view() {
      this.$emit("input-architecture-view", this.selected_architecture_views);
    },
    get_architecture_views() {
      this.$axios.get("/get_architecture_views").then((res) => {
        res.data.data.forEach((architecture_view) => {
          this.architecture_views.push({
            architecture_view: architecture_view,
          });
        });
      });
    },
    toggleArchitectureViewInfo() {
      this.architectureViewInfo = !this.architectureViewInfo;
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
  min-width: 100%;
  min-height: 175px;
}
</style>