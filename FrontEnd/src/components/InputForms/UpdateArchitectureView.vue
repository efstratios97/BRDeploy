<template>
  <div>
    <form>
      <div class="p-fluid">
        <div class="p-inputgroup">
          <span class="p-inputgroup-addon">
            <b-icon-upc />
          </span>
          <InputText placeholder="Name" v-model="architecture_view_name" />
        </div>
        <br />
        <div class="p-inputgroup">
          <span class="p-inputgroup-addon">
            <b-icon-journal-text />
          </span>
          <InputText
            placeholder="Description"
            v-model="architecture_view_description"
          />
        </div>
        <br />
        <MultiSelect
          v-model="selected_architecture_view_components"
          :options="architecture_view_components"
          optionLabel="architecture_view_component"
          placeholder="Select a Architecture View Component"
          :filter="true"
          filterPlaceholder="Find a Architecture View Component"
          class="multiselect-custom"
        />
        <br />

        <div class="p-grid p-nogutter p-justify-between">
          <Button
            label="Update Architecture View"
            @click="updateArchitectureView()"
          />
        </div>
      </div>
    </form>
  </div>
</template>
<script>
export default {
  props: ["architecture_view"],
  data() {
    return {
      architecture_view_components: this.getComponents(),
      selected_architecture_view_components: [],
      selected_architecture_view: "",
      architecture_view_description: "",
      architecture_view_name: "",
    };
  },
  created() {
    this.architecture_view_name = this.architecture_view.name;
    this.architecture_view_description = this.architecture_view.description;
    this.architecture_view.components.forEach((component) => {
      this.selected_architecture_view_components.push({
        architecture_view_component: component,
      });
    });
  },
  methods: {
    updateArchitectureView() {
      var formData = new FormData();
      formData.append(
        "architecture_view_id",
        this.architecture_view.architecture_view_id
      );
      formData.append("name", this.architecture_view_name);
      formData.append("description", this.architecture_view_description);
      var components_string = "";
      this.selected_architecture_view_components.forEach(
        (architecture_view_component) => {
          components_string +=
            architecture_view_component.architecture_view_component + ",";
        }
      );
      formData.append("components", components_string.slice(0, -1));
      this.$axios
        .post("/update_architecture_view", formData)
        .then(() => {
          this.$toast.add({
            severity: "success",
            summary: "Architecture View Update Successful",
            detail: "The selected Architecture View was updated",
            life: 3000,
          });
          this.emitClose();
        })
        .catch(() => {
          this.$toast.add({
            severity: "error",
            summary: "Architecture View Update Unsuccessful",
            detail: "Check if Architecture View Name already exists",
            life: 3000,
          });
        });
    },
    getComponents() {
      this.$axios
        .get("/get_components/" + localStorage.selected_dataset_id)
        .then((res) => {
          var data_tmp = [];
          for (let index = 0; index < res.data.data.length; index++) {
            data_tmp.push({
              architecture_view_component: res.data.data[index],
            });
          }
          this.architecture_view_components = data_tmp;
        });
    },
    emitClose() {
      this.$emit("close");
    },
  },
};
</script>