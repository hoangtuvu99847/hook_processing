<template>
  <div>
    <div id="content-wrapper" class="d-flex flex-column">
      <!-- Main Content -->
      <div id="content">
        <!-- Topbar -->
        <!-- End of Topbar -->

        <!-- Begin Page Content -->
        <div class="container-fluid">
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
                      @overload="getStatus"
                    />
                  </div>
                  <hr />
                  <div class="row">
                    <div class="col-9">
                      <div class="card border-success mb-3">
                        <div class="card-header" style="font-weight: bold">
                          Logs
                        </div>
                        <div
                          class="card-body"
                          style="max-height: 80px; overflow: scroll"
                          id="logs"
                        >
                          <ul
                            style="
                              list-style: none;
                              padding-left: 0px;
                              font-family: monospace;
                            "
                          >
                            <li v-for="(log, idx) in logs" :key="idx">
                              <i
                                v-if="log.type === 'warning'"
                                class="fas fa-exclamation-triangle text-warning"
                              ></i>

                              <i v-else class="fas fa-exclamation"></i>
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

              <!-- Bar Chart -->
              <div class="card shadow mb-4">
                <div class="card-header py-3">
                  <h6 class="m-0 font-weight-bold text-primary">Bar Chart</h6>
                </div>
                <div class="card-body">
                  <div class="chart-bar">
                    <bar-chart />
                  </div>
                  <hr />
                  Styling for the bar chart can be found in the
                  <code>/js/demo/chart-bar-demo.js</code> file.
                </div>
              </div>
            </div>

            <!-- Donut Chart -->
            <div class="col-xl-4 col-lg-5">
              <div class="card shadow mb-4">
                <!-- Card Header - Dropdown -->
                <div class="card-header py-3">
                  <h6 class="m-0 font-weight-bold text-primary">Donut Chart</h6>
                </div>
                <!-- Card Body -->
                <div class="card-body">
                  <div class="chart-pie pt-4">
                    <canvas id="myPieChart"></canvas>
                  </div>
                  <hr />
                  Styling for the donut chart can be found in the
                  <code>/js/demo/chart-pie-demo.js</code> file.
                </div>
              </div>
            </div>
            <div class="col-xl-8 col-lg-7">
              <!-- Area Chart -->
              <div class="card shadow mb-4">
                <div class="card-header py-3">
                  <h6 class="m-0 font-weight-bold text-primary"></h6>
                </div>
                <div class="card-body">
                  <div class="chart-area">
                    <line-chart />
                  </div>
                  <hr />
                  Styling for the area chart can be found in the
                  <code>/js/demo/chart-area-demo.js</code> file.
                </div>
              </div>

              <!-- Bar Chart -->
              <div class="card shadow mb-4">
                <div class="card-header py-3">
                  <h6 class="m-0 font-weight-bold text-primary">Bar Chart</h6>
                </div>
                <div class="card-body">
                  <div class="chart-bar">
                    <bar-chart />
                  </div>
                  <hr />
                  Styling for the bar chart can be found in the
                  <code>/js/demo/chart-bar-demo.js</code> file.
                </div>
              </div>
            </div>

            <!-- Donut Chart -->
            <div class="col-xl-4 col-lg-5">
              <div class="card shadow mb-4">
                <!-- Card Header - Dropdown -->
                <div class="card-header py-3">
                  <h6 class="m-0 font-weight-bold text-primary">Donut Chart</h6>
                </div>
                <!-- Card Body -->
                <div class="card-body">
                  <div class="chart-pie pt-4">
                    <canvas id="myPieChart"></canvas>
                  </div>
                  <hr />
                  Styling for the donut chart can be found in the
                  <code>/js/demo/chart-pie-demo.js</code> file.
                </div>
              </div>
            </div>
            <div class="col-xl-4 col-lg-5">
              <div class="card shadow mb-4">
                <!-- Card Header - Dropdown -->
                <div class="card-header py-3">
                  <h6 class="m-0 font-weight-bold text-primary">Donut Chart</h6>
                </div>
                <!-- Card Body -->
                <div class="card-body">
                  <div class="chart-pie pt-4">
                    <canvas id="myPieChart"></canvas>
                  </div>
                  <hr />
                  Styling for the donut chart can be found in the
                  <code>/js/demo/chart-pie-demo.js</code> file.
                </div>
              </div>
            </div>
          </div>
        </div>
        <!-- /.container-fluid -->
      </div>
      <!-- End of Main Content -->
    </div>
  </div>
</template>

<script>
import BarChart from "../dashboard/components/BarChart.vue";
import LineChart from "../dashboard/components/LineChart.vue";
import CpuChart from "./Chart/CPUChart.vue";

export default {
  name: "Detail",
  props: ["id"],
  components: { LineChart, BarChart, CpuChart },
  data() {
    return {
      topic: {},
      avgCPU: "",
      logs: [],
    };
  },
  methods: {
    getAvg(value) {
      this.avgCPU = value;
    },
    getStatus(val) {
      this.logs = [...this.logs, val];
      var container = this.$el.querySelector("#logs");
      container.scrollTop = container.scrollHeight;
    },
  },
  created() {
    console.log("IP: ", this.$route.params);
  },
};
</script>

<style scoped>
</style>
