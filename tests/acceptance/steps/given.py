"""
'Given' step implementations for acceptance tests.  Powered by behave.
"""
from behave import given


@given(u'PythonTurtle is installed')
def step_impl(context):
    """
    Running the test with Tox this should be taken for granted
    """
    pass
