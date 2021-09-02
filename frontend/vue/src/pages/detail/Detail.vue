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
export default {
  name: "Detail",
  components: { LineChart, BarChart },
  data() {
    return {
      topic: {},
    };
  },
  created() {
    
  },
  mounted() {},
  methods: {
    // getTopic() {
    //   const { params } = this.$route;
    //   this.topic = params;
    // },
    // consumerSubscribeTopic() {},
    // initConsumer() {
    //   _mqtt.on("message", (topic, message) => {
    //     console.log("TOPIC: ", topic, "Message: ", message);
    //   });
    // },
  },
};
</script>

<style scoped>
</style>
