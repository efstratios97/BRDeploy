<template>
  <div>
    <form>
      <div class="p-grid p-fluid">
        <div class="p-col-12 p-md-12">
          <div class="p-inputgroup">
            <span class="p-inputgroup-addon">
              <i class="pi pi-file"></i>
            </span>
            <InputText
              placeholder="Dataset's Name"
              v-model="name"
              class="inputfield w-full"
            />
          </div>
        </div>
      </div>

      <div class="p-grid p-fluid">
        <div class="p-col-12 p-md-12">
          <Textarea
            placeholder="Dataset Description"
            v-model="description"
            :autoResize="true"
            rows="5"
            cols="30"
          />
        </div>
      </div>

      <div class="p-grid p-fluid">
        <div class="p-col-12 p-md-12">
          <div class="p-inputgroup">
            <span class="p-inputgroup-addon">
              <i class="pi pi-users"></i>
            </span>
            <MultiSelect
              v-model="selected_users"
              :options="users"
              :filter="true"
              optionLabel="user.email"
              placeholder="Assign Users with Access (Optional)"
              filterPlaceholder="Find Users"
              class="multiselect-custom"
              :showClear="true"
            />
          </div>
        </div>
      </div>

      <div class="p-grid p-fluid">
        <div class="p-col-12 p-md-12">
          <div class="p-inputgroup">
            <span class="p-inputgroup-addon">
              <b-icon-building />
            </span>
            <MultiSelect
              v-model="selected_departments"
              :options="departments"
              :filter="true"
              optionLabel="dep.name"
              placeholder="Assign Departments with Access (Optional)"
              filterPlaceholder="Find Departments"
              class="multiselect-custom"
              :showClear="true"
            />
          </div>
        </div>
      </div>

      <div class="p-grid p-fluid">
        <div class="p-col">
          <ToggleButton
            v-model="to_clean"
            onLabel="Apply Cleanser at Dataset Creation"
            offLabel="Just create Dataset"
            onIcon="pi pi-check"
            offIcon="pi pi-times"
            class="p-toggleButton"
            @click="this.listCleansers()"
          />
        </div>
      </div>

      <div v-if="this.to_clean" class="p-grid p-fluid">
        <div class="p-col-12 p-md-12">
          <div class="p-inputgroup">
            <span class="p-inputgroup-addon">
              <i class="pi pi-cog"></i>
            </span>
            <Dropdown
              v-model="selected_cleanser"
              :options="cleansers"
              :filter="true"
              optionLabel="cleanser.name"
              placeholder="Choose Cleanser"
              filterPlaceholder="Find a Cleanser"
              class="multiselect-custom"
              :showClear="true"
            />
          </div>
        </div>
      </div>

      <div class="p-grid p-fluid">
        <div class="p-col">
          <div class="card p-align-center">
            <h5>Delete older Versions of Dataset</h5>
            <InputSwitch
              v-model="delete_all_previous_versions"
              v-tooltip="'Datasets can be still recovered from the Archive'"
              @click="this.listAllDatasets"
            />
          </div>
        </div>
      </div>

      <div class="form-list__row">
        <label for="formFile"
          ><b-icon-file-earmark-spreadsheet-fill /> File Input</label
        >
        <input class="form-control" type="file" id="formFile" ref="file" />
      </div>

      <div class="p-grid p-fluid">
        <div class="p-col-12 p-md-12">
          <Button
            v-if="this.to_clean === false"
            label="Create Dataset"
            icon="pi pi-plus-circle"
            iconPos="center"
            @click="createDataSet"
          />
          <Button
            v-else
            label="Create cleaned Dataset"
            icon="pi pi-plus-circle"
            iconPos="center"
            @click="create_cleaned_dataset"
          />
        </div>
      </div>
      <div v-if="submitted">
        <br />
        <ProgressBar mode="indeterminate" v-if="submitted" />
      </div>
    </form>
    <transition class="modal-animation">
      <modal-view v-if="new_label">
        <template v-slot:header>New Dataset Identified</template>
        <template v-slot:body>
          <h3>
            The Dataset you upload seems <b>not</b> to have any predecessors.
            Please label your Dataset with a designated Label. By doing so the
            next time you upload a newer version of Dataset it will
            automatically be assigned to the correct Label.
          </h3>
          <form>
            <div class="p-grid p-fluid">
              <div class="p-col-12 p-md-12">
                <div class="p-inputgroup">
                  <span class="p-inputgroup-addon">
                    <i class="pi pi-tag"></i>
                  </span>
                  <InputText
                    placeholder="Labels's Name"
                    v-model="label_name"
                    class="inputfield w-full"
                  />
                </div>
              </div>
            </div>
            <div class="p-grid p-fluid">
              <div class="p-col-12 p-md-12">
                <Button
                  label="Assign Label"
                  icon="pi pi-tag"
                  iconPos="center"
                  @click="assignLabel"
                />
              </div>
            </div>
          </form> </template
      ></modal-view>
    </transition>
    <Dialog
      v-model:visible="cleaned_operation"
      :breakpoints="{ '960px': '75vw', '640px': '100vw' }"
      :style="{ width: '50vw' }"
    >
      <DataTable
        :value="cleaned_rows"
        v-model:selection="selectedCleanedRows"
        dataKey="Name"
        :paginator="true"
        :rows="10"
        filterDisplay="menu"
        paginatorTemplate="FirstPageLink PrevPageLink PageLinks NextPageLink LastPageLink CurrentPageReport RowsPerPageDropdown"
        :rowsPerPageOptions="[10, 25, 50]"
        currentPageReportTemplate="Showing {first} to {last} of {totalRecords} entries"
        responsiveLayout="scroll"
        :rowHover="true"
        showGridlines
        stripedRows
        ref="dt"
        p-dataTable
        csvSeparator=";"
      >
        <template #header>
          <div class="p-d-flex p-jc-between p-ai-center">
            <h5 class="p-m-0">Cleaned Rows</h5>
            <span class="p-input-icon-left">
              <Button
                icon="pi pi-external-link"
                label="Export"
                @click="exportCSV($event)"
              />
            </span>
            <span class="p-input-icon-right">
              <Button
                icon="pi pi-cloud-upload"
                label="Return Rows to Dataset"
                @click="return_rows_to_dataset()"
              />
            </span>
            <span class="p-input-icon-right">
              <Button
                icon="pi pi-chevron-circle-down"
                label="Close"
                @click="close()"
              />
            </span>
          </div>
        </template>
        <template #empty>
          <span v-if="architecture_view_loading">
            Loading Cleaned Rows. Please wait.
            <ProgressBar mode="indeterminate" />
          </span>
          <span v-else> There are no Cleaned Rows. </span>
        </template>
        <template #loading>
          Loading Cleaned Rows. Please wait.
          <ProgressBar mode="indeterminate" />
        </template>
        <Column selectionMode="multiple" style="min-width: 3rem"></Column>
        <Column
          v-for="col of columns"
          :field="col"
          :header="col"
          :key="col"
          sortable
        ></Column>
      </DataTable>
    </Dialog>
  </div>
</template>

<script>
import Modal from "../components/Modal.vue";
export default {
  components: {
    "modal-view": Modal,
  },
  data() {
    return {
      name: "",
      to_clean: false,
      cleaned: "",
      description: "",
      storageType: true,
      file: "",
      users: this.getUsersOptions(),
      departments: this.getDepartmentsOptions(),
      datasets_all: "",
      selected_users: "",
      selected_departments: "",
      formData: "",
      submitted: false,
      new_label: false,
      created_dataset: "",
      label_name: "",
      cleansers: "",
      selected_cleanser: "",
      cleaned_operation: false,
      new_created_dataset: "",
      selectedCleanedRows: "",
      cleaned_rows: "",
      columns: "",
      delete_all_previous_versions: false,
    };
  },
  methods: {
    getUsersOptions() {
      this.$axios.get("/users").then((res) => {
        var users_tmp = [];
        for (let index = 0; index < res.data.length; index++) {
          users_tmp.push({ user: res.data[index] });
        }
        this.users = users_tmp;
      });
    },
    listAllDatasets() {
      this.$axios
        .get("/get_datasets/" + localStorage.loggedUser)
        .then((res) => {
          this.datasets_all = res.data.data;
        });
    },
    getDepartmentsOptions() {
      this.$axios.get("/departments").then((res) => {
        var departments_tmp = [];
        for (let index = 0; index < res.data.length; index++) {
          departments_tmp.push({ dep: res.data[index] });
        }
        this.departments = departments_tmp;
      });
    },
    toString(dict_key) {
      var key_word = "";
      var object_input = "";
      if (dict_key === "user") {
        key_word = "email";
        object_input = this.selected_users;
      } else if (dict_key === "dep") {
        key_word = "name";
        object_input = this.selected_departments;
      }
      var updt_list = "";
      for (let index = 0; index < object_input.length; index++) {
        updt_list = updt_list.concat(object_input[index][dict_key][key_word]);
        updt_list = updt_list.concat(",");
      }
      return updt_list.slice(0, -1);
    },
    create_cleaned_dataset() {
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
      this.formData.append("access_user_list", this.toString("user"));
      this.formData.append("access_business_unit_list", this.toString("dep"));
      this.$axios
        .post(
          "/create_cleaned_dataset_at_dataset_creation/" +
            this.selected_cleanser.cleanser.cleanser_id +
            "/" +
            localStorage.loggedUser,
          this.formData
        )
        .then((res) => {
          this.cleaned_rows = JSON.parse(res.data.eliminated_rows);
          this.columns = Object.keys(this.cleaned_rows[0]);
          this.submitted = false;
          this.cleaned_operation = true;
          this.new_created_dataset = res.data;
          if (
            this.new_created_dataset.cleaned_dataset["label"] ===
            "NO_LABEL_6aba48df0cb55992803d864977c3aa204520d659"
          ) {
            this.new_label = true;
          }
          if (this.delete_all_previous_versions) {
            this.delete_all_previous_versions_of_datasets();
          }
          this.$toast.add({
            severity: "success",
            summary: "Cleaned Dataset Creation Successful",
            detail: "The cleaned Dataset was created",
            life: 3000,
          });
        })
        .catch(() => {
          this.$toast.add({
            severity: "error",
            summary:
              "Cleaned Dataset Creation Unsuccessful || Cleanser NOT Applicable",
            detail:
              "The Cleanser you chose is not applicable to this dataset! Please try another one or create a new suitable Cleanser",
            life: 10000,
          });
          this.submitted = false;
        });
    },
    listCleansers() {
      this.$axios.get("/get_cleansers").then((res) => {
        var cleanser_tmp = [];
        if (res.data.data.length === 0) {
          this.$toast.add({
            severity: "warn",
            summary: "No Cleansers Available",
            detail:
              "Please got to the DataCleanser section and create a Cleanser first!",
            life: 15000,
          });
          this.to_clean = false;
        } else {
          for (let index = 0; index < res.data.data.length; index++) {
            cleanser_tmp.push({
              cleanser: res.data.data[index],
            });
          }
          this.cleansers = cleanser_tmp;
        }
      });
    },
    return_rows_to_dataset() {
      this.$toast.add({
        severity: "info",
        summary: "Row Re-Addition is starting",
        detail: "Adding selected Rows will start shortly",
        life: 5000,
      });
      for (let index = 0; index < this.selectedCleanedRows.length; index++) {
        var element = this.selectedCleanedRows[index];
        var jsonString = JSON.stringify(element);
        this.$axios
          .post(
            "/return_to_dataset_cleaned_rows/" +
              this.new_created_dataset.cleaned_dataset.dataset_id,
            jsonString
          )
          .then(() => {
            this.$toast.add({
              severity: "success",
              summary: "Row Re-Addition was Succesul",
              detail:
                "Following Row was added:\n " +
                jsonString.substring(1, 130) +
                "......",
              life: 5000,
            });
          })
          .catch(() => {
            this.$toast.add({
              severity: "error",
              summary: "Row RE-Addition Unsuccessful",
              detail:
                "The selected Row could not be re-added! Check if Row is compatible with dataset",
              life: 5000,
            });
          });
      }
      if (this.selectedCleanedRows.length === 0) {
        this.$toast.add({
          severity: "warn",
          summary: "No Row selected",
          detail: "Please select a Row to re-add to dataset",
          life: 5000,
        });
      } else {
        this.close();
      }
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
      this.formData.append("access_user_list", this.toString("user"));
      this.formData.append("access_business_unit_list", this.toString("dep"));
      this.$axios
        .post("/create_dataset?uid=" + localStorage.loggedUser, this.formData)
        .then((res) => {
          this.new_created_dataset = res.data;
          if (
            this.new_created_dataset.cleaned_dataset["label"] ===
            "NO_LABEL_6aba48df0cb55992803d864977c3aa204520d659"
          ) {
            this.new_label = true;
          }
          if (this.delete_all_previous_versions) {
            this.delete_all_previous_versions_of_datasets();
            this.close();
          } else {
            this.close();
          }
          this.$toast.add({
            severity: "success",
            summary: "Dataset Creation Successful",
            detail: "The selected Dataset was created",
            life: 3000,
          });
        })
        .catch(() => {
          console.log("Here");

          this.$toast.add({
            severity: "error",
            summary: "Dataset Creation Unsuccessful",
            detail: "The selected Dataset could not be created",
            life: 3000,
          });
          this.submitted = false;
        });
    },
    assignLabel() {
      this.$axios
        .post(
          "/assign_label/" +
            this.new_created_dataset.cleaned_dataset.dataset_id +
            "/" +
            this.label_name
        )
        .then(() => {
          this.$toast.add({
            severity: "success",
            summary: "Label Creation Successful",
            detail:
              "The Label was created and assigned to your Dataset and will be assigned to any future similar Dataset automatically",
            life: 10000,
          });
          this.new_label = false;
          this.close();
        })
        .catch(() => {
          this.$toast.add({
            severity: "error",
            summary: "Label Creation Unuccessful",
            detail: "The Label could not have been assigned",
            life: 3000,
          });
          this.$emit("close");
        });
    },
    delete_all_previous_versions_of_datasets() {
      var label_of_dataset = this.new_created_dataset.cleaned_dataset.label;
      for (let index = 0; index < this.datasets_all.length; index++) {
        if (label_of_dataset === this.datasets_all[index].label) {
          this.$axios.delete(
            "/delete_dataset/" +
              this.datasets_all[index].dataset_id +
              "/" +
              this.datasets_all[index].storage_type
          );
        }
      }
    },
    close() {
      if (this.new_label) {
        this.cleaned_operation = false;
      } else {
        this.$emit("close");
      }
    },
    exportCSV() {
      this.$refs.dt.exportCSV();
    },
  },
};
</script>

<style>
label {
  margin-top: 5px;
  display: block;
}

.p-checkbox-icon {
  margin: 5px;
}

.p-field-checkbox {
  margin-top: 6px;
}

.p-grid {
  margin-top: 15px;
}

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

h2 {
  color: #111;
  font-family: "Open Sans Condensed", sans-serif;
  font-size: 28x;
  font-weight: 700;
  line-height: 28px;
  margin: 0 0 5px;
  padding: 0 5px;
  text-align: center;
  text-transform: uppercase;
}

h1 {
  color: #111;
  font-family: "Open Sans Condensed", sans-serif;
  font-size: 30x;
  font-weight: 700;
  line-height: 35px;
  margin: 0 0 5px;
  padding: 0 5px;
  text-align: center;
  text-transform: uppercase;
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
</style>