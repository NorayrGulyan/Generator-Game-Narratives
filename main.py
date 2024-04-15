from src.OpenAI.AI import OpenAIAssistant
from src.Generators.Generator import GameGenerator
api_key = None

if __name__ == "__main__":
    ai = OpenAIAssistant(5, 7, api_key)
    ai.init_client()
    statuses = ai.generate_statuses()
    generator = GameGenerator()
    actions = generator.generate_game_actions(statuses)
    print(generator.generate_json_configuration(statuses, actions))