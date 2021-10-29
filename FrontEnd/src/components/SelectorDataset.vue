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
      <Dropdown
        v-model="selected_dataset"
        :options="datasets"
        optionLabel="dataset"
        placeholder="Select a Dataset"
        :filter="true"
        filterPlaceholder="Find a Dataset"
        :showClear="true"
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
      datasets: this.getDatasetOptions(),
      selected_dataset: "",
    };
  },
  methods: {
    nextPage() {
      if (this.selected_dataset !== "") {
        this.selected_dataset.dataset = this.selected_dataset.dataset.split(
          "ID: "
        )[1];
        this.$emit("next-page", {
          selected_dataset: this.selected_dataset.dataset,
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
          for (let index = 0; index < res.data.data.length; index++) {
            datasets_tmp.push({
              dataset:
                "NAME: " +
                res.data.data[index]["name"] +
                "   |   " +
                "ID: " +
                res.data.data[index]["dataset_id"],
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