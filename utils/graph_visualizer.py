def visualize(graph):
    return "\n".join([f"{u} -> {v}" for u, v in graph.edges()])