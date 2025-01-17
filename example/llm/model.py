# Copyright 2002-2007 the original author or authors.
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from typing import List, Union

import openai



class OpenAI():

    name = "OpenAI"
    description = "OpenAI API for text completion using various models"

    def __init__(self, api_key: str, 
                       model: str = "text-davinci-003"):
        
        self._api_key = api_key
        self.model    = model
        self._openai  = openai
        self._openai.api_key = self._api_key
        self.supported_models = ["text-davinci-003", "text-curie-001", "text-babbage-001", "text-ada-001"]

    def run(
        self,
        prompts: List[str],
        temperature: float = 0.7,
        max_tokens: int = 4000,
        top_p: float = 0.1,
        frequency_penalty: float = 0,
        presence_penalty: float = 0,
        stop: Union[str, None] = None,
    ):
        """
        prompts: The prompt(s) to generate completions for, encoded as a string, array of strings, array of tokens, or array of token arrays.
        temperature: What sampling temperature to use. Higher values means the model will take more risks. Try 0.9 for more creative applications, and 0 (argmax sampling) for ones with a well-defined answer.
                    We generally recommend altering this or top_p but not both.
        max_tokens: The maximum number of tokens to generate in the completion.
                    The token count of your prompt plus max_tokens cannot exceed the model's context length. Most models have a context length of 2048 tokens (except for the newest models, which support 4096).
        top_p: An alternative to sampling with temperature, called nucleus sampling, where the model considers the results of the tokens with top_p probability mass. So 0.1 means only the tokens comprising the top 10% probability mass are considered.
                We generally recommend altering this or temperature but not both.
        frequency_penalty: Number between -2.0 and 2.0. Positive values penalize new tokens based on their existing frequency in the text so far, decreasing the model's likelihood to repeat the same line verbatim.
        presence_penalty: Number between -2.0 and 2.0. Positive values penalize new tokens based on whether they appear in the text so far, increasing the model's likelihood to talk about new topics.
        stop: Up to 4 sequences where the API will stop generating further tokens. The returned text will not contain the stop sequence.
        """
        
        result = []
        for prompt in prompts:
            response = self._openai.Completion.create(
                model=self.model,
                prompt=prompt,
                temperature=temperature,
                max_tokens= max_tokens - len(prompt),
                top_p=top_p,
                frequency_penalty=frequency_penalty,
                presence_penalty=presence_penalty,
                stop=stop,
            )
            data = {}
            data.update(response["usage"])
            data["text"] = response["choices"][0]["text"]
            result.append(data)

        return result