<script>
import { Doughnut } from "vue-chartjs";
import ws from "../../../../ws";
import moment from "moment";
import { LOG_LEVEL } from "../../../utils/constants";

export default {
  name: "RamChart",
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
    console.log("this.machine: ", this.$route.params);
    console.log("Da: ", this.data);
    this.onMessage();
  },
  computed: {
    chartDataRender: function () {
      return this.chartData;
    },
  },

  mounted() {
    this.renderRAMChart();
  },
  methods: {
    onMessage() {
      ws.on("message", (topic, message) => {
        const data = JSON.parse(message.toString());
        if (topic == this.topic) {
          console.log("==>> Message of RAM: ", data, "Topic: ", topic);
          let used = data.percent.toFixed(1);
          let remain = (100 - used).toFixed(1);
          if (used !== this.chartData[0]) {
            this.$set(this.chartData, 0, used);
          }
          if (remain !== this.chartData[1]) {
            this.$set(this.chartData, 1, remain);
          }
          // Emit message when overload
          if (used >= 80 && used < 100) {
            const msg = {
              text: `${used}% RAM at ${moment().format()}`,
              type: LOG_LEVEL.WARNING,
            };
            this.$emit("overload", msg);
          }
          if (used >= 100) {
            const msg = {
              text: `RAM overload at ${moment().format()}`,
              type: LOG_LEVEL.DANGER,
            };
            this.$emit("overload", msg);
          }
        }
      });
    },
    /**
     * Get detail RAM instance of machine
     */
    getRAMMachine() {},
    /**
     * Function subscribe topic in MQTT broker
     */
    subscribeRAMTopic() {
      return Promise.resolve()
        .then(() => {
          this.topic = `server/${this.topic}/resources/ram`;
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
    renderRAMChart() {
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
    return Promise.resolve()
      .then(() => {
        ws.unsubscribe(this.topic, function (err, res) {
          if (err) {
            ws.publish("error", err);
            return;
          }
          console.log("Unsubscribe to topics res", res);
        });
      })
      .then(() => {
        console.log("UNSUBSCRIBE TOPIC SUCCESS");
      });
  },
  watch: {
    data: function (val) {
      console.log("Cursors: ", val);
      this.topic = val.ip_address;
      this.subscribeRAMTopic();
    },
    chartData: function (val) {
      console.log("CHART: ", val);
      this.renderRAMChart();
    },
  },
};
</script>
