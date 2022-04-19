<template>
  <div>
    <div class="p-grid p-fluid">
      <div class="p-col">
        <div class="p-inputgroup">
          <span class="p-inputgroup-addon">
            <i class="pi pi-file"></i>
          </span>
          <CascadeSelect
            v-model="selected_dataset"
            :options="datasets"
            optionLabel="dataset_desc"
            optionGroupLabel="label"
            :optionGroupChildren="['dataset']"
            style="minwidth: 14rem"
            :placeholder="selected_dataset_placeholder"
            @change="send_dataset()"
          />
        </div>
      </div>
    </div>
  </div>
</template>
<script>
export default {
  props: ["selected_dataset_specific"],
  data() {
    return {
      datasets: this.getDatasetOptions(),
      selected_dataset: "",
      selected_dataset_placeholder: "",
    };
  },
  created() {
    this.selected_dataset_specific === undefined
      ? (this.selected_dataset_placeholder = "Select Dataset")
      : (this.selected_dataset_placeholder =
          this.selected_dataset_specific[0]["dataset"][0].dataset_desc);
  },
  methods: {
    send_dataset() {
      let selected_dataset = {};
      selected_dataset["dataset_id"] = this.selected_dataset.dataset_desc
        .split("ID: ")[1]
        .substring(
          0,
          this.selected_dataset.dataset_desc.split("ID: ")[1].indexOf(" ")
        );
      selected_dataset["dataset_label"] =
        this.selected_dataset.dataset_desc.split("Label: ")[1];
      this.$emit("input-dataset", selected_dataset);
    },
    getDatasetOptions() {
      this.$axios
        .get("/get_datasets_only_name/" + localStorage.loggedUser)
        .then((res) => {
          var datasets_tmp = [];
          var datasets_tmp_plain_list = [];
          const label_prefix = "Dataset Category: ";
          for (let index = 0; index < res.data.data.length; index++) {
            if (
              datasets_tmp_plain_list.indexOf(
                label_prefix + res.data.data[index]["label"]
              ) < 0
            ) {
              datasets_tmp.push({
                label: label_prefix + res.data.data[index]["label"],
                dataset: [],
              });
              datasets_tmp_plain_list.push(
                label_prefix + res.data.data[index]["label"]
              );
            }
          }
          for (let index = 0; index < res.data.data.length; index++) {
            var index_dataset_tmp = datasets_tmp_plain_list.indexOf(
              label_prefix + res.data.data[index]["label"]
            );
            datasets_tmp[index_dataset_tmp]["dataset"].push({
              dataset_desc:
                "Dataset: " +
                res.data.data[index]["name"] +
                "   |   " +
                "Created: " +
                res.data.data[index]["creation_date"].split(",")[1] +
                "   |   " +
                "ID: " +
                res.data.data[index]["dataset_id"] +
                "   |   " +
                "Label: " +
                res.data.data[index]["label"],
            });
          }
          this.datasets = datasets_tmp;
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
