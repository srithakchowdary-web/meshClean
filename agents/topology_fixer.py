import time
from agents.base_agent import BaseAgent

class TopologyFixer(BaseAgent):
    def run(self, state, logger):
        logger.log("Fixing topology...")
        time.sleep(1)
        state["topology"] = "fixed"
        return state