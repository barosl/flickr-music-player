window.AudioContext = window.AudioContext||window.webkitAudioContext

class Player
    constructor: (@flickr_keys) ->
        @source = null
        @photoset = {}

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

    get_photoset: ->
        url = "http://api.flickr.com/services/rest/" +
        "?method=flickr.photosets.getPhotos&api_key=" +
        @flickr_keys.api_key + "&photoset_id=" +
        @flickr_keys.photoset_id + "&format=json" +
        "&nojsoncallback=1"

        $.getJSON(url).done (data) =>
            photoset = data.photoset.photo
            for photo in photoset
                @get_sizes(photo.id)

    get_sizes: (photo_id) ->
        url = "http://api.flickr.com/services/rest/" +
        "?method=flickr.photos.getSizes&api_key=" +
        @flickr_keys.api_key + "&photo_id=" +
        photo_id + "&format=json" +
        "&nojsoncallback=1"

        $.getJSON(url).done (data) =>
            size = data.sizes.size
            for item in size
                if item.label == "Small"
                    img = $("<img />").attr("src", item.source)
                    handler = (pid, this_) ->
                        ->
                            this_.on_item_click(pid)
                    img.on('click', handler(photo_id, this))
                    $("#photoset").append(img)

                if item.label = "Original"
                    photoset[photo_id] = item.source

    on_item_click: (photo_id) ->
        url = photoset[photo_id]
        proxy_url = @get_proxy_url(url)
        $("#nowplaying").attr("src", proxy_url)
        $("#nowplaying_a").attr("href", proxy_url)
        @play(proxy_url)

    get_proxy_url: (url) ->
        "/proxy/?url=" + url

window.Player = Player
