#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Standard Library Modules
import random
import string
import json
from typing import NoReturn, List, Dict, Union

# Related Third-Party Modules
import requests


# DeepInfra Chat Provider
def deep_infra_chat(messages: List[Dict[str, str]]) -> Union[str, NoReturn]:
    """
    Chat completion for DeepInfra chat

    Parameters:
        messages (List[Dict[str, str]]): Conversation history

    Returns:
        result (Union[str, None]): result or None in failure
    """
    # Base URL for provider API
    url: str = "https://api.deepinfra.com/v1/openai/chat/completions"
    
    # Request headers
    headers: Dict[str, str] = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        'Accept-Language': 'en,fr-FR;q=0.9,fr;q=0.8,es-ES;q=0.7,es;q=0.6,en-US;q=0.5,am;q=0.4,de;q=0.3',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        'Origin': 'https://deepinfra.com',
        'Pragma': 'no-cache',
        'Referer': 'https://deepinfra.com/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'X-Deepinfra-Source': 'web-embed',
        'accept': 'text/event-stream',
        'sec-ch-ua': '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"'
    }

    # Request data
    data: Dict[str, Any] = json.dumps(
        {
        'model' : 'meta-llama/Llama-2-70b-chat-hf',
        'messages': messages,
        'stream': False
        }, separators=(',', ':')
    )
    
    # Try to send request or return None on failure
    try:
        result = requests.post(url=url, data=data, headers=headers)
        return result.json()['choices'][0]['message']['content']
    except:
        return None
