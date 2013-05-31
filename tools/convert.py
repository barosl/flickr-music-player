#!/usr/bin/env python

from PIL import Image, ImageDraw, ImageFont
import struct
from cStringIO import StringIO
import math
import mutagen.id3
import os
import tempfile
import re

def encode_to_png(data, cover=None, font=None):
	data_size = len(data)
	header_s = struct.pack('<i', data_size)
	new_data = header_s + data + '\0'*(-len(data) % 3)

	px_cnt = ((len(new_data) + 2) / 3) * 2

	w = int(math.sqrt(px_cnt))
	w += -w % 2
	h = (px_cnt + w - 1) / w

	img = Image.new('RGBA', (w, h))
	buf = img.load()

	try:
		fp = tempfile.NamedTemporaryFile(delete=False)
		fp.write(data)
		fp.close()

		if not cover:
			id3 = mutagen.id3.ID3(fp.name)
			cover_data = id3.getall('APIC')[0].data

			cover = Image.open(StringIO(cover_data))

		lyrics_data = os.popen('./alsong-lyrics %s' % fp.name).read()
	finally:
		try: os.remove(fp.name)
		except OSError: pass

	new_cover = cover.resize((w, h), Image.BILINEAR)
	new_cover_buf = new_cover.load()

	if lyrics_data and font:
		font_h = 30

		draw = ImageDraw.Draw(new_cover)
		font_o = ImageFont.truetype(font, font_h)

		spaced = True
		x, y = 50, 50
		for line in lyrics_data.decode('utf-8', 'replace').splitlines():
			try:
				line = line[line.index(']')+1:].strip()
				if not line: raise RuntimeError
				spaced = False
			except:
				if spaced: continue
				spaced = True
				line = ''

			draw.text((x, y), line, font=font_o, fill='#0000ff')

			y += font_h + font_h/2
			if y + font_h > h:
				x = 50 + w/2
				y = 50

	data_pos = 0
	for j in xrange(h):
		for i in xrange(w):
			if i % 2 == 0:
				if i == 0 and j == 0:
					px = tuple(ord(x) for x in new_data[data_pos:data_pos+4])
					data_pos += 4
				else:
					px = new_cover_buf[i, j]
			else:
				px = tuple(ord(x) for x in new_data[data_pos:data_pos+3]+'\xFF')
				data_pos += 3

				if len(px) == 1: px = (0, 0, 0, 0)
				else: assert len(px) == 4

			buf[i, j] = px

	out = StringIO()
	img.save(out, format='PNG')
	return out.getvalue()

def decode_from_png(img_data):
	img = Image.open(StringIO(img_data))
	buf = img.load()

	w, h = img.size

	data = ''
	data_size = 0
	for j in xrange(h):
		for i in xrange(w):
			px_s = ''.join(chr(x) for x in buf[i, j])
			if i % 2 == 0:
				if i == 0 and j == 0:
					header = struct.unpack('<i', px_s)
					data_size, = header
			else:
				data += px_s[:3]

	return data[:data_size]

def main():
	img_data = encode_to_png(open('in.mp3', 'rb').read(), font='in.ttf')
	open('out.png', 'wb').write(img_data)
	open('out.mp3', 'wb').write(decode_from_png(img_data))

if __name__ == '__main__':
	main()
