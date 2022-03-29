<template>
  <div>
    <div v-if="input_field_selected === false">
      <Card class="component-card">
        <template v-slot:title> Input Field Selection </template>
        <template v-slot:subtitle>
          Select based on what values you want to perform the Analysis
        </template>
        <template v-slot:content>
          <div class="p-grid p-align-center">
            <div class="p-col-6">
              <div class="p-fluid">
                <Button
                  label="Analysis based on Department"
                  @click="toggleInputFieldDepartment()"
                  icon="pi pi-filter"
                  iconPos="right"
                />
              </div>
            </div>
            <div class="p-col">
              <div class="p-fluid">
                <Button
                  label="Analysis based on Domain"
                  @click="toggleInputFieldDomain()"
                  icon="pi pi-filter"
                  iconPos="right"
                />
              </div>
            </div>
          </div>
        </template>
      </Card>
    </div>
    <div v-if="selected_department_input_field">
      <Card class="component-card">
        <template v-slot:title> Department </template>
        <template v-slot:subtitle> Select Department </template>
        <template v-slot:content>
          <form>
            <div class="p-grid">
              <div class="p-col">
                <Dropdown
                  v-model="selected_department"
                  :options="departments"
                  :filter="true"
                  optionLabel="dep"
                  placeholder="Select Department"
                  filterPlaceholder="Find a Departmet"
                  @change="send_departments"
                />
              </div>
              <div class="p-col">
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
                    By selecting a department all sub departments associated
                    with the selected department will be included in the
                    Analysis too! In your current case:
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
              </div>
            </div>
          </form>
        </template>
        <template #footer>
          <div class="p-grid">
            <div class="p-col">
              <div class="p-fluid">
                <Button
                  label="Select other Input Options"
                  @click="toggleInputFields()"
                  icon="pi pi-undo"
                  iconPos="right"
                />
              </div>
            </div>
          </div>
        </template>
      </Card>
    </div>
    <div v-if="selected_domain_input_field">
      <Card class="component-card">
        <template v-slot:title> Domain </template>
        <template v-slot:subtitle> Select Domain </template>
        <template v-slot:content>
          <form class="overflow-auto">
            <Dropdown
              v-model="selected_domain"
              :options="domains"
              :filter="true"
              optionLabel="domain"
              placeholder="Select Domain"
              filterPlaceholder="Find a Domain"
              @change="send_domain"
            />
          </form>
        </template>
        <template #footer>
          <div class="p-grid">
            <div class="p-col">
              <div class="p-fluid">
                <Button
                  label="Select other Input Options"
                  @click="toggleInputFields()"
                  icon="pi pi-undo"
                  iconPos="right"
                />
              </div>
            </div>
          </div>
        </template>
      </Card>
    </div>
  </div>
</template>
<script>
export default {
  props: [
    "departments",
    "domains",
    "selected_dataset_id",
    "selected_dataset_label",
  ],
  data() {
    return {
      selected_domain_input_field: false,
      selected_department_input_field: false,
      input_field_selected: false,
      selected_domain: "",
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
    send_domain() {
      this.$emit("input-parameter", this.selected_domain);
    },
    toggleDepInfo() {
      if (this.selected_department === "") {
        this.disabled_depInfo = true;
      } else {
        this.disabled_depInfo = false;
        this.depInfo = !this.depInfo;
      }
    },
    toggleInputFields() {
      this.input_field_selected = !this.input_field_selected;
      this.selected_domain_input_field = false;
      this.selected_department_input_field = false;
      this.selected_domain = "";
      this.selected_department = "";
    },
    toggleInputFieldDepartment() {
      this.selected_department_input_field =
        !this.selected_department_input_field;
      this.input_field_selected = true;
    },
    toggleInputFieldDomain() {
      this.selected_domain_input_field = !this.selected_domain_input_field;
      this.input_field_selected = true;
    },
    getDatasetDepartmentByHiearchy() {
      this.$axios
        .get(
          "/get_data_special_by_br_hierarchy/" +
            this.selected_dataset_id +
            "/" +
            this.selected_dataset_label +
            "/" +
            "get_departments_by_br_hiararchy/" +
            this.selected_department["dep"]
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
  min-width: 100%;
  min-height: 175px;
}
</style>