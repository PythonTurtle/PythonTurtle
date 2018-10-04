"""
Tests for application.
"""


def test_import_turtle():
    """
    Try to import PythonTurtle module and perform some stupid verifications.
    """
    import pythonturtle
    assert pythonturtle.__version__ is not None

    from pythonturtle import application
    assert application is not None

    from pythonturtle import helppages
    assert helppages is not None

    from pythonturtle import my_turtle
    assert my_turtle is not None

    from pythonturtle import turtleprocess
    assert turtleprocess is not None

    from pythonturtle import turtlewidget
    assert turtlewidget is not None


def test_import_misc():
    """
    Try to import the misc submodule and perform some stupid verifications.
    """
    from pythonturtle.misc import helpers
    assert helpers is not None

    from pythonturtle.misc import smartsleep
    assert smartsleep is not None

    from pythonturtle.misc import vector
    assert vector is not None


def test_import_shelltoprocess():
    """
    Try to import the misc submodule and perform some stupid verifications.
    """
    from pythonturtle import shelltoprocess
    assert shelltoprocess is not None

    from pythonturtle.shelltoprocess import console
    assert console is not None

    from pythonturtle.shelltoprocess import forkedpyshell
    assert forkedpyshell is not None

    from pythonturtle.shelltoprocess import shell
    assert shell is not None
