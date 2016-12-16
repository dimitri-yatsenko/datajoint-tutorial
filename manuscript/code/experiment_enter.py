e = Experiment()

# enter one at a time
e.insert1(dict(exp_date="2016-10-01", name="Carol", notes="awesome data!"))

# enter with default attribute value
e.insert1(dict(exp_date="2016-10-02", name="Bob"))

# enter by position (without attribute names)
e.insert1(('2016-10-03', 'Alice', 'found a piece of dark matter.'))

# enter several tuples together
e.insert((
        ("2016-10-04", "Carol", "stunning!"),
        ("2016-10-05", "Bob", "inexplicable patterns."),
        ("2016-10-06", "Alice", "A boson got loose.")
    ))

