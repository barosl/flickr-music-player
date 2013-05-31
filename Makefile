OUTPUT = static/player.js static/png.js static/zlib.js static/jquery-2.0.2.min.js

.PHONY: all
all: $(OUTPUT)

static/player.js: player.coffee
	coffee -c $< && mv player.js ./static/

static/png.js:
	cp lib/png.js/png.js ./static/png.js

static/zlib.js:
	cp lib/png.js/zlib.js ./static/zlib.js

static/jquery-2.0.2.min.js:
	cp lib/jquery-2.0.2.min.js ./static/jquery-2.0.2.min.js

.PHONY: clean
clean:
	rm -f $(OUTPUT)
