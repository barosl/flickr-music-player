OUTPUT = player.js png.js zlib.js

.PHONY: all
all: $(OUTPUT)

player.js: player.coffee
	coffee -c $<

png.js:
	cp lib/png.js/png.js ./png.js

zlib.js:
	cp lib/png.js/zlib.js ./zlib.js

.PHONY: clean
clean:
	rm -f $(OUTPUT)
