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
            :placeholder="operation_type_placeholder"
            filterPlaceholder="Find Category"
            class="multiselect-custom"
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
    "operation_type",
  ],
  data() {
    return {
      selected_operation_type: "",
      operation_type_placeholder: "",
      disabled_type: false,
    };
  },
  created() {
    this.selected_operation_type = this.operation_type;
    this.operation_type_placeholder = this.operation_type;
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
