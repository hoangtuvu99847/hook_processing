<template>
  <div>
    <!--    <bar-chart :chartdata="dataCollection"/>-->
    <!--    <line-chart/>-->
    <div class="row px-2">
      <div class="card shadow" v-for="(server, idx) in payload" :key="idx"
           style="width: 18rem; margin-right: 20px; margin-bottom: 20px">
        <div class="card-body">
          <div class="d-flex bd-highlight mb-3">
            <h5 class="card-title">{{ server.client }}</h5>
            <div class="ms-auto p-2 bd-highlight"><i class="fas fa-signal text-success"></i> Connected</div>
          </div>
          <h6 class="card-subtitle mb-2 text-muted">{{ server.ip }}</h6>
          <div class="row">
            <div class="col">
              <div>
                <div style="margin-left: 30px">
                  <span class="text-muted pl-4" style="font-size: 80%"> CPU</span>
                </div>
                <i class="fas fa-microchip text-success fa-lg"></i>
                <span class="font-weight-bold text-danger"
                      style="margin-left: 10px">%</span>
              </div>
            </div>
            <div class="col">
              <div>
                <div style="margin-left: 30px">
                  <span class="text-muted pl-4" style="font-size: 80%"> RAM</span>
                </div>
                <i class="fas fa-memory text-danger fa-lg"></i>
                <span class="font-weight-bold text-danger" style="margin-left: 8px">{{ server.ram.percent }}%</span>
              </div>
            </div>
          </div>
          <div class="row py-2">
            <div class="col">
              <div>
                <div style="margin-left: 30px">
                  <span class="text-muted pl-4" style="font-size: 80%"> DISK</span>
                </div>
                <i class="fas fa-hdd text-primary fa-lg"></i>
                <span class="font-weight-bold text-danger" style="margin-left: 8px">80%</span>
              </div>
            </div>
            <div class="col">
              <div>
                <div style="margin-left: 30px">
                  <span class="text-muted pl-4" style="font-size: 80%"> NETWORK</span>
                </div>
                <i class="fas fa-network-wired text-info fa-lg"></i>
                <span class="font-weight-bold text-danger" style="margin-left: 6px">80%</span>
              </div>
            </div>
          </div>
        </div>
      </div>

    </div>
  </div>
</template>

<script>

import {listServer} from "@/api/dashboard";
import {CONSTANTS} from "@/utils/constants";
import _mqtt from "../../../_mqtt";


export default {
  name: "Dashboard",
  components: {},
  data() {
    return {
      dataCollection: null,
      servers: {},
      obj: {},
      payload: {},
      topics: [],
      options: {
        clean: true,
        connectTimeout: 4000,
        reconnectPeriod: 4000,
      },
    }
  },
  created() {
    this.requestGetListServer()
  },
  mounted() {
  },
  methods: {
    consumerSubscribeTopics(topics) {
      topics.map(topic => {
        _mqtt.subscribe(`${CONSTANTS.TOPIC_PREFIX}${topic.ip_address}`, (error, res) => {
          if (error) {
            console.log('Subscribe to topics error', error)
            return
          }
          console.log('Subscribe to topics res', res)
        })
      })
    },
    initConsumer(topics) {
      let payload = {}
      _mqtt.on('connect', () => {
        console.log('Connection succeeded!')
        this.consumerSubscribeTopics(topics)
      })
      _mqtt.on('error', error => {
        console.log('Connection failed', error)
      })
      _mqtt.on('message', (topic, message) => {
        const messageObject = JSON.parse(message.toString())
        payload[messageObject.ip] = messageObject
        this.payload = payload
      })
      _mqtt.on('disconnect', () => {
      })

    },
    requestGetListServer() {
      try {
        return listServer()
            .then(response => {
              const topics = response.data
              this.initConsumer(topics)
            })
            .catch(error => console.log(error))
      } catch (err) {
        console.log("requestGetListServer :: -> Error: ", err)
      }

    }
  },
  watch: {
    servers: function (v) {
      console.log('CHANGE: ', v)
    }
  }

}
</script>

<style scoped>
.small {
  max-width: 600px;
  margin: 150px auto;
}
</style>
