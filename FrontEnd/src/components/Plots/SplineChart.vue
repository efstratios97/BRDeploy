<template>
  <div>
    <fusioncharts
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
  props: ["id", "data"],
  data() {
    return {
      type: "line",
      width: "100%",
      height: "300",
      dataFormat: "json",
      dataSource: this.data,
    };
  },
};
</script>
