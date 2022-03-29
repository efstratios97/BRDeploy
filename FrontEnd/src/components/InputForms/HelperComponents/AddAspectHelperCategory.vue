<template>
  <div>
    <div class="p-grid p-fluid">
      <div class="p-col-12 p-md-12">
        <div class="p-inputgroup">
          <span class="p-inputgroup-addon">
            <b-icon-tag />
          </span>
          <Dropdown
            v-model="selected_operation_type"
            :options="operation_types"
            :filter="true"
            optionLabel="operation_type"
            placeholder="Assign Category to an Aspect"
            filterPlaceholder="Find Category"
            class="multiselect-custom"
            :showClear="true"
            :disabled="disabled_type"
            @change="send_operation_type()"
          />
        </div>
      </div>
    </div>
  </div>
</template>
<script>
export default {
  props: [
    "id",
    "selected_dataset_id",
    "selected_dataset_label",
    "operation_types",
  ],
  data() {
    return {
      selected_operation_type: "",
      disabled_type: false,
    };
  },
  methods: {
    send_operation_type() {
      this.$emit(
        "input-operation-type",
        this.selected_operation_type.operation_type
      );
    },
  },
};
</script>
