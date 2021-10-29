<template>
  <div>
    <div class="body"></div>
    <div class="grad"></div>
    <div class="header">
      <div>
        <span>BR</span>
        Enterprise <br />
        Architecture <br />
        Manager
      </div>
    </div>
    <div class="login">
      <input type="text" placeholder="email" v-model="email" /><br />
      <input
        type="password"
        placeholder="password"
        v-model="password"
      /><br /><br />
      <button @click="login()">Login</button>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      email: "",
      password: "",
      users: "",
    };
  },
  methods: {
    findUser(value) {
      if (value.email == this.email) {
        return value;
      }
    },
    login() {
      this.$axios
        .get("/user/auth?email=" + this.email + "&passwd=" + this.password)
        .then((res) => {
          this.users = res.data;
          this.allUsers = res.data;
          localStorage.token = res.data.token;
          this.$axios.get("/users").then((res) => {
            this.users = res.data;
            localStorage.loggedUser = this.users.filter(
              this.findUser
            )[0].user_id;
            for (let i = 0; i < this.users.length; i++) {
              if (this.users[i]["user_id"] === localStorage.loggedUser) {
                this.$toast.add({
                  severity: "success",
                  summary: "Welcome " + this.users[i]["first_name"],
                  detail: "You successfully logged in",
                  life: 3000,
                });
                this.users = null;
                this.$router.push("/mainmenu");
              }
            }
          });
          this.$router.push("/");
        })
        .catch(() => {
          this.$toast.add({
            severity: "error",
            summary: "Wrong Credentials",
            detail: "The entered Email or Password is wrong",
            life: 3000,
          });
        });
    },
  },
};
</script>

<style scoped>
@import url(https://fonts.googleapis.com/css?family=Exo:100,200,400);
@import url(https://fonts.googleapis.com/css?family=Source+Sans+Pro:700,400,300);

body {
  margin: 0;
  padding: 0;
  background: #fff;

  color: #fff;
  font-family: Arial;
  font-size: 12px;
}

.body {
  position: absolute;
  top: -20px;
  left: -20px;
  right: -40px;
  bottom: -40px;
  width: auto;
  height: auto;
  background-image: url(https://www.br.de/unternehmen/br-logo-hochhaus-100~_v-img__16__9__xl_-d31c35f8186ebeb80b0cd843a7c267a0e0c81647.jpg?version=3513b);
  background-attachment: fixed;
  background-position: center center;
  background-size: cover;
  z-index: 0;
}

.grad {
  position: absolute;
  top: -20px;
  left: -20px;
  right: -40px;
  bottom: -40px;
  width: auto;
  height: auto;
  background: -webkit-gradient(
    linear,
    left top,
    left bottom,
    color-stop(0%, rgba(0, 0, 0, 0)),
    color-stop(100%, rgba(0, 0, 0, 0.65))
  ); /* Chrome,Safari4+ */
  z-index: 1;
  opacity: 0.7;
}

.header {
  position: absolute;
  top: calc(45% - 35px);
  left: calc(50% - 255px);
  z-index: 2;
  margin: -20px;
}

.header div {
  float: left;
  color: #fff;
  font-family: "Exo", sans-serif;
  font-size: 35px;
  font-weight: 200;
}

.header div span {
  color: #5379fa !important;
}

.login {
  position: absolute;
  top: calc(48% - 75px);
  left: calc(50% - 50px);
  height: 150px;
  width: 350px;
  padding: 10px;
  z-index: 2;
}

.login input[type="text"] {
  width: 250px;
  height: 30px;
  background: transparent;
  border: 1px solid rgba(255, 255, 255, 0.6);
  border-radius: 2px;
  color: #fff;
  font-family: "Exo", sans-serif;
  font-size: 16px;
  font-weight: 400;
  padding: 4px;
}

.login input[type="password"] {
  width: 250px;
  height: 30px;
  background: transparent;
  border: 1px solid rgba(255, 255, 255, 0.6);
  border-radius: 2px;
  color: #fff;
  font-family: "Exo", sans-serif;
  font-size: 16px;
  font-weight: 400;
  padding: 4px;
  margin-top: 10px;
}

button {
  width: 250px;
  height: 35px;
  background: #fff;
  border: 1px solid #fff;
  cursor: pointer;
  border-radius: 2px;
  color: #a18d6c;
  font-family: "Exo", sans-serif;
  font-size: 16px;
  font-weight: 400;
  padding: 6px;
  margin-top: 10px;
}

button:hover {
  opacity: 0.8;
}

.login input[type="text"]:focus {
  outline: none;
  border: 1px solid rgba(255, 255, 255, 0.9);
}

.login input[type="password"]:focus {
  outline: none;
  border: 1px solid rgba(255, 255, 255, 0.9);
}

.login input[type="button"]:focus {
  outline: none;
}

::-webkit-input-placeholder {
  color: rgba(255, 255, 255, 0.6);
}

::-moz-input-placeholder {
  color: rgba(255, 255, 255, 0.6);
}
</style>