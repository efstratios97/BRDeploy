<template>
  <div>
    <form>
      <div class="p-field p-grid">
        <div class="p-col-12">
          <label for="old_pw">Please Enter your current Password</label>
        </div>
        <div class="p-col-12">
          <Password v-model="old_password" :feedback="false">
            <template #header>
              <h6>Enter your current Password</h6>
            </template>
          </Password>
        </div>
        <div class="p-col-12">
          <label for="new_pw1">Please Enter your new Password</label>
        </div>
        <div class="p-col-12">
          <Password v-model="new_password_1">
            <template #header>
              <h6>Enter your new Password</h6>
            </template>
            <template #footer>
              <Divider />
              <p class="p-mt-2">Suggestions</p>
              <ul class="p-pl-2 p-ml-2 p-mt-0" style="line-height: 1.5">
                <li>At least one lowercase</li>
                <li>At least one uppercase</li>
                <li>At least one numeric</li>
                <li>Minimum 8 characters</li>
              </ul>
            </template>
          </Password>
        </div>
        <div class="p-col-12">
          <label for="new_pw2">Please Re-enter your new Password</label>
        </div>
        <div class="p-col-12">
          <Password v-model="new_password_2" :feedback="false">
            <template #header>
              <h6>Repeat your new Password</h6>
            </template>
          </Password>
        </div>
      </div>
      <Button
        label="Submit"
        icon="pi pi-check"
        iconPos="right"
        @click="updatePassword"
      />
    </form>
  </div>
</template>
<script>
export default {
  data() {
    return {
      email: this.getUserMail(),
      old_password: "",
      new_password_1: "",
      new_password_2: "",
    };
  },
  methods: {
    getUserMail() {
      this.$axios.get("/user/" + localStorage.loggedUser).then((res) => {
        this.email = res.data.email;
      });
    },
    updatePassword() {
      this.$axios
        .get("/user/auth?email=" + this.email + "&passwd=" + this.old_password)
        .then(() => {
          if (this.new_password_2 === this.new_password_1) {
            this.$axios;
            var password = {
              old_password: this.old_password,
              new_password: this.new_password_1,
            };
            const jsonString = JSON.stringify(password);
            this.$axios
              .post("/change_password/" + localStorage.loggedUser, jsonString)
              .then(() => {
                this.$toast.add({
                  severity: "success",
                  summary: "Successfully updated Password",
                  detail: "You successfully updated your password",
                  life: 3000,
                });
              });
            this.$emit("close");
          } else {
            this.$toast.add({
              severity: "error",
              summary: "No Password Matching",
              detail: "The entered passwords do not match",
              life: 3000,
            });
          }
        })
        .catch(() => {
          this.$toast.add({
            severity: "error",
            summary: "Wrong Password",
            detail: "The entered password is wrong",
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