import mqtt from "mqtt";

const {VUE_APP_HOST, VUE_APP_BROKER_PORT} = process.env
export default mqtt.connect(`ws://${VUE_APP_HOST}:${VUE_APP_BROKER_PORT}/mqtt`)

