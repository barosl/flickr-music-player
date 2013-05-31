window.AudioContext = window.AudioContext||window.webkitAudioContext

class Player
    constructor: ->
        @source = null

    extract_audio: (idata, length) ->
        view = new Uint8Array(idata)
        odata = new Uint8Array(length)

        count = 0
        for d, i in view
            p = Math.floor(i / 4)
            if p % 2 == 0 && i % 4 != 3
                odata[count] = d
                count += 1
                if count == length
                    break
        odata.buffer

    play: (url) ->
        console.log("loading...")
        xhr = new XMLHttpRequest()
        xhr.open("GET", url, true)
        xhr.responseType = "arraybuffer"
        xhr.onload = =>
            data = new Uint8Array(xhr.response || xhr.mozResponseArrayBuffer)
            @png = new PNG(data)
            dat = @png.decodePixels()
            header = dat.buffer.slice(0, 4)
            header_u32 = new Uint32Array(header)
            body = dat.buffer.slice(4)
            body = @extract_audio(body, header_u32[0])

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
