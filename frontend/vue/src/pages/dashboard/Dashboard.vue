<template>
  <div>
    <!--    <bar-chart :chartdata="dataCollection"/>-->
    <!--    <line-chart/>-->
    <div class="row px-2">
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
    </div>
  </div>
</template>

<script>
import { listServer } from "@/api/dashboard";
import { CONSTANTS } from "@/utils/constants";
import _mqtt from "../../../_mqtt";

export default {
  name: "Dashboard",
  components: {},
  computed: {},
  data() {
    return {
      dataCollection: null,
      payload: [],
      topics: [],
      options: {
        clean: true,
        connectTimeout: 4000,
        reconnectPeriod: 4000,
      },
    };
  },
  created() {
    this.requestGetListServer();

  },
  mounted() {},
  methods: {
    consumerUnsubscribeTopic() {
      console.log("Destroy: ", this.topics);
      this.topics.map((item) => {
        const topicName = "server/" + item.ip_address;
        _mqtt.unsubscribe(topicName, (err) => {
          if (err) {
            console.log("consumerUnsubscribeTopic: ", err);
          }
        });
      });
    },
    consumerSubscribeTopics(topics) {
      _mqtt.subscribe("disconnect_server", (error, res) => {
        if (error) {
          console.log("Subscribe to topics error", error);
          return;
        }
        console.log("Subscribe to topics res", res);
      });
      topics.map((topic) => {
        _mqtt.subscribe(
          `${CONSTANTS.TOPIC_PREFIX}${topic.ip_address}`,
          (error, res) => {
            if (error) {
              console.log("Subscribe to topics error", error);
              return;
            }
            console.log("Subscribe to topics res", res);
          }
        );
      });
    },
    initConsumer(topics) {
      const obj = {};
      _mqtt.on("connect", () => {
        console.log("Connection succeeded!");
        this.consumerSubscribeTopics(topics);
      });
      _mqtt.on("error", (error) => {
        console.log("Connection failed", error);
      });
      _mqtt.on("message", (topic, message) => {
        const messageObject = JSON.parse(message.toString());
        console.log("MESSAGE_OBJ: ", messageObject);
        if (topic === "disconnect_server") {
          const ip = messageObject.server;
          this.payload = this.payload.map((flow) => {
            flow.user.ip === ip && (flow["status"] = "OFF");
            return flow;
          });
        } else {
          obj[messageObject.ip] = messageObject;
        }
        this.payload = Object.values(obj).map((v) => v);
      });
    },
    detail(payload) {
      this.$router.push({ name: "detail", params: payload });
    },
    requestGetListServer() {
      try {
        return listServer()
          .then((response) => {
            const topics = response.data;
            this.initConsumer(topics);
            this.topics = topics;
          })
          .catch((error) => console.log(error));
      } catch (err) {
        console.log("requestGetListServer :: -> Error: ", err);
      }
    },
  },
  destroyed() {
    this.consumerUnsubscribeTopic();
  },
  watch: {
    payload: function (old, val) {
      console.log("OLD: ", old);
      console.log("CHANGE: ", val);
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
