#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Standard Library Modules
import random
import string
import json
from typing import NoReturn, List, Dict, Union, Optional

# Related Third-Party Modules
import requests


# Open Ai Chat Provider 
def remix_ai(messages: List[Dict[str, str]]) -> Union[str, NoReturn]:
    """
    Chat completion for remix ai 
    
    Parameters:
        messages (List[Dict[str, str]]): Conversation history

    Returns:
        result (Union[str, None]): result or None in failure
    """
    # Base URL for provider API
    url: str = "https://openai-gpt.remixproject.org/"
    
    # Request headers
    headers: Dict[str, str] = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Accept-Language": "en",
        "Connection": "keep-alive",
        "Origin": "https://remix.ethereum.org",
        "Referer": "https://remix.ethereum.org/",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "cross-site",
        "user-agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/119.0",
    }
    
    # Request data
    data = {
        "prompt": str(messages),
    }

    # Try to send request or return None on failure
    try:
        result = requests.post(url=url, json=data, headers=headers)
        print(result.json())
        return result.json()['choices'][0]['message']['content']
    except:
        return None
