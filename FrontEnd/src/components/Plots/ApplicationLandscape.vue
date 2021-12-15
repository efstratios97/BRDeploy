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
  props: ["id", "data", "caption", "subCaption", "threshold"],
  data() {
    return {
      type: "treemap",
      width: "100%",
      height: "700",
      dataFormat: "json",
      dataSource: {
        chart: {
          animation: "0",
          hideTitle: "1",
          plotToolText: "<div><b>$label</b><br/><b>KPI : </b>$value</div>",
          horizontalPadding: "0",
          verticalPadding: "0",
          plotborderthickness: ".5",
          plotbordercolor: "ffffff",
          chartBottomMargin: "0",
          labelGlow: "0",
          labelFontColor: "ffffff",
          showLegend: "1",
          legendpadding: "0",
          legendItemFontSize: "10",
          legendItemFontBold: "1",
          legendPointerWidth: "8",
          legenditemfontcolor: "3d5c5c",
          legendScaleLineThickness: "0",
          legendCaptionFontSize: "10",
          algorithm: "squarified",
          caption: this.caption,
          theme: "fusion",
          subcaption: this.subcaption,
          showChildLabels: "1",
          exportEnabled: "1",
        },
        data: this.data,
        colorrange: {
          mapbypercent: "0",
          gradient: "1",
          minvalue: "0",
          maxvalue: this.threshold,
          code: "6baa01",
          startlabel: "Ideal",
          endlabel: "Alarming",
          color: [
            {
              code: "#ffba00",
              minvalue: this.threshold,
              maxvalue: this.threshold,
              label: "Threshold",
            },
            {
              code: "#cc0000",
              minvalue: this.threshold + 0.5,
              maxvalue: "10",
              label: "AVERAGE",
            },
          ],
        },
      },
    };
  },
  methods: {},
};
</script>
