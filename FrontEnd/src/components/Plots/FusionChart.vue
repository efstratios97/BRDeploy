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
import { FCComponent } from "vue-fusioncharts";

export default {
  components: { fusioncharts: FCComponent },
  props: ["data"],
  data() {
    return this.data;
  },
};
</script>