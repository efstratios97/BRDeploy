<template>
  <Menubar
    :model="items_admin"
    style="
      white-space: nowrap;
      max-width: 100vw !important;
      justify-content: space-between;
      overflow: auto;
      font-size: 17px;
    "
  >
    <template #start>
      <router-link to="/mainmenu">
        <img alt="logo" src="~@/assets/CLIENT_LOGO.png" height="40"
        class="p-mr-2" to=/mainmenu />
      </router-link>
    </template>
    <template #end>
      <div class="p-grid p-menubar">
        <div class="p-col">
          <p
            class="p-menuitem-text"
            style="white-space: nowrap; font-size: 15px"
          >
            Hello {{ user }}
          </p>
        </div>
        <div class="p-col">
          <Button
            icon="pi pi-fw pi-power-off"
            class="p-button-rounded p-button-secondary"
            @click="logout"
          />
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
      items_admin: [
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
          icon: "pi pi-qrcode",
          to: "/datahealthmanager",
        },
        {
          label: "KPIManager",
          icon: "pi pi-compass",
          to: "/kpimanager",
        },
        {
          label: "ExecutiveDashboardManager",
          icon: "pi pi-sliders-h",
          to: "/executivedashboardmanager",
        },
        {
          label: "MyExecutiveDashboard",
          icon: "pi pi-globe",
          to: "/executivedashboard",
        },
      ],
    };
  },
  methods: {
    logout() {
      delete localStorage.loggedUser;
      delete localStorage.token;
      delete localStorage.admin;
      this.autenticateSession();
      this.$toast.add({
        severity: "success",
        summary: "Log Out",
        detail: "You have successfully logged out",
        life: 3000,
      });
    },
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
<style scoped>
.p-menubar {
  background-color: white;
}
.p-menuitem-icon {
  font-size: 18px;
}
.p-menuitem-text {
  font-size: 18px;
}
.p-grid {
  margin: 0px;
}
.p-col {
  margin: 0px;
}
</style>