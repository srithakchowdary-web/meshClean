import time
from agents.base_agent import BaseAgent

class NoiseCleaner(BaseAgent):
    def run(self, state, logger):
        logger.log("Cleaning noise...")
        time.sleep(1)
        state["noise"] = "cleaned"
        return state