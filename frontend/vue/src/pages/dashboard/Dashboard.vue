<template>
  <div>
    <div class="row px-2">
      <div
        class="card shadow"
        v-for="machine in machines"
        :class="[machine.status === 0 && 'border-danger']"
        :key="machine.machine.hostname"
        style="width: 18rem; margin-right: 20px; margin-bottom: 20px"
      >
        <div class="card-body">
          <div class="d-flex bd-highlight">
            <h5 class="card-title">{{ machine.machine.hostname }}</h5>
            <div class="ms-auto bd-highlight">
              <a class="btn btn-sm btn-outline-primary" @click="detail(server)"
                >Details</a
              >
            </div>
          </div>
          <div class="mb-2">
            <div v-if="machine.status === 0">
              <i class="fas fa-exclamation-triangle text-danger"></i>
              Disconnected
            </div>
            <div v-else>
              <i class="fas fa-signal text-success"></i> Connected
            </div>
          </div>
          <h6 class="card-subtitle mb-2 text-muted">
            {{ machine.machine.ip_address }}
          </h6>
          <div class="row">
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
                  {{ machine.resource.cpu.avg }} %</span
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
                  >{{ machine.resource.ram.percent }}%</span
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
                  >{{ machine.resource.disk.percent }}%</span
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
                  >{{ machine.resource.disk.percent }}%</span
                >
                <div></div>
              </div>
            </div>
          </div>
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
  data() {
    return {
      lstServer: [],
      machines: [],
      topics: 0,
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
  computed: {
    machinesOnline: function () {
      return this.machines.filter((el) => el.status === 1);
    },
  },
  methods: {
    /**
     * Function init connection connect MQTT
     */
    createConnection() {
      // let arr = [];
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
        console.log("TOPIC: ", topic, "DATA: ", data);

        topic = topic.split("/").at(-1);

        // console.log(topic);
        this.handleReceiveEvent(topic, data);
      });
    },
    /**
     * @param {Object} data -  Data corresponding topic receive from broker
     * @param {String} topic - Topic data receive from broker
     */
    handleReceiveEvent(topic, data) {
      switch (topic) {
        case "*":
          this.monitorMessage(topic, data);
          break;
        case "disconnected":
          this.handleDisconnect(topic, data);
          break;
      }
    },
    /**
     * Function handle event when machine disconnect
     * @param {Object} topic - Topic subscribe already
     * @param {Object} payload - Data sent from broker
     */
    handleDisconnect(topic, payload) {
      console.log("Disconnect topic: ", topic);
      console.log("Disconnect message: ", payload);

      const idx = this.machines.findIndex(
        (el) =>
          el.machine.hostname === payload.hostname &&
          el.machine.ip_address === payload.ip_address
      );
      if (idx !== -1) {
        // Disconnected!
        this.machines[idx].status = 0;
      }
    },
    /**
     * Function view realtime data receive from broker
     * @param {Object} topic - Topic subscribe already
     * @param {Object} payload - Data sent from broker
     */
    monitorMessage(topic, payload) {
      payload["status"] = 1;
      // Check if machine is existing monitor -> Update, else -> Push to list machines
      const idx = this.machines.findIndex(
        (el) =>
          el.machine.hostname === payload.machine.hostname &&
          el.machine.ip_address === payload.machine.ip_address
      );
      if (idx === -1) {
        this.machines = [...this.machines, payload];
        return;
      }
      // Vue is not reactive when change item in array. Eg:
      // a = ['a','b','c']
      // a[1] = 'd' (Will NOT reactive)
      // Solution: this.$set(a, 1, 'd')
      this.$set(this.machines, idx, payload);
    },
    /**
     * Function handle MQTT events
     * @param {Array} topics - List topic subscribe
     */
    handleEventMQTT(topics) {
      // MQTT Client connect event

      // Subscribe event disconnected first
      this.client.subscribe("server/disconnected", function (err, res) {
        if (err) {
          this.client.publish("error", "Hello mqtt");
          return;
        }
        console.log("Subscribe to topics res", res);
      });

      // Subscribe event of all machine
      topics.forEach((ip) => {
        const topic = `server/${ip}/resources/*`;
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
    machines: function (v) {
      console.log("Machines: ", v);
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
