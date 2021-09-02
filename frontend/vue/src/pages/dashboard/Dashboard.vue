<template>
  <div>
    <div class="row px-2">
      <div
        class="card shadow"
        :class="[server.status === 'OFF' && 'border-danger']"
        v-for="(server, idx) in lstServer"
        :key="idx"
        style="width: 18rem; margin-right: 20px; margin-bottom: 20px"
      >
        <div class="card-body">
          <div class="d-flex bd-highlight">
            <h5 class="card-title">{{ server.hostname }}</h5>
            <div class="ms-auto bd-highlight">
              <a class="btn btn-sm btn-outline-primary" @click="detail(server)"
                >Details</a
              >
            </div>
          </div>
          <div class="mb-2">
            <div v-if="server.status === 'OFF'">
              <i class="fas fa-exclamation-triangle text-danger"></i>
              Disconnected
            </div>
            <div v-else>
              <i class="fas fa-signal text-success"></i> Connected
            </div>
          </div>
          <h6 class="card-subtitle mb-2 text-muted">{{ server.ip_address }}</h6>
          <!-- <div class="row">
            <div class="col">
              <div>
                <div style="margin-left: 30px">
                  <span class="text-muted pl-4" style="font-size: 80%">
                    CPU</span
                  >
                </div>
                <i class="fas fa-microchip text-success fa-lg"></i>
                <span
                  class="font-weight-bold text-danger"
                  style="margin-left: 10px"
                >
                  {{ server.cpu.cpu_avg }} %</span
                >
              </div>
            </div>
            <div class="col">
              <div>
                <div style="margin-left: 30px">
                  <span class="text-muted pl-4" style="font-size: 80%">
                    RAM</span
                  >
                </div>
                <i class="fas fa-memory text-info fa-lg"></i>
                <span
                  class="font-weight-bold text-danger"
                  style="margin-left: 8px"
                  >{{ server.ram.percent }}%</span
                >
              </div>
            </div>
          </div>
          <div class="row py-2">
            <div class="col">
              <div>
                <div style="margin-left: 30px">
                  <span class="text-muted pl-4" style="font-size: 80%">
                    DISK</span
                  >
                </div>
                <i class="fas fa-hdd text-primary fa-lg"></i>
                <span
                  class="font-weight-bold text-danger"
                  style="margin-left: 8px"
                  >{{ server.disk.percent }}%</span
                >
              </div>
            </div>
            <div class="col">
              <div>
                <div style="margin-left: 30px">
                  <span class="text-muted pl-4" style="font-size: 80%">
                    TEMPRATURE</span
                  >
                </div>
                <i
                  class="fas fa-thermometer-three-quarters fa-lg text-danger"
                  style="margin-left: 5px"
                ></i>
                <span
                  class="font-weight-bold text-danger"
                  style="margin-left: 17px"
                  >{{ server.disk.percent }}%</span
                >
                <div></div>
              </div>
            </div>
          </div> -->
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import mqtt from "mqtt";
import { listServer } from "../../api/dashboard";

export default {
  name: "Dashboard",
  components: {},
  computed: {},
  data() {
    return {
      lstServer: [],
      client: {
        connected: false,
      },
      connection: {
        host: process.env.VUE_APP_HOST,
        port: process.env.VUE_APP_BROKER_PORT,
        endpoint: "/mqtt",
        clean: true, // Reserved session
        connectTimeout: 4000, // Time out
        reconnectPeriod: 4000, // Reconnection interval
      },
      subscribeSuccess: false,
    };
  },
  created() {
    this.createConnection();
  },
  methods: {
    /**
     * Function init connection connect MQTT
     */
    createConnection() {
      const { host, port, endpoint, ...options } = this.connection;
      const connectUrl = `ws://${host}:${port}${endpoint}`;
      try {
        this.client = mqtt.connect(connectUrl, options);
      } catch (error) {
        console.log("mqtt.connect error", error);
      }
      this.client.on("connect", () => {
        console.log("Connection succeeded!");
        this.handleGetListServer();
      });
      this.client.on("error", (error) => {
        console.log("Connection failed", error);
      });
      this.client.on("message", (topic, message) => {
        const data = JSON.parse(message.toString());
        console.log(data);
      });
    },
    /**
     * Function handle MQTT events
     * @param {Array} topics - List topic subscribe
     */
    handleEventMQTT(topics) {
      // MQTT Client connect event
      topics.forEach((ip) => {
        const topic = `server/${ip}/resources/#`;
        this.client.subscribe(topic, function (err, res) {
          if (err) {
            this.client.publish("error", "Hello mqtt");
            return;
          }
          // this.subscribeSuccess = true;
          console.log("Subscribe to topics res", res);
        });
      });
    },

    /**
     * Function fetch all server connected to broker
     */
    handleGetListServer() {
      listServer()
        .then((response) => {
          console.log(response);
          if (response.status === 200) {
            return response.data;
          }
        })
        .then((data) => (this.lstServer = data))
        .then((data) => {
          if (data) {
            const topics = data.map((e) => e.ip_address);

            this.handleEventMQTT(topics);
            console.log(topics);
          }
        })
        .catch((error) => console.log(error));
    },
  },
  watch: {
    lstServer: function (v) {
      console.log("V: ", v);
    },
  },
};
</script>

<style scoped>
.small {
  max-width: 600px;
  margin: 150px auto;
}

.card-disable {
  background: rgba(245, 245, 245, 0.4);
}
</style>
