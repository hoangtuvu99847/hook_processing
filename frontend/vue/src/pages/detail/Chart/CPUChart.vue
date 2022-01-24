<script>
import ws from "../../../../ws";
import {Line, mixins} from "vue-chartjs";
import "chartjs-plugin-streaming";
import {DetailCPU} from "@/api/details";
import {GraphLineColor} from "@/utils/commonColor";
import {LOG_LEVEL} from "@/utils/constants";
import moment from "moment";

function createCountCPU() {
}

createCountCPU();

export default {
  name: "CpuChart",
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
    };
  },
  created() {
    this.getCPUMachine();
    this.onMessage();
  },
  mounted() {
  },
  methods: {
    /**
     * Function listener message from topic subscribed
     */
    onMessage() {
      ws.on("message", (topic, message) => {
        const data = JSON.parse(message.toString());
        if (topic === this.topic) {
          // console.log("==>> Message of CPU: ", data, "Topic: ", topic);
          let line = {};
          data.cpus.map((cpu) => {
            line[cpu.cpu_name] = cpu.percent;
          });
          this.yGraphAxis = line;
          this.$emit("avg", data.avg);
          // Send log when CPU is overload
          if (data.avg > 80 && data.avg < 100) {
            const now = moment().format();
            const msg = {
              text: `${data.avg} % CPU at ${now}`,
              type: LOG_LEVEL.WARNING,
            };
            this.$emit("overload", msg);
          } else if (data.avg === 100) {
            const now = moment().format();
            const msg = {
              text: `CPU Overload at ${now}`,
              type: LOG_LEVEL.DANGER,
            };
            this.$emit("overload", msg);
          }
        }
      });
    },
    /**
     * Get detail CPU instance of machine
     */
    getCPUMachine() {
      const {id} = this.data;
      DetailCPU(id)
          .then((response) => {
            return response.data;
          })
          .then((r) => {
            this.datasets = r.data; // List CPU name
            return r;
          })
          .then((r) => {
            const topic = r.ip_address;
            this.subscribeCPUTopic(topic);
          })
          .then(() => {
            const datasets = this.datasets.map((dataset) => ({
              label: dataset,
              fill: false,
              tension: 0.1,
              borderColor: GraphLineColor[dataset].borderColor,
              backgroundColor: GraphLineColor[dataset].backgroundColor,
              data: [],
            }));
            this.renderCPUChart(datasets);
          });
    },
    /**
     * Function subscribe topic in MQTT broker
     */
    subscribeCPUTopic(topic) {
      return Promise.resolve()
          .then(() => {
            this.topic = `server/${topic}/resources/cpu`;
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
    renderCPUChart(datasets) {
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

<style>
</style>
