<template>
  <div class="p-fluid">
    <span v-if="multiple_options">
      <MultiSelect
        v-model="selected_department"
        :options="departments"
        :filter="true"
        :maxSelectedLabels="5"
        optionLabel="dep"
        placeholder="Select Department"
        filterPlaceholder="Find a Departmet"
        @change="send_departments"
      />
    </span>
    <span v-else>
      <Dropdown
        v-model="selected_department"
        :options="departments"
        :filter="true"
        optionLabel="dep"
        placeholder="Select Department"
        filterPlaceholder="Find a Departmet"
        @change="send_departments"
      />
    </span>
  </div>
</template>
<script>
export default {
  props: ["departments", "multiple_options"],
  data() {
    return {
      selected_department: "",
    };
  },
  methods: {
    send_departments() {
      this.disabled_depInfo = false;
      this.$emit("input-parameter", this.selected_department);
    },
  },
};
</script>