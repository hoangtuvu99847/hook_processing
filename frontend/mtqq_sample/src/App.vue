<template>
  <div id="app">
    <p>Holla</p>
  </div>
</template>

<script>
import mqtt from "mqtt";

export default {
  data() {
    return {
      connection: {
        host: '172.16.0.121',
        port: 8000,
        endpoint: '/mqtt',
        clean: true, // Reserved session
        connectTimeout: 4000, // Time out
        reconnectPeriod: 4000, // Reconnection interval

      },
      subscription: {
        topic: 'server/127.0.1.1',
      },
      publish: {
        topic: 'server/127.0.1.1',
        payload: '{ "msg": "Hello, I am browser." }',
      },
      receiveNews: '',

      client: {
        connected: false,
      },
      subscribeSuccess: false,
    }
  },
  created() {
    this.createConnection()
  },
  methods: {
    createConnection() {
      const {host, port, endpoint, ...options} = this.connection
      const connectUrl = `ws://${host}:${port}${endpoint}`
      try {
        this.client = mqtt.connect(connectUrl, options)
      } catch (error) {
        console.log('mqtt.connect error', error)
      }
      this.client.on('connect', () => {
        console.log('Connection succeeded!')
        this.doSubscribe()
      })
      this.client.on('error', error => {
        console.log('Connection failed', error)
      })
      this.client.on('message', (topic, message) => {
        this.receiveNews = this.receiveNews.concat(message)
        console.log(`Received message ${message} from topic ${topic}`)
      })
    },
    doSubscribe() {
      const {topic} = this.subscription
      this.client.subscribe(topic, (error, res) => {
        if (error) {
          console.log('Subscribe to topics error', error)
          return
        }
        this.subscribeSuccess = true
        console.log('Subscribe to topics res', res)
      })
    },
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
