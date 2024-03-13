#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Standard Library Modules
import random
import string
import json
import typing

# Related Third-Party Modules
import requests


# FreeGpt4 Chat Provider
def free_gpt_4(messages: typing.List[typing.Dict[str, str]]) -> typing.Union[str, typing.NoReturn]:
    """
    Chat completion for FreeGpt4
    
    Parameters:
        messages (List[Dict[str, str]]): Conversation history

    Returns:
        result (Union[str, None]): result or None in failure
    """
    # Base URL for provider API
    url: str = "https://api.freegpt4.tech/v1/chat/completions"
    
    # Request headers
    headers: typing.Dict[str, str] = {
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/119.0",
        "Accept": "text/event-stream",
        "Accept-Language": "de,en-US;q=0.7,en;q=0.3",
        "Accept-Encoding": "gzip, deflate, br",
        "Content-Type": "application/json",
        "Authorization": "Bearer fg4-5KHloX6hCWhyRnJlZUdQVDQiQSiwwZ8ysll",
        "Connection": "keep-alive"
    }

    # Request data
    data: typing.Dict[str, typing.Any] = {
        "messages": messages,
        "stream": True,
        "model": "gpt-4",
        "temperature": 0.5,
        "presence_penalty": 0,
        "frequency_penalty": 0,
        "top_p": 0.5,
    }
   
    # Try to send request or return None on failure
    try:
        # Get result from request
        res = requests.post(url=url, json=data, headers=headers).text
        
        # Get final streamed response
        gpt_result = ""
        for chuck in res.strip().split("\n\n")[:-1]:
            temp = json.loads(chuck.split("data: ")[1])
            try:
                gpt_result += temp['choices'][0]['delta']["content"]
            except:
                pass

        # Return response
        return gpt_result
        
    except:
        return None