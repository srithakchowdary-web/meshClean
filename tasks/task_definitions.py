
from agents.noise_cleaner import NoiseCleaner
from agents.topology_fixer import TopologyFixer
from agents.validator import Validator

def build_pipeline(pipeline):
    pipeline.add_task("noise_cleaning", NoiseCleaner().run)
    pipeline.add_task("topology_fixing", TopologyFixer().run, ["noise_cleaning"])
    pipeline.add_task("validation", Validator().run, ["topology_fixing"])