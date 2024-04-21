#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Standard Library Modules
import typing

# Related Third-Party Modules
from g4f.client import Client


# FreeGpt4 Chat Provider
def gpt_4_free_client(messages: typing.List[typing.Dict[str, str]]) -> typing.Union[str, typing.NoReturn]:
    """
    Chat completion for gpt4free client
    
    Parameters:
        messages (List[Dict[str, str]]): Conversation history

    Returns:
        result (Union[str, None]): result or None in failure
    """
    client = Client()

    # Try to send request or return None on failure
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=messages,
        )
        return response.choices[0].message.content
        
    except:
        return None