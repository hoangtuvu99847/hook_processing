<template>
  <div style="height: 800px; overflow-y: auto">
    <ul>
      <li v-for="(log, idx) in logs" :key="idx"><span class="text-secondary fw-bold"> {{ log.ip }} - </span>
        <span v-if="log.type === 'warning'" class="fw-bold text-warning" style="margin-right: 30px"> [WARN] </span>
        <span v-if="log.type === 'danger'" class="fw-bold text-danger" style="margin-right: 15px"> [DANGER] </span>
        <span class="ml-5"> [{{ log.resource.toUpperCase() }}] </span>
        <span class="ml-4 fw-bold"> {{ log.percent }} %</span>
        <span class="mx-3">at {{ log.time }}</span>
      </li>
    </ul>
  </div>
</template>

<script>
import ws from "../../../../ws";

export default {
  name: "Logs",
  data() {
    return {
      CPUTopic: "",
      RAMTopic: "",
      logs: []
    }
  },
  created() {
    this.subscribeProcessTopic()
    this.onMessage()
  },
  methods: {
    onMessage() {
      ws.on("message", (topic, message) => {
        const data = JSON.parse(message.toString());
        if (topic === this.RAMTopic || topic === this.CPUtopic) {
          this.logs = [...this.logs, data]
        }
      });
    },


    subscribeProcessTopic() {
      return Promise.resolve()
          .then(() => {
            this.CPUtopic = 'logger/cpu';
            this.RAMTopic = 'logger/ram';
          })
          .then(() => {
            ws.subscribe([this.CPUtopic, this.RAMTopic],
                function (err, res) {
                  if (err) {
                    ws.publish("error", err);
                    return;
                  }
                  console.log("Subscribe to topics of logger", res);
                }
            );
          });
    },
  }
}
</script>

<style scoped>

</style>