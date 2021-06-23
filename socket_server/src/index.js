const httpServer = require("http").createServer();
const io = require("socket.io")(httpServer, {
    cors: {
        origin: "*",
        methods: ["GET", "POST"]
    }
});
let CLIENT_CONNECTED = []
let CLIENTS_STATUS = []
let temp = []

PORT = 3000
HOST = 'localhost'

const updateStatusClientByPosition = (payload) => {
    // GET index of and replace position
    position = CLIENTS_STATUS.map(item => item.client).indexOf(payload.client)
    CLIENTS_STATUS[position] = payload
}

const pushNewClientStatus = (payload) => {
    temp = [...temp, payload.client]
    CLIENTS_STATUS = [...CLIENTS_STATUS, payload]
}

const handleReplaceStatusByNewStatus = (data) => {
    (!temp.includes(data.client))
        ? pushNewClientStatus(data)
        : updateStatusClientByPosition(data)
}

const onConnection = (socket) => {

    const { client_id } = socket.handshake.headers
    client_id !== undefined && (CLIENT_CONNECTED = [...CLIENT_CONNECTED, client_id]);
    socket.on('manager', (data) => {
        handleReplaceStatusByNewStatus(data)
        io.emit('manager', CLIENTS_STATUS)
        io.emit('clients', CLIENT_CONNECTED)
    })
    socket.on('warning', (data) => {
        console.log('warning: ', data);
    })

    socket.on('disconnect', () => {
        console.log('Socket disconnected: ', socket.id);
        if (CLIENT_CONNECTED.length > 0) {
            CLIENT_CONNECTED = CLIENT_CONNECTED.filter(client => client !== client_id)
        }
        console.log('CLIENT_CONNECTED: ', CLIENT_CONNECTED);
        io.emit('clients', CLIENT_CONNECTED)
    })
}

io.of('/').on('connection', onConnection)

httpServer.listen(PORT, HOST, () => {
    console.log(`Listen at ${HOST}:${PORT}`);
})