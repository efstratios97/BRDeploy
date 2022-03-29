<template>
  <div>
    <div
      :class="
        altClass === undefined ? 'p-grid p-fluid p-justify-between' : altClass
      "
      :style="altStyle === undefined ? '' : altStyle"
    >
      <Button
        :label="altLabel === undefined ? 'Click me' : altLabel"
        @click="buttonClick()"
        :icon="altIcon === undefined ? 'pi pi-replay' : altIcon"
        :class="
          altButtonClass === undefined ? 'p-button-raised' : altButtonClass
        "
        :style="altButtonStyle === undefined ? '' : altButtonStyle"
        :iconPos="altIconPos === undefined ? 'left' : altIconPos"
      />
    </div>
  </div>
</template>

<script>
export default {
  props: [
    "altLabel",
    "altClass",
    "altStyle",
    "altButtonClass",
    "altIcon",
    "altIconPos",
    "altButtonStyle",
  ],
  data() {
    return {};
  },
  methods: {
    buttonClick() {
      this.$emit("button-click", { pageIndex: 1 });
    },
  },
};
</script>