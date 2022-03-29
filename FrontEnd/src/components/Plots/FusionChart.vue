<template>
  <div>
    <fusioncharts
      :id="id"
      :type="type"
      :width="width"
      :height="height"
      :dataFormat="dataFormat"
      :dataSource="dataSource"
    >
    </fusioncharts>
  </div>
</template>

<script>
export default {
  props: ["data"],
  data() {
    return this.data;
  },
};
</script>