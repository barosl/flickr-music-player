OUTPUT = static/player.js static/png.js static/zlib.js static/jquery-2.0.2.min.js

.PHONY: all
all: $(OUTPUT)

static/player.js: player.coffee
	mkdir static 2>/dev/null || true
	coffee -c $< && mv player.js ./static/

static/png.js: lib/png.js/png.js
	mkdir static 2>/dev/null || true
	cp -a $+ $@

static/zlib.js: lib/png.js/zlib.js
	mkdir static 2>/dev/null || true
	cp -a $+ $@

static/jquery-2.0.2.min.js: lib/jquery-2.0.2.min.js
	mkdir static 2>/dev/null || true
	cp -a $+ $@

.PHONY: clean
clean:
	rm -f $(OUTPUT)
