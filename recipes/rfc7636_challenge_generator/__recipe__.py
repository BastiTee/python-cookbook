# noqa: D100
# -*- coding: utf-8 -*-

import base64
import hashlib
import urllib.parse


def calculate_code_challenge(code_verifier):
    """Calculate the RFC 7636 code_challenge for the given code_verifier.

    Takes as input a user-defined string (code_verifier) and
    calculates the corresponding RFC-7636-conform code_challenge.

    See https://tools.ietf.org/html/rfc7636 for further information.
    """
    code_verifier = code_verifier.encode('utf-8')
    sha = hashlib.sha256(code_verifier).digest()
    b64 = base64.urlsafe_b64encode(sha)
    b64_strip = b64.rstrip(b'=')
    code_challenge = urllib.parse.quote_plus(b64_strip)
    return code_challenge
