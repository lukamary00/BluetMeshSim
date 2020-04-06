from simulation.environment.environment_variables import EnvironmentVariable


class Environment:
    """
    Class which should state of world.

    Provide interface to interaction between nodes and elements.
    """

    def __init__(self):
        """Bake all exising variables."""
        self.bake()

    def bake(self):
        """Create all implemented environment variables."""
        self.variables = {}
        for env_variable, var_creator in EnvironmentVariable.existing_variables.items():
            self.variables[env_variable] = var_creator()
        