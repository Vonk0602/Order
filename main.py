from simulation import Simulation
from visualization import visualize_3d, visualize_angular_distribution
import config

sim = Simulation()
timestamp = sim.run()
sim.export_results(f'results_{timestamp}.csv', timestamp)

DISTANCES = config.DISTANCES[:-1]
ANGLES = config.ANGLES[:-1]

for distance in DISTANCES:
    for angle in ANGLES:
        visualize_3d(sim.detectors, sim.generator.position, sim.generator.emit_particles(sim.time, timestamp), timestamp, distance, angle)

results = [r for r in sim.results]
visualize_angular_distribution(results, timestamp)
