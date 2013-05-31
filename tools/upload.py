#!/usr/bin/env python

import flickr_api
import tempfile
import convert
import os
import utils

def main():
	utils.flickr_login()

#	flickr_api.upload(photo_file='in.jpg', title='Test twice')

	img_data = convert.encode_to_png(open('in.mp3', 'rb').read(), font='in.ttf')

	try:
		fp = tempfile.NamedTemporaryFile(delete=False)
		fp.write(img_data)
		fp.close()

		flickr_api.upload(photo_file=fp.name, title='Final fusion')
	finally:
		try: os.remove(fp.name)
		except OSError: pass

if __name__ == '__main__':
	main()
