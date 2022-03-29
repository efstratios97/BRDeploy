<template>
  <Card>
    <template v-slot:title> Dataset Selection </template>
    <template v-slot:subtitle>
      Select the Dataset you want to analyze
    </template>
    <template v-slot:content>
      <CascadeSelect
        v-model="selected_dataset"
        :options="datasets"
        optionLabel="dataset_desc"
        optionGroupLabel="label"
        :optionGroupChildren="['dataset']"
        style="minwidth: 14rem"
        placeholder="Select a Dataset"
      />
    </template>
    <template v-slot:footer>
      <customazible-button
        @button-click="nextPage()"
        altLabel="Next"
        altClass="p-flex p-justify-content-center"
        altButtonStyle="min-width: 100%"
        altIcon="pi pi-arrow-circle-right"
        altIconPos="right"
      ></customazible-button>
    </template>
  </Card>
</template>

<script>
import CustomazibleButton from "./HelperComponents/CustomazibleButton.vue";

export default {
  components: {
    "customazible-button": CustomazibleButton,
  },
  data() {
    return {
      selected_dataset: "",
      datasets: this.getDatasetOptions(),
    };
  },

  methods: {
    nextPage() {
      if (this.selected_dataset !== "") {
        var selected_dataset_selector = {};
        selected_dataset_selector["dataset_id"] =
          this.selected_dataset.dataset_desc
            .split("ID: ")[1]
            .substring(
              0,
              this.selected_dataset.dataset_desc.split("ID: ")[1].indexOf(" ")
            );
        selected_dataset_selector["dataset_label"] =
          this.selected_dataset.dataset_desc.split("Label: ")[1];
        localStorage.selected_dataset_id =
          selected_dataset_selector["dataset_id"];
        localStorage.selected_dataset_label =
          selected_dataset_selector["dataset_label"];
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