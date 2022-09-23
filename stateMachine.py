# states: list containing all possible states
# transistions: list containing all possible transitions
# initialstate: str equal to key of starting state
class StateMachine:
    def __init__(self,states,transitions,initialState):
        self.oldStateName = "None"
        self.currentStateName = initialState
        self.states = {}
        for state in states:
            self.states[state.name] = state
        self.transitions = {}
        for transistion in transitions:
            self.transitions[transistion.name] = transistion
    
    def __call__(self):
        self.checkTransitions()
        self.run()
    
    # This method should be called continously in a loop
    def run(self):
        currentState = self.states[self.currentStateName]
        # Run current State's loop function, if it exists
        if callable(currentState.loop): currentState.loop()

# This method should be called continously in a loop
# checks if each transition's trigger is true. If so, checks if current
# state is in list of source states. if so, change state to corresponding
# target state
    def checkTransitions(self):
        for transition in self.transitions:
            currentTransition = self.transitions[transition]
            if currentTransition.checkTrigger():
                for index,source in enumerate(currentTransition.sourceStates):
                    if self.currentStateName == source.name:
                        self.changeState(currentTransition.targetStates[index])
                        break

    # call leave function, if any, switch to new State, call enter function, if any
    def changeState(self,newState):
        oldState = self.states[self.currentStateName]
        if callable(oldState.leave): oldState.leave()
        self.oldStateName = oldState.name
        self.currentStateName = newState.name
        
        newState = self.states[self.currentStateName]
        if callable(newState.enter): newState.enter()


# name: str name of State
# loop: func to run continuously while in given state
# enter: func to run once upon entering state
# leave: func to run once upon leaving state
class State:
    def __init__(self,name,loop=None,enter=None,leave=None):
        self.name = name
        self.loop = loop
        self.enter = enter
        self.leave = leave


# name: str name of Transition
# trigger: func to trigger transition. Should return Bool
# sources: list of source State objects
# targets: list of target State objects
# sources and targets should be lists of equal size. elements that share an
# index represent a source-destination pair
class Transition:
    def __init__(self, name,trigger,sources,targets):
        self.name = name
        self.getTrigger = trigger
        self.sourceStates = sources
        self.targetStates = targets

    def checkTrigger(self):
        return self.getTrigger()