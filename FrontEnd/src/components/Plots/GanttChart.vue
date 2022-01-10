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
      type: "gantt",
      width: "100%",
      height: "1500",
      dataFormat: "json",
      dataSource: this.data,
    };
  },
};
</script>
