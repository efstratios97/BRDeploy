<template>
  <div>
    <div v-if="admin === 'true'">
      <admin-nav-bar></admin-nav-bar>
    </div>
    <div v-else>
      <user-nav-bar></user-nav-bar>
    </div>
  </div>
</template>
<script>
import AdminNavBar from "./AdminNavBar.vue";
import UserNavBar from "./UserNavBar.vue";

export default {
  components: {
    "admin-nav-bar": AdminNavBar,
    "user-nav-bar": UserNavBar,
  },
  data() {
    return {
      admin: localStorage.admin,
    };
  },
  methods: {},
};
</script>
<style scoped>
.p-menubar {
  background-color: white;
}
.p-menuitem-icon {
  font-size: 18px !important;
}
.p-menuitem-text {
  font-size: 18px !important;
}
.p-grid {
  margin: 0px;
}
.p-col {
  margin: 0px;
}
</style>