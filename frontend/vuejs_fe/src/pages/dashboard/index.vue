<template>
  <div>
    <h1>Hello</h1>
    <ul>
      <li v-for="(client, idx) in states" :key="idx">
        {{ client['ram'] }}
        <new-chart :status="client['ram']"/>
      </li>
    </ul>
    <div style="height: 20%; width: 50%">
      <new-chart/>
    </div>
  </div>
</template>

<script>
import socket from "../../../socket";
import NewChart from "@/pages/dashboard/NewChart";

export default {
  name: "index",
  components: {NewChart},
  props: {
    status: Object
  },
  data() {
    return {
      states: [],
      clients: []
    }
  },
  created() {
    this.init()
    this.subscribe()
  },
  mounted() {

  },
  methods: {
    init() {
      socket.connect()
    },
    subscribe() {
      socket.on('manager', (data) => {
        this.states = data
      })
      socket.on('clients', listClient => {
        console.log('listClient: ', listClient)

      })
    },
    off() {
      socket.off('manager')
    }
  },
  destroyed() {
    this.off()
  }
}
</script>

<style scoped>

</style>
