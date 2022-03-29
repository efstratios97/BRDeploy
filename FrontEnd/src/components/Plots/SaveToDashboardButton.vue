<template>
  <div>
    <br />
    <div class="p-grid">
      <div class="p-col-4 p-offset-4">
        <div class="p-fluid">
          <Button
            label="Save to Dashboard"
            @click="show_add_to_dashboard()"
            icon="pi pi-save"
            iconPos="right"
            class="p-button-info"
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
    show_add_to_dashboard() {
      this.$emit("show_add_to_dashboard");
    },
  },
};
</script>
