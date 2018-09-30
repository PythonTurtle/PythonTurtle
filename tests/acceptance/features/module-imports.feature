Feature: Basic verification of Python version support
  As a PythonTurtle developer
  I want Python to import modules successfully
  So that I can prove that the program would start up

  Scenario: Try to import major modules
    Given PythonTurtle is installed
    When I import major modules
    Then the modules loaded correctly
