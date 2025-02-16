from PyMisc.variable import constant

#####################
# Logic State
#####################
class State(constant):
    def __init__(self, state: bool):
        super().__init__(state)

    def __repr__(self) -> str:
        return '01'[self.value]


#####################
# Gate
#####################
class Gate:
    @staticmethod
    def AND(logic_states: list[State]) -> State:
        pass


#####################
# Testing
#####################
if __name__ == '__main__':
    states: list[State] = [State(True), State(False), State(True)]
    print(
        Gate.AND(states)
    )
