#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Standard Library Modules
import random
import string
import json
import typing

# Related Third-Party Modules
import requests


def brian_tts(message: str) -> typing.Union[bytes, typing.NoReturn]:
    """
    Brian Text to speech

    Parameters:
        message str: Prompt

    Returns:
        result (Union[bytes, None]): result or None in failure
    """
    # Base URL for provider API
    url: str = "https://api.streamelements.com/kappa/v2/speech?voice=Brian&text={prompt}"
    
    # Request headers
    headers: typing.Dict[str, str] = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
    }
    
    # Try to send request or return None on failure
    try:
        result = requests.get(url=url.format(prompt=message), headers=headers)
        return result.content
    except:
        return None
