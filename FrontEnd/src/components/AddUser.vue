<template>
  <form>
    <div class="mb-3">
      <label for="firstName" class="form-label">
        <b-icon-person-fill /> First Name:</label
      >
      <input
        class="input100"
        id="firstName"
        type="text"
        v-model="firstName"
        placeholder="First Name"
      />
    </div>

    <div class="mb-3">
      <label for="lastName" class="form-label" id="lastName">
        <b-icon-person-fill /> Last Name:
      </label>
      <input
        class="input100"
        v-model="lastName"
        placeholder="Last Name"
        id="lastName"
      />
    </div>

    <div class="mb-3">
      <label for="email" class="form-label" id="email">
        <b-icon-envelope-open-fill /> Email:
      </label>
      <input class="input100" v-model="email" placeholder="Email" id="email" />
    </div>

    <div class="mb-3">
      <label for="admin"> <b-icon-shield-lock-fill /> Admin</label>
      <input class="input200" type="checkbox" v-model="admin" id="admin" />
    </div>

    <div class="mb-3">
      <label for="rolemanager">
        <b-icon-check-circle-fill /> Role Manager
      </label>
      <input
        class="input200"
        type="checkbox"
        v-model="roleManager"
        id="rolemanager"
      />
    </div>

    <div class="mb-3">
      <label> <b-icon-building /> Department</label>
      <select v-model="selectedDepartment">
        <option
          v-for="department in departments"
          v-bind:value="department.name"
          :key="department.name"
        >
          {{ department.name }}
        </option>
      </select>
    </div>

    <button class="btn-form" @click="createUser">
      <b-icon-upload />
      <b>Create User</b>
    </button>
  </form>
</template>

<script>
export default {
  data() {
    return {
      first_name: "",
      last_name: "",
      business_unit: "",
      email: "",
      password: "12345",
      access_rights_pillars: "{'UserManager':1, 'DataManager':1}",
      admin: 0,
      role_manager: 0,
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
        this.departments = res.data;
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
          business_unit: this.selectedDepartment,
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
          })
          .catch(() => {
            this.$toast.add({
              severity: "error",
              summary: "User Creation Unsuccessful",
              detail:
                "The User: " +
                this.firstName +
                " " +
                this.lastName +
                " could not be created!\nIf you have no Admin rights you cannot create a new User",
              life: 3000,
            });
            return;
          });
      }
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