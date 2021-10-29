<template>
  <form>
    <ul class="form-list">
      <li class="form-list__row">
        <label for="DatasetName"> <b-icon-archive-fill /> Name:</label>
        <input
          class="input100"
          id="DatasetName"
          type="text"
          v-model="name"
          placeholder="Data Set Name"
          required=""
        />
      </li>
      <li class="form-list__row">
        <label for="DatasetName" id="description">
          <b-icon-pencil-fill /> Description:
        </label>
        <textarea
          class="input100"
          v-model="description"
          placeholder="Description"
          id="description"
        ></textarea>
      </li>
      <li class="form-list__row form-list__row--inline">
        <div class="container-2">
          <div class="row">
            <div class="col-6">
              <label> <b-icon-shield-lock-fill /> Users with Access</label>
              <select v-model="selected_users" multiple>
                <option
                  v-for="user in users"
                  v-bind:value="user.email"
                  :key="user.email"
                >
                  {{ user.email }}
                </option>
              </select>
            </div>
            <div class="col-6">
              <label>
                <b-icon-shield-lock-fill /> Departments with Access
              </label>
              <select v-model="selected_departments" multiple>
                <option
                  v-for="department in departments"
                  v-bind:value="department.name"
                  :key="department.name"
                >
                  {{ department.name }}
                </option>
              </select>
            </div>
          </div>
        </div>
      </li>
      <li class="form-list__row form-list__row--agree">
        <div class="container-2">
          <div class="row">
            <div class="col-4">
              <label for="cleaned">
                <input
                  type="checkbox"
                  v-model="cleaned"
                  id="cleaned"
                  name="cleaned_ds"
                />
                Cleaned
              </label>
            </div>
            <div class="col-6">
              <label for="storage">
                <input
                  class="input200"
                  type="checkbox"
                  v-model="storageType"
                  id="storage"
                />
                <b-icon-cloud-check-fill /> Stored in Cloud
              </label>
            </div>
          </div>
        </div>
      </li>
      <li class="form-list__row">
        <label for="formFile"
          ><b-icon-file-earmark-spreadsheet-fill /> File Input</label
        >
        <input class="form-control" type="file" id="formFile" ref="file" />
      </li>
      <li>
        <button type="submit" class="button" @click="createDataSet">
          Create Dataset
        </button>
      </li>
      <li v-if="submitted">
        <br />
        <ProgressBar mode="indeterminate" v-if="submitted" />
      </li>
    </ul>
  </form>
</template>

<script>
export default {
  data() {
    return {
      name: "",
      cleaned: "",
      description: "",
      storageType: true,
      file: "",
      users: this.getUsersOptions(),
      departments: this.getDepartmentsOptions(),
      selected_users: "",
      selected_departments: "",
      formData: "",
      submitted: false,
    };
  },
  methods: {
    getUsersOptions() {
      this.$axios.get("/users").then((res) => {
        this.users = res.data;
      });
    },
    getDepartmentsOptions() {
      this.$axios.get("/departments").then((res) => {
        this.departments = res.data;
      });
    },
    createDataSet() {
      this.submitted = true;
      this.formData = new FormData();
      this.formData.append("name", this.name);
      this.formData.append("file", this.$refs.file.files[0]);
      this.formData.append("cleaned", this.cleaned);
      this.formData.append("description", this.description);
      this.formData.append(
        "storage_type",
        this.storageType === true ? "cloud" : "local"
      );
      this.formData.append("access_user_list", this.selected_users);
      this.formData.append(
        "access_business_unit_list",
        this.selected_departments
      );
      this.$axios
        .post("/create_dataset?uid=" + localStorage.loggedUser, this.formData)
        .then(() => {
          this.$toast.add({
            severity: "success",
            summary: "Dataset Creation Successful",
            detail: "The selected Dataset was created",
            life: 3000,
          });
          this.$emit("close");
        })
        .catch(() => {
          this.$toast.add({
            severity: "error",
            summary: "Dataset Creation Unsuccessful",
            detail: "The selected Dataset could not be created",
            life: 3000,
          });
          this.submitted = false;
        });
    },
  },
};
</script>

<style>
.visuallyhidden {
  border: 0;
  clip: rect(0 0 0 0);
  height: 1px;
  margin: -1px;
  overflow: hidden;
  padding: 0;
  position: absolute;
  width: 1px;
}

body {
  font-family: "Open Sans", sans-serif;
  color: #1a1a1a;
  background-color: #f0f0f0;
}

h1,
h2,
h3,
h4,
h5 {
  margin: 0;
  font-weight: 600;
}

.button {
  color: #ffffff;
  background-color: #24cf5f;
  margin-top: 10px;

  padding: 12px 25px;
  font-size: 12px;
  letter-spacing: 1px;
  text-transform: uppercase;
  border: 0;
  border-radius: 2px;
  outline: 0;
  box-shadow: 3px 3px 20px rgba(0, 0, 0, 0.2);
  transition: all 0.2s;
}
.button:hover,
.button:active,
.button:focus {
  -ms-transform: scale(1.1);
  transform: scale(1.1);
}

input {
  width: calc(100% - 10px);
  min-height: 30px;
  padding-left: 5px;
  padding-right: 5px;
  letter-spacing: 0.5px;
  border: 0;
  border-bottom: 2px solid #f0f0f0;
}
input:valid {
  border-color: #24cf5f;
}
input:focus {
  outline: none;
  border-color: #fbcf34;
}

.form-list {
  padding-left: 0;
  list-style: none;
}
.form-list__row {
  margin-bottom: 25px;
}
.form-list__row label {
  position: relative;
  display: block;
  text-transform: uppercase;
  font-weight: 600;
  font-size: 11px;
  letter-spacing: 0.5px;
  color: #939393;
}
.form-list__row--inline {
  display: -ms-flexbox;
  display: flex;
  -ms-flex-pack: justify;
  justify-content: space-between;
}
.form-list__row--inline > :first-child {
  -ms-flex: 2;
  flex: 2;
  padding-right: 20px;
}
.form-list__row--inline > :nth-child(2n) {
  -ms-flex: 1;
  flex: 1;
}
.form-list__input-inline {
  display: -ms-flexbox;
  display: flex;
  -ms-flex-pack: justify;
  justify-content: space-between;
}
.form-list__input-inline > * {
  width: calc(50% - 10px - 10px);
}
.form-list__row--agree {
  margin-top: 10px;
  margin-bottom: 10px;
  font-size: 12px;
}
.form-list__row--agree label {
  font-weight: 400;
  text-transform: none;
  color: #676767;
}
.form-list__row--agree input {
  width: auto;
  margin-right: 5px;
}

#input--cc {
  position: relative;
  padding-top: 6px;
}
#input--cc input {
  padding-left: 46px;
  width: calc(100% - 46px);
}
#input--cc:before {
  content: "";
  position: absolute;
  left: 0;
  top: 50%;
  width: 36px;
  height: 45px;
  background-image: url("data:image/svg+xml;utf8,%3Csvg%20class%3D%22nc-icon%20glyph%22%20xmlns%3D%22http%3A//www.w3.org/2000/svg%22%20xmlns%3Axlink%3D%22http%3A//www.w3.org/1999/xlink%22%20x%3D%220px%22%20y%3D%220px%22%20width%3D%2248px%22%20height%3D%2248px%22%20viewBox%3D%220%200%2048%2048%22%3E%3Cg%3E%20%3Cpath%20data-color%3D%22color-2%22%20fill%3D%22%238c8c8c%22%20d%3D%22M47%2C16V9c0-1.105-0.895-2-2-2H3C1.895%2C7%2C1%2C7.895%2C1%2C9v7H47z%22%3E%3C/path%3E%20%3Cpath%20fill%3D%22%238c8c8c%22%20d%3D%22M1%2C22v17c0%2C1.105%2C0.895%2C2%2C2%2C2h42c1.105%2C0%2C2-0.895%2C2-2V22H1z%20M18%2C33H8c-0.552%2C0-1-0.448-1-1s0.448-1%2C1-1h10%20c0.552%2C0%2C1%2C0.448%2C1%2C1S18.552%2C33%2C18%2C33z%20M40%2C33h-5c-0.552%2C0-1-0.448-1-1s0.448-1%2C1-1h5c0.552%2C0%2C1%2C0.448%2C1%2C1S40.552%2C33%2C40%2C33z%22%3E%3C/path%3E%20%3C/g%3E%3C/svg%3E");
  background-position: center;
  background-repeat: no-repeat;
  background-size: 36px;
  -ms-transform: translateY(-50%);
  transform: translateY(-50%);
}
</style>