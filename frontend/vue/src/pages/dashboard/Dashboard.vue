<template>
  <div>
    <bar-chart :chartdata="dataCollection"/>
  </div>
</template>

<script>

import BarChart from "@/pages/dashboard/components/BarChart";

export default {
  name: "Dashboard",
  components: {BarChart},
  data() {
    return {
      dataCollection: null
    }
  },
  mounted() {
    this.fillData()
  },
  methods: {
    fillData() {

    },
  }
}
</script>

<style scoped>
.small {
  max-width: 600px;
  margin: 150px auto;
}
</style>
