<template>
  <div class="jumbotron d-flex align-items-center">
    <div class="container">
      <div class="row">
        <div class="col-xl-12">
          <div class="row py-2">
            <div class="col-7">
              <div>
                <div style="margin-top: 10px">
                  Total process: <b> {{ getProcessing.length }}</b>
                </div>
              </div>
            </div>
            <div class="col-5">
              <input
                type="text"
                class="form-control"
                placeholder="Input process name..."
              />
            </div>
          </div>

          <div class="pt-3" style="overflow-y: scroll; height: 600px">
            <table class="table table-striped table-bordered">
              <thead class="table-dark">
                <tr>
                  <th scope="col">PID</th>
                  <th scope="col">Name</th>
                  <th scope="col">CPU(%)</th>
                  <th scope="col">RAM(%)</th>
                  <th scope="col">User</th>
                  <th scope="col">Status</th>
                  <th scope="col">Action</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(process, idx) in getProcessing" :key="idx">
                  <td style="font-weight: bold">{{ process.pid }}</td>
                  <td>{{ process.name }}</td>
                  <td>{{ process.cpu_percent }}</td>
                  <td>{{ process.memory_percent }}</td>
                  <td>{{ process.username }}</td>
                  <td>
                    <i
                      v-if="process.status === 'running'"
                      class="fas fa-dot-circle"
                      style="color: #45f00c"
                    ></i>
                    <i
                      v-else-if="process.status === 'zombie'"
                      class="fas fa-dot-circle"
                      style="color: #cce2f0"
                    ></i>
                    <i
                      v-else
                      class="fas fa-dot-circle"
                      style="color: #eb1a2f"
                    ></i>
                    {{ process.status }}
                  </td>
                  <td>
                    <i
                      class="fas fa-times text-danger"
                      title="Kill Process"
                    ></i>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import ws from "../../../../ws";
import { DetaiMachine } from "../../../api/details";

export default {
  name: "Process",
  data() {
    return {
      machine: {},
      topic: {},
      abccc: "",
      processes: [],
    };
  },
  computed: {
    getProcessing() {
      return this.processes;
    },
  },
  created() {
    this.getMachineDetail();
    this.onMessage();
  },
  methods: {
    onMessage() {
      ws.on("message", (topic, message) => {
        const data = JSON.parse(message.toString());
        if (topic == this.topic) {
          console.log("==>> Message of Process: ", data, "Topic: ", topic);
          this.processes = data.process;
        }
      });
    },
    getMachineDetail() {
      const { id } = this.$route.params;
      DetaiMachine(id)
        .then((response) => {
          this.machine = response.data;
          return response.data;
        })
        .then((val) => {
          const topic = val.ip_address;
          this.subscribeProcessTopic(topic);
        });
    },
    subscribeProcessTopic(topic) {
      return Promise.resolve()
        .then(() => {
          this.topic = `server/${topic}/process/all`;
        })
        .then(() => {
          ws.subscribe(this.topic, function (err, res) {
            if (err) {
              ws.publish("error", err);
              return;
            }
            console.log("Subscribe to topics res ONPROCESS", res);
          });
        });
    },
  },
  watch: {
    getProcessing: function (val) {
      console.log(":: Watch : ->  process: ", val);
    },
  },
};
</script>

<style>
</style>