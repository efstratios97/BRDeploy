<template>
  <div>
    <form>
      <div class="p-grid p-fluid">
        <div class="p-col-12 p-md-12">
          <div class="p-inputgroup">
            <span class="p-inputgroup-addon">
              <i class="pi pi-users"></i>
            </span>
            <MultiSelect
              v-model="selected_executive_dashboards"
              :options="executive_dashboards"
              :filter="true"
              optionLabel="executive_dashboard.name"
              placeholder="Assign Plot to Executive Dashboard"
              filterPlaceholder="Find Executive Dashboards"
              class="multiselect-custom"
            />
          </div>
        </div>
      </div>
      <div class="p-grid p-fluid">
        <div class="p-col-12 p-md-12">
          <div class="p-inputgroup">
            <span class="p-inputgroup-addon">
              <i class="pi pi-database"></i>
            </span>
            <Dropdown
              v-model="selected_visualization_right"
              :options="visualization_rights"
              :filter="true"
              optionLabel="visualization_right.name"
              placeholder="Select Visualization right"
              filterPlaceholder="Find Visualization Rights"
            />
          </div>
        </div>
      </div>
      <div class="p-grid p-fluid">
        <div class="p-col-12 p-md-12">
          <Button
            label="Assign Visualization to Dashboard"
            icon="pi pi-plus-circle"
            iconPos="center"
            @click="save_plot_to_dashboard"
          />
        </div>
      </div>
    </form>
  </div>
</template>

<script>
export default {
  props: [
    "formdata",
    "visualization",
    "grouped",
    "component_name",
    "separated_display",
  ],
  data() {
    return {
      executive_dashboards: this.getExecutiveDashboardOptions(),
      selected_executive_dashboards: "",
      selected_visualization_right: "",
      visualization_rights: this.getVisualizationRightsOptions(),
    };
  },
  methods: {
    getVisualizationRightsOptions() {
      this.$axios.get("/get_visualization_rights").then((res) => {
        var visualization_rights_tmp = [];
        for (let index = 0; index < res.data.length; index++) {
          visualization_rights_tmp.push({
            visualization_right: res.data[index],
          });
        }
        this.visualization_rights = visualization_rights_tmp;
      });
    },
    getExecutiveDashboardOptions() {
      this.$axios.get("/get_executive_dashboards").then((res) => {
        var executive_dashboards_tmp = [];
        for (let index = 0; index < res.data.data.length; index++) {
          executive_dashboards_tmp.push({
            executive_dashboard: res.data.data[index],
          });
        }
        this.executive_dashboards = executive_dashboards_tmp;
      });
    },
    save_plot_to_dashboard() {
      for (
        let index = 0;
        index < this.selected_executive_dashboards.length;
        index++
      ) {
        var formdata = new FormData();
        formdata.append("formdata", JSON.stringify(this.formdata));
        formdata.append("grouped", this.grouped);
        formdata.append("visualization_type", this.visualization);
        formdata.append(
          "visualization_right",
          this.selected_visualization_right.visualization_right.name
        );
        formdata.append("component_name", this.component_name);
        formdata.append("separated_display", this.separated_display);
        var executive_dashboard_id =
          this.selected_executive_dashboards[index].executive_dashboard
            .executive_dashboard_id;
        this.$axios
          .post("/create_plot/" + executive_dashboard_id, formdata)
          .then(() => {
            this.$toast.add({
              severity: "success",
              summary: "Plot Creation Successful",
              detail: "The Plot was created",
              life: 3000,
            });
          })
          .catch(() => {
            this.$toast.add({
              severity: "error",
              summary: "Plot Creation Unsuccessful",
              detail: "The Plot Creation was Unsuccessful",
              life: 3000,
            });
            this.submitted = false;
          });
      }
      this.$emit("close");
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