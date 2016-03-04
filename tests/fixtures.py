# -*- coding: utf-8 -*-

import random

import pytest

import snakes.nets as snakes

_iterations = (
    ("zero_iter", 0),
    ("one_iter", 1),
    ("two_iter", 2),
    ("three_iter", 3),
    ("ten_iter", 10),
    ("huge_iter", 100),
)


def _random_sync_runner(pnet):
    enabled = {}
    while True:
        enabled.clear()
        for t in pnet.transition():
            modes = t.modes()
            if modes:
                enabled[t.name] = random.choice(modes)
        if enabled:
            keys = tuple(enabled.keys())
            t_name = random.choice(keys)
            t_mode = enabled[t_name]
            print("firing:", t_name, t_mode)
            pnet.transition(t_name).fire(t_mode)
        else:
            break

_runners = (
    ("sync_random", _random_sync_runner),
)

_petri_nets = (
    ("empty_net", lambda: snakes.PetriNet('Test Petri Net')),
)

def remove_empty_places(marking):
    to_remove = set()
    for name, tokens in marking.items():
        if not tokens:
            to_remove.add(name)
    for name in to_remove:
        del marking[name]


@pytest.fixture(params=[e[1] for e in _petri_nets], ids=[e[0] for e in _petri_nets])
def net(request):
    return request.param()


@pytest.fixture(params=[e[1] for e in _iterations], ids=[e[0] for e in _iterations])
def iterations(request):
    return request.param


@pytest.fixture(params=[e[1] for e in _runners], ids=[e[0] for e in _runners])
def runner(request):
    return request.param

