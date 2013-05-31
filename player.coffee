window.AudioContext = window.AudioContext||window.webkitAudioContext

class Player
    constructor: ->
        @source = null

    play: (url) ->
        console.log("loading...")
        xhr = new XMLHttpRequest()
        xhr.open("GET", url, true)
        xhr.responseType = "arraybuffer"
        xhr.onload = =>
            data = new Uint8Array(xhr.response || xhr.mozResponseArrayBuffer)
            png = new PNG(data)
            dat = png.decodePixels()
            header = dat.buffer.slice(0, 4)
            header_u32 = new Uint32Array(header)
            body = dat.buffer.slice(4, 4+header_u32[0])
            context = new window.AudioContext()
            source = context.createBufferSource()
            console.log("decoding...")
            context.decodeAudioData body, (buf) =>
                source.buffer = buf
                source.loop = false
                source.connect(context.destination)
                source.start(0)
                @source = source
                console.log("started.")
            , (err) ->
                console.error(err)
        xhr.send(null)

    stop: ->
        @source?.stop(0)
        @source = null

window.Player = Player
