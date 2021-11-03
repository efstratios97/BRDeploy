<template>
  <form>
    <div class="p-grid p-fluid">
      <div class="p-col-12 p-md-12">
        <div class="p-inputgroup">
          <span class="p-inputgroup-addon">
            <i class="pi pi-cog"></i>
          </span>
          <InputText
            placeholder="Cleanser's Name"
            v-model="name"
            class="inputfield w-full"
          />
        </div>
      </div>
    </div>

    <div class="p-grid p-fluid">
      <div class="p-col-12 p-md-12">
        <Textarea
          placeholder="Cleanser Description"
          v-model="description"
          :autoResize="true"
          rows="5"
          cols="30"
        />
      </div>
    </div>

    <div class="p-grid p-fluid">
      <div class="p-col-12 p-md-12">
        <div class="p-inputgroup">
          <span class="p-inputgroup-addon">
            <i class="pi pi-file"></i>
          </span>
          <MultiSelect
            v-model="selected_datasets"
            :options="datasets"
            :filter="true"
            optionLabel="dataset"
            placeholder="Assign applicable Datasets"
            filterPlaceholder="Find Datasets"
            :showClear="true"
          />
        </div>
      </div>
    </div>

    <div class="p-grid p-fluid">
      <div class="p-col-12 p-md-12">
        <div class="p-inputgroup">
          <span class="p-inputgroup-addon">
            <i class="pi pi-cog"></i>
          </span>
          <MultiSelect
            v-model="selected_cleanser_operation_types"
            :options="cleanser_operation_types"
            :filter="true"
            optionLabel="operation"
            placeholder="Assign applicable Operations"
            filterPlaceholder="Find Operations"
            class="multiselect-custom"
            :showClear="true"
          />
        </div>
      </div>
    </div>

    <div class="p-grid p-fluid">
      <div class="p-col-12 p-md-12">
        <Button
          label="Create Cleanser"
          icon="pi pi-plus-circle"
          iconPos="center"
          @click="createCleanser"
        />
      </div>
    </div>
  </form>
</template>

<script>
export default {
  data() {
    return {
      name: "",
      description: "",
      datasets: this.getDatasetOptions(),
      cleanser_operation_types: this.getCleanserOperationTypesOptions(),
      selected_datasets: "",
      selected_cleanser_operation_types: "",
      formData: "",
    };
  },
  methods: {
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
    getCleanserOperationTypesOptions() {
      this.$axios.get("/get_cleanser_operation_types").then((res) => {
        var cleanser_operation_types_tmp = [];
        for (let index = 0; index < res.data.data[0].length; index++) {
          cleanser_operation_types_tmp.push({
            operation: res.data.data[0][index],
          });
        }
        this.cleanser_operation_types = cleanser_operation_types_tmp;
      });
    },
    toString(dict_key) {
      var object_input = "";
      if (dict_key === "dataset") {
        object_input = this.selected_datasets;
      } else {
        object_input = this.selected_cleanser_operation_types;
      }
      var updt_list = "";
      for (let index = 0; index < object_input.length; index++) {
        var temp_elem = object_input[index][dict_key];
        if (dict_key === "dataset") {
          temp_elem = object_input[index][dict_key].split("ID: ")[1];
        }
        updt_list = updt_list.concat(temp_elem);
        updt_list = updt_list.concat(",");
      }
      return updt_list.slice(0, -1);
    },
    createCleanser() {
      this.formData = new FormData();
      this.formData.append("name", this.name);
      this.formData.append("datasets", this.toString("dataset"));
      this.formData.append("description", this.description);
      this.formData.append(
        "cleanser_operation_types",
        this.toString("operation")
      );
      this.$axios
        .post("/create_cleanser", this.formData)
        .then(() => {
          this.$toast.add({
            severity: "success",
            summary: "Cleanser Creation Successful",
            detail: "The selected Cleanser was created",
            life: 3000,
          });
          this.$emit("close");
        })
        .catch(() => {
          this.$toast.add({
            severity: "error",
            summary: "Cleanser Creation Unsuccessful",
            detail:
              "The selected Cleanser could not be created! Check if given Name is a duplicate!",
            life: 3000,
          });
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