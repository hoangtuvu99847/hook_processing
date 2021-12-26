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
              <a
                class="btn btn-sm btn-outline-primary"
                @click="machineDetail(machine)"
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
// import mqtt from "mqtt";
import ws from "../../../ws";
import { listServer } from "../../api/dashboard";

export default {
  name: "Dashboard",
  components: {},
  data() {
    return {
      lstServer: [],
      machines: [],
      topics: [],
      subscribeSuccess: false,
    };
  },
  created() {
    // this.createConnection();
    console.log("CREATED DASHBOARD");
    this.handleGetListServer();
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
      console.log("Connected: ", ws.connected);
      ws.on("connect", () => {
        console.log("Connection succeeded!");
      });
      ws.on("error", (error) => {
        console.log("Connection failed", error);
      });
      ws.on("message", (topic, message) => {
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
      console.log("handleEventMQTT");
      ws.subscribe("server/disconnected", function (err, res) {
        if (err) {
          ws.publish("error", "Hello mqtt");
          return;
        }
        console.log("Subscribe to topics res", res);
      });

      // Subscribe event of all machine
      return Promise.resolve()
        .then(() => topics.map((topic) => `server/${topic.name}/resources/*`))
        .then((ip) => {
          ws.subscribe(ip, function (err, res) {
            if (err) {
              ws.publish("error", "Hello mqtt");
              return;
            }
            // this.subscribeSuccess = true;
            console.log("Subscribe to topics res", res);
          });
          ws.subscribe(ip, function (err, res) {
            if (err) {
              ws.publish("error", "Hello mqtt");
              return;
            }
            // this.subscribeSuccess = true;
            console.log("Subscribe to topics res", res);
          });
        });
    },
    /**
     * Function get detail info machine resource
     * @param {Object} payload - Machine to get infor
     */
    machineDetail(payload) {
      const url = `detail/${payload.id}/resources`;
      document.location.href = url;
      // this.$router.push({
      //   name: "resources",
      //   params: {
      //     id: payload.id,
      //   },
      // });
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
        .then((data) => {
          console.log("LIST: ", data);
          if (data) {
            const topics = data.map((e) => ({
              name: e.ip_address,
              id: e.id,
            }));
            this.topics = topics;
            return topics;
          }
        })
        .then((topics) => {
          // Init connect MQTT
          this.createConnection();

          // Handle on event MQTT
          this.handleEventMQTT(topics);
        })
        .catch((error) => console.log(error));
    },
  },
  beforeDestroy() {
    /**
     * Unsubscribe all event ( machine ) before navigate
     */
    // return Promise.resolve()
    //   .then(() => {
    //     console.log(this.topics);
    //     return this.topics.map((server) => `server/${server.name}/resources/*`);
    //   })
    //   .then((topics) => {
    //     console.log("TOPICS: ", topics);
    //     ws.unsubscribe(topics, function (err, res) {
    //       if (err) {
    //         ws.publish("error", err);
    //         return;
    //       }
    //       // this.subscribeSuccess = true;
    //       console.log("====> Un - Subscribe to topics res", res);
    //     });
    //   });
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
