from core.pipeline import Pipeline
from tasks.task_definitions import build_pipeline
from utils.logger import Logger
from utils.graph_visualizer import visualize

def run_system():
    pipeline = Pipeline()
    build_pipeline(pipeline)

    logger = Logger()
    state = {}

    pipeline.execute(state, logger)

    return logger.get_logs(), visualize(pipeline.graph)