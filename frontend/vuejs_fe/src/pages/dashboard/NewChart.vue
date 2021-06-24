<script>

import {Line} from 'vue-chartjs'
import 'chartjs-plugin-streaming'

export default {
  extends: Line,
  props: {
    status: Object
  },
  data() {
    return {
      test: {}
    }
  },
  mounted() {
    const dataSets = [{
      label: 'RAM',
      backgroundColor: 'rgba(54, 162, 235, 0.5)',
      borderColor: 'rgb(54, 162, 235)',
      cubicInterpolationMode: 'monotone',
      fill: false,
      data: []
    }]
    this.renderChart(
        {
          datasets: dataSets,
        },
        {
          responsive: false,
          maintainAspectRatio: false,
          scales: {
            yAxes: [{
              ticks: {
                beginAtZero: true,
                max: 100
              }
            }],
            xAxes: [{
              type: 'realtime',
              realtime: {
                delay: 2000,
                onRefresh: chart => {
                  chart.data.datasets.forEach(dataset => {
                    dataset.data.push({
                      x: Date.now(),
                      y: this.test['percent']
                    })
                  })
                }
              }
            }]
          }
        })
  },
  watch: {
    status: function (v) {
      console.log('STATUS: ', v['percent'])
      this.test = v
      // Hello
    }
  }
}
</script>

<style scoped>

</style>
