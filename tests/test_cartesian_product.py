# -*- coding: utf-8 -*-

import pytest

import collections
import itertools

import snakes.nets as snakes

# NB: due to the discovery mechanism carried out by py.test, we can import test modules
# in the same way as if they were proper modules (even if no __init__.py is present).
# For further details: https://pytest.org/latest/goodpractises.html
from fixtures import *

_data = collections.OrderedDict()
for i in range(4):
    for j in range(4):
        _data['{}_{}'.format(i, j)] = [tuple(range(i)), tuple(range(j))]

_data['mix_2_4'] = [(1, 2), ('a', 'b', 'c', 'd')]

@pytest.fixture(params=tuple(_data.values()), ids=tuple(_data.keys()))
def initial_marking(request):
    return snakes.Marking(input_place_0=request.param[0], input_place_1=request.param[1])

def _full_petri_net():
    net = snakes.PetriNet('Cartesian product')
    net.add_place(snakes.Place('input_place_0'))
    net.add_place(snakes.Place('input_place_1'))
    
    net.add_place(snakes.Place('output_place'))
    
    #net.add_transition(snakes.Transition('t'))
    
    net.add_place(snakes.Place('input_place_0_buffer'))
    net.add_transition(snakes.Transition('transition_0', snakes.Expression('not x_inhibitor')))
    net.add_input('input_place_0_buffer', 'transition_0', snakes.Test(snakes.Flush('x_inhibitor')))
    net.add_input('input_place_0', 'transition_0', snakes.Variable('x_0'))
    
    net.add_place(snakes.Place('input_place_1_buffer'))
    net.add_input('input_place_1', 'transition_0', snakes.Test(snakes.Flush('x_1')))
    net.add_output('input_place_0_buffer', 'transition_0', snakes.Expression('x_0'))
    net.add_output('input_place_1_buffer', 'transition_0', snakes.Flush('x_1'))
    
    net.add_transition(snakes.Transition('transition_1'))
    net.add_input('input_place_0_buffer', 'transition_1', snakes.Test(snakes.Variable('y_0')))
    net.add_input('input_place_1_buffer', 'transition_1', snakes.Variable('y_1'))
    net.add_output('output_place', 'transition_1', snakes.Expression('(y_0, y_1)'))
    
    net.add_transition(snakes.Transition('clear_buffer', snakes.Expression('not z_inhibitor')))
    net.add_input('input_place_0_buffer', 'clear_buffer', snakes.Variable('z'))
    net.add_input('input_place_1_buffer', 'clear_buffer', snakes.Test(snakes.Flush('z_inhibitor')))

    net.add_transition(snakes.Transition('clear_input_place_1', snakes.Expression('w_1') & snakes.Expression('not w_inhibitor')))
    net.add_input('input_place_1', 'clear_input_place_1', snakes.Flush('w_1'))
    net.add_input('input_place_0', 'clear_input_place_1', snakes.Test(snakes.Flush('w_inhibitor')))
    return net


def _itertools_net():
    net = snakes.PetriNet('Cartesian product')
    net.declare("import itertools")
    net.add_place(snakes.Place('input_place_0'))
    net.add_place(snakes.Place('input_place_1'))
    net.add_place(snakes.Place('output_place'))
    net.add_transition(snakes.Transition('transition', snakes.Expression("x_0 or x_1")))

    net.add_input('input_place_0', 'transition', snakes.Flush('x_0'))
    net.add_input('input_place_1', 'transition', snakes.Flush('x_1'))

    net.add_output('output_place', 'transition', snakes.Flush("itertools.product(x_0, x_1)"))

    return net


@pytest.fixture(params=[_full_petri_net, _itertools_net], ids=['full_petri_net', 'itertools'])
def net(request):
    return request.param()


def test_cartesian_product(runner, net, initial_marking):
    net.set_marking(initial_marking)
    runner(net)
    
    final_marking = net.get_marking()
    expected_output = snakes.MultiSet(itertools.product(initial_marking['input_place_0'], initial_marking['input_place_1']))
    expected_marking = snakes.Marking(output_place=expected_output)

    remove_empty_places(expected_marking)

    assert final_marking == expected_marking
    






