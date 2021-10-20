<template>
  <div>
    <!-- Content Row -->
    <div class="row">
      <div class="col-xl-8 col-lg-7">
        <!-- Area Chart -->
        <div class="card shadow mb-4">
          <div class="card-header py-3">
            <h6 class="m-0 font-weight-bold text-primary">CPU Status</h6>
          </div>
          <div class="card-body">
            <div class="chart-area">
              <cpu-chart
                :data="$route.params"
                @avg="getAvg"
                @overload="getStatusCPU"
              />
            </div>
            <hr />
            <div class="row">
              <div class="col-9">
                <div class="card border-success mb-3">
                  <div class="card-header" style="font-weight: bold">Logs</div>
                  <div
                    class="card-body"
                    style="max-height: 80px; overflow: scroll"
                    id="logsCPU"
                  >
                    <ul
                      style="
                        list-style: none;
                        padding-left: 0px;
                        font-family: monospace;
                      "
                    >
                      <li v-for="(log, idx) in logsCPU" :key="idx">
                        <i
                          v-if="log.type === 'warning'"
                          class="fas fa-exclamation-triangle text-warning"
                        ></i>
                        <i v-else class="fas fa-exclamation text-danger"></i>
                        {{ log.text }}
                      </li>
                    </ul>
                  </div>
                </div>
              </div>
              <div class="col-3">
                <div class="card border-success mb-3">
                  <div class="card-header" style="font-weight: bold">
                    CPU Avgs
                  </div>
                  <div
                    :class="[
                      'card-body',
                      avgCPU > 60 && avgCPU < 80
                        ? 'text-warning'
                        : avgCPU >= 80
                        ? 'text-danger'
                        : 'text-success',
                    ]"
                  >
                    <h5 class="card-title">{{ avgCPU }} %</h5>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Donut Chart -->
      <div class="col-xl-4 col-lg-5">
        <div class="card shadow mb-4">
          <!-- Card Header - Dropdown -->
          <div class="card-header py-3">
            <h6 class="m-0 font-weight-bold text-primary">RAM Status</h6>
          </div>
          <!-- Card Body -->
          <div class="card-body">
            <div class="chart-pie pt-4">
              <ram-chart :data="machineDetail" @overload="getStatusRAM" />
            </div>
            <hr />
            <div>
              <div class="card border-success mb-3">
                <div class="card-header" style="font-weight: bold">Logs</div>
                <div
                  class="card-body"
                  style="max-height: 80px; overflow: scroll"
                  id="logsRAM"
                >
                  <ul
                    style="
                      list-style: none;
                      padding-left: 0px;
                      font-family: monospace;
                    "
                  >
                    <li v-for="(log, idx) in logsRAM" :key="idx">
                      <i
                        v-if="log.type === 'warning'"
                        class="fas fa-exclamation-triangle text-warning"
                      ></i>
                      <i v-else class="fas fa-exclamation text-danger"></i>
                      {{ log.text }}
                    </li>
                  </ul>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { DetaiMachine } from "../../../api/details";
import CpuChart from "../Chart/CPUChart.vue";
import RamChart from "../Chart/RAMChart.vue";

export default {
  name: "Resources",
  components: { CpuChart, RamChart },
  data() {
    return {
      topic: {},
      avgCPU: "",
      logsCPU: [],
      logsRAM: [],
      machine: {},
    };
  },
  computed: {
    machineDetail: function () {
      return this.machine;
    },
  },
  created() {
    console.log("ID Resourcess: ", this.$route.params);
    this.getMachineDetail();
  },
  methods: {
    getAvg(value) {
      this.avgCPU = value;
    },
    getStatusCPU(val) {
      this.logsCPU = [...this.logsCPU, val];
      var container = this.$el.querySelector("#logsCPU");
      container.scrollTop = container.scrollHeight;
    },
    getStatusRAM(val) {
      this.logsRAM = [...this.logsRAM, val];
      var container = this.$el.querySelector("#logsRAM");
      container.scrollTop = container.scrollHeight;
    },
    getMachineDetail() {
      const { id } = this.$route.params;
      DetaiMachine(id).then((response) => {
        this.machine = response.data;
      });
    },
  },
};
</script>

<style>
</style>