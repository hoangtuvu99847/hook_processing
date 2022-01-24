<script>
import {Line, mixins} from "vue-chartjs";
import "chartjs-plugin-streaming";
import ws from "../../../../ws";
import moment from "moment";
import {LOG_LEVEL} from "@/utils/constants";
import {DetailMachine} from "@/api/details";

export default {
  name: "RamChart",
  extends: Line,
  mixins: [mixins.reactiveData],
  props: {
    data: Object,
  },
  data() {
    return {
      datasets: [],
      count: 1,
      yGraphAxis: "",
      topic: ""
    };
  },
  created() {
    console.log('AAA: ', this.$props.data)
    this.getDetailMachine()
    this.onMessage();

  },
  computed: {
    dataProps: function () {
      console.log('AAA: ', this.$props.data)
      return this.$props.data
    },
    chartDataRender: function () {
      return this.chartData;
    },
  },

  mounted() {
  },
  methods: {
    onMessage() {
      ws.on("message", (topic, message) => {
        const data = JSON.parse(message.toString());

        if (topic === this.topic) {
          // console.log("==>> Message of RAM: ", data, "Topic: ", topic);
          let used = data.percent.toFixed(1);
          this.yGraphAxis = {
            used: used
          };
          this.$emit("used", used);
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
     * Get detail information machine
     */
    getDetailMachine() {
      const {id} = this.data
      DetailMachine(id).then((r) => {
        return r.data
      }).then(r => {
        const topic = r.ip_address
        this.subscribeRAMTopic(topic)
      }).then(() => {
        const datasets = [{
          label: "used",
          backgroundColor: 'rgba(255, 99, 132, 0.5)',
          borderColor: 'rgb(255, 99, 132)',
          fill: false,
          data: []
        }]
        this.renderRAMChart(datasets)
      })
    },

    /**
     * Function subscribe topic in MQTT broker
     */
    subscribeRAMTopic(topic) {
      return Promise.resolve()
          .then(() => {
            this.topic = `server/${topic}/resources/ram`;
          })
          .then(() => {
            ws.subscribe(this.topic, function (err, res) {
              if (err) {
                ws.publish("error", err);
                return;
              }
              console.log("Subscribe to topics res", res);
            });
          })
    },
    renderRAMChart(datasets) {
      this.renderChart(
          {
            datasets: datasets,
          },
          {
            scales: {
              xAxes: [
                {
                  type: "realtime",
                  realtime: {
                    delay: 1000,
                    onRefresh: (chart) => {
                      chart.data.datasets.forEach((dataset) => {
                        dataset.data.push({
                          x: Date.now(),
                          y: this.yGraphAxis[dataset.label],
                        });
                      });
                    },
                  },
                },
              ],
              yAxes: [
                {
                  ticks: {
                    min: 0,
                    max: 100,
                    stepSize: 20,
                  },
                },
              ],
            },
            maintainAspectRatio: false,
          }
      );
    },
  },
  beforeDestroy() {

  },
  watch: {},
};
</script>
