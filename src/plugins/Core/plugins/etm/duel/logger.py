from typing import TYPE_CHECKING
from ..._utils import *

if TYPE_CHECKING:
    from .entity import Entity


class Logger:

    def __init__(self, user_id: str) -> None:
        self.logs = []
        self.current = ""
        self.user_id = user_id

    def text(self, key: str, _format: list = []) -> str:
        return lang.text(f"duel_logger.{key}", _format, self.user_id)

    def log(self, key: str, _format: list = []) -> None:
        self.log_string(self.text(key, _format))

    def log_string(self, string: str) -> None:
        self.current += string

    def create_block(self) -> None:
        self.logs.append(self.current)
        self.current = ""

    def clear(self) -> None:
        self.logs = []

    def add_action_queue(
        self, entities_: "list[Entity]", entity_count: int = 8
    ) -> None:
        entities = sorted(entities_, key=lambda e: e.get_action_value())
        self.log(
            "action_queue_title",
            [
                self.text("long_entity_name", [entities[0].name, entities[0].team_id]),
                self.text("action_queue_array", []),
            ],
        )
        entities.pop(0)
        for i in range(len(entities)):
            if i >= entity_count - 2:
                break
            elif i != 0:
                self.log("action_queue_array")
            entity = entities[i + 1]
            self.log("long_entity_name", [entity.name, entity.team_id])
        self.log_string("\n\n\n")

    def add_entity_hp(self, entity: "Entity") -> None:
        self.log(
            "entity_hp",
            [entity.hp, entity.max_hp, int(entity.hp / entity.max_hp * 100)],
        )

    def add_action_title(self, entity: "Entity") -> None:
        self.log(
            "action_title",
            [self.text("long_entity_name", [entity.name, entity.team_id])],
        )
