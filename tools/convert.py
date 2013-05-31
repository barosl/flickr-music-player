#!/usr/bin/env python

from PIL import Image
import struct
import cStringIO
import math

def encode_to_png(data, poster):
	data_size = len(data)
	header_s = struct.pack('<i', data_size)
	data = header_s + data + '\0'*(-len(data) % 3)

	px_cnt = ((len(data) + 2) / 3) * 2

	w = int(math.sqrt(px_cnt))
	w += -w % 2
	h = (px_cnt + w - 1) / w

	img = Image.new('RGBA', (w, h))
	buf = img.load()

	poster_buf = poster.resize((w, h), Image.BILINEAR).load()

	data_pos = 0
	for j in xrange(h):
		for i in xrange(w):
			if i % 2 == 0:
				if i == 0 and j == 0:
					px = tuple(ord(x) for x in data[data_pos:data_pos+4])
					data_pos += 4
				else:
					px = poster_buf[i, j]
			else:
				px = tuple(ord(x) for x in data[data_pos:data_pos+3]+'\0')
				data_pos += 3

				if len(px) == 1: px = (0, 0, 0, 0)
				else: assert len(px) == 4

			buf[i, j] = px

	out = cStringIO.StringIO()
	img.save(out, format='PNG')
	return out.getvalue()

def decode_from_png(img_data):
	img = Image.open(cStringIO.StringIO(img_data))
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
	poster = Image.open('in.jpg')
	img_data = encode_to_png(open('in.mp3', 'rb').read(), poster)
	open('out.png', 'wb').write(img_data)
	open('out.mp3', 'wb').write(decode_from_png(img_data))

if __name__ == '__main__':
	main()
