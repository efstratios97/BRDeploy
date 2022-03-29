<template>
  <div>
    <div class="p-grid p-fluid">
      <div class="p-col">
        <div class="p-inputgroup">
          <span class="p-inputgroup-addon">
            <i class="pi pi-file"></i>
          </span>
          <Dropdown
            v-model="selected_dataset_label"
            :options="dataset_labels"
            optionLabel="label.name"
            style="minwidth: 14rem"
            placeholder="Select a Dataset Label"
            @change="send_dataset_label()"
          />
        </div>
      </div>
    </div>
  </div>
</template>
<script>
export default {
  data() {
    return {
      dataset_labels: this.getDatasetLabels(),
      label_desc: "",
      selected_dataset_label: "",
    };
  },
  methods: {
    send_dataset_label() {
      this.$emit("input-label", this.selected_dataset_label);
    },
    getDatasetLabels() {
      this.$axios.get("/get_all_labels").then((res) => {
        var labels_tmp = [];
        for (let index = 0; index < res.data.length; index++) {
          labels_tmp.push({ label: res.data[index] });
        }
        this.dataset_labels = labels_tmp;
      });
    },
  },
};
</script>
<style scoped>
.p-cascadeselect {
  max-width: 50%;
}
.p-grid {
  margin-left: 5px;
}
</style>
