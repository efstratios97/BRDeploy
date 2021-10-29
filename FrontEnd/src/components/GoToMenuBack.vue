<template>
  <Menubar :model="items">
    <template #start>
      <router-link to="/mainmenu">
        <img alt="logo"
        src="https://upload.wikimedia.org/wikipedia/commons/thumb/9/98/BR_Dachmarke.svg/2000px-BR_Dachmarke.svg.png"
        height="40" class="p-mr-2" to=/mainmenu />
      </router-link>
    </template>
    <template #end>
      <div class="container p-menubar">
        <div class="row">
          <div class="col">
            <p class="p-menuitem-text" style="white-space: nowrap">
              Hello {{ user }}
            </p>
          </div>
          <div class="col">
            <Button
              icon="pi pi-fw pi-power-off"
              class="p-button-rounded p-button-secondary"
              @click="logout"
            />
          </div>
        </div>
      </div>
    </template>
  </Menubar>
</template>
<script>
export default {
  data() {
    return {
      user: this.enumUser(),
      items: [
        {
          label: "UserManager",
          icon: "pi pi-users",
          to: "/usermanager",
        },
        {
          label: "DataManager",
          icon: "pi pi-file",
          to: "/datamanager",
        },
        {
          label: "DataCleanser",
          icon: "pi pi-cog",
          to: "/cleanser",
        },
        {
          label: "DataAnalyzer",
          icon: "pi pi-chart-bar",
          to: "/dataanalyzer",
        },
        {
          label: "DataHealth",
          icon: "pi pi-compass",
          to: "/datahealthmanager",
        },
      ],
    };
  },
  methods: {
    enumUser() {
      this.$axios.get("/users").then((res) => {
        this.allUsers = res.data;
        for (let i = 0; i < this.allUsers.length; i++) {
          if (this.allUsers[i]["user_id"] === localStorage.loggedUser) {
            this.user = this.allUsers[i]["first_name"];
            return;
          } else {
            this.user = false;
          }
        }
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
<style >
.p-menubar {
  background-color: white;
}
.p-menuitem-icon {
  font-size: 18px !important;
}
.p-menuitem-text {
  font-size: 18px !important;
}
</style>