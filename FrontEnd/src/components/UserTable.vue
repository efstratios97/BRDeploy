<template>
  <DataTable
    :value="users"
    v-model:selection="selected_user"
    dataKey="user_id"
    :paginator="true"
    :rows="10"
    filterDisplay="menu"
    paginatorTemplate="FirstPageLink PrevPageLink PageLinks NextPageLink LastPageLink CurrentPageReport RowsPerPageDropdown"
    :rowsPerPageOptions="[10, 25, 50]"
    currentPageReportTemplate="Showing {first} to {last} of {totalRecords} entries"
    responsiveLayout="scroll"
  >
    <template #header>
      <div class="p-d-flex p-jc-between p-ai-center">
        <h5 class="p-m-0">Users</h5>
        <span class="p-input-icon-left">
          <i class="pi pi-search" />
          <InputText placeholder="Keyword Search" />
        </span>
      </div>
    </template>
    <template #empty>
      Loading Users. Please wait. <ProgressBar mode="indeterminate" />
    </template>
    <template #loading> Loading Users. Please wait. </template>
    <Column selectionMode="single" headerStyle="width: 3em"></Column>
    <Column field="user_id" header="ID" sortable style="min-width: auto">
    </Column>
    <Column
      field="first_name"
      header="First Name"
      sortable
      style="min-width: auto"
    >
    </Column>
    <Column
      field="last_name"
      header="Last Name"
      sortable
      style="min-width: auto"
    >
    </Column>
    <Column field="email" header="Email" sortable style="min-width: auto">
    </Column>
    <Column
      field="business_unit"
      header="Department"
      sortable
      style="min-width: auto"
    >
    </Column>
    <Column
      field="role_manager"
      header="Role Manager"
      sortable
      style="min-width: auto"
    >
    </Column>
    <Column field="admin" header="Admin" sortable style="min-width: auto">
    </Column>
    <Column header="Ad hoc Operations" style="min-width: auto">
      <template #body>
        <div class="btn-align-td">
          <button
            v-on:click="deleteUser(this.selected_user.user_id)"
            class="btn btn-secondary"
            v-tooltip="'Select User first'"
          >
            <b-icon-trash-fill />
          </button>
        </div>
        <ProgressBar mode="indeterminate" v-if="user_operations" /> </template
    ></Column>
  </DataTable>
</template>
 
<script>
export default {
  data() {
    return {
      users: this.listUsers(),
      selected_user: "",
      user_operations: false,
    };
  },
  methods: {
    deleteUser(user_id) {
      if (user_id === undefined) {
        this.$toast.add({
          severity: "warn",
          summary: "No User selected",
          detail: "Please select User first",
          life: 3000,
        });
      } else {
        this.user_operations = true;
        this.$toast.add({
          severity: "info",
          summary: "User is being deleted",
          detail: "This may take a few minutes depending on User's datasets",
          life: 8000,
        });
      }
      const issued_user = localStorage.loggedUser;
      this.$axios
        .delete("/delete_user/" + user_id + "/" + issued_user)
        .then(() => {
          this.listUsers();
          if (user_id === issued_user) {
            this.logout();
          }
          if (this.user_operations === true) {
            this.$toast.add({
              severity: "success",
              summary: "User Deletion Successful",
              detail: "The selected User: " + user_id + " was deleted",
              life: 3000,
            });
          }
          this.user_operations = false;
          this.selected_user = "";
        })
        .catch(() => {
          if (user_id === issued_user && Object.keys(this.users).length !== 1) {
            this.logout();
          }
          this.user_operations = false;
          this.user_operations = false;
          this.selected_user = "";
          this.listUsers();
          this.checkSuccessDeletion(user_id);
        });
    },
    checkSuccessDeletion(user_id) {
      if (user_id !== undefined && Object.keys(this.users).length !== 1) {
        this.$toast.add({
          severity: "success",
          summary: "User Deletion Successful",
          detail: "The selected User: " + user_id + " was deleted",
          life: 3000,
        });
        this.user_operations = false;
        this.selected_user = "";
      } else {
        this.$toast.add({
          severity: "error",
          summary: "User Deletion Unsuccessful",
          detail:
            "The selected User: " +
            user_id +
            " could not be deleted!\n Check if you have admin rights",
          life: 3000,
        });
      }
    },
    listUsers() {
      this.$axios.get("/users").then((res) => {
        this.users = res.data;
      });
    },
    logout() {
      delete localStorage.loggedUser;
      delete localStorage.token;
      this.autenticateSession();
      this.$toast.add({
        severity: "success",
        summary: "Log Out",
        detail: "You have successfully logged out",
        life: 3000,
      });
    },
    autenticateSession() {
      if (localStorage.loggedUser && localStorage.token) {
        this.$axios
          .get("/user/validatetoken?token=" + localStorage.token)
          .then(() => {
            this.selected_user = localStorage.loggedUser;
            this.$axios.get("/user/" + this.selected_user).then((res) => {
              this.$store.state.loggedUser = res.data;
            });
          })
          .catch(() => {
            this.$router.push("/");
          });
      } else {
        this.$router.push("/");
      }
    },
  },
};
</script>
<style>
button {
  color: white;
  background: #0c8cd3;
  border: 0px solid blue;
  border-radius: 2px;
}
</style>