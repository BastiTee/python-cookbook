#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""RFC 7636 code_verifier to code_challenge example.

This script takes as input a user-defined string (code_verifier) and
calculates the corresponding RFC-7636-conform code_challenge.

See https://tools.ietf.org/html/rfc7636 for further information.
"""
import base64
import hashlib
import urllib.parse
import sys

if len(sys.argv) < 2:
    print('No code_verifier string provided.')
    sys.exit(1)

verifier = (sys.argv[1].encode('utf-8'))
sha = hashlib.sha256(verifier).digest()
b64 = base64.urlsafe_b64encode(sha)
b64_strip = b64.rstrip(b'=')
code_challenge = urllib.parse.quote_plus(b64_strip)

print('SHA        {}\nB64        {}\nB64-STRIP  {}\nCC         {}'.format(
    sha,
    b64.decode('utf-8'),
    b64_strip.decode('utf-8'),
    code_challenge
))
