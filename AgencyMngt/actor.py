from datapipes.factory import Factory
from datapipes.observer import Subject
from abc import ABC, abstractmethod
from typing import Generator, Dict, Any, List
from tasking import *
from neodb import *
import numpy as np


@Factory.register("Manager")
class Manager(): # Actor() with Management functions

  def __init__(self, *args, **kwargs):
    self.__dict__.update(kwargs)
    self._team = {"sprint_stats":{},"developers":[dev for dev in self.observers if "Developer" in dev]}
    self.actors_neo = ActorsNeo()
    # Establish the network we save to later.
    self.actors_neo.create_node("Manager",self.name,self.type)
    for node in self.observers:
      if "Developer" in node:
        self.actors_neo.create_node("Developer",node,"Developer") # Would rather access that object directly...
        self.actors_neo.create_relationship( "Manager", "Developer", self.name, node, "Tasking" )

  # OBSERVER PATTERN -----------------------------------------------
  def update(self, subject: Subject) -> None:
    """What are subject states that would make us act differently?"""
    if subject._state is "Tasking":
      self._listen()

    elif subject._state is "Sharing":
      self._manage_sprint( name=subject.pubsub_message['cfg']['name'],
                    last_sprint=subject.pubsub_message['sprint_stats'])

    elif subject._state is "source":
      self.sprint = subject.pubsub_message
      self._start_sprint()

    # elif subject._state is "Structuring":
    #   self._configure()
    # elif subject._state is "Sharing":
    #   self._share()
    # elif subject._state is "Time":
    #   self._work()

    return 0

  def _listen(self):
    """For a Manager to be listening, they are determining if their tasks have been executed or not."""
    # Not implemented, what would they do different anyway?
    pass

  def _manage_sprint(self,name=None,last_sprint=None):
    """A manager report would be the progress of the team, maybe that Developer's relative performance."""
    if type(last_sprint)==type(None):
      raise NotImplementedError("How?")

    self._team['sprint_stats'][name] = last_sprint # Saves to Neo4j??

    if len(self._team['sprint_stats'].keys())==(len(self.observers)-1):
      self.actors_neo.assign_node_stats(stats=self._team['sprint_stats'])
      self._team['sprint_stats'] = {}

      # Try to start new sprint, write to Neo4j otherwise and finish.
      # for sprint in range(0,self.num_sprints-1):
      uid, tasks = next(self.sprint['data'])
      if len(tasks)>0:
        self._start_sprint(tasks=tasks)
      else:
        # Simulation is over.
        self.calc_final_stats()
        # self.actors_neo.close()
        print("Need to close neo connections?")

  def calc_final_stats(self):
    for dev in self._team['developers']:
      stats = self.actors_neo.calc_dev_stats(dev)

  def _start_sprint(self,tasks=None):
    if type(tasks)==type(None):
      uid, tasks = next(self.sprint['data'])
    self.PubSub._state = "Tasking"
    sprint_tasks = {}
    num_devs = len(self._team["developers"])
    step = int(len(tasks) / num_devs)
    for dx in range(0,num_devs):
      dev = self._team["developers"][dx]
      sx = dx * (step+1)
      sprint_tasks[dev] = tasks[sx:(sx+step)]
    self.PubSub.pubsub_message['tasks'] = sprint_tasks
    self.notify() # Notifies all subscribers.

  def _configure(self):
    """A Manager could conceivably change who officially communicates what."""
    # Not implementing dynamic org structures
    pass

  def _share(self):
    """Share the next set of tasks with the Developer team."""
    # Get the next set of tasks from the csv
    # Maybe add noise
    dev_tasks = create_tasks(num_devs, max_velocity, scale="fibonacci")
    self.PubSub._state = "Time"
    self.PubSub.pubsub_message['tasks'] = tasks
    self.notify()

  def _work(self):
    """Organize the next set of tasks for Developers."""
    # This is covered by the flat file.
    pass

  # def _save2Neo4j(self):
  #   print("Neo Saved too")
  #   self.actors_neo.assign_node_stats()


@Factory.register("Developer")
class Developer(): # Actor() with Developer functions
  """
  Developers can develop independently, coordinate within their team, or across teams.
  When developing independently, the only cost to Managers is context switching, which is usually blamed on the developer.
  When coordinating within a team, Managers gain the extra velocity but pay a larger price for context switching.
  When coordinating across teams, Managers suddenly have to coordinate with other Managers.
  The goal is to show that developers coordinating increases productivity as well as cost of context switching.
  Secondary goal is to show that if Managers work with Developers and set priorities once tasks are complete,
  in other words give time horizons to Developer coordination, everyone wins.
    Questions:
      - How best can Manager choose the time horizon?
      - Can Managers estimate lost productivity due to context switching?
  Tertiary goal, next steps really, would be to show that this concept can be applied as the hierarchy grows.
  """

  def __init__(self, *args, **kwargs):
    self.__dict__.update(kwargs)
    self.sprint_knowledge_learned = 0
    self.sprint_velocity = self.velocity
    self.actors_neo = ActorsNeo()
    for node in self.observers:
      if "Developer" in node:
        self.actors_neo.create_relationship("Developer", "Developer", self.name, node, "Sharing")

  # OBSERVER PATTERN -----------------------------------------------
  def update(self, subject: Subject) -> None:
    """What are subject states that would make us act differently?"""
    # Does a simple pub/sub cover the simulation?
    # How do actor's find out what to subscribe to?
    # Why do they try to connect?
    #   How do they become a candidate to someone for connection?
    #     When they have a candidate, how do they select?
    #     Once they've selected, how do they evaluate?
    #     Once the candidate is approved, when do they share? :: Probably after some configuration of stories completed.
    #   How do they...
    # These questions are for a much more dynamic simulation.
    # A far simpler first step is to randomize these connections and measure their performance.
    # These connections are twofold:
    #   1. Connections expected (management)
    #   2. Connections desired (friends and associates)
    # Neither of these connection patterns is good or bad, the goal is to recognize what patterns compliment each other best.

    if subject._state is "Tasking":
      self._listen_tasks(subject)

    elif subject._state is "Requesting":
      self._report()
    elif subject._state is "Structuring":
      self._configure()

    elif subject._state is "Sharing":
      self._listen_work(subject)

    elif subject._state is "Time":
      self._work()

  def _listen_tasks(self,subject):
    """A Developer gets their task."""
    self.this_sprint = subject.pubsub_message
    # Work, save, and measure
    self._work()
    self._calc_sprint_stats()
    # Organize message
    self.PubSub._state = "Sharing"
    self.PubSub.pubsub_message['sprint_tasks_completed'] = self.sprint_tasks_completed
    self.PubSub.pubsub_message['sprint_stats'] = self.sprint_stats
    self.PubSub.pubsub_message['sprint_knowledge'] = self._share()
    # Reset sprint variables
    self.sprint_velocity = self.velocity # Reset sprint
    self.sprint_knowledge_learned = 0
    # Share your work
    self.notify()

  def _listen_work(self, subject):
    """Listen and learn from their work"""
    self.sprint_knowledge_learned += subject.pubsub_message['sprint_knowledge']
    self.actors_neo.assign_relationship_knowledge_learned("Developer", "Developer", self.name,
                                                           subject.pubsub_message['cfg']['name'],
                                                           subject.pubsub_message['sprint_knowledge'])

  def _report(self):
    """Report on the progress of the task."""
    pass
  def _configure(self):
    """Choose Developers to work with, perhaps on a given task."""
    pass

  def _share(self):
    """Share your work with another developer."""
    knowledge_sharing = False
    for observer in self.observers:
      if "Developer" in observer:
        knowledge_sharing = True
        break

    if knowledge_sharing:
      cost = 5
      self.sprint_velocity = max(0,self.sprint_velocity - cost)
      self.actors_neo.assign_relationship_knowledge_cost( self.name, cost)
      # print(f"saving cost for node {self.name}")
      return int(np.ceil(sum([task for xx,task,energy in self.PubSub.pubsub_message['sprint_tasks_completed'] if energy>=task]) / 10))
    return 1

  def _work(self):
    """Advance the task at hand.
    https://neo4j.com/docs/graph-data-science/current/management-ops/graph-catalog-ops/index.html
    """
    energy = self.sprint_velocity + self.sprint_knowledge_learned
    sprint_tasks_completed = []
    for t in range(0,len(self.this_sprint['tasks'])-1):
      task = self.this_sprint['tasks'][self.name][t]
      sprint_tasks_completed += [(t,task,max(energy,0))]
      energy -= task

    self.sprint_tasks_completed = sprint_tasks_completed

  # QUESTION PATTERN -------------------------------------------------
  def _calc_sprint_stats(self):
    # How productive are they now
    sprint_velocity = sum([task for t,task,energy in self.sprint_tasks_completed if energy>=task])
    efficiency = sprint_velocity / self.velocity
    self.sprint_stats = {"sprint_velocity":sprint_velocity,"efficiency":efficiency}

# How would a manager use Agency Management?
# Is there an optimum org structure? What’s the tradeoff? (efficiency vs flexibility)
# How does this empower developers? (model your organization)
