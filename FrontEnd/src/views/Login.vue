<template>
  <div>
    <div class="body"></div>
    <div class="grad"></div>
    <div class="header">
      <div class="container" id="container">
        <div class="form-container sign-in-container">
          <form action="#">
            <div class="p-grid">
              <div class="p-col inline-block">
                <img
                  src="~@/assets/CLIENT_LOGO.png"
                  alt="My image"
                  style="width: 80px; height: 70px; margin-top: -50px"
                />
              </div>
              <div class="p-col inline-block">
                <img
                  src="~@/assets/LTEP_LOGO_2.png"
                  alt="My image"
                  style="width: 110px; height: 90px; margin-top: -50px"
                />
              </div>
            </div>
            <h4 style="color: black; margin-bottom: -5px; margin-top: -5px">
              <b>BR Architecture Manager</b>
            </h4>
            <h6 style="margin-bottom: 15px">by <b>LTEP Technologies</b></h6>
            <hr style="margin: 1px; color: black" />
            <h1 style="color: black">Sign in</h1>
            <span>Enter your Credentials</span>
            <input v-model="email" type="email" placeholder="Email" />
            <input v-model="password" type="password" placeholder="Password" />
            <a href="javascript:void(0);" @click="toggleForgotPassword()"
              >Forgot your password?</a
            >
            <button @click="login()">Sign In</button>
          </form>
        </div>
        <div class="overlay-container">
          <div class="overlay">
            <div class="overlay-panel overlay-left">
              <h1>Welcome Back!</h1>
              <p>
                To keep connected with us please login with your personal info
              </p>
              <button class="ghost" id="signIn">Sign In</button>
            </div>
            <div class="overlay-panel overlay-right">
              <h1>Welcome!</h1>
              <p>
                Thank you for choosing to use the
                <b>BR Architecture Manager</b> powered by
                <b>LTEP Technologies</b>
              </p>
              <button class="ghost" id="signUp" @click="toggleSignUp()">
                Sign Up
              </button>
            </div>
          </div>
        </div>
      </div>

      <Dialog
        v-model:visible="forgot_password"
        :breakpoints="{ '960px': '75vw', '640px': '100vw' }"
      >
        <Card>
          <template #header>
            <img
              alt="User Forgot PWD"
              src="~@/assets/forgot_pwd.png"
              style="width: 400px; height: auto"
            />
          </template>
          <template #title>
            <h1 style="color: black">Password Recovery</h1></template
          >
          <template #content>
            <h3>
              Due to the sensitivity of the data contained in the BR
              Architecture Manager please contact your responsible BR Enterprise
              Architecture Manager Admin: <br /><br />
              Johannes Lederle : johannes.lederle@br.de
            </h3>
          </template>
          <template #footer>
            <Button
              icon="pi pi-check"
              label="Okay"
              @click="toggleForgotPassword()"
            />
          </template>
        </Card>
      </Dialog>

      <Dialog
        v-model:visible="sign_up"
        :breakpoints="{ '960px': '75vw', '640px': '100vw' }"
      >
        <Card>
          <template #header>
            <div class="p-grid">
              <div class="p-col inline-block">
                <img
                  src="~@/assets/CLIENT_LOGO.png"
                  alt="My image"
                  style="width: 80px; height: 70px"
                />
              </div>
              <div class="p-col inline-block">
                <img
                  src="~@/assets/LTEP_LOGO_2.png"
                  alt="My image"
                  style="width: 110px; height: 90px"
                />
              </div>
            </div>
          </template>
          <template #title> <h1 style="color: black">SIGN UP</h1></template>
          <template #content>
            <h3>
              Thank you for choosing to use the BR Architecture Manager! <br />
              Please contact your responsible BR Enterprise Architecture Manager
              Admin: <br />
              <br />
              Johannes Lederle : johannes.lederle@br.de
            </h3>
          </template>
          <template #footer>
            <Button icon="pi pi-check" label="Okay" @click="toggleSignUp()" />
          </template>
        </Card>
      </Dialog>

      <footer>
        <p>
          Created by LTEP Technologies. Copyright 2021 ©
          <a
            target="_blank"
            href="https://de.linkedin.com/in/leo-thieroff-a5b965161"
            >More</a
          >.
        </p>
      </footer>
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
      forgot_password: false,
      sign_up: false,
    };
  },
  methods: {
    toggleForgotPassword() {
      this.forgot_password = !this.forgot_password;
    },
    toggleSignUp() {
      this.sign_up = !this.sign_up;
    },
    findUser(value) {
      if (value.email == this.email) {
        return value;
      }
    },
    check_user_admin() {
      this.$axios.get("/user/" + localStorage.loggedUser).then((res) => {
        if (res.data.admin == 1) {
          localStorage.admin = true;
          this.$router.push("/mainmenu-landing-a");
        } else {
          localStorage.admin = false;
          this.$router.push("/mainmenu-landing-u");
        }
      });
    },
    login() {
      this.email = this.email.toLowerCase();
      this.$axios
        .get("/user/auth?email=" + this.email + "&passwd=" + this.password)
        .then((res) => {
          localStorage.token = res.data.token;
        })
        .then(() => {
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
                this.check_user_admin();
              }
            }
          });
        })
        .catch(() => {
          this.$toast.add({
            severity: "error",
            summary: "Wrong Credentials",
            detail: "The entered Email or Password is wrong",
            life: 3000,
          });
          this.$router.push("/");
        });
    },
  },
};
</script>

<style scoped>
@import url("https://fonts.googleapis.com/css?family=Montserrat:400,800");

* {
  box-sizing: border-box;
}

.grid {
  margin-bottom: -30px;
  margin-top: -50px;
}

body {
  background: #f6f5f7;
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
  font-family: "Montserrat", sans-serif;
  height: 100vh;
  margin: -20px 0 50px;
}

h1 {
  font-weight: bold;
  margin: 0;
  color: white;
}

h2 {
  text-align: center;
}

p {
  font-size: 14px;
  font-weight: 100;
  line-height: 20px;
  letter-spacing: 0.5px;
  margin: 20px 0 30px;
}

span {
  font-size: 12px;
}

a {
  color: #333;
  font-size: 14px;
  text-decoration: none;
  margin: 15px 0;
}

button {
  border-radius: 20px;
  border: 1px solid #24cf5f;
  background-color: #24cf5f;
  color: #ffffff;
  font-size: 12px;
  font-weight: bold;
  padding: 12px 45px;
  letter-spacing: 1px;
  text-transform: uppercase;
  transition: transform 80ms ease-in;
}

button:active {
  transform: scale(0.95);
}

button:focus {
  outline: none;
}

button.ghost {
  background-color: transparent;
  border-color: #ffffff;
}

form {
  background-color: #ffffff;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-direction: column;
  padding: 0 50px;
  height: 100%;
  text-align: center;
}

input {
  background-color: #eee;
  border: none;
  padding: 12px 15px;
  margin: 8px 0;
  width: 100%;
}

.container {
  background-color: #fff;
  border-radius: 10px;
  box-shadow: 0 14px 28px rgba(0, 0, 0, 0.25), 0 10px 10px rgba(0, 0, 0, 0.22);
  position: relative;
  overflow: hidden;
  width: 768px;
  max-width: 100%;
  min-height: 480px;
}

.form-container {
  position: absolute;
  top: 0;
  height: 100%;
  transition: all 0.6s ease-in-out;
}

.sign-in-container {
  left: 0;
  width: 50%;
  z-index: 2;
}

.container.right-panel-active .sign-in-container {
  transform: translateX(100%);
}

.sign-up-container {
  left: 0;
  width: 50%;
  opacity: 0;
  z-index: 1;
}

.container.right-panel-active .sign-up-container {
  transform: translateX(100%);
  opacity: 1;
  z-index: 5;
  animation: show 0.6s;
}

@keyframes show {
  0%,
  49.99% {
    opacity: 0;
    z-index: 1;
  }

  50%,
  100% {
    opacity: 1;
    z-index: 5;
  }
}

.overlay-container {
  position: absolute;
  top: 0;
  left: 50%;
  width: 50%;
  height: 100%;
  overflow: hidden;
  transition: transform 0.6s ease-in-out;
  z-index: 100;
}

.container.right-panel-active .overlay-container {
  transform: translateX(-100%);
}

.overlay {
  background: #0c8cd3;
  background: -webkit-linear-gradient(to right, #2b8eff, #0c8cd3);
  background: linear-gradient(to right, #2b8eff, #0c8cd3);
  background-repeat: no-repeat;
  background-size: cover;
  background-position: 0 0;
  color: #ffffff;
  position: relative;
  left: -100%;
  height: 100%;
  width: 200%;
  transform: translateX(0);
  transition: transform 0.6s ease-in-out;
}

.container.right-panel-active .overlay {
  transform: translateX(50%);
}

.overlay-panel {
  position: absolute;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-direction: column;
  padding: 0 40px;
  text-align: center;
  top: 0;
  height: 100%;
  width: 50%;
  transform: translateX(0);
  transition: transform 0.6s ease-in-out;
}

.overlay-left {
  transform: translateX(-20%);
}

.container.right-panel-active .overlay-left {
  transform: translateX(0);
}

.overlay-right {
  right: 0;
  transform: translateX(0);
}

.container.right-panel-active .overlay-right {
  transform: translateX(20%);
}

.social-container {
  margin: 20px 0;
}

.social-container a {
  border: 1px solid #dddddd;
  border-radius: 50%;
  display: inline-flex;
  justify-content: center;
  align-items: center;
  margin: 0 5px;
  height: 40px;
  width: 40px;
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

footer p {
  margin: 10px 0;
}

footer i {
  color: red;
}

footer a {
  color: #3c97bf;
  text-decoration: none;
}

.body {
  position: absolute;
  top: -20px;
  left: -20px;
  right: -40px;
  bottom: -40px;
  width: auto;
  height: auto;
  background-image: url(~@/assets/LOGIN_BACKGROUND.jpg);
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
  );
  z-index: 1;
  opacity: 0.7;
}

.header {
  position: relative;
  /* top: calc(45% - 35px);
  left: calc(50% - 255px); */
  z-index: 2;
  margin-top: calc(10%);
}
</style>