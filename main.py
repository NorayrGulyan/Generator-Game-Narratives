from src.OpenAI.AI import OpenAIAssistant
from src.Generators.Generator import GameGenerator

api_key = None
all_statuses = {"win": 2, "almostwin": 1, "almostfail": -1, "fail": -2}
min_count_actions = 5
max_count_actions = 7

if __name__ == "__main__":
    ai = OpenAIAssistant(min_count_actions, max_count_actions, all_statuses, api_key)
    ai.init_client()
    statuses = ai.generate_statuses()
    generator = GameGenerator(all_statuses)
    actions = generator.generate_game_actions(statuses)
    print(generator.generate_json_configuration(statuses, actions))