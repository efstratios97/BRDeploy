<template>
  <div>
    <Button
      label="Submit"
      icon="pi pi-check"
      iconPos="right"
      @click="getUser"
    />
    <Card>
      <template v-slot:title> Hello {{ this.user.first_name }}</template>
      <template v-slot:subtitle>
        Here you can see and manage your profile
      </template>
      <template v-slot:content>
        <div class="p-field p-grid">
          <label for="firstname" class="p-col-fixed" style="width: 100px"
            >Firstname:
          </label>
          <div class="p-col">
            {{ this.user.first_name }}
          </div>
        </div>
        <div class="p-field p-grid">
          <label for="lastname" class="p-col-fixed" style="width: 100px"
            >Lastname:
          </label>
          <div class="p-col">
            {{ this.user.last_name }}
          </div>
        </div>
        <div class="p-field p-grid">
          <label for="lastname" class="p-col-fixed" style="width: 100px"
            >Email:
          </label>
          <div class="p-col">
            {{ this.user.email }}
          </div>
        </div>
        <div class="p-field p-grid">
          <label for="department" class="p-col-fixed" style="width: 100px"
            >Department:
          </label>
          <div class="p-col">
            {{ this.user.business_unit }}
          </div>
        </div>
        <div class="p-field p-grid">
          <label for="rights" class="p-col-fixed" style="width: 100px"
            >Rights:
          </label>
          <div class="p-col">
            {{ this.enumAdmin() }}
          </div>
        </div>
        <div class="p-field p-grid">
          <label for="password" class="p-col-fixed" style="width: 100px"
            >Change Password:
          </label>
          <Password v-model="password" toggleMask></Password>
        </div>
      </template>
    </Card>
  </div>
</template>
<script>
export default {
  data() {
    return {
      selected_user: "",
      password: "",
      showUser: false,
      user: this.getUser(),
    };
  },
  methods: {
    deleteUser(userid) {
      const issued_user = localStorage.loggedUser;
      this.$axios
        .delete("/delete_user/" + userid + "/" + issued_user)
        .then(() => {
          //   this.logout();
        });
    },

    enumAdmin() {
      if (this.user.admin === 0) {
        return "No Admin Rights";
      } else {
        return "Admin Rights";
      }
    },
    getUser() {
      this.$axios.get("/user/" + localStorage.loggedUser).then((res) => {
        return res.data;
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