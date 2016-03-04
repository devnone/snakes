# -*- coding: utf-8 -*-

import snakes.nets as snakes

# NB: due to the discovery mechanism carried out by py.test, we can import test modules
# in the same way as if they were proper modules (even if no __init__.py is present).
# For further details: https://pytest.org/latest/goodpractises.html
from fixtures import *


def test_no_enabled(net, iterations, runner):
    net.add_place(snakes.Place('stage_0'))
    net.add_place(snakes.Place('stage_1'))
    #
    t = snakes.Transition('t', snakes.Expression('x<{}'.format(iterations)))
    net.add_transition(t)
    net.add_input('stage_0', 't', snakes.Variable('x'))
    net.add_output('stage_1', 't', snakes.Expression('x'))
    #
    initial_marking = snakes.Marking({'stage_0': snakes.MultiSet([iterations+1])})
    net.set_marking(initial_marking)
    assert(len(t.modes()) == 0)
    runner(net)
    #
    final_marking = net.get_marking()
    assert(final_marking == initial_marking)


def test_increment_loop(net, iterations, runner):
    net.add_place(snakes.Place('body'))
    #
    loop_t = snakes.Transition('loop', snakes.Expression('x<{}'.format(iterations)))
    net.add_transition(loop_t)
    net.add_input('body', 'loop', snakes.Variable('x'))
    net.add_output('body', 'loop', snakes.Expression('x+1'))
    #
    net.set_marking({'body': 0})
    runner(net)
    #
    final_marking = net.get_marking()['body']
    assert(len(final_marking) == 1)
    value = next(iter(final_marking))
    assert(value >= iterations)


def test_increment_unroll(net, iterations, runner):
    net.add_place(snakes.Place('stage_0'))
    for i in range(1, iterations+1):
        p_start = i-1
        p_start_name = 'stage_{}'.format(p_start)
        p_end = i
        p_end_name = 'stage_{}'.format(p_end)
        t_name = '{}_to_{}'.format(p_start, p_end)
        #
        net.add_place(snakes.Place(p_end_name))
        #
        net.add_transition(snakes.Transition(t_name))
        net.add_input(p_start_name, t_name, snakes.Variable('x'))
        net.add_output(p_end_name, t_name, snakes.Expression('x+1'))
    #
    net.set_marking({'stage_0': 0})
    runner(net)
    #
    final_marking = net.get_marking()['stage_{}'.format(iterations)]
    assert(len(final_marking) == 1)
    value = next(iter(final_marking))
    assert(value >= iterations)


