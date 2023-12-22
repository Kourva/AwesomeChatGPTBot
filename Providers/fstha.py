#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Standard Library Modules
import random
import string
import json
from typing import NoReturn, List, Dict, Union

# Related Third-Party Modules
import requests


# Fstha Chat Provider
def fstha_chat_gpt(messages: List[Dict[str, str]]) -> Union[str, NoReturn]:
    """
    Chat completion for Fstha 
    
    Parameters:
        messages (List[Dict[str, str]]): Conversation history

    Returns:
        result (Union[str, None]): result or None in failure
    """
    # Base URL for provider API
    url: str = "https://chat.fstha.com/api/openai/v1/chat/completions"
    
    # Request headers
    headers: Dict[str, str] = {
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/119.0",
        "Accept": "text/event-stream",
        "Accept-Language": "de,en-US;q=0.7,en;q=0.3",
        "Accept-Encoding": "gzip, deflate, br",
        "Content-Type": "application/json",
        "Referer": "https://chat.fstha.com/",
        "x-requested-with": "XMLHttpRequest",
        "Origin": "https://chat.fstha.com",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "Authorization": "Bearer ak-chatgpt-nice",
        "Connection": "keep-alive",
        "Alt-Used": "chat.fstha.com"
    }

    # Request data
    data: Dict[str, Any] = {
        "messages": messages,
        "stream": False,
        "model": "gpt-3.5-turbo",
        "temperature": 0.5,
        "presence_penalty": 0,
        "frequency_penalty": 0,
        "top_p": 0.5,
    }
   
    # Try to send request or return None on failure
    try:
        res = requests.post(url=url, json=data, headers=headers).json()
        return res["choices"][0]["message"]["content"]
    except:
        return None
