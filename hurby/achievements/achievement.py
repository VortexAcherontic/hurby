from hurby.achievements.evaluation import Evaluation
from hurby.achievements.hook import Hook
from hurby.achievements.scope import Scope
from hurby.achievements.type import Type
from hurby.character.character import Character
from hurby.utils import logger


class Achievement:

    def __init__(self, achieve_id: str, json_data: dict):
        self.id: str = achieve_id
        self.title: str = json_data["title"]
        self.condition_text: str = json_data["condition_text"]
        self.reward_credits: int = json_data["reward_credits"]
        self.hook: Hook = json_data["condition"]["hook"]
        self.scope: Scope = json_data["condition"]["scope"]
        self.type: Type = json_data["condition"]["type"]
        self.trigger: str = json_data["condition"]["trigger"]
        self.eval: Evaluation = json_data["condition"]["eval"]

    def validate(self, hook: Hook, scope: Scope, achieve_type: Type, scope_object, trigger_reference) -> bool:
        if self.hook == hook and self.scope == scope and self.type == achieve_type:
            if isinstance(scope_object, Character):
                match self.eval:
                    case Evaluation.EQUALS:
                        return trigger_reference == self.trigger
                    case Evaluation.LESSER:
                        return trigger_reference < self.trigger
                    case Evaluation.GREATER:
                        return trigger_reference > self.trigger
                    case Evaluation.LESSER_THEN:
                        return trigger_reference <= self.trigger
                    case Evaluation.GREATER_THEN:
                        return trigger_reference >= self.trigger
                    case _:
                        logger.log(logger.WARN, "Unknown evaluation type: " + str(self.eval))
        else:
            return False

    def achieve(self, scope_object):
        match self.scope:
            case Scope.CHARACTER:
                if isinstance(scope_object, Character):
                    if self.id not in scope_object.achievements_gained or not scope_object.achievements_gained[self.id]:
                        scope_object.add_credits(self.reward_credits)
                        scope_object.achievements_gained[self.id] = True
                else:
                    logger.log(logger.WARN, "Scope object type does not match scope: " + str(self.scope))
            case _:
                logger.log(logger.WARN, "Unknown scope: " + str(self.scope))
