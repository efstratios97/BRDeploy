<template>
  <div>
    <div class="p-fluid">
      <h1 class="h1_widget">Statistical Analysis</h1>
      <Card>
        <template v-slot:title> Input Values </template>
        <template v-slot:subtitle> Set all Plot Inputs </template>
        <template v-slot:content>
          <form>
            <div class="p-fluid p-formgrid p-grid p-jc-center">
              <div class="p-field p-col-3 p-sm-3">
                <label for="bu">Business Units</label>
                <MultiSelect
                  v-model="business_units"
                  :options="business_units_options"
                  optionLabel="bu"
                  placeholder="Select BUs"
                  :filter="true"
                  class="multiselect-custom"
                >
                  <template #value="slotProps">
                    <div
                      class="country-item selected-item-value"
                      v-for="option of slotProps.value"
                      :key="option.bu"
                    >
                      <div>{{ option.bu }}</div>
                    </div>
                    <template
                      v-if="!slotProps.value || slotProps.value.length === 0"
                    >
                      Select Departments
                    </template>
                  </template>
                  <template #option="slotProps">
                    <div class="country-item">
                      <div>{{ slotProps.option.bu }}</div>
                    </div>
                  </template>
                </MultiSelect>
              </div>
              <div class="p-field p-col-3 p-sm-3">
                <label for="bc">Business Capabilities</label>
                <MultiSelect
                  v-model="business_capabilities"
                  :options="business_capabilities_options"
                  optionLabel="bc"
                  placeholder="Select BCs"
                  :filter="true"
                  class="multiselect-custom"
                >
                  <template #value="slotProps">
                    <div
                      class="country-item selected-item-value"
                      v-for="option of slotProps.value"
                      :key="option.bc"
                    >
                      <div>{{ option.bc }}</div>
                    </div>
                    <template
                      v-if="!slotProps.value || slotProps.value.length === 0"
                    >
                      Select Business Capabilities
                    </template>
                  </template>
                </MultiSelect>
              </div>
              <div class="p-field p-col-3 p-sm-3">
                <label for="bubble_y_axis">Y axis</label>
                <Dropdown
                  v-model="bubble_y_axis"
                  :options="bubble_y_axis_options"
                  optionLabel="bubble_y_axis"
                  placeholder="Select a Y Axis Value"
                  :filter="true"
                  filterPlaceholder="Find available Parameters"
                  :showClear="true"
                />
              </div>
              <div class="p-field p-col-3 p-sm-3">
                <label for="top">Top</label>
                <Dropdown
                  v-model="range"
                  :options="range_options"
                  optionLabel="range"
                  placeholder="Select a Range"
                  :filter="true"
                  filterPlaceholder="Find available Parameters"
                  :showClear="true"
                />
              </div>
              <div class="p-field p-col-3 p-sm-3">
                <label for="sorting">Sort</label>
                <Dropdown
                  v-model="sorting"
                  :options="sorting_options"
                  optionLabel="sorting"
                  placeholder="Select a Sorting Order"
                  :filter="true"
                  filterPlaceholder="Find available Parameters"
                  :showClear="true"
                />
              </div>
            </div>
          </form>
        </template>
        <template v-slot:footer>
          <Button
            label="Submit"
            icon="pi pi-check"
            iconPos="right"
            @click="send_inputs"
          />
        </template>
      </Card>
    </div>
    <br />
    <Card>
      <template v-slot:title> Statistics Plot</template>
      <template v-slot:subtitle> View powered by Python </template>
      <template v-slot:content>
        <div class="container">
          <div class="row">
            <div class="col d-flex justify-content-center">
              <div v-html="html" style="resize: both; overflow: auto"></div>
            </div>
          </div>
        </div>
      </template>
    </Card>
  </div>
</template>

<script>
export default {
  props: ["selected_dataset_id", "selected_dataset_label"],
  data() {
    return {
      // selected_dataset_id: "",
      // selected_dataset_label: "",
      business_units_options: [],
      business_units: [],
      business_capabilities: [],
      business_capabilities_options: [],
      bubble_y_axis: "",
      bubble_y_axis_options: [],
      range: "",
      range_options: [],
      sorting: "",
      sorting_options: [],
      html: this.show_graph(),
      params: this.get_params(),
    };
  },
  methods: {
    // normalize_selected_dataset() {
    //   this.selected_dataset_id = this.selected_dataset.dataset_id;
    //   this.selected_dataset_label = this.selected_dataset.dataset_label;
    // },
    show_graph() {
      const bokehVersion = "2.3.1";
      let link = document.createElement("link");
      link.setAttribute("rel", "stylesheet");
      link.setAttribute(
        "href",
        "https://cdn.bokeh.org/bokeh/release/bokeh-0.13.0" + ".min.css"
      );
      link.setAttribute("type", "text/css");
      document.head.appendChild(link);

      let script = document.createElement("script");
      // Insert js code in the header
      script.setAttribute(
        "src",
        "https://cdn.bokeh.org/bokeh/release/bokeh-" + bokehVersion + ".min.js"
      );
      script.async = "async";
      document.head.appendChild(script);

      // cdn js is loaded after requesting bokeh parameters
      script.onload = () => {
        this.$axios
          .get(
            "/show_plotter/" + this.selected_dataset_id + "/simple_statistics"
          )
          .then((response) => {
            this.html = response.data.div;
            // insert drawing script code
            let bokehRunScript = document.createElement("SCRIPT");
            bokehRunScript.setAttribute("type", "text/javascript");
            let t = document.createTextNode(response.data.script);
            bokehRunScript.appendChild(t);
            document.body.appendChild(bokehRunScript);
            // Close the wait screen after the drawing code is executed
            // _this.loading = false;
          })
          .catch(() => {
            this.$toast.add({
              severity: "error",
              summary: "Not suitable Dataset",
              detail:
                "The chosen Dataset is not suitable for this data analysis",
              life: 5000,
            });
          });
      };
    },
    get_params() {
      this.$axios.get("/get_params/" + this.selected_dataset_id).then((res) => {
        this.params = res.data;
        for (let index = 0; index < res.data.list_bu.length; index++) {
          this.business_units_options.push({ bu: res.data.list_bu[index] });
        }
        for (let index = 0; index < res.data.list_bc.length; index++) {
          this.business_capabilities_options.push({
            bc: res.data.list_bc[index],
          });
        }
        for (let index = 0; index < res.data.bubble_y_axis.length; index++) {
          this.bubble_y_axis_options.push({
            bubble_y_axis: res.data.bubble_y_axis[index],
          });
        }
        for (let index = 0; index < res.data.range.length; index++) {
          this.range_options.push({
            range: res.data.range[index],
          });
        }
        for (let index = 0; index < res.data.sorting.length; index++) {
          this.sorting_options.push({
            sorting: res.data.sorting[index],
          });
        }
      });
    },
    send_inputs() {
      let business_units = [];
      let business_capabilities = [];
      for (let index = 0; index < this.business_units.length; index++) {
        business_units.push(this.business_units[index]["bu"]);
      }
      for (let index = 0; index < this.business_capabilities.length; index++) {
        business_capabilities.push(this.business_capabilities[index]["bc"]);
      }
      var user_input = {
        responsible_unit: business_units,
        supported_bc: business_capabilities,
        bubble_y_axis: this.bubble_y_axis.bubble_y_axis,
        sorting: this.sorting.sorting,
        top: this.range.range,
      };
      const jsonString = JSON.stringify(user_input);
      this.$axios
        .post(
          "/post_inputs/" + this.selected_dataset_id + "/simple_statistics",
          jsonString
        )
        .then((response) => {
          this.html = response.data.div;
          let bokehRunScript = document.createElement("SCRIPT");
          bokehRunScript.setAttribute("type", "text/javascript");
          let t = document.createTextNode(response.data.script);
          bokehRunScript.appendChild(t);
          document.body.appendChild(bokehRunScript);
        })
        .catch(() => {
          this.$toast.add({
            severity: "error",
            summary: "Input Incomplete",
            detail: "Please select all Input fields",
            life: 3000,
          });
        });
    },
  },
};
</script>
<style src="@vueform/multiselect/themes/default.css">
</style>
<style scoped>
.h1_widget {
  text-align: center;
  color: black;
  padding-bottom: 10px;
}
.h3_widget {
  text-align: center;
  color: black;
}

button {
  width: 250px;
  height: 35px;
  background: #fff;
  border: 1px solid dodgerblue;
  cursor: pointer;
  border-radius: 2px;
  color: #050504;
  font-family: "Exo", sans-serif;
  font-size: 16px;
  font-weight: 400;
  padding: 6px;
  margin-top: 10px;
}

button:hover {
  opacity: 0.8;
}

.p-multiselect {
  max-width: 800px;
}

.p-multiselect-label:not(.p-placeholder) {
  padding-top: 0.25rem;
  padding-bottom: 0.25rem;
}
.selected-item-value {
  padding: 0.25rem 0.5rem;
  border-radius: 3px;
  /* display: inline-block; */
  margin-bottom: 0.5rem;
  background-color: var(--primary-color);
  color: var(--primary-color-text);
}

@media screen and (max-width: 900px) {
  .p-multiselect {
    width: 100%;
  }
}
.label-form {
  text-align: center;
}
.p-card {
  width: 250vh;
}
</style>