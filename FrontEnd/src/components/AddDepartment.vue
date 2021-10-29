<template>
  <form>
    <div class="mb-3">
      <label for="name" class="form-label"> <b-icon-building /> Name:</label>
      <input
        class="input100"
        id="name"
        type="text"
        v-model="name"
        placeholder="BU Name"
      />
    </div>

    <button class="btn-form" @click="createBU">
      <b-icon-upload />
      <b>Create BU</b>
    </button>
  </form>
</template>

<script>
export default {
  data() {
    return {
      name: "",
      bu: "",
    };
  },
  methods: {
    createBU() {
      this.bu = {
        dep_name: this.name,
      };
      const jsonString = JSON.stringify(this.bu);
      this.$axios
        .post("/create_department/" + localStorage.loggedUser, jsonString)
        .then(() => {
          this.$toast.add({
            severity: "success",
            summary: "Department Creation Successful",
            detail: "The Department: " + this.name + " was created",
            life: 3000,
          });
          this.$emit("close");
        })
        .catch(() => {
          this.$toast.add({
            severity: "error",
            summary: "Department Creation Unsuccessful",
            detail:
              "The Department: " +
              this.name +
              " could not be created!\nIf you have no Admin rights you cannot create a new Department",
            life: 3000,
          });
        });
    },
  },
};
</script>
<style scoped>
label {
  display: block;
}

.btn-form {
  color: white;
  background: #0d6efd;
  border: 0px solid blue;
  border-radius: 2px;
}

select {
  color: black;
}

input {
  color: black;
}

textarea {
  color: black;
}
</style>