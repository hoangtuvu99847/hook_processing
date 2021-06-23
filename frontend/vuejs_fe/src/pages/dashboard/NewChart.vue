<script>

import {Line} from 'vue-chartjs'
import 'chartjs-plugin-streaming'

export default {
  extends: Line,
  props: {
    status: Object
  },
  data(){
    return {
      test: {}
    }
  },
  mounted() {
    const dataSets = [{
      label: 'Dataset 1',
      backgroundColor: 'rgba(255, 99, 132, 0.5)',
      borderColor: 'rgb(255, 99, 132)',
      borderDash: [8, 4],
      fill: false,
      data: []
    }, {
      label: 'Dataset 2',
      backgroundColor: 'rgba(54, 162, 235, 0.5)',
      borderColor: 'rgb(54, 162, 235)',
      cubicInterpolationMode: 'monotone',
      fill: false,
      data: []
    }]
    this.renderChart({
      datasets: dataSets
    }, {
      scales: {
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
    status: function (v){
      console.log('STATUS: ', v['percent'])
      this.test = v
      // Hello
    }
  }
}
</script>

<style scoped>

</style>
