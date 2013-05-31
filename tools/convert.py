#!/usr/bin/env python

from PIL import Image
import struct
import cStringIO

def encode_to_png(data):
	data_size = len(data)
	header_s = struct.pack('<i', data_size)
	data = header_s + data + '\0'*(-len(data) % 4)

	w = 1024
	h = ((len(data) + 3) / 4 + w - 1) / w

	img = Image.new('RGBA', (w, h))
	buf = img.load()

	data_pos = 0
	for j in xrange(h):
		for i in xrange(w):
			px = tuple(ord(x) for x in data[data_pos:data_pos+4])
			if not px: px = (0, 0, 0, 0)
			else: assert len(px) == 4

			buf[i, j] = px
			data_pos += 4

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
			if i == 0 and j == 0:
				header = struct.unpack('<i', px_s)
				data_size, = header
			else:
				data += px_s

	return data[:data_size]

def main():
	img_data = encode_to_png(open('in.mp3', 'rb').read())
	open('out.png', 'wb').write(img_data)
	open('out.mp3', 'wb').write(decode_from_png(img_data))

if __name__ == '__main__':
	main()
