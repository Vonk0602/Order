from simulation import Simulation
from visualization import visualize_3d, visualize_angular_distribution, visualize_particle_trajectories
from datetime import datetime
import config

timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

sim = Simulation()
sim.run()
sim.export_results(f'results_{timestamp}.csv', timestamp)
visualize_3d(sim.detectors, timestamp)
angles = sim.angular_distribution()
visualize_angular_distribution(angles, timestamp)
particles = sim.generator.emit_particles(0)
visualize_particle_trajectories(particles, timestamp, particle_type='all')
