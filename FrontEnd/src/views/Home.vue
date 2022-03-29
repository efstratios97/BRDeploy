<template>
  <main class="site-wrapper">
    <div class="pt-table desktop-768">
      <div class="pt-tablecell page-home relative">
        <div class="overlay"></div>
        <div class="container">
          <div class="row">
            <div
              class="
                col-xs-12 col-md-offset-1 col-md-10 col-lg-offset-2 col-lg-8
              "
            >
              <div class="page-title home text-center">
                <span class="heading-page">
                  <span class="heading-page" style="color: #0c8cd3">BR</span>
                  Enterprise Architecture Manager
                </span>
              </div>
            </div>
          </div>
          <nav>
            <input checked="checked" class="speed-dial" type="checkbox" />
            <label for="speed-dial"></label>
            <ul v-if="admin === 'true'">
              <li class="speed-dial-item">
                <router-link to="/usermanager" class="speed-dial-item-link">
                  <i><b-icon-person-workspace /></i>
                  <p>UserManager</p>
                </router-link>
              </li>
              <li class="speed-dial-item">
                <router-link to="/datamanager" class="speed-dial-item-link">
                  <i><b-icon-file-earmark-diff-fill /></i>
                  <p>DataManager</p>
                </router-link>
              </li>
              <li class="speed-dial-item">
                <router-link to="/cleanser" class="speed-dial-item-link">
                  <i><b-icon-gear-fill /></i>
                  <p>DataCleanser</p>
                </router-link>
              </li>
              <li class="speed-dial-item">
                <router-link to="/dataanalyzer" class="speed-dial-item-link">
                  <i><b-icon-graph-up /></i>
                  <p>DataAnalyzer</p>
                </router-link>
              </li>
              <li class="speed-dial-item">
                <router-link
                  to="/datahealthmanager"
                  class="speed-dial-item-link"
                >
                  <i> <b-icon-activity /></i>
                  <p>DataHealth</p>
                </router-link>
              </li>
              <li class="speed-dial-item">
                <router-link to="/kpimanager" class="speed-dial-item-link">
                  <i> <b-icon-speedometer /></i>
                  <p>KPIManager</p>
                </router-link>
              </li>
              <li class="speed-dial-item">
                <router-link
                  to="/executivedashboardmanager"
                  class="speed-dial-item-link"
                >
                  <i> <b-icon-sliders /></i>
                  <p>DashboardManager</p>
                </router-link>
              </li>
              <li class="speed-dial-item">
                <router-link
                  to="/executivedashboard"
                  class="speed-dial-item-link"
                >
                  <i> <b-icon-window-sidebar /> </i>
                  <p>MyDashboards</p>
                </router-link>
              </li>
            </ul>
            <ul v-else>
              <li class="speed-dial-item">
                <router-link
                  to="/executivedashboard"
                  class="speed-dial-item-link"
                >
                  <i> <b-icon-window-sidebar /> </i>
                  <p>MyDashboards</p>
                </router-link>
              </li>
            </ul>
          </nav>
        </div>
      </div>
    </div>
    <footer>
      <p>
        Created by LTEP Technologies. Copyright {{ new Date().getFullYear() }} ©
        <a target="_blank" href="http://ltep-technologies.com/">More </a>.
      </p>
    </footer>
  </main>
</template>

<script>
// @ is an alias to /src

export default {
  data() {
    this.autenticateSession();
    return {
      admin: localStorage.admin,
      items: [
        {
          label: "Delete",
          icon: "pi pi-trash",
          command: () => {
            this.deleteUser(this.selected_user.user_id);
          },
        },
        {
          label: "Update",
          icon: "pi pi-refresh",
          command: () => {
            this.updateUser(this.selected_user);
          },
        },
      ],
    };
  },
  methods: {
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
@import url("https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css");
body {
  font-family: "Libre Baskerville", serif;
  font-weight: 400;
  font-size: 16px;
  line-height: 30px;
  background-color: #07090c;
  color: #ababab;
}

.heading-page {
  text-transform: uppercase;
  font-size: 43px;
  font-weight: bolder;
  letter-spacing: 3px;
  color: white;
  text-align: center;
}

.pt-table {
  display: table;
  width: 100%;
  height: -webkit-calc(100vh - 4px);
  height: -moz-calc(100vh - 4px);
  height: calc(100vh - 4px);
}

.pt-tablecell {
  display: table-cell;
  vertical-align: middle;
}

.overlay {
  position: absolute;
  left: 0;
  top: 0;
  width: 100%;
  height: 100%;
  overflow-y: auto;
  overflow-x: hidden;
}

.relative {
  position: relative;
}

.text-center {
  margin-left: auto;
}

p {
  top: 0;
  font-size: 12px;
  height: 5px;
  display: none;
  font: bolder;
}

/*------------------------------------------------
	Start Styling
-------------------------------------------------*/
.page-title {
  margin-bottom: 675px;
}

/*------------------------------------------------
    Home Page
-------------------------------------------------*/

.page-home {
  background-image: url(~@/assets/HOME_BACKGROUND.jpg);
  background-position: center;
  background-size: cover;
  /* background-position: center center; */
  background-repeat: no-repeat;
  background-size: cover;
  vertical-align: middle;
  background-attachment: fixed;
}
.page-home .overlay {
  background-color: rgba(7, 8, 10, 0.712);
}

footer {
  background-color: #222;
  color: #fff;
  font-size: 14px;
  bottom: 0;
  position: fixed;
  left: 0;
  right: 0;
  text-align: center;
  z-index: 999;
}
.speed-dial {
  position: absolute;
  display: block;
  top: 0;
  bottom: 0;
  right: 0;
  left: 0;
  margin: auto;
  width: 80px;
  height: 80px;
  z-index: 2;
  opacity: 0;
  cursor: pointer;
}
.speed-dial:hover + label,
.speed-dial:hover + label:before,
.speed-dial:hover + label:after {
  background: white;
}
.speed-dial:checked + label {
  background: transparent;
}
.speed-dial:checked + label:before,
.speed-dial:checked + label:after {
  top: 0;
  width: 80px;
  transform-origin: 50% 70%;
}
.speed-dial:checked + label:before {
  transform: rotate(45deg) translateY(-15px) translateX(-15px);
}
.speed-dial:checked + label:after {
  transform: rotate(-45deg);
}
.speed-dial:checked ~ ul .speed-dial-item {
  opacity: 1;
}
.speed-dial:checked ~ ul .speed-dial-item:nth-child(1) {
  transform: rotate(0deg) translate(-170px);
}
.speed-dial:checked ~ ul .speed-dial-item:nth-child(2) {
  transform: rotate(45deg) translateX(-170px);
}
.speed-dial:checked ~ ul .speed-dial-item:nth-child(3) {
  transform: rotate(90deg) translateX(-170px);
}
.speed-dial:checked ~ ul .speed-dial-item:nth-child(4) {
  transform: rotate(135deg) translateX(-170px);
}
.speed-dial:checked ~ ul .speed-dial-item:nth-child(5) {
  transform: rotate(180deg) translateX(-170px);
}
.speed-dial:checked ~ ul .speed-dial-item:nth-child(6) {
  transform: rotate(225deg) translateX(-170px);
}
.speed-dial:checked ~ ul .speed-dial-item:nth-child(7) {
  transform: rotate(270deg) translateX(-170px);
}
.speed-dial:checked ~ ul .speed-dial-item:nth-child(8) {
  transform: rotate(315deg) translateX(-170px);
}
.speed-dial:checked ~ ul .speed-dial-item a {
  pointer-events: auto;
}
.speed-dial + label {
  width: 80px;
  height: 10px;
  display: block;
  z-index: 1;
  border-radius: 2.5px;
  background: rgba(239, 240, 241, 0.9);
  transition: transform 0.5s top 0.5s;
  position: absolute;
  display: block;
  top: 0;
  bottom: 0;
  left: 0;
  right: 0;
  margin: auto;
}
.speed-dial + label:before,
.speed-dial + label:after {
  width: 80px;
  height: 10px;
  display: block;
  z-index: 1;
  border-radius: 2.5px;
  background: rgba(255, 255, 255, 0.7);
  transition: transform 0.5s top 0.5s;
  content: "";
  position: absolute;
  display: block;
  left: 0;
}
.speed-dial + label:before {
  top: 20px;
}
.speed-dial + label:after {
  top: -20px;
}
.speed-dial-item:nth-child(1) .speed-dial-item-link {
  transform: rotate(0deg);
}
.speed-dial-item:nth-child(2) .speed-dial-item-link {
  transform: rotate(-45deg);
}
.speed-dial-item:nth-child(3) .speed-dial-item-link {
  transform: rotate(-90deg);
}
.speed-dial-item:nth-child(4) .speed-dial-item-link {
  transform: rotate(-135deg);
}
.speed-dial-item:nth-child(5) .speed-dial-item-link {
  transform: rotate(180deg);
}
.speed-dial-item:nth-child(6) .speed-dial-item-link {
  transform: rotate(137deg);
}
.speed-dial-item:nth-child(7) .speed-dial-item-link {
  transform: rotate(90deg);
}
.speed-dial-item:nth-child(8) .speed-dial-item-link {
  transform: rotate(45deg);
}
.speed-dial-item {
  position: absolute;
  display: block;
  top: 0;
  bottom: 0;
  left: 0;
  right: 0;
  margin: auto;
  width: 80px;
  height: 0px;
  opacity: 0;
  transition: 0.5s;
}
.speed-dial-item a {
  display: block;
  width: 110px;
  height: 110px;
  line-height: 80px;
  color: rgba(255, 255, 255, 0.7);
  background: rgba(230, 230, 250, 0.726);
  border-radius: 50%;
  text-align: center;
  text-decoration: none;
  font-size: 40px;
  pointer-events: none;
  transition: 0.2s;
}
.speed-dial-item a:hover {
  box-shadow: 0 0 0 2px rgba(255, 255, 255, 0.3);
  color: white;
  background: rgba(255, 255, 255, 0.3);
  font-size: 44.44px;
}
.speed-dial-item a:hover i {
  display: none;
}
.speed-dial-item a:hover p {
  display: block;
  overflow-wrap: break-word;
  white-space: pre-wrap;
  word-wrap: break-word;
}
</style>
