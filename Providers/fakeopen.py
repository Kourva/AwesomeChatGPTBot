#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Standard Library Modules
import random
import string
import json
from typing import NoReturn, List, Dict, Union, Optional

# Related Third-Party Modules
import requests


# Fake Open Chat Provider 
def fakeopen_chat(messages: List[Dict[str, str]]) -> Union[str, NoReturn]:
    """
    Chat completion for OnlineGPT 
    
    Parameters:
        messages (List[Dict[str, str]]): Conversation history

    Returns:
        result (Union[str, None]): result or None in failure
    """
    # Base URL for provider API
    url: str = "https://ai.fakeopen.com/v1/chat/completions"
    
    # Request headers
    headers: Dict[str, str] = {
        "user-agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/119.0",
        'authority': 'ai.fakeopen.com',
        'accept': '*/*',
        'accept-language': 'en,fr-FR;q=0.9,fr;q=0.8,es-ES;q=0.7,es;q=0.6,en-US;q=0.5,am;q=0.4,de;q=0.3',
        'authorization': 'Bearer pk-this-is-a-real-free-pool-token-for-everyone',
        'content-type': 'application/json',
        'origin': 'https://chat.geekgpt.org',
        'referer': 'https://chat.geekgpt.org/',
        'sec-ch-ua': '"Chromium";v="118", "Google Chrome";v="118", "Not=A?Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site'
    }
    
    # Request data
    data = {
        "frequency_penalty": 0,
        "messages": messages,
        "model": "gpt-3.5-turbo",
        "presence_penalty": 0,
        "stream": False,
        "temperature": 0.5,
        "top_p": 0.5
    }

    # Try to send request or return None on failure
    try:
        result = requests.post(url=url, json=data, headers=headers)
        return result.json()['choices'][0]['message']['content']
    except:
        return None
