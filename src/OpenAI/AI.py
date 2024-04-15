import os
import json
from openai import OpenAI


class OpenAIAssistant:
    def __init__(self, min_items: int, max_items: int, key=None, statuses=None):
        self.max_items = max_items
        self.min_items = min_items
        self.get_rit = False
        self.client = None
        self.statuses = {"win": 2, "almostwin": 1, "almostfail": -1, "fail": -2} if statuses is None else statuses
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
            while not self.get_rit:
                response = self.client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    response_format={"type": "json_object"},
                    messages=[
                        {
                            "role": "user",
                            "content": f"""generate a list of objects in JSON format from the given string 
                          "win", "fail", "almostwin", "almostfail" with a number of {self.min_items} to {self.max_items} 
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
            if self.min_items <= count <= self.max_items and type(content[0]) == str:
                for i in range(count):
                    if content[i] in self.statuses:
                        self.get_rit = True
                        continue
                    else:
                        self.get_rit = False
                        break
            return content
