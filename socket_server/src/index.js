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

PORT = 9999
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
    io.emit('manager', CLIENTS_STATUS)
    io.emit('clients', CLIENT_CONNECTED)

}

const clear = (client_id) => {
    if (CLIENT_CONNECTED.length > 0) {
        CLIENT_CONNECTED = CLIENT_CONNECTED.filter(client => client !== client_id)
    }
    if (CLIENTS_STATUS.length > 0) {
        CLIENTS_STATUS = CLIENTS_STATUS.filter(item => item.client !== client_id)
    }
    if (temp.length > 0) {
        temp = temp.filter(item => item !== client_id)

    }
}
const clientDisconnect = (socket) => {
    console.log('Socket disconnected: ', socket.id);
    const { client_id } = socket.handshake.headers
    clear(client_id)
    io.emit('clients', CLIENT_CONNECTED)
    io.emit('manager', CLIENTS_STATUS)
}

const onConnection = (socket) => {

    const { client_id } = socket.handshake.headers
    client_id !== undefined && (CLIENT_CONNECTED = [...CLIENT_CONNECTED, client_id]);

    console.log('CLIENT_ID: ', client_id);
    socket.on('manager', (data) => {
        handleReplaceStatusByNewStatus(data)
    })
    socket.on('warning', (data) => {
    })

    socket.on('disconnect', () => {

        clientDisconnect(socket)

    })
}

io.of('/').on('connection', onConnection)

httpServer.listen(PORT, HOST, () => {
    console.log(`Listen at ${HOST}:${PORT}`);
})