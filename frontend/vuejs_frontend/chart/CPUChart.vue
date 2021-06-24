<script>
import {Line} from 'vue-chartjs'
import 'chartjs-plugin-streaming'

export default {
  extends: Line,
  props: {
    data: Object
  },
  data(){
    return  {
      ram: {}
    }
  },
  mounted() {
    this.renderChart({
      datasets: [{
        label: 'Dataset 1',
        backgroundColor: 'rgba(255, 99, 132, 0.5)',
        borderColor: 'rgb(255, 99, 132)',
        borderDash: [8, 4],
        fill: true,
        data: []
      }, {
        label: 'Dataset 2',
        backgroundColor: 'rgba(54, 162, 235, 0.5)',
        borderColor: 'rgb(54, 162, 235)',
        cubicInterpolationMode: 'monotone',
        fill: true,
        data: []
      }]
    }, {
      responsive: false,
      maintainAspectRatio: false,
      scales: {
        xAxes: [{
          type: 'realtime',
          realtime: {
            delay: 2000,
            onRefresh: chart => {
              chart.data.datasets.forEach(dataset => {
                dataset.data.push({
                  x: Date.now(),
                  y: this.ram['percent']
                })
              })
            }
          }
        }],
        yAxes: [{
          display: true,
          ticks: {
            max: 100,
            suggestedMin: 10,    // minimum will be 0, unless there is a lower value.
            beginAtZero: true   // minimum value will be 0.
          }
        }]
      }
    })
  },
  watch: {
    data: function (v){
      console.log('V: ', v)
      this.ram = v
    }
  }
}
</script>
