import os
import json
from openai import OpenAI


class OpenAIAssistant:
    def __init__(self, min_count_actions: int, max_count_actions: int, statuses, key=None):
        self.min_count_actions = min_count_actions
        self.max_count_actions = max_count_actions
        self.statuses = statuses
        self.response_status = False
        self.client = None
        if key is None:
            self.key = os.environ.get('OPENAI_API_KEY')
        else:
            self.key = key

    def init_client(self) -> None:
        if self.client is None:
            if not self.key is None and len(self.key) != 0:
                print("Initializing OpenAI")
                self.client = OpenAI(
                    api_key=self.key
                )
            else:
                raise Exception("Please provide key")

    def generate_statuses(self) -> list:
        if self.client is not None:
            while not self.response_status:
                response = self.client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    response_format={"type": "json_object"},
                    frequency_penalty=-1,
                    messages=[
                        {
                            "role": "system",
                            "content": f"""generate a list of objects in JSON format from the given string 
                          "win", "fail", "almostwin", "almostfail" with a number of {self.min_count_actions} to {self.max_count_actions} 
                          objects and return only the list in json format"""
                        }
                    ],
                )
                return self.check_statuses(response)

    def check_statuses(self, response) -> list:
        if response is not None:
            content = json.loads(response.choices[0].message.content)
            content = content['objects']
            count = len(content)
            if self.min_count_actions <= count <= self.max_count_actions and type(content[0]) == str:
                for i in range(count):
                    if content[i] in self.statuses:
                        self.response_status = True
                        continue
                    else:
                        self.response_status = False
                        break
            return content
