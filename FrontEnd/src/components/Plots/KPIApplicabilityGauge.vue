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
  props: [
    "id",
    "selected_component",
    "selected_parameter",
    "width",
    "height",
    "gauge_type",
  ],
  data() {
    return {
      type: this.gauge_type,
      // width: this.width,
      // height: this.height,
      dataFormat: "json",
      dataSource: {
        chart: {
          theme: "fusion",
          caption: "Applicability Analysis",
          subcaption: "Current Data Status of " + this.selected_component,
          lowerLimit: "0",
          upperLimit: "100",
          numberSuffix: "%",
          chartBottomMargin: "40",
          valueFontSize: "11",
          valueFontBold: "1",
          valueFontColor: "#000000",
          baseFontSize: 15,
          exportEnabled: "1",
        },
        colorRange: {
          color: [
            {
              minValue: "0",
              maxValue: "40",
              label: "Low",
              code: "#cc0000",
            },
            {
              minValue: "40",
              maxValue: "60",
              label: "Moderate",
              code: "#ffba00",
            },
            {
              minValue: "60",
              maxValue: "100",
              label: "High",
              code: "#228b22",
            },
          ],
        },
        pointers: {
          pointer: [
            {
              value: "0",
            },
          ],
        },
        annotations: {
          origw: "400",
          origh: "190",
          autoscale: "1",
          groups: [
            {
              id: "range",
              items: [
                {
                  id: "rangeBg",
                  type: "rectangle",
                  x: "$chartCenterX-115",
                  y: "$chartEndY-35",
                  tox: "$chartCenterX +115",
                  toy: "$chartEndY-15",
                  fillcolor: "#0075c2",
                },
                {
                  id: "rangeText",
                  type: "Text",
                  fontSize: "15",
                  fillcolor: "#ffffff",
                  text: "Recommended Data Status : >40%",
                  x: "$chartCenterX",
                  y: "$chartEndY-25",
                },
              ],
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
