from datapipes.base import MathBase
from datapipes.factory import Factory
from datapipes.observer import Subject,Observer,ConcreteSubject
from typing import Generator, Dict, Any, List


@Factory.register("Actor")
class Actor(MathBase,Observer,ConcreteSubject):

  def __init__(self, *args, **kwargs):
    self.__dict__.update(kwargs)

    # There needs to be some serious configuration here for the Actor's states and initial connections.

  # OBSERVER PATTERN -----------------------------------------------
  def update(self, subject: Subject) -> None:

    # What are subject states that would make us act differently?
    if subject._state is "Tasking":
      self._listen()
    elif subject._state is "Requesting":
      self._report()
    elif subject._state is "Structuring":
      self._configure()
    elif subject._state is "Sharing":
      self._share()
    elif subject._state is "Time":
      self._work()

    if subject.pubsub_message['type'] is 'spigot_data':
        self.batch_in = subject.pubsub_message['data']
        self.batch_out = self.batch_data(self.batch_in)
        self._state_notify()

  def _state_notify(self):
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

    self.PubSub._state = 1  # Depending on the results of the algorithm, this state can have useful knowledge
    self.PubSub.pubsub_message['data'] = self.batch_out
    self.notify()


  def _work(self):
    """
    https://neo4j.com/docs/graph-data-science/current/management-ops/graph-catalog-ops/index.html
    """

  # SUBJECT PATTERN -------------------------------------------------
  def notify_all(self):
    pass

  # QUESTION PATTERN -------------------------------------------------
  def velocity(self):
    # How productive are they now
    pass

  # SHARING PATTERN -------------------------------------------------
  def _share(self): # packs the message and calls notify()
    # Swap helpful information
    # Store the information
    return

  # MANAGEMENT PATTERN ----------------------------------------------
  def _listen(self):
    # Receive assigned points
    # Do some math
    return

  def _report(self):
    # Say what you've done
    # Do some math
    return

  def _configure(self):
    # Update internal configuration
    # Configure variables
    return
