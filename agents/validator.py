import time
from agents.base_agent import BaseAgent

class Validator(BaseAgent):
    def run(self, state, logger):
        logger.log("Validating mesh...")
        time.sleep(1)
        state["valid"] = True
        return state