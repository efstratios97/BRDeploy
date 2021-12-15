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
  props: ["id", "data", "caption", "subCaption", "threshold", "color_coding"],
  data() {
    return {
      type: "angulargauge",
      width: "500",
      height: "300",
      dataFormat: "json",
      dataSource: {
        chart: {
          plotToolText: "Current Score: $value",
          theme: "fusion",
          caption: this.caption,
          subcaption: this.subcaption,
          lowerLimit: "0",
          upperLimit: "10",
          chartBottomMargin: "40",
          valueFontSize: "11",
          valueFontBold: "1",
          valueFontColor: "#000000",
          baseFontSize: 15,
          exportEnabled: "1",
          showValue: "1",
        },
        colorRange: {
          color: this.color_coding,
        },
        dials: {
          dial: [
            {
              value: this.data,
              showValue: 1,
            },
          ],
        },
        trendpoints: {
          point: [
            {
              startValue: this.threshold,
              displayValue: "Threshold: " + this.threshold,
              color: "#0075c2",
              thickness: "2",
              radius: "180",
              innerRadius: "82",
              alpha: "100",
              valueInside: "1",
              dashed: "0",
              dashLen: "2",
              dashGap: "1",
              trendValueDistance: "3",
              useMarker: "1",
              markerColor: "#F1f1f1",
              markerBorderColor: "#666666",
              markerRadius: "10",
              markerTooltext: "Threshold: " + this.threshold,
            },
          ],
        },
      },
    };
  },
  methods: {
    update_value(gauge_value) {
      var chartRef = FusionCharts(this.id),
        strData = "&value=" + gauge_value;
      chartRef.feedData(strData);
    },
  },
};
</script>