<template>
  <div>
    <!--    <bar-chart :chartdata="dataCollection"/>-->
    <!--    <line-chart/>-->
    <!-- <div class="row px-2">
      <div
        class="card shadow"
        :class="[server.status === 'OFF' && 'border-danger']"
        v-for="(server, idx) in payload"
        :key="idx"
        style="width: 18rem; margin-right: 20px; margin-bottom: 20px"
      >
        <div class="card-body">
          <div class="d-flex bd-highlight">
            <h5 class="card-title">{{ server.user.hostname }}</h5>
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
          <h6 class="card-subtitle mb-2 text-muted">{{ server.user.ip }}</h6>
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
          </div>
        </div>
      </div>
    </div> -->
  </div>
</template>

<script>
import client from "../../../_mqtt";
import { listServer } from "../../api/dashboard";

export default {
  name: "Dashboard",
  components: {},
  computed: {},
  data() {
    return {};
  },
  created() {
    this.handleGetListServer()
    this.handleEventMQTT();
  },
  methods: {
    /**
     * Function handle MQTT events
     */
    handleEventMQTT() {
      // MQTT Client connect event

      client.on("connect", function () {
        client.subscribe("sample", function (err) {
          if (err) {
            client.publish("sample", "Hello mqtt");
          }
        });
      });

      // MQTT Client on message receive event

      client.on("message", function (topic, message) {
        console.log(message.toString());
      });
    },

    /**
     * Function fetch all server connected to broker
     */
    handleGetListServer() {
      listServer()
        .then((res) => console.log(res))
        .catch((error) => console.log(error));
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
