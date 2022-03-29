<template>
  <div>
    <br />
    <div class="p-grid">
      <div class="p-col-4 p-offset-4">
        <div class="p-fluid">
          <Button
            label="Apply"
            @click="render_graphs()"
            icon="pi pi-check"
            iconPos="right"
          />
        </div>
      </div>
    </div>
  </div>
</template> 
      
<script>
export default {
  props: ["formdata", "inputfields_number"],
  data() {
    return {};
  },
  methods: {
    render_graphs() {
      if (Object.keys(this.formdata).length === this.inputfields_number) {
        this.$emit("render", { render: true, formdata: this.formdata });
      } else {
        this.$toast.add({
          severity: "warn",
          summary: "No Parameter chosen",
          detail:
            "Please select first the Parameter in all of the input fields",
          life: 8000,
        });
      }
    },
  },
};
</script>
