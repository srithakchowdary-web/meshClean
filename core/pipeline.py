import networkx as nx

class Pipeline:
    def __init__(self):
        self.graph = nx.DiGraph()

    def add_task(self, name, func, dependencies=[]):
        self.graph.add_node(name, func=func)
        for dep in dependencies:
            self.graph.add_edge(dep, name)

    def execute(self, state, logger):
        order = list(nx.topological_sort(self.graph))

        for node in order:
            logger.log(f"Running {node}")
            state.set_progress(node, "running")

            func = self.graph.nodes[node]['func']
            func(state, logger)

        state.set_progress(node, "completed")
        return state