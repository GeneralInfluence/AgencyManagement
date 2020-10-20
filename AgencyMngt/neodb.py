from neo4j import GraphDatabase

# Set of queries
# MATCH (n {name: 'Manager_1'}

class ActorsNeo():

  def __init__(self):
    uri = "bolt://localhost:7687"
    user = "neo4j"
    password = "password"
    self.driver = GraphDatabase.driver(uri, auth=(user, password))

  def close(self):
    self.driver.close()

  def create_node(self,label,name,type):
    with self.driver.session() as session:
      source = session.write_transaction(self._create_node, label, name, type)

  def create_relationship(self,label1,label2,name1,name2,rel_type):
    with self.driver.session() as session:
      source = session.write_transaction(self._create_relationship, label1,label2,name1,name2,rel_type)

  def assign_node_stats(self,stats=None):
    if type(stats)==type(None):
      raise NotImplementedError("cmon!")
    Developers = stats.keys()
    with self.driver.session() as session:
      for dev in Developers:
        source = session.write_transaction(self._assign_node_stats, "Developer", dev,
                                           int(stats[dev]["sprint_velocity"]*100),
                                           int(stats[dev]["efficiency"]*100))

  def calc_dev_stats(self, dev):
    """
    1. MVDev
    2. MVRel
    3. Switching Cost
    4. Collaboration Gain
    """

  def assign_relationship_knowledge_learned(self,label1,label2,name1,name2, knowledge_learned):
    with self.driver.session() as session:
      source = session.write_transaction(self._assign_relationship_knowledge_learned,
                                         label1, label2,name1,name2, knowledge_learned)

  def assign_relationship_knowledge_cost(self, name, knowledge_cost):
    with self.driver.session() as session:
      source = session.write_transaction(self._assign_relationship_knowledge_cost, name, knowledge_cost)

  @staticmethod
  def _create_node(tx,label,name,type):
    result = tx.run(f"CREATE (a:{label}) "
                    "SET a.name = $name "
                    "SET a.type = $type "
                    "SET a.velocity = [] "
                    "SET a.efficiency = [] "
                    "SET a.knowledge_cost = [] ",
                    name=name,type=type)
    return result

  @staticmethod
  def _create_relationship(tx,label1,label2,name1,name2,rel_type):
    result = tx.run(f"MATCH (a:{label1}),(b:{label2}) "
                    "WHERE a.name = $name1 AND b.name = $name2 "
                    f"CREATE (a)-[r:{rel_type}]->(b) "
                    "SET r.type = $rel_type "
                    "SET r.knowledge_shared = [] ",
                    name1=name1,name2=name2,rel_type=rel_type)
    return result

  @staticmethod
  def _assign_node_stats(tx, label, name, sprint_velocity, efficiency):

    result = tx.run("MATCH (a {name: '"+name+"'}) "
                    "SET a.velocity = a.velocity + $sprint_velocity "
                    "SET a.efficiency = a.efficiency + $efficiency ",
                    name=name,
                    sprint_velocity=sprint_velocity,
                    efficiency=efficiency)
    return result

  @staticmethod
  def _assign_relationship_knowledge_learned(tx, label1,label2,name1,name2, knowledge_learned):

    result = tx.run("MATCH (a { name: $name1 })-[r]-(b { name: $name2 }) "
                    "SET r.knowledge_shared = r.knowledge_shared + $knowledge_learned ",
                    name1=name1,name2=name2,knowledge_learned=knowledge_learned)
    return result

  @staticmethod
  def _assign_relationship_knowledge_cost(tx, name, knowledge_cost):

    result = tx.run("MATCH (a { name: $name }) "
                    "SET a.knowledge_cost = a.knowledge_cost + $knowledge_cost ",
                    name=name, knowledge_cost=knowledge_cost)
    return result