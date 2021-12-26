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
                v-model="search"
              />
            </div>
          </div>

          <div class="pt-3" style="overflow-y: scroll; height: 600px">
            <table class="table table-striped table-bordered">
              <thead class="table-secondary">
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
                      v-else-if="process.status === 'idle'"
                      class="fas fa-dot-circle"
                      style="color: #9c9df7"
                    ></i>
                    <i
                      v-else-if="process.status === 'sleeping'"
                      class="fas fa-dot-circle"
                      style="color: #f7b69c"
                    ></i>
                    <i
                      v-else
                      class="fas fa-dot-circle"
                      style="color: #eb1a2f"
                    ></i>
                    {{ process.status }}
                  </td>
                  <td>
                    <div
                      class="btn-group mx-2"
                      role="group"
                      aria-label="First group"
                    >
                      <button
                        class="btn btn-outline-secondary btn-sm"
                        @click="terminateProcess(process)"
                      >
                        <i class="fas fa-hand-paper" title="Terminate"></i>
                      </button>
                    </div>
                    <div
                      class="btn-group"
                      role="group"
                      aria-label="First group"
                    >
                      <button
                        class="btn btn-outline-danger btn-sm"
                        @click="killProcess(process)"
                      >
                        <i class="fas fa-times" title="Kill Process"></i>
                      </button>
                    </div>
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
import { PROCESS_ACTIONS } from "../../../utils/constants";
export default {
  name: "Process",
  data() {
    return {
      machine: {},
      showProcessTopic: {},
      abccc: "",
      processes: [],
      search: "",
      ip: "",
      notificationTopic: "",
    };
  },
  computed: {
    getProcessing() {
      return this.processes.filter((item) => {
        return item.name.toLowerCase().includes(this.search);
      });
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
        if (topic == this.showProcessTopic) {
          // console.log("==>> Message of Process: ", data, "Topic: ", topic);
          this.processes = data.process;
        } else if (topic == this.notificationTopic) {
          console.log("ME: ", data);
          if (data.code === "END_PROCESS_SUCCESS") {
            this.$swal({
              icon: "success",
              title: "Kill process successful!",
            });
          }
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
          this.ip = val.ip_address;
          this.subscribeProcessTopic(topic);
        });
    },
    subscribeProcessTopic(topic) {
      return Promise.resolve()
        .then(() => {
          this.showProcessTopic = `server/${topic}/process/all`;
          this.interactProcessTopic = `server/${this.ip}/actions`;
          this.notificationTopic = `server/${this.ip}/notifications`;
        })
        .then(() => {
          ws.subscribe(
            [
              this.showProcessTopic,
              this.interactProcessTopic,
              this.notificationTopic,
            ],
            function (err, res) {
              if (err) {
                ws.publish("error", err);
                return;
              }
              console.log("Subscribe to topics of process", res);
            }
          );
        });
    },
    terminateProcess(process) {
      this.$swal({
        icon: "question",
        title: `Do you want terminate ${process.name} process ?`,
        showDenyButton: true,
      }).then((result) => {
        if (result.value) {
          const payload = JSON.stringify({
            type: PROCESS_ACTIONS.TERMINATE,
            pid: process.pid,
          });
          // Emit message to broker
          ws.publish(this.interactProcessTopic, payload);
        }
      });
    },
    killProcess(process) {
      console.log("Kill: ", process);
    },
  },
  watch: {
    // getProcessing: function (val) {
    //   console.log(":: Watch : ->  process: ", val);
    // },
  },
};
</script>

<style scoped>
.btn-sm {
  padding: 5px 10px 5px 10px;
  font-size: 10px;
}
.swal2-title {
  position: relative;
  max-width: 100%;
  margin: 0;
  padding: 0.8 em 1 em 0;
  color: #595959;
  font-size: 1.2em;
  font-weight: 600;
  text-align: center;
  text-transform: none;
  word-wrap: break-word;
}
</style>>