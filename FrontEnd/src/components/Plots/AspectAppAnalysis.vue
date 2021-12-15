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
  props: ["id", "data", "caption", "subCaption"],
  data() {
    return {
      type: "column2d",
      width: "500",
      height: "300",
      dataFormat: "json",
      dataSource: {
        // Chart Configuration
        chart: {
          caption: this.caption, //Set the chart caption
          subCaption: this.subCaption, //Set the chart subcaption
          xAxisName: "Aspect", //Set the x-axis name
          yAxisName: "Score", //Set the y-axis name
          numberSuffix: "",
          theme: "fusion", //Set the theme for your chart
          yAxisMaxValue: "10",
          yAxisMinValue: "0",
          exportEnabled: "1",
        },
        data: this.data,
        //     trendlines: [
        //       {
        //         line: [
        //           {
        //             startvalue: "175000",
        //             color: "#29C3BE",
        //             isTrendZone: "1",
        //             displayvalue: "Target - $175K",
        //           },
        //         ],
        //       },
        //     ],
      },
    };
  },
};
</script>


