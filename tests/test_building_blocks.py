import snakes.nets as snakes


def factory(cons, prod, init=(1, 2, 3)):
    n = snakes.PetriNet("Test Net")
    n.add_place(snakes.Place("src", list(init)))
    n.add_place(snakes.Place("tgt", []))
    t = snakes.Transition("t")
    n.add_transition(t)
    n.add_input("src", "t", cons)
    n.add_output("tgt", "t", prod)
    return n, t, t.modes()


def test_place():
    p = snakes.Place('my_place', [])
    p.add(1)
    assert 1 in p
    p.remove(1)
    assert 1 not in p


def test_expression():
    n, t, modes = factory(snakes.Variable("x"), snakes.Expression("x-1"))
    t.fire(snakes.Substitution(x=1))
    assert 0 in n.get_marking()['tgt']


def test_annotations():
    n, t, modes = factory(snakes.Test(snakes.Variable("x")), snakes.Expression("10+x"))
    t.fire(snakes.Substitution(x=1))
    assert 1 in n.get_marking()['src']
    n, t, modes = factory(snakes.Flush("x"), snakes.Variable("x"))
    assert snakes.Substitution(x=snakes.MultiSet([1, 2, 3])) in t.modes()
    n, t, modes = factory(snakes.MultiArc([snakes.Variable("x"), snakes.Variable("y")]),
                          snakes.MultiArc([snakes.Expression("x+y"), snakes.Value(0), snakes.Expression("x<y")]))
    t.fire(snakes.Substitution(y=2, x=1))
    assert n.get_marking()['tgt'] == snakes.MultiSet([0, True, 3])


def test_guard():
    n = snakes.PetriNet("Test Net")
    n.add_place(snakes.Place("src", [0, 1, 2]))
    n.add_place(snakes.Place("tgt", []))
    t = snakes.Transition("t", snakes.Expression("x==0"))
    n.add_transition(t)
    assert snakes.Substitution(x=1) not in t.modes()


def test_structured_token():
    n, t, modes = factory(snakes.Tuple([snakes.Variable("x"), snakes.Variable("y")]),
                          snakes.Tuple([snakes.Expression("x+y"), snakes.Value(0), snakes.Expression("x<y")]),
                          [(0, 1), (1, 2), (2, 3)])
    t.fire(snakes.Substitution(y=1, x=0))
    assert n.get_marking()['tgt'] == snakes.MultiSet([(1, 0, True)])


def test_marking():
    n = snakes.PetriNet("Test Net")
    n.add_place(snakes.Place("tgt", []))
    n.set_marking(snakes.Marking({'tgt': snakes.MultiSet([1, 2, 3])}))
    assert n.get_marking()["tgt"] == snakes.MultiSet([1, 2, 3])
    n.set_marking(snakes.Marking({'tgt': snakes.MultiSet([1, 1, 1, 2, 3])}))
    assert n.get_marking()["tgt"][1] == 3


def test_fire():
    n, t, modes = factory(snakes.Value(2), snakes.Value(8))
    t.fire(snakes.Substitution())
    marking = n.get_marking()
    assert 8 in marking["tgt"]
    assert 2 not in marking["src"]
