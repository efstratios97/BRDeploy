 <template>
  <div v-if="admin === 'true'">
    <div class="banner-head banner-image p-shadow-14"></div>
    <div class="page-background">
      <div class="container-xxl main-page p-shadow-14">
        <h1 style="text-align: left; font-size: 38px">User Manager</h1>
        <br />
        <br />
        <TabView class="tabview-custom" ref="tabview4">
          <TabPanel
            ><template #header>
              <i class="pi pi-users" style="font-size: 18px; margin: 3px"></i>
              <span><h4>Users</h4></span>
            </template>
            <Card class="component-card">
              <template v-slot:title> Users </template>
              <template v-slot:subtitle> Manager here your Users </template>
              <template v-slot:content>
                <user-table
                  :key="componentKey"
                  @update="updateUser($event)"
                ></user-table>
              </template>
            </Card>
          </TabPanel>
          <TabPanel
            ><template #header>
              <i
                class="pi pi-briefcase"
                style="font-size: 18px; margin: 3px"
              ></i>
              <span><h4>Departments</h4></span>
            </template>
            <div class="container-sm justify-content-start">
              <div class="row justify-content-start">
                <div class="col">
                  <Card class="component-card">
                    <template v-slot:title> Departments </template>
                    <template v-slot:subtitle>
                      Manager here your Departments
                    </template>
                    <template v-slot:content>
                      <dep-table :key="componentKey"></dep-table>
                    </template>
                  </Card>
                </div>
              </div>
            </div>
          </TabPanel>
          <TabPanel
            ><template #header>
              <i class="pi pi-cog" style="font-size: 18px; margin: 3px"></i>
              <span><h4>UserManager Operation</h4></span>
            </template>
            <Card class="component-card">
              <template v-slot:content>
                <Carousel
                  :value="operationsItems"
                  :numVisible="1"
                  :numScroll="1"
                  :responsiveOptions="responsiveOptions"
                >
                  <template #header>
                    <h1 style="text-align: center">Available Operations</h1>
                  </template>
                  <template #item="slotProps">
                    <div class="operation-item">
                      <div class="operation-item-content">
                        <div class="p-mb-3">
                          <span style="text-align: center">
                            <span v-html="slotProps.data.operation_img"></span
                          ></span>
                        </div>
                        <h4>{{ slotProps.data.operation_desc }}</h4>
                        <div
                          v-html="slotProps.data.operation_button"
                          @click.capture="toggleShowAddUser"
                          v-if="slotProps.data.operation === 'add_user'"
                        ></div>
                        <div
                          v-html="slotProps.data.operation_button"
                          @click.capture="toggleShowAddDep"
                          v-if="slotProps.data.operation === 'add_dep'"
                        ></div>
                        <div
                          v-html="slotProps.data.operation_button"
                          @click.capture="toggleShowUpdateDepartment"
                          v-if="slotProps.data.operation === 'update_dep'"
                        ></div>
                      </div>
                    </div>
                  </template>
                </Carousel>
              </template>
            </Card>
          </TabPanel>
          <TabPanel>
            <template #header>
              <i
                class="pi pi-user-edit"
                style="font-size: 18px; margin: 3px"
              ></i>
              <span><h4>My Profile</h4></span>
            </template>
            <Card class="component-card">
              <template v-slot:content>
                <Carousel
                  :value="operationsItemsMyProfile"
                  :numVisible="1"
                  :numScroll="1"
                  :responsiveOptions="responsiveOptions"
                >
                  <template #header>
                    <h1 style="text-align: center">Available Operations</h1>
                  </template>
                  <template #item="slotProps">
                    <div class="operation-item">
                      <div class="operation-item-content">
                        <div class="p-mb-3">
                          <span style="text-align: center">
                            <span v-html="slotProps.data.operation_img"></span
                          ></span>
                        </div>
                        <h4>{{ slotProps.data.operation_desc }}</h4>
                        <div
                          v-html="slotProps.data.operation_button"
                          @click.capture="toggleShowUpdatePassword"
                          v-if="slotProps.data.operation === 'update_password'"
                        ></div>
                        <div
                          v-html="slotProps.data.operation_button"
                          @click.capture="toggleShowDeleteUser"
                          v-if="slotProps.data.operation === 'delete_user'"
                        ></div>
                      </div>
                    </div>
                  </template>
                </Carousel>
              </template>
            </Card>
          </TabPanel>
        </TabView>
      </div>
    </div>
    <transition class="modal-animation">
      <modal-view v-if="showAddUser" @close="toggleShowAddUser">
        <template v-slot:header>ADD USER</template>
        <template v-slot:body>
          <add-user @close="refreshData"> </add-user> </template
      ></modal-view>
    </transition>
    <transition class="modal-animation">
      <modal-view v-if="showAddDep" @close="toggleShowAddDep">
        <template v-slot:header>ADD Department</template>
        <template v-slot:body>
          <add-dep @close="refreshData"> </add-dep> </template
      ></modal-view>
    </transition>
    <transition class="modal-animation">
      <modal-view v-if="showUpdatePassword" @close="toggleShowUpdatePassword">
        <template v-slot:header>Update Password</template>
        <template v-slot:body>
          <update-password @close="refreshData"> </update-password> </template
      ></modal-view>
    </transition>
    <transition class="modal-animation">
      <modal-view
        v-if="showUpdateDepartment"
        @close="toggleShowUpdateDepartment"
      >
        <template v-slot:header>Update Department</template>
        <template v-slot:body>
          <update-department @close="refreshData">
          </update-department> </template
      ></modal-view>
    </transition>
    <transition class="modal-animation">
      <modal-view v-if="showUpdateUser" @close="toggleShowUpdateUser">
        <template v-slot:header>Update Update</template>
        <template v-slot:body>
          <update-user @close="refreshData" :user="selected_user">
          </update-user> </template
      ></modal-view>
    </transition>
    <Dialog
      header="Profile Deletion"
      v-model:visible="showDeleteUser"
      :style="{ width: '50vw' }"
      :maximizable="true"
      :modal="true"
    >
      <h5 class="p-m-0">Are you sure you want to delete your Profile?</h5>
      <template #footer>
        <Button
          label="No"
          icon="pi pi-times"
          @click="toggleShowDeleteUser"
          class="p-button-text"
          autofocus
        />
        <Button label="Yes" icon="pi pi-check" @click="deleteUser" />
      </template>
    </Dialog>
  </div>
</template>

<script>
import UserTable from "../components/UserTable.vue";
import TableDepartments from "../components/TableDepartments.vue";
import AddUser from "../components/AddUser.vue";
import AddDepartment from "../components/AddDepartment.vue";
import Modal from "../components/Modal.vue";
import UpdatePassword from "../components/UpdatePassword.vue";
import UpdateDepartment from "../components/UpdateDepartment.vue";
import UpdateUser from "../components/InputForms/UpdateUser.vue";

export default {
  components: {
    "user-table": UserTable,
    "add-user": AddUser,
    "add-dep": AddDepartment,
    "modal-view": Modal,
    "dep-table": TableDepartments,
    "update-password": UpdatePassword,
    "update-department": UpdateDepartment,
    "update-user": UpdateUser,
  },
  data() {
    this.autenticateSession();
    return {
      admin: localStorage.admin,
      showDeleteUser: false,
      showUpdatePassword: false,
      showUpdateDepartment: false,
      showUpdateUser: false,
      showAddUser: false,
      showAddDep: false,
      componentKey: 0,
      selected_user: "",
      operations: [
        {
          operation: 0,
          operation_img: "",
          operation_desc: "",
          operation_buton: "",
        },
        {
          operation: 0,
          operation_img: "",
          operation_desc: "",
          operation_button: "",
        },
      ],
      operationsItems: [
        {
          operation: "add_user",
          operation_img:
            "<i class='pi pi-user-plus' style='font-size: 230px'></i>",
          operation_desc: "Click here to create new User",
          operation_button:
            '<div class="d-grid"><button class="btn btn-primary" ' +
            'type="button" @click="toggleShowAddData"> <span class="btn-label"> <i class="pi pi-user-plus" style="font-size: 23px"></i>' +
            " </button>   </div>",
        },
        {
          operation: "add_dep",
          operation_img:
            "<i class='pi pi-plus-circle' style='font-size: 230px'></i>",
          operation_desc: "Click here to create new Department",
          operation_button:
            '<div class="d-grid"> <button class="btn btn-primary" ' +
            'type="button" @click="toggleShowAddDep"> <span class="btn-label"> <i class="pi pi-plus-circle" style="font-size: 23px"></i>' +
            " </button>  </div>",
        },
        {
          operation: "update_dep",
          operation_img:
            "<i class='pi pi-briefcase' style='font-size: 230px'></i>",
          operation_desc: "Click here to update an User's Department",
          operation_button:
            '<div class="d-grid"> <button class="btn btn-primary" ' +
            'type="button" @click="toggleShowUpdateDepartment"> <span class="btn-label"> <i class="pi pi-briefcase" style="font-size: 23px"></i>' +
            " </button>  </div>",
        },
      ],
      operationsItemsMyProfile: [
        {
          operation: "update_password",
          operation_img:
            "<i class='pi pi-user-edit' style='font-size: 230px'></i>",
          operation_desc: "Click here to change Password",
          operation_button:
            '<div class="d-grid"><button class="btn btn-primary" ' +
            'type="button" @click="toggleShowUpdatePassword"> <span class="btn-label"> <i class="pi pi-user-edit" style="font-size: 23px"></i>' +
            " </button>   </div>",
        },
        {
          operation: "delete_user",
          operation_img:
            "<i class='pi pi-user-minus' style='font-size: 230px'></i>",
          operation_desc: "Click here to delete your profile",
          operation_button:
            '<div class="d-grid"><button class="btn btn-primary" ' +
            'type="button" @click="toggleShowDeleteUser"> <span class="btn-label"> <i class="pi pi-user-minus" style="font-size: 23px"></i>' +
            " </button>   </div>",
        },
      ],
    };
  },
  methods: {
    deleteUser() {
      const issued_user = localStorage.loggedUser;
      this.$toast.add({
        severity: "info",
        summary: "User is being deleted",
        detail: "This may take a few minutes depending on User's datasets",
        life: 5000,
      });
      this.axios
        .delete("/delete_user/" + issued_user + "/" + issued_user)
        .then(() => {
          this.logout();
          this.$toast.add({
            severity: "success",
            summary: "Profile Deletion Successful",
            detail: "You have successfully deleted your profile",
            life: 3000,
          });
        })
        .catch(() => {
          this.$toast.add({
            severity: "error",
            summary: "Profile Deletion Unsuccessful",
            detail:
              "You can not delete you User Profile if you are the last remaining User!",
            life: 8000,
          });
          this.toggleShowDeleteUser();
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
    updateUser(user) {
      this.selected_user = user;
      this.toggleShowUpdateUser();
    },
    toggleShowDeleteUser() {
      this.showDeleteUser = !this.showDeleteUser;
    },
    toggleShowUpdatePassword() {
      this.showUpdatePassword = !this.showUpdatePassword;
    },
    toggleShowUpdateDepartment() {
      this.showUpdateDepartment = !this.showUpdateDepartment;
    },
    toggleShowUpdateUser() {
      this.showUpdateUser = !this.showUpdateUser;
    },
    toggleShowAddUser() {
      this.showAddUser = !this.showAddUser;
    },
    toggleShowAddDep() {
      this.showAddDep = !this.showAddDep;
    },
    refreshData() {
      this.componentKey += 1;
      if (this.showAddUser === true) {
        this.toggleShowAddUser();
      }
      if (this.showAddDep === true) {
        this.toggleShowAddDep();
      }
      if (this.showUpdatePassword === true) {
        this.toggleShowUpdatePassword();
      }
      if (this.showUpdateDepartment === true) {
        this.toggleShowUpdateDepartment();
      }
      if (this.showUpdateUser === true) {
        this.toggleShowUpdateUser();
      }
    },
    autenticateSession() {
      if (localStorage.loggedUser && localStorage.token) {
        this.$axios
          .get("/user/validatetoken?token=" + localStorage.token)
          .then(() => {
            this.selected_user = localStorage.loggedUser;
            this.axios.get("/user/" + this.selected_user).then((res) => {
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
.banner-image {
  background-image: url("~@/assets/USERMANAGER_BACKGROUND.jpg");
}
.component-card {
  margin-top: 30px;
  position: relative;
  display: flex;
  flex-direction: column;
  min-width: 0;
  word-wrap: break-word;
  background-color: #fff;
  background-clip: border-box;
  border-radius: 0.25rem;
  /* min-width: 100%; */
}
</style>
