flickr-music-player: proof-of-concept music player with Flickr backend

Inspired by [Flickr-FS][] and [flickr-store][].

# Setup

Create `static/flickr_keys.json` file as like:
(WARNING: it will be publicly served by web server!)

    {
        "api_key": "<Flickr API Key>",
        "nsid": "<Flickr NSID>",
        "photoset_id": "<Photoset ID>"
    }

flickr-music-player will load music files from specified photoset.

Use `tools/convert.py` to encode music file inside PNG file.
Add it to Flickr photoset.

Execute `run.py` to run web server.

[Flickr-FS]: https://github.com/Rotten194/flickr-fuse
[flickr-store]: https://github.com/meltingice/flickr-store
