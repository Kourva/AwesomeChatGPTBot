#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Standard Library Modules
import random
import string
import json
import typing

# Related Third-Party Modules
import requests


# UncensoredAI Chat Provider
def uncensored_ai(messages: typing.List[typing.Dict[str, str]]) -> typing.Union[str, typing.NoReturn]:
    """
    Chat completion for UncensoredAI
    
    Parameters:
        messages (List[Dict[str, str]]): Conversation history

    Returns:
        result (Union[str, None]): result or None in failure
    """
    # Base URL for provider API
    url: str = "https://creativeai-68gw.onrender.com/chat"

    # Request data
    data: typing.Dict[str, typing.Any] = {
        "query":messages[-1]["content"],
        "history": messages[:-1],
        "model": "llama-3-70b"
    }
   
    # Try to send request or return None on failure
    try:
        # Get result from request
        res = requests.post(url=url, json=data).text
        
        # Get final streamed response
        gpt_result = json.loads(res.split("data: ")[-1])["data"]["message"]

        # Return response
        return gpt_result
        
    except:
        return None