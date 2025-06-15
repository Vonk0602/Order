import os
import csv
from utils import np
from particle import Particle
from config import GENERATOR_PULSE_DISTRIBUTION, GENERATOR_PULSE_MEAN, GENERATOR_PULSE_STD, GENERATOR_PULSE_UNIFORM_MIN, GENERATOR_PULSE_UNIFORM_MAX

class Generator:
    def __init__(self, position=(0.0, 0.0, 0.0)):
        self.position = np.array(position)

    def emit_particles(self, current_time, timestamp, num_neutrons=10, num_alphas=5):
        particles = []
        directions_log = []
        
        def generate_direction():
            u = np.random.uniform(0, 1)
            v = np.random.uniform(0, 1)
            theta = 2 * np.pi * u
            phi = np.arccos(1 - 2 * v)
            direction = np.array([np.sin(phi) * np.cos(theta), np.sin(phi) * np.sin(theta), np.cos(phi)])
            norm = np.linalg.norm(direction)
            if norm < 1e-8:
                return generate_direction()
            return direction / norm, theta, phi

        for _ in range(num_neutrons):
            direction, theta, phi = generate_direction()
            if GENERATOR_PULSE_DISTRIBUTION == 'gaussian':
                time_offset = np.random.normal(GENERATOR_PULSE_MEAN, GENERATOR_PULSE_STD)
            elif GENERATOR_PULSE_DISTRIBUTION == 'uniform':
                time_offset = np.random.uniform(GENERATOR_PULSE_UNIFORM_MIN, GENERATOR_PULSE_UNIFORM_MAX)
            else:
                time_offset = 0
            emit_time = max(current_time, current_time + time_offset)
            neutron = Particle('neutron', self.position, direction, emit_time)
            particles.append(neutron)
            directions_log.append([np.rad2deg(theta), np.rad2deg(phi), direction[0], direction[1], direction[2]])
            print(f"Сгенерирован нейтрон с направлением {direction} в {emit_time}")

        for _ in range(num_alphas):
            direction, theta, phi = generate_direction()
            if GENERATOR_PULSE_DISTRIBUTION == 'gaussian':
                time_offset = np.random.normal(GENERATOR_PULSE_MEAN, GENERATOR_PULSE_STD)
            elif GENERATOR_PULSE_DISTRIBUTION == 'uniform':
                time_offset = np.random.uniform(GENERATOR_PULSE_UNIFORM_MIN, GENERATOR_PULSE_UNIFORM_MAX)
            else:
                time_offset = 0
            emit_time = max(current_time, current_time + time_offset)
            alpha = Particle('alpha', self.position, direction, emit_time)
            particles.append(alpha)
            directions_log.append([np.rad2deg(theta), np.rad2deg(phi), direction[0], direction[1], direction[2]])
            print(f"Сгенерирована альфа-частица с направлением {direction} в {emit_time}")
        
        history_path = os.path.join('history', timestamp)
        os.makedirs(history_path, exist_ok=True)
        diag_file = os.path.join(history_path, f'generated_directions_{timestamp}.csv')
        try:
            with open(diag_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f, delimiter=';')
                writer.writerow(['Theta_deg', 'Phi_deg', 'Dir_X', 'Dir_Y', 'Dir_Z'])
                for row in directions_log:
                    writer.writerow([f"{x:.6f}" for x in row])
            print(f"Диагностика направлений сохранена в {diag_file}")
        except PermissionError as e:
            print(f"Ошибка записи файла {diag_file}: Отказано в доступе ({e}). Диагностика направлений не сохранена.")
        
        return particles
