<template>
  <form>
    <div class="p-grid p-fluid">
      <div class="p-col-12 p-md-12">
        <div class="p-inputgroup">
          <span class="p-inputgroup-addon">
            <i class="pi pi-user"></i>
          </span>
          <InputText
            placeholder="First Name"
            v-model="first_name"
            class="inputfield w-full"
          />
        </div>
      </div>
    </div>

    <div class="p-grid p-fluid">
      <div class="p-col-12 p-md-12">
        <div class="p-inputgroup">
          <span class="p-inputgroup-addon">
            <i class="pi pi-user"></i>
          </span>
          <InputText
            placeholder="Last Name"
            v-model="last_name"
            class="inputfield w-full"
          />
        </div>
      </div>
    </div>

    <div class="p-grid p-fluid">
      <div class="p-col-12 p-md-12">
        <div class="p-inputgroup">
          <span class="p-inputgroup-addon">
            <i class="pi pi-envelope"></i>
          </span>
          <InputText placeholder="E-mail" v-model="email" />
        </div>
      </div>
    </div>

    <div class="p-grid p-fluid">
      <div class="p-col-12 p-md-12">
        <div class="p-inputgroup">
          <span class="p-inputgroup-addon">
            <b-icon-building />
          </span>
          <Dropdown
            v-model="selected_department"
            :options="departments"
            :filter="true"
            optionLabel="dep.name"
            :placeholder="placeholder"
            filterPlaceholder="Find an Department"
          />
        </div>
      </div>
    </div>

    <div class="p-grid p-align-center">
      <div class="p-col-6 p-md-6">
        <div class="p-inputgroup">
          <span class="p-inputgroup-addon">
            <i class="pi pi-shield"></i>
            Admin:
          </span>
        </div>
      </div>
      <div class="p-col-6 p-md-6">
        <InputSwitch v-model="admin" />
      </div>
    </div>

    <div class="p-grid p-fluid">
      <div class="p-col-12 p-md-12">
        <Button
          label="Update User"
          icon="pi pi-user-plus"
          iconPos="center"
          @click="updateUser"
        />
      </div>
    </div>
  </form>
</template>

<script>
export default {
  props: ["user"],
  data() {
    return {
      selected_department: "",
      placeholder: "",
      first_name: "",
      last_name: "",
      email: "",
      access_rights_pillars: "{'UserManager':1, 'DataManager':1}",
      admin: "",
      roleManager: "",
      departments: this.getDepartmentsOptions(),
      users: this.listUsers(),
    };
  },
  created() {
    this.first_name = this.user.first_name;
    this.last_name = this.user.last_name;
    this.selected_department = [];
    this.placeholder = this.user.business_unit;
    this.$axios
      .get("/department_by_name/" + this.user.business_unit)
      .then((res) => {
        this.selected_department.push({ dep: res.data });
      });
    this.email = this.user.email;
    this.admin = this.user.admin === "1" ? true : false;
  },
  methods: {
    listUsers() {
      this.$axios.get("/users").then((res) => {
        this.users = res.data;
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
    updateUser() {
      if (this.selected_department.dep === undefined) {
        this.selected_department = this.selected_department[0];
      }
      var formData = new FormData();
      formData.append("user_id", this.user.user_id);
      formData.append("first_name", this.first_name);
      formData.append("last_name", this.last_name);
      formData.append("admin", this.admin);
      formData.append("email", this.email);
      formData.append("business_unit", this.selected_department.dep.name);
      this.$axios.post("/update_user", formData).then(() => {
        this.$toast.add({
          severity: "success",
          summary: "User Update Successful",
          detail:
            "The User: " +
            this.first_name +
            " " +
            this.last_name +
            " was updated",
          life: 3000,
        });
        this.$emit("close");
        return;
      });
    },
  },
};
</script>
