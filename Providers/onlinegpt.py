#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Standard Library Modules
import random
import string
import json
from typing import NoReturn, List, Dict, Union, Optional

# Related Third-Party Modules
import requests

# Random token generator
def random_token_generator(size: Optional[int] = 10):
    return "".join(
        random.choices(string.ascii_letters, k=size)
    )

# OnlineGPT Provider
def online_gpt_chat(messages: List[Dict[str, str]]) -> Union[str, NoReturn]:
    """
    Chat completion for OnlineGPT 
    
    Parameters:
        messages (List[Dict[str, str]]): Conversation history

    Returns:
        result (Union[str, None]): result or None in failure
    """
    # Base URL for provider API
    url: str = "https://onlinegpt.org"
    
    # Request headers
    headers: Dict[str, str] ={
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/119.0",
        "Accept": "text/event-stream",
        "Accept-Language": "de,en-US;q=0.7,en;q=0.3",
        "Accept-Encoding": "gzip, deflate, br",
        "Referer": f"{url}/chat/",
        "Content-Type": "application/json",
        "Origin": url,
        "Alt-Used": "onlinegpt.org",
        "Connection": "keep-alive",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "TE": "trailers"
    }

    # Request data
    data: Dict[str, Any] = {
        "botId": "default",
        "customId": None,
        "session": random_token_generator(12),
        "chatId": random_token_generator(),
        "contextId": 9,
        "messages": messages,
        "newMessage": messages[-1]["content"],
        "newImageId": None,
        "stream": False
    }

    # Try to send request or return None on failure
    try:
        res = requests.post(
            url=f"{url}/chatgpt/wp-json/mwai-ui/v1/chats/submit",
            json=data,
            headers=headers
        ).json()
        return res['reply']
    except:
        return None