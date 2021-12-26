
<script>
import ws from "../../../../ws";
import { Bubble, mixins } from "vue-chartjs";
import "chartjs-plugin-streaming";
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
    console.log("SOUUSSIU: ", this.data);
    this.onMessage();
  },
  mounted() {},
  methods: {
    /**
     * Function listener message from topic subscribed
     */
    onMessage() {
      ws.on("message", (topic, message) => {
        const data = JSON.parse(message.toString());
        if (topic == this.topic) {
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
  beforeDestroy() {
    // console.log("========> THIS.TOPIC: ", this.topic);
    // return Promise.resolve()
    //   .then(() => {
    //     ws.unsubscribe(this.topic, function (err, res) {
    //       if (err) {
    //         ws.publish("error", err);
    //         return;
    //       }
    //       console.log("Unsubscribe to topics res", res);
    //     });
    //   })
    //   .then(() => {
    //     console.log("UNSUBSCRIBE TOPIC SUCCESS");
    //   });
  },
  watch: {
    dataMachine: function (val) {
      console.log("Cursors network: ", val);
      this.topic = val.ip_address;
      this.subscribeNetworkTopic();
    },
  },
};
</script>

<style>
</style>