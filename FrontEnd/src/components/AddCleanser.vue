<template>
  <form>
    <div class="mb-3">
      <label for="CleanserName" class="form-label">
        <b-icon-archive-fill /> Name:</label
      >
      <input
        class="input100"
        id="CleanserName"
        type="text"
        v-model="name"
        placeholder="Cleanser Name"
      />
    </div>

    <div class="mb-3">
      <label for="description" class="form-label" id="description">
        <b-icon-pencil-fill /> Description:
      </label>
      <textarea
        class="input100"
        v-model="description"
        placeholder="Description"
        id="description"
      ></textarea>
    </div>

    <div class="mb-3">
      <label> <b-icon-shield-lock-fill /> Datasets</label>
      <select v-model="selected_datasets" multiple>
        <option
          v-for="dataset in datasets"
          v-bind:value="dataset"
          :key="dataset"
        >
          {{ dataset }}
        </option>
      </select>
    </div>

    <div class="mb-3">
      <label> <b-icon-shield-lock-fill /> Cleanser Operation Types</label>
      <select v-model="selected_cleanser_operation_types" multiple>
        <option
          v-for="operations in cleanser_operation_types"
          v-bind:value="operations"
          :key="operations"
        >
          {{ operations }}
        </option>
      </select>
    </div>

    <button class="btn-form" @click="createCleanser">
      <b-icon-upload />
      <b> Add Cleanser</b>
    </button>
  </form>
</template>

<script>
export default {
  data() {
    return {
      name: "",
      cleaned: "",
      description: "",
      storageType: "",
      file: "",
      users: this.getUsersOptions(),
      departments: this.getDepartmentsOptions(),
      cleanser_operation_types: this.getCleanserOperationTypesOptions(),
      datasets: this.getDatasetOptions(),
      selected_users: "",
      selected_datasets: "",
      selected_departments: "",
      selected_cleanser_operation_types: "",
      formData: "",
    };
  },
  methods: {
    getUsersOptions() {
      this.users = this.$axios.get("/users").then((res) => {
        this.users = res.data;
      });
    },
    getDepartmentsOptions() {
      this.users = this.$axios.get("/departments").then((res) => {
        this.departments = res.data;
      });
    },
    createDataSet() {
      this.formData = new FormData();
      this.formData.append("name", this.name);
      this.formData.append("file", this.$refs.file.files[0]);
      this.formData.append("cleaned", this.cleaned);
      this.formData.append("description", this.description);
      this.formData.append(
        "storage_type",
        this.storageType === true ? "cloud" : "local"
      );
      this.formData.append("access_user_list", this.selected_users);
      this.formData.append(
        "access_business_unit_list",
        this.selected_departments
      );
      this.$axios
        .post("/create_dataset?uid=" + localStorage.loggedUser, this.formData)
        .then(() => {
          this.$emit("close");
        });
    },
    getDatasetOptions() {
      this.$axios
        .get("/get_datasets_only_id/" + localStorage.loggedUser)
        .then((res) => {
          this.datasets = res.data.data;
        });
    },
    getCleanserOperationTypesOptions() {
      this.$axios.get("/get_cleanser_operation_types").then((res) => {
        this.cleanser_operation_types = res.data.data[0];
      });
    },
    createCleanser() {
      this.formData = new FormData();
      this.formData.append("name", this.name);
      this.formData.append("datasets", this.selected_datasets);
      this.formData.append("description", this.description);
      this.formData.append(
        "cleanser_operation_types",
        this.selected_cleanser_operation_types
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