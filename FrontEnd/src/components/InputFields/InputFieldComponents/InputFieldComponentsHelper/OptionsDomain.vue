<template>
  <div class="p-fluid">
    <span v-if="multiple_options">
      <MultiSelect
        v-model="selected_domain"
        :options="domains"
        :filter="true"
        :maxSelectedLabels="5"
        optionLabel="domain"
        placeholder="Select Domain"
        filterPlaceholder="Find a Domain"
        @change="send_domain()"
      />
    </span>
    <span v-else>
      <Dropdown
        v-model="selected_domain"
        :options="domains"
        :filter="true"
        optionLabel="domain"
        placeholder="Select Domain"
        filterPlaceholder="Find a Domain"
        @change="send_domain()"
      />
    </span>
  </div>
</template>
<script>
export default {
  props: ["domains", "multiple_options"],
  data() {
    return {
      selected_domain: "",
    };
  },
  methods: {
    send_domain() {
      this.$emit("input-parameter", this.selected_domain);
    },
  },
};
</script>