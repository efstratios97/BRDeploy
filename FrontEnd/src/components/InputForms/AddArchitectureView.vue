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
            label="Create Architecture View"
            @click="createArchitectureView()"
          />
        </div>
      </div>
    </form>
  </div>
</template>
<script>
export default {
  props: ["selected_dataset_id", "selected_dataset_label"],
  data() {
    return {
      selected_architecture_view_components: "",
      selected_architecture_view: "",
      architecture_view_description: "",
      architecture_view_name: "",
      architecture_view_components: this.getComponents(),
    };
  },
  methods: {
    createArchitectureView() {
      this.submitted = true;
      this.formData = new FormData();
      this.formData.append("name", this.architecture_view_name);
      this.formData.append("description", this.architecture_view_description);
      var components_string = "";
      for (
        let index = 0;
        index < this.selected_architecture_view_components.length;
        index++
      ) {
        components_string +=
          this.selected_architecture_view_components[index]
            .architecture_view_component;
        if (index < this.selected_architecture_view_components.length - 1) {
          components_string += ",";
        }
      }
      this.formData.append("components", components_string);
      this.$axios
        .post("/create_architecture_view", this.formData)
        .then((res) => {
          this.$toast.add({
            severity: "success",
            summary:
              "Architecture View " + res.data.name + "Creation Successful",
            detail: "The selected Architecture View was created",
            life: 3000,
          });
          this.emitClose();
        })
        .catch(() => {
          this.$toast.add({
            severity: "error",
            summary: "Architecture View Creation Unsuccessful",
            detail: "Check if Architecture View Name already exists",
            life: 3000,
          });
        });
    },
    getComponents() {
      this.$axios
        .get("/get_components/" + this.selected_dataset_id)
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