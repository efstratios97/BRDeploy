<template>
  <Card class="component-card">
    <template v-slot:title> Department </template>
    <template v-slot:subtitle>
      Select Department to perform KPI Analysis
    </template>
    <template v-slot:content>
      <form class="overflow-auto">
        <Dropdown
          v-model="selected_department"
          :options="departments"
          :filter="true"
          optionLabel="dep"
          placeholder="Select Department"
          filterPlaceholder="Find a Departmet"
          @change="send_departments"
        />
        <Button
          icon="pi pi-info"
          class="p-button-rounded p-button-info"
          @click="toggleDepInfo()"
          :disabled="disabled_depInfo"
        />
        <Dialog
          header="Info"
          v-model:visible="depInfo"
          :style="{ width: '50vw' }"
          :maximizable="true"
          :modal="true"
        >
          <p class="p-m-0">
            By selecting a department all sub departments associated with the
            selected department will be included in the Analysis too! In your
            current case:
          </p>
          <ul
            v-for="department in departments_by_hierarchy"
            :key="department.dep"
          >
            <li>{{ department.dep }}</li>
          </ul>
          <template #footer>
            <Button
              label="Confirm"
              icon="pi pi-check"
              @click="toggleDepInfo()"
              autofocus
            />
          </template>
        </Dialog>
      </form>
    </template>
    <template #footer> </template>
  </Card>
</template>
<script>
export default {
  props: ["departments", "selected_dataset_id", "selected_dataset_label"],
  data() {
    return {
      selected_department: "",
      departments_by_hierarchy: "",
      depInfo: false,
      disabled_depInfo: true,
    };
  },
  methods: {
    send_departments() {
      this.disabled_depInfo = false;
      this.getDatasetDepartmentByHiearchy();
      this.$emit("input-parameter", this.selected_department);
    },
    toggleDepInfo() {
      if (this.selected_department === "") {
        this.disabled_depInfo = true;
      } else {
        this.disabled_depInfo = false;
        this.depInfo = !this.depInfo;
      }
    },
    getDatasetDepartmentByHiearchy() {
      this.$axios
        .get(
          "/get_departments_by_br_hiararchy/" +
            this.selected_department["dep"] +
            "/" +
            this.selected_dataset_id +
            "/" +
            this.selected_dataset_label
        )
        .then((res) => {
          var departments_tmp = [];
          for (let index = 0; index < res.data.data.length; index++) {
            departments_tmp.push({ dep: res.data.data[index] });
          }
          this.departments_by_hierarchy = departments_tmp;
        });
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
</style>