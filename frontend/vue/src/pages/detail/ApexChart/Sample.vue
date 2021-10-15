
<script>
import ws from "../../../../ws";
import { Line, mixins } from "vue-chartjs";
import "chartjs-plugin-streaming";

function createCountCPU() {}
createCountCPU();

const datasetColors = [
  {
    backgroundColor: "rgba(255, 99, 132, 0.5)",
    borderColor: "rgb(255, 99, 132)",
  },
  {
    backgroundColor: "rgba(54, 162, 235, 0.5)",
    borderColor: "rgb(54, 162, 235)",
  },
];

export default {
  extends: Line,
  mixins: [mixins.reactiveData],
  props: {
    data: Object,
  },
  name: "Sample",
  data() {
    return {
      machine: "",
      topic: "",
      value: 0,
      datasets: [],
      dataStreams: [],
    };
  },
  created() {
    this.subscribeCPUTopic();
    this.onMessage();
  },
  mounted() {
    this.createDataset().then((datasets) => {
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
                      let value = this.value;
                      dataset.data.push({
                        x: Date.now(),
                        y: value,
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
          interaction: {
            intersect: false,
          },
          maintainAspectRatio: false,
        }
      );
    });
  },
  methods: {
    /**
     * Function to subscribe broker topic
     */
    onMessage() {
      ws.on("message", (topic, message) => {
        const data = JSON.parse(message.toString());
        console.log("==>> Message of CPU: ", data, "Topic: ", topic);
      });
    },
    createDataset() {
      /**
       * Function create dataset first berofe render data in chart
       */
      return Promise.resolve().then(() => {
        console.log("DATA: ", this.d);
        const { cpus } = this.data.cpu;
        // TODO: GET payload from params
        let datasets = [];
        cpus.forEach((dataset, idx) => {
          datasets.push({
            label: dataset.cpu_name,
            backgroundColor: datasetColors[idx].backgroundColor,
            borderColor: datasetColors[idx].borderColor,
            cubicInterpolationMode: "monotone",
            fill: true,
            data: [],
          });
        });
        return datasets;
      });
    },

    subscribeCPUTopic() {
      return Promise.resolve()
        .then(() => {
          this.topic = `server/${this.$route.params.ip}/resources/cpu`;
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
  },
  beforeDestroy() {
    /**
     * Unsubscribe CPU event ( machine ) before navigate
     */
    console.log("this.machine.ip_address: ", this.machine.ip_address);
    ws.unsubscribe(this.topic, function (err, res) {
      if (err) {
        ws.publish("error", err);
        return;
      }
      console.log("Subscribe to topics res", res);
    });
  },
};
</script>

<style>
</style>