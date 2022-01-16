const express = require('express')
const request = require('request');
const app = express()
const http = require('http').createServer(app)

const PORT = process.env.PORT || 3000

http.listen(PORT, () => {
    console.log(`Listening on port ${PORT}`)
})

app.use(express.static(__dirname + '/public'))

app.get('/', (req, res) => {
    res.sendFile(__dirname + '/index.html')
})


app.get('/home', (req, res) => {
    const { spawn } = require('child_process');
    const pyProg = spawn('python', ['./app.py', req.query.text]);

    pyProg.stdout.on('data', function(data){
        console.log('35',data.toString())
        res.write(data)
        res.end('')
    });
})

// Socket 
const io = require('socket.io')(http)

io.on('connection', (socket) => {
    console.log('Connected...')
    socket.on('message', (msg) => {
        socket.broadcast.emit('message', msg)
    })
})





