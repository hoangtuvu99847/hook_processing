
import mqtt from "mqtt"

const { VUE_APP_HOST, VUE_APP_BROKER_PORT } = process.env


const connection = {
    host: VUE_APP_HOST,
    port: VUE_APP_BROKER_PORT,
    endpoint: "/mqtt",
    clean: true, // Reserved session
    connectTimeout: 4000, // Time out
    reconnectPeriod: 4000, // Reconnection interval
}

const { host, port, endpoint, ...options } = connection;
const connectUrl = `ws://${host}:${port}${endpoint}`;

const ws = mqtt.connect(connectUrl, options);
export default ws