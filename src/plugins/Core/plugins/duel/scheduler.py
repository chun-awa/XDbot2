from .monomer import Monomer


class Scheduler:

    def __init__(self, active: list[Monomer], passive: list[Monomer]):
        self.active = active
        self.passive = passive
        

    def start_fighting(self):
        for monomer in self.active + self.passive:
            monomer.prepare_before_fighting()
            monomer.action_value = 10000 / monomer.data["speed"]
        while not self.is_fighting_end():
            self.handle_round()


    def handle_round(self):
        for monomer in self.active + self.passive:
            monomer.prepare_before_the_round()
        action_monomer = self.get_action_monomer()
        action_monomer.prepare_before_action()
        action_monomer.start_action()


    def reset_action_value(self):
        for monomer in self.active + self.passive:
            if monomer.action_value == 0:
                monomer.action_value = 10000 / monomer.data["speed"]
                monomer.reduced_action_value = 0


    def is_fighting_end(self) -> bool:
        active_side_survives = False
        for monomer in self.active:
            if monomer.hp > 0:
                active_side_survives = True

        passive_side_survives = False
        for monomer in self.passive:
            if monomer.hp > 0:
                passive_side_survives = True
        
        return not (active_side_survives and passive_side_survives)
        

    def init_action_value(self):
        for monomer in self.active + self.passive:
            monomer.action_value = 10000 / monomer.data["speed"] - monomer.reduced_action_value
    

    def get_action_monomer(self):
        self.init_action_value()
        minimum_action_value_monomer: Monomer = self.active[0]
        for monomer in self.active + self.passive:
            if monomer.action_value < minimum_action_value_monomer.action_value:
                minimum_action_value_monomer = monomer

        reduced_action_value = minimum_action_value_monomer.action_value
        for monomer in self.active + self.passive:
            monomer.reduced_action_value += reduced_action_value
            monomer.action_value -= reduced_action_value
        return minimum_action_value_monomer
