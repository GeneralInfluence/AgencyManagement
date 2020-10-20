"""
Utilities to create new tasks (context switch) or related tasks (context building).
"""
import numpy as np
import uuid, sys
from datapipes.dataio import _DataStrategy

fibonacci = np.array([0,1,2,3,5,8,13,21])

class StrategyTasks(_DataStrategy):
    """Accept yaml arguments and generate data."""
    def __init__(self,**kwargs):
        self.__dict__.update(kwargs)
        sys.setrecursionlimit(10**6)

    def load(self):
        # Get developer tasks for the sprint
        uid = uuid.uuid4()
        dev_points = self.create_tasks(self.num_devs, self.max_velocity)
        for sprint in range(0,self.num_sprints-1):
        # while True:
            yield uid, dev_points
            dev_points = self.create_tasks(self.num_devs, self.max_velocity)
        yield uid, []

    def save(self):
        raise NotImplementedError("Save another way, this doesn't make sense!")

    def create_tasks(self, num_devs, max_velocity, scale="fibonacci"):
        """Create fibonacci tasks"""

        if scale=="fibonacci": # linear, quadratic, etc.
            sprint_points = 0
            dev_points = []
            while sprint_points <= (max_velocity * num_devs):
                chisq = list(np.random.chisquare(df=1, size=(1, num_devs))[0])
                scales = [num_devs / max(chisq)] * len(chisq)
                dev_points += [fibonacci[int(x)] for x in np.rint(np.array(scales) * np.array(chisq))]
                sprint_points = np.sum(dev_points)
        else:
            raise NotImplementedError("Supported Distributions Include: ['fibonacci']")

        return dev_points