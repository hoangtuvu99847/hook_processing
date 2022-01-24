<script>
import {Doughnut} from "vue-chartjs";
import ws from "../../../../ws";

export default {
  name: "DiskChart",
  extends: Doughnut,
  props: {
    data: Object,
  },
  data() {
    return {
      chartData: [0, 100],
      chartdataRAM: {
        labels: ["Used", "Free"],
        datasets: [
          {
            label: "My First Dataset",
            data: this.chartDataRender,
            backgroundColor: ["rgb(255, 99, 132)", "rgb(54, 162, 235)"],
            hoverOffset: 4,
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        elements: {
          line: {
            borderWidth: 3,
          },
        },
      },
      topic: "",
    };
  },
  created() {
    this.onMessage();
  },
  computed: {
    chartDataRender: function () {
      return this.chartData;
    },
  },

  mounted() {
    this.renderDiskChart();
  },
  methods: {
    onMessage() {
      ws.on("message", (topic, message) => {
        const data = JSON.parse(message.toString());
        if (topic === this.topic) {
          let used = data.percent.toFixed(1);
          let remain = (100 - used).toFixed(1);

          this.$emit("statistical", {used: data.used, free: data.free})
          if (used !== this.chartData[0]) {
            this.$set(this.chartData, 0, used);
          }
          if (remain !== this.chartData[1]) {
            this.$set(this.chartData, 1, remain);
          }

        }
      });
    },
    /**
     * Function subscribe topic in MQTT broker
     */
    subscribeRAMTopic() {
      return Promise.resolve()
          .then(() => {
            this.topic = `server/${this.topic}/resources/disk`;
          })
          .then(() => {
            ws.subscribe(this.topic, function (err, res) {
              if (err) {
                ws.publish("error", err);
                return;
              }
              console.log("Subscribe to topics res", res);
            });
          });
    },
    renderDiskChart() {
      this.renderChart(
          {
            labels: ["Used", "Free"],
            datasets: [
              {
                label: "My First Dataset",
                data: this.chartDataRender,
                backgroundColor: ["rgb(255, 99, 132)", "rgb(54, 162, 235)"],
                hoverOffset: 4,
              },
            ],
          },
          {
            responsive: true,
            maintainAspectRatio: false,
            elements: {
              line: {
                borderWidth: 3,
              },
            },
          }
      );
    },
  },
  beforeDestroy() {
  },
  watch: {
    data: function (val) {
      console.log("Cursors: ", val);
      this.topic = val.ip_address;
      this.subscribeRAMTopic();
    },
    chartData: function (val) {
      console.log("CHART: ", val);
      this.renderDiskChart();
    },
  },
};
</script>
