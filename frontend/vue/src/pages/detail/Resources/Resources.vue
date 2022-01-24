<template>
  <div class="mt-4">
    <!-- Content Row -->
    <div class="row">
      <div class="col">
        <div class="row">
          <div class="">
            <!-- Area Chart -->
            <div class="card shadow mb-4">
              <div class="card-header py-3" style="background-color: #00bfa5">
                <div class="d-flex justify-content-between">
                  <div>
                    <h6 class="m-0 font-weight-bold text-light">CPU Status</h6>
                  </div>
                  <div>
                <span :class="['badge', avgCPU > 60 && avgCPU < 80
                                    ? 'bg-warning'
                                    : avgCPU >= 80
                                    ? 'bg-danger'
                                    : 'bg-success']" style="font-size: 100%">{{ avgCPU }} % </span>
                  </div>
                </div>

              </div>
              <div class="card-body">
                <div class="chart-area">
                  <cpu-chart
                      :data="$route.params"
                      @avg="getAvg"
                      @overload="getStatusCPU"
                  />
                </div>
              </div>
            </div>
          </div>


        </div>
        <div class="row">
          <div class="col-xl-6 col-lg-7">
            <!-- Area Chart -->
            <div class="card shadow mb-4">
              <div class="card-header py-3" style="background-color: #00bfa5">
                <div class="d-flex justify-content-between">
                  <div>
                    <h6 class="m-0 font-weight-bold text-light">RAM Status</h6>
                  </div>
                  <div>
                <span :class="['badge', RAMUsed > 60 && RAMUsed < 80
                                    ? 'bg-warning'
                                    : RAMUsed >= 80
                                    ? 'bg-danger'
                                    : 'bg-success']" style="font-size: 100%">{{ RAMUsed }} % </span>
                  </div>
                </div>

              </div>
              <div class="card-body">
                <div class="chart-area">
                  <ram-chart :data="$route.params" @overload="getStatusRAM" @used="getRamUsed"/>
                </div>

              </div>

            </div>
          </div>
          <div class="col-xl-6 col-lg-7">
            <!-- Area Chart -->
            <div class="card shadow mb-4">
              <div class="card-header py-3" style="background-color: #00bfa5">
                <div class="d-flex justify-content-between">
                  <div>
                    <h6 class="m-0 font-weight-bold text-light">Disk Status</h6>
                  </div>
                  <div>

                  </div>
                  <div>
                <span :class="['badge', 'mx-2', 'bg-danger']" style="font-size: 100%">Used: {{
                    diskStatus.used
                  }}</span>
                    <span :class="['badge', 'bg-success']" style="font-size: 100%">Free: {{ diskStatus.free }} </span>
                  </div>
                </div>

              </div>
              <div class="card-body">
                <div class="chart-area">
                  <disk-chart :data="machineDetail" @statistical="getStatisticalDisk"/>
                </div>
              </div>

            </div>
          </div>

        </div>
      </div>
      <div class="col">

        <div class="card">
          <div class="card-header py-3" style="background-color: #00bfa5">
            <div>
              <h6 class="m-0 font-weight-bold text-light">Process</h6>
            </div>
          </div>
          <div class="card-body">
            <process/>
          </div>
        </div>
      </div>

    </div>
  </div>
</template>

<script>
import {DetailMachine} from "@/api/details";
import CpuChart from "../Chart/CPUChart.vue";
import RamChart from "../Chart/RAMChart.vue";
import DiskChart from "@/pages/detail/Chart/DiskChart";
import Process from "@/pages/detail/Process/Process";

export default {
  name: "Resources",
  components: {Process, DiskChart, CpuChart, RamChart},
  data() {
    return {
      topic: {},
      avgCPU: "",
      RAMUsed: "",
      diskStatus: {},
      logsCPU: [],
      logsRAM: [],
      machine: {},

      // Process
      showProcessTopic: {},
      processes: [],
      search: "",
      ip: "",
      notificationTopic: "",
    };
  },
  computed: {
    machineDetail: function () {
      return this.machine;
    },
  },
  created() {
    this.getMachineDetail();
  },
  methods: {
    getAvg(value) {
      this.avgCPU = value;
    },
    getStatisticalDisk(value) {
      console.log(value)
      this.diskStatus = value
    },
    getRamUsed(value) {
      this.RAMUsed = value
    },
    getStatusCPU(val) {
      this.logsCPU = [...this.logsCPU, val];
      const container = this.$el.querySelector("#logsCPU");
      container.scrollTop = container.scrollHeight;
    },
    getStatusRAM(val) {
      this.logsRAM = [...this.logsRAM, val];
      const container = this.$el.querySelector("#logsRAM");
      container.scrollTop = container.scrollHeight;
    },
    getMachineDetail() {
      const {id} = this.$route.params;
      DetailMachine(id).then((response) => {
        this.machine = response.data;

      });
    },
  },
};
</script>

<style>
</style>
