<script>
import ws from "../../../../ws";
import {Bubble, mixins} from "vue-chartjs";
import "chartjs-plugin-streaming";
import {DetailMachine} from "@/api/details";
// import { GraphLineColor } from "../../../utils/commonColor";

export default {
  name: "NetworkChart",
  extends: Bubble,
  mixins: [mixins.reactiveData],
  props: {
    dataMachine: Object,
  },
  data() {
    return {
      datasets: [],
      count: 1,
      yGraphAxis: "",
      topic: "",
    };
  },
  created() {
    this.getDetailMachine()
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
          console.log("==>> Message of Network: ", data, "Topic: ", topic);
        }
      });
    },

    /**
     * Function subscribe topic in MQTT broker
     */
    subscribeNetworkTopic() {
      return Promise.resolve()
          .then(() => {
            this.topic = `server/${this.topic}/resources/network`;
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
    renderNetworkChart(datasets) {
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
                          r: 5,
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
};
</script>

<style>
</style>
