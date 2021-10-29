<template>
  <div>
    <form>
      <div class="p-field p-grid">
        <div class="p-col-12">
          <label for="old_pw">
            <b-icon-person-fill /> Please select User to change
            Department</label
          >
        </div>
        <div class="p-col-12">
          <Dropdown
            v-model="selected_user"
            :options="users"
            optionLabel="user"
            placeholder="Select a User"
            :filter="true"
            filterPlaceholder="Find a User"
            :showClear="true"
          />
        </div>
        <div class="p-col-12">
          <br />
          <label for="new_pw1"
            ><b-icon-building /> Please select the new Department</label
          >
        </div>
        <div class="p-col-12">
          <Dropdown
            v-model="selected_dep"
            :options="departments"
            optionLabel="dep"
            placeholder="Select a Department"
            :filter="true"
            filterPlaceholder="Find a Department"
            :showClear="true"
          />
        </div>
      </div>
      <Button
        label="Submit"
        icon="pi pi-check"
        iconPos="right"
        @click="updateDepartment"
      />
    </form>
  </div>
</template>
<script>
export default {
  data() {
    return {
      selected_user: "",
      selected_dep: "",
      users_complete: "",
      users: this.listUsers(),
      departments: this.listDepartments(),
    };
  },
  methods: {
    listUsers() {
      this.$axios.get("/users").then((res) => {
        var users_tmp = [];
        this.users_complete = res.data;
        for (let index = 0; index < res.data.length; index++) {
          users_tmp.push({
            user: res.data[index]["email"],
          });
        }
        this.users = users_tmp;
      });
    },
    listDepartments() {
      this.$axios.get("/departments").then((res) => {
        var dep_tmp = [];
        for (let index = 0; index < res.data.length; index++) {
          dep_tmp.push({
            dep: res.data[index]["name"],
          });
        }
        this.departments = dep_tmp;
      });
    },
    updateDepartment() {
      for (let index = 0; index < this.users_complete.length; index++) {
        if (this.users_complete[index]["email"] === this.selected_user.user) {
          this.selected_user.user = this.users_complete[index]["user_id"];
        }
      }
      this.$axios
        .post(
          "/update_department/" +
            this.selected_dep.dep +
            "/" +
            this.selected_user.user
        )
        .then(() => {
          this.$toast.add({
            severity: "success",
            summary: "Successfully updated User's Department",
            detail: "You successfully updated User's Department",
            life: 3000,
          });
          this.$emit("close");
        })
        .catch(() => {
          this.$toast.add({
            severity: "error",
            summary: "Update of User's Department was unsuccessful",
            detail:
              "You could not successfully update the User's Department! Check if you have admin rights!",
            life: 3000,
          });
        });
    },
  },
};
</script>
<style scoped>
.p-password input {
  width: 15rem;
}
</style>