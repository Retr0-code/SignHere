#!/usr/bin/python3

import socketserver
import http.server

def Server(ip, port):
	try:
		print(f"\033[32m[+]\033[0m HTTP Server successfully started up on {ip}:{port}")
		httpd = socketserver.TCPServer((ip, port), http.server.SimpleHTTPRequestHandler)
		httpd.serve_forever()

	except OSError:
		print(f"\033[31m[-]\033[0m Unavalible to reach {ip} or allready in use")

