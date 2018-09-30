"""
'Then' step implementations for acceptance tests.  Powered by behave.
"""
from behave import then


@then(u'the modules loaded correctly')
def step_impl(context):
    """
    Do some ultra-basic verifications
    """
    [
        pythonturtle,
        pythonturtle_misc,
        pythonturtle_shelltoprocess
    ] = context.imported_modules

    assert pythonturtle.__version__ is not None
    assert pythonturtle_misc is not None
    assert pythonturtle_shelltoprocess is not None
