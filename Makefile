OUTPUT = player.js png.js zlib.js jquery-2.0.2.min.js

.PHONY: all
all: $(OUTPUT)

player.js: player.coffee
	coffee -c $<

png.js:
	cp lib/png.js/png.js ./png.js

zlib.js:
	cp lib/png.js/zlib.js ./zlib.js

jquery-2.0.2.min.js:
	cp lib/jquery-2.0.2.min.js ./jquery-2.0.2.min.js

.PHONY: clean
clean:
	rm -f $(OUTPUT)
