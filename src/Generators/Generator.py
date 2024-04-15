import json


class GameGenerator:
    def __init__(self, statuses=None):
        print("Initializing Generator")
        self.statuses = {"win": 2, "almostwin": 1, "almostfail": -1, "fail": -2} if statuses is None else statuses

    def generate_game_actions(self, statuses: list) -> list:
        if statuses is not None:
            actions = []
            for stat in statuses:
                action = {
                    "type": "user_action",
                    "component": "TTCollectThree2DUserAction",
                    "params": {
                        "outcome": stat
                    }
                }
                actions.append(action)
            return actions

    def determine_final_outcome(self, statuses: list) -> str:
        if statuses is not None:
            result = 0
            for stat in statuses:
                result += self.statuses[stat]
            return "win" if result > 0 else "fail"

    def generate_json_configuration(self, statuses: list, actions: list) -> list:
        if statuses is not None and actions is not None:
            final_outcome = self.determine_final_outcome(statuses)
            game_narrative = actions + [{
                "type": "gameplay_outcome",
                "component": "FinalOutcome",
                "params": {
                    "final_outcome": final_outcome
                }
            }]
            with open('game_narrative.json', 'w') as file:
                json.dump(game_narrative, file, indent=4)
            print("JSON configuration generated successfully. Check 'game_narrative.json'.")
            return game_narrative
