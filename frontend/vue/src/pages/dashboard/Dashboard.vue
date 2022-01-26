<template>
  <div class="row">
    <div class="col">
      <div class="row px-2">
        <div
            class="card shadow"
            v-for="machine in machines"
            :class="[machineStatus[machine.machine.ip_address] === 0 && 'border-danger']"
            :key="machine.machine.hostname"
            style="width: 18rem; margin-right: 20px; margin-bottom: 20px"
        >
          <div class="card-body">
            <div class="d-flex bd-highlight">
              <h5 class="card-title">{{ machine.machine.hostname }} </h5>
              <div class="ms-auto bd-highlight">
                <a
                    class="btn btn-sm btn-outline-primary"
                    @click="machineDetail(machine)"
                >Details</a
                >
              </div>
            </div>
            <div class="mb-2">
              <div v-if="machineStatus[machine.machine.ip_address] === 0">
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
    <div class="col">
      <div class="card">
        <div class="card-header" style="background-color: #00bfa5">
          <div>
            <h6 class="m-0 font-weight-bold text-light">Log</h6>
          </div>
        </div>
        <div class="card-body">
          <logs/>
        </div>
      </div>
    </div>

  </div>
</template>

<script>
import ws from "../../../ws";
import {listServer} from "@/api/dashboard";
import Logs from "@/pages/detail/Logs/Logs";

export default {
  name: "Dashboard",
  components: {Logs},
  data() {
    return {
      lstServer: [],
      machines: [],
      topics: [],
      subscribeSuccess: false,
      machineStatus: {}
    };
  },
  created() {
    this.handleGetListServer();
  },
  computed: {},

  methods: {
    /**
     * Function init connection connect MQTT
     */
    createConnection() {
      ws.on("connect", () => {
        console.log("Connection succeeded!");
      });
      ws.on("error", (error) => {
        console.log("Connection failed", error);
      });
      ws.on("message", (topic, message) => {
        const data = JSON.parse(message.toString());
        const topicName = topic.split("/").at(-1);
        const ipAddress = topic.split("/")[1]
        this.handleReceiveEvent(topicName, ipAddress, data);
      });
    },
    /**
     * @param {Object} data -  Data corresponding topic receive from broker
     * @param {String} topic - Topic data receive from broker
     * @param {String} ipAddress - IP Address of server
     */
    handleReceiveEvent(topic, ipAddress, data) {
      switch (topic) {
        case "*":
          this.monitorMessage(topic, data);
          break;
        case "status":
          this.handleConnecter(topic, ipAddress, data);
          break;
      }
    },
    /**
     * Function handle event when machine connect or disconnect
     * @param {Object} topic Topic subscribe already
     * @param {String } ipAddress IP Address of server
     * @param {Object} payload Data sent from broker
     */
    handleConnecter(topic, ipAddress, payload) {
      if (this.machines.length === 0) {
        return
      }
      const position = this.machines.findIndex(
          (el) => el.machine.ip_address === ipAddress
      );
      this.machines[position].status = payload
      let status = {}
      status[ipAddress] = payload
      console.log('Status changed: ', status)
      this.machineStatus = status

      // console.log(this.machineStatus)
    },
    /**
     * Function view realtime data receive from broker
     * @param {Object} topic - Topic subscribe already
     * @param {Object} payload - Data sent from broker
     */
    monitorMessage(topic, payload) {
      // Check if machine is existing monitor -> Update, else -> Push to list machines

      const idx = this.machines.findIndex(
          (el) =>
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
     * @param {AxiosResponse<any>} topics - List topic subscribe
     */
    handleEventMQTT(topics) {
      // MQTT Client connect event
      // Subscribe event disconnected first
      const statusTopic = topics.map((ip_address) => `server/${ip_address.name}/status`)
      ws.subscribe(statusTopic, function (err, res) {
        if (err) {
          ws.publish("error", "Hello mqtt");
          return;
        }
        console.log("Subscribe to topics status res", res);
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
      document.location.href = `detail/${payload.id}/resources`;

    },
    /**
     * Function fetch all server connected to broker
     */
    handleGetListServer() {
      listServer()
          .then((response) => {
            if (response.status === 200) {
              return response.data;
            }
          })
          .then((data) => {
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
  watch: {}

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
