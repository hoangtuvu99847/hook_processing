const httpServer = require("http").createServer();
const io = require("socket.io")(httpServer, {
    cors: {
        origin: "*",
        methods: ["GET", "POST"]
    }
});
let SOCKET_CONNECTED = []
let CLIENTS_STATUS = []
let CLIENTS = []

PORT = 9999
HOST = 'localhost'

const updateStatusClientByPosition = (payload) => {
    // GET index of and replace position
    position = CLIENTS_STATUS.map(item => item.client).indexOf(payload.client)
    CLIENTS_STATUS[position] = payload
}

const pushNewClientStatus = (payload) => {
    CLIENTS = [...CLIENTS, payload.client]
    CLIENTS_STATUS = [...CLIENTS_STATUS, payload]
}

const handleReplaceStatusByNewStatus = (data) => {
    (!CLIENTS.includes(data.client))
        ? pushNewClientStatus(data)
        : updateStatusClientByPosition(data)
    io.emit('manager', CLIENTS_STATUS)
    io.emit('clients', SOCKET_CONNECTED)

}

const clear = (client_id) => {
    if (SOCKET_CONNECTED.length > 0) {
        SOCKET_CONNECTED = SOCKET_CONNECTED.filter(client => client !== client_id)
    }
    if (CLIENTS_STATUS.length > 0) {
        CLIENTS_STATUS = CLIENTS_STATUS.filter(item => item.client !== client_id)
    }
    if (CLIENTS.length > 0) {
        CLIENTS = CLIENTS.filter(item => item !== client_id)

    }
}
const clientDisconnect = (socket) => {
    console.log('Socket disconnected: ', socket.id);
    const { client_id } = socket.handshake.headers
    clear(client_id)
    io.emit('clients', SOCKET_CONNECTED)
    io.emit('manager', CLIENTS_STATUS)
}

const onConnection = (socket) => {

    const { client_id } = socket.handshake.headers
    client_id !== undefined && (SOCKET_CONNECTED = [...SOCKET_CONNECTED, client_id]);

    console.log('SOCKET_ID: ', socket.id);
    socket.on('manager', (data) => {
        handleReplaceStatusByNewStatus(data)
    })
    socket.on('warning', (data) => {

    })
    socket.on('details', (client_id) => {

    })
    socket.on('disconnect', () => {

        clientDisconnect(socket)

    })
}

io.on('connection', onConnection)

httpServer.listen(PORT, HOST, () => {
    console.log(`Listen at ${HOST}:${PORT}`);
})