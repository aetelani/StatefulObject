from concurrent.futures._base import Executor, Future
from concurrent.futures.thread import ThreadPoolExecutor
from functools import partial
from queue import Queue, PriorityQueue
from typing import Callable, Any, Tuple, List, NewType, Optional

Condition = Callable[[Any], bool]
prio = int
Action = Tuple[prio, Callable[[Any], bool]]
ActionDoneCb = Callable[[Any], Any]
State = int
event_name, event_args = str, Optional[Any]
Event = Tuple[event_name, event_args]
from_state, to_state = State, State
Transition = Tuple[from_state, to_state, Condition, Action, ActionDoneCb]
Transitions = NewType('Transitions', List[Transition])


def exec_next_action(q: Queue):
    return q.get()[2]()


def stateful_generator(initial: int, ts: Transitions, executor: Executor = None, q: Queue = None,
                       exec_wait_result=True):
    pool = executor or ThreadPoolExecutor()

    next_state = (initial,)

    (f, t, c, pa, d) = zip(*ts)
    p, a = zip(*pa)

    prio_default: int = len(ts)

    def seq_prio():
        start_ind = 0
        while True:
            yield start_ind
            start_ind += 1

    next_prio = seq_prio()

    if q is None:
        local_execution = True
        q: PriorityQueue = PriorityQueue()
    else:
        local_execution = False

    def test(tester: Callable):
        return tester(event)

    def run(action_index) -> bool:
        def wrap(fun, ev, done, queue: Queue):
            def done_wrap(done_future: Future):
                queue.task_done()
                done(done_future)

            action_future = pool.submit(fun, ev)
            action_future.add_done_callback(done_wrap)
            return action_future

        priority, prio_seq = p[action_index] or prio_default, next(next_prio)
        item = (priority, prio_seq, partial(wrap, a[action_index], event, d[action_index], q))
        q.put(item)

        if local_execution:
            exec_next_action(q)

        return True

    try:
        while True:
            event: Event = yield next_state
            ss = [t[i] for i in range(len(f)) if f[i] in next_state and test(c[i]) and run(i)]
            next_state = set(ss) or next_state
    finally:
        if exec_wait_result:
            q.join()
