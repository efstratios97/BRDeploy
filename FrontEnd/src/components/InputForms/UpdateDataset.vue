<template>
  <div>
    <form>
      <div class="p-grid p-fluid">
        <div class="p-col-12 p-md-12">
          <div class="p-inputgroup">
            <span class="p-inputgroup-addon">
              <i class="pi pi-file"></i>
            </span>
            <InputText
              placeholder="Dataset's Name"
              v-model="name"
              class="inputfield w-full"
            />
          </div>
        </div>
      </div>

      <div class="p-grid p-fluid">
        <div class="p-col-12 p-md-12">
          <Textarea
            placeholder="Dataset Description"
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
              <i class="pi pi-users"></i>
            </span>
            <MultiSelect
              v-model="selected_users"
              :options="users"
              :filter="true"
              optionLabel="user.email"
              placeholder="Assign Users with Access (Optional)"
              filterPlaceholder="Find Users"
              class="multiselect-custom"
            />
          </div>
        </div>
      </div>
      <div class="p-grid p-fluid">
        <div class="p-col-12 p-md-12">
          <div class="p-inputgroup">
            <span class="p-inputgroup-addon">
              <b-icon-building />
            </span>
            <MultiSelect
              v-model="selected_departments"
              :options="departments"
              :filter="true"
              optionLabel="dep.name"
              placeholder="Assign Departments with Access (Optional)"
              filterPlaceholder="Find Departments"
              class="multiselect-custom"
              :showClear="true"
            />
          </div>
        </div>
      </div>

      <div class="p-grid p-align-center">
        <div class="p-col-6 p-md-6">
          <div class="p-inputgroup">
            <span class="p-inputgroup-addon">
              <i class="pi pi-filter-fill"></i>
              Cleaned:
            </span>
          </div>
        </div>
        <div class="p-col-6 p-md-6">
          <InputSwitch v-model="cleaned" />
        </div>
      </div>

      <div class="p-grid p-fluid">
        <div class="p-col-12 p-md-12">
          <Button
            label="Update Dataset"
            icon="pi pi-refresh"
            iconPos="center"
            @click="updateDataset"
          />
        </div>
      </div>
      <div v-if="submitted">
        <br />
        <ProgressBar mode="indeterminate" v-if="submitted" />
      </div>
    </form>
  </div>
</template>

<script>
export default {
  props: ["dataset"],
  data() {
    return {
      name: "",
      cleaned: "",
      description: "",
      selected_users: [],
      selected_departments: [],
      users: this.getUsersOptions(),
      departments: this.getDepartmentsOptions(),
      submitted: false,
    };
  },
  created() {
    this.name = this.dataset.name;
    this.cleaned = this.dataset.cleaned === 1 ? true : false;
    this.description = this.dataset.description;
    for (let index = 0; index < this.dataset.access_user_list.length; index++) {
      this.$axios
        .get("/user_by_email/" + this.dataset.access_user_list[index])
        .then((res) => {
          this.selected_users.push({ user: res.data });
        });
    }
    for (
      let index = 0;
      index < this.dataset.access_business_unit_list.length;
      index++
    ) {
      if (
        this.dataset.access_business_unit_list[index] !==
        "None Department Assigned"
      ) {
        this.$axios
          .get(
            "/department_by_name/" +
              this.dataset.access_business_unit_list[index]
          )
          .then((res) => {
            this.selected_departments.push({ dep: res.data });
          });
      }
    }
  },
  methods: {
    getUsersOptions() {
      this.$axios.get("/users").then((res) => {
        var users_tmp = [];
        for (let index = 0; index < res.data.length; index++) {
          users_tmp.push({ user: res.data[index] });
        }
        this.users = users_tmp;
      });
    },
    getDepartmentsOptions() {
      this.$axios.get("/departments").then((res) => {
        var departments_tmp = [];
        for (let index = 0; index < res.data.length; index++) {
          departments_tmp.push({ dep: res.data[index] });
        }
        this.departments = departments_tmp;
      });
    },
    updateDataset() {
      var formData = new FormData();
      formData.append("dataset_id", this.dataset.dataset_id);
      formData.append("name", this.name);
      formData.append("cleaned", this.cleaned);
      formData.append("description", this.description);
      formData.append("access_user_list", this.toString("user"));
      formData.append("access_business_unit_list", this.toString("dep"));
      this.$axios
        .post("/update_dataset?uid=" + localStorage.loggedUser, formData)
        .then(() => {
          this.$toast.add({
            severity: "success",
            summary: "Dataset Update Successful",
            detail: "The Dataset was updated",
            life: 3000,
          });
          this.submitted = true;
          this.close();
        })
        .catch(() => {
          this.$toast.add({
            severity: "error",
            summary: "Dataset Update Unsuccessful",
            detail: "The Dataset updatenwas unsuccessful",
            life: 3000,
          });
          this.submitted = false;
        });
    },
    toString(dict_key) {
      var key_word = "";
      var object_input = "";
      if (dict_key === "user") {
        key_word = "email";
        object_input = this.selected_users;
      } else if (dict_key === "dep") {
        key_word = "name";
        object_input = this.selected_departments;
      }
      var updt_list = "";
      for (let index = 0; index < object_input.length; index++) {
        updt_list = updt_list.concat(object_input[index][dict_key][key_word]);
        updt_list = updt_list.concat(",");
      }
      return updt_list.slice(0, -1);
    },
    close() {
      this.$emit("close");
    },
  },
};
</script>