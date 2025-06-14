import numpy as np
from simulation import Simulation
from visualization import visualize_3d, visualize_angular_distribution, visualize_3d_trajectories
from datetime import datetime
import config
import os

timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
print(f"Запуск скрипта в {timestamp}")

sim = Simulation()
sim.run()
sim.export_results(f'results_{timestamp}.csv', timestamp)

DISTANCES = [0.2, 0.4, 0.6, 0.8]
ANGLES = [0, 30, 60, 90]

if sim.results:
    print(f"Найдено {len(sim.results)} пересечений для визуализации")
    for distance in DISTANCES:
        for angle in ANGLES:
            tilt_rad = np.deg2rad(angle)
            rotation_matrix = np.array([
                [np.cos(tilt_rad), 0, np.sin(tilt_rad)],
                [0, 1, 0],
                [-np.sin(tilt_rad), 0, np.cos(tilt_rad)]
            ])
            generator_pos = np.array([-distance, 0, 0])
            rotated_generator_pos = rotation_matrix @ generator_pos
            particles = sim.generator.emit_particles(0, num_neutrons=10)
            visualize_3d(sim.detectors, rotated_generator_pos, particles, timestamp, distance, angle)
    visualize_angular_distribution(sim.results, timestamp)
    visualize_3d_trajectories(timestamp)
else:
    print("Нет данных для визуализации. Проверьте параметры симуляции.")
