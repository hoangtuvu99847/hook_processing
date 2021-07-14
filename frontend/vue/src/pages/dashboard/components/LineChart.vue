<script>
import 'chartjs-plugin-streaming';
import {Line} from 'vue-chartjs'

export default {
  name: "LineChart",
  extends: Line,
  mounted() {
    this.renderChart({
      datasets: [{
        label: 'Dataset 1',
        fill: false,
        borderColor: 'rgb(255, 99, 132)',
        backgroundColor: 'rgba(255, 99, 132, 0.5)',
        lineTension: 0,
        borderDash: [8, 4]

      }, {
        label: 'Dataset 2',
        fill: false,
        borderColor: 'rgb(54, 162, 235)',
        backgroundColor: 'rgba(54, 162, 235, 0.5)'
      }]
    }, {
      maintainAspectRatio: false,
      // responsive: false,
      scales: {
        xAxes: [{
          type: 'realtime',
          realtime: {
            onRefresh: function (chart) {
              chart.data.datasets.forEach(function (dataset) {
                dataset.data.push({
                  x: Date.now(),
                  y: Math.random()
                });
              });
            },
            delay: 2000
          }
        }]
      }
    });
  }
}

</script>
<style scoped>

</style>
