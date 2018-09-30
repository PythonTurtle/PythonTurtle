"""
'When' step implementations for acceptance tests.  Powered by behave.
"""
from behave import when


@when(u'I import major modules')
def step_impl(context):
    """
    Try to import PythonTurtle module
    """
    import pythonturtle
    import pythonturtle.misc
    import pythonturtle.shelltoprocess

    context.imported_modules = [
        pythonturtle,
        pythonturtle.misc,
        pythonturtle.shelltoprocess,
    ]
