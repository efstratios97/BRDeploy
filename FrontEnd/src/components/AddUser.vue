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
            v-model="firstName"
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
            v-model="lastName"
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
            v-model="selectedDepartment"
            :options="departments"
            :filter="true"
            optionLabel="dep.name"
            placeholder="Assign Department"
            filterPlaceholder="Find an Department"
            class="multiselect-custom"
            :showClear="true"
          />
        </div>
      </div>
    </div>

    <div class="p-grid p-fluid">
      <div class="col-4 col-offset-1">
        <i class="pi pi-id-card p-checkbox-icon"></i>
        <label>Admin</label>
      </div>
      <div class="p-field-checkbox">
        <Checkbox v-model="admin" :binary="true" />
      </div>
    </div>

    <div class="p-grid p-fluid">
      <div class="col-4 col-offset-1">
        <i class="pi pi-eye p-checkbox-icon"></i>
        <label>Role Manager</label>
      </div>
      <div class="p-field-checkbox">
        <Checkbox v-model="roleManager" :binary="true" />
      </div>
    </div>

    <div class="p-grid p-fluid">
      <div class="p-col-12 p-md-12">
        <Button
          label="Create User"
          icon="pi pi-user-plus"
          iconPos="center"
          @click="createUser"
        />
      </div>
    </div>
  </form>
</template>

<script>
export default {
  data() {
    return {
      selectedDepartment: "Select Department",
      first_name: "",
      last_name: "",
      business_unit: "",
      email: "",
      password: "12345",
      access_rights_pillars: "{'UserManager':1, 'DataManager':1}",
      admin: 0,
      roleManager: 0,
      user: {},
      departments: this.getDepartmentsOptions(),
      users: this.listUsers(),
    };
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
    createUser() {
      for (let index = 0; index < this.users.length; index++) {
        if (this.email === this.users[index].email) {
          this.$toast.add({
            severity: "error",
            summary: "Email already exists",
            detail: "The provided Email: " + this.email + " already exists",
            life: 3000,
          });
          return;
        }
        this.user = {
          first_name: this.firstName,
          last_name: this.lastName,
          business_unit: this.selectedDepartment.dep.name,
          email: this.email,
          password: "12345",
          access_rights_pillars: "{'UserManager':1, 'DataManager':1}",
          admin: this.admin === true ? 1 : 0,
          role_manager: this.roleManager === true ? 1 : 0,
        };
        const jsonString = JSON.stringify(this.user);
        this.$axios
          .post("/create_user/" + localStorage.loggedUser, jsonString)
          .then(() => {
            this.$toast.add({
              severity: "success",
              summary: "User Creation Successful",
              detail:
                "The User: " +
                this.firstName +
                " " +
                this.lastName +
                " was created",
              life: 3000,
            });
            this.$emit("close");
            return;
          });
      }
    },
  },
};
</script>
