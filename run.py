import configparser
config = configparser.ConfigParser()
config.read('config.ini')

from forest_fire.gui.terminal import TerminalGUI
from forest_fire.board import Board
from forest_fire.engines import (
    RandomTreeGrowthEngine, 
    InverseDensityTreeGrowthEngine,
    ProximityTreeGrowthEngine,
    RandomFireSourceEngine,
    FireSpreadEngine,
    FireExtinguishEngine,
)

config_engine_mapper = {
    "Random Tree Growth": RandomTreeGrowthEngine,
    "Inverse Density Tree Growth": InverseDensityTreeGrowthEngine,
    "Proximity Tree Growth Engine": ProximityTreeGrowthEngine,
    "Random Fire Source Engine": RandomFireSourceEngine,
    "Fire Spread Engine": FireSpreadEngine,
    "Fire Extinguish Engine": FireExtinguishEngine,
}

engines = []
for option, engine in config_engine_mapper.items():
    engine_config = config[option]

    use_engine = engine_config.getboolean("use")
    if use_engine:
        engine_config.pop("use")  # This isn't an engine kwargs, just a config one.
        kwargs = {k: float(v) for k, v in engine_config.items()}
        engines.append(engine(**kwargs))


gui = TerminalGUI(engines = engines)
gui.start()
