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
      dataSource: {
        chart: {
          caption: "Applications Lifecycle Overview",
          yaxisname: "# of Application to Shut-Down",
          anchorradius: "3",
          plottooltext: "# App shut-Downs in $label is <b>$dataValue</b>",
          showhovereffect: "1",
          showvalues: "0",
          theme: "fusion",
          anchorbgcolor: "#72D7B2",
          palettecolors: "#72D7B2",
          yAxisMinValue: 0,
          exportEnabled: 1,
        },
        data: this.data,
      },
    };
  },
};
</script>
