from typing import Callable, Any, Tuple, List, NewType, Optional

Condition = Callable[[Any], bool]
Action = Callable[[Any], bool]
ActionDone = Callable[[Any], Any]
State = int
event_name, event_args = str, Optional[Any]
Event = Tuple[event_name, event_args]
from_state, to_state = State, State
Transition = Tuple[from_state, to_state, Condition, Action, ActionDone]
Transitions = NewType('Transitions', List[Transition])


def stateful_generator(initial: int, ts: Transitions):
    next_state = initial
    (f, t, c, a, d) = zip(*ts)

    def test(tester: Callable):
        return tester(event)

    def run(action_index) -> bool:
        result = a[action_index](event)
        d[action_index](result)
        return True

    while True:
        event: Event = yield next_state
        ss = [t[i] for i in range(len(f)) if f[i] == next_state and test(c[i]) and run(i)]
        next_state = ss and ss[0] or next_state
