<template>
  <Card>
    <template v-slot:title> Dataset Selection </template>
    <template v-slot:subtitle>
      Select the Dataset you want to analyze
    </template>
    <template v-slot:content>
      <div class="p-fluid">
        <div class="p-field"></div>
      </div>
      <CascadeSelect
        v-model="selected_dataset_v2"
        :options="datasets_v2"
        optionLabel="dataset_desc"
        optionGroupLabel="label"
        :optionGroupChildren="['dataset']"
        style="minwidth: 14rem"
        placeholder="Select a Dataset"
      />
    </template>
    <template v-slot:footer>
      <div class="p-grid p-nogutter p-justify-between">
        <i></i>
        <Button
          label="Next"
          @click="nextPage()"
          icon="pi pi-angle-right"
          iconPos="right"
        />
      </div>
    </template>
  </Card>
</template>

<script>
export default {
  data() {
    return {
      selected_dataset_v2: "",
      datasets_v2: this.getDatasetOptions_v2(),
      label_desc: "",
    };
  },
  methods: {
    nextPage() {
      if (this.selected_dataset_v2 !== "") {
        var selected_dataset_selector = {};
        selected_dataset_selector["dataset_id"] =
          this.selected_dataset_v2.dataset_desc.split("ID: ")[1];
        selected_dataset_selector["dataset_label"] = this.label_desc;
        this.$emit("next-page", {
          selected_dataset: selected_dataset_selector,
          pageIndex: 0,
        });
      } else {
        this.$toast.add({
          severity: "warn",
          summary: "No Dataset selected",
          detail: "Please select dataset",
          life: 3000,
        });
      }
    },
    getDatasetOptions_v2() {
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
            if (index === 0) {
              datasets_tmp[index_dataset_tmp]["dataset"].push({
                dataset_desc:
                  "Dataset: " +
                  res.data.data[index]["name"] +
                  "   |   " +
                  "NEWEST" +
                  "   |   " +
                  "ID: " +
                  res.data.data[index]["dataset_id"],
              });
              this.label_desc = res.data.data[index]["label"];
            } else {
              datasets_tmp[index_dataset_tmp]["dataset"].push({
                dataset_desc:
                  "Dataset: " +
                  res.data.data[index]["name"] +
                  "   |   " +
                  "Created: " +
                  res.data.data[index]["creation_date"].split(",")[1] +
                  "   |   " +
                  "ID: " +
                  res.data.data[index]["dataset_id"],
              });
              this.label_desc = res.data.data[index]["label"];
            }
          }
          this.datasets_v2 = datasets_tmp;
        });
    },
  },
};
</script>
<style scoped>
label {
  display: block;
}

.btn-form {
  color: white;
  background: #0d6efd;
  border: 0px solid blue;
  border-radius: 2px;
}

select {
  color: black;
}

input {
  color: black;
}

textarea {
  color: black;
}
</style>