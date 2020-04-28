from typing import Callable, Any, Tuple, List, NewType

Condition = Callable[[Any], bool]
Action = Callable[[Any], Any]

from_state, to_state = int, int
Transition = Tuple[from_state, to_state, Condition, Action]
Transitions = NewType('Transitions', List[Transition])


def stateful_generator(initial: int, ts: Transitions):
    next_state = initial
    (f, t, c, a) = zip(*ts)

    def test(tester: Callable):
        return tester(event)

    def run(action: Callable) -> bool:
        action(event)
        return True

    while True:
        event = yield next_state
        ss = [t[i] for i in range(len(f)) if f[i] == next_state and test(c[i]) and run(a[i])]
        next_state = ss and ss[0] or next_state
