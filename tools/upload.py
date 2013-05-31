#!/usr/bin/env python

import flickr_api
import tempfile
import convert
import os

def main():
	def login():
		auth = flickr_api.auth.AuthHandler()
		url = auth.get_authorization_url('write')
		key = raw_input('Visit\n%s\n...and type the oauth_verifier code: ' % url)
		auth.set_verifier(key)
		auth.save('auth.txt')
		return auth

	try: flickr_api.set_auth_handler('auth.txt')
	except IOError: flickr_api.set_auth_handler(login())

#	flickr_api.upload(photo_file='in.jpg', title='Test twice')

	img_data = convert.encode_to_png(open('in.mp3', 'rb').read())

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
