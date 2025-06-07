import numpy as np
from particle import Particle
from config import GENERATOR_POSITION, GENERATOR_PULSE_DISTRIBUTION, GENERATOR_PULSE_MEAN, GENERATOR_PULSE_STD, GENERATOR_PULSE_UNIFORM_MIN, GENERATOR_PULSE_UNIFORM_MAX

class Generator:
    def __init__(self):
        self.position = np.array(GENERATOR_POSITION)

    def emit_particles(self, current_time):
        try:
            theta = np.random.uniform(0, 2 * np.pi)
            phi = np.random.uniform(0, np.pi)
            direction_neutron = np.array([np.sin(phi) * np.cos(theta), np.sin(phi) * np.sin(theta), np.cos(phi)])
            direction_alpha = -direction_neutron
            
            if GENERATOR_PULSE_DISTRIBUTION == 'gaussian':
                time_offset = np.random.normal(GENERATOR_PULSE_MEAN, GENERATOR_PULSE_STD)
            elif GENERATOR_PULSE_DISTRIBUTION == 'uniform':
                time_offset = np.random.uniform(GENERATOR_PULSE_UNIFORM_MIN, GENERATOR_PULSE_UNIFORM_MAX)
            else:
                print(f"Неизвестное распределение импульсов: {GENERATOR_PULSE_DISTRIBUTION}. Используется нулевое смещение")
                time_offset = 0
                
            emit_time = current_time + time_offset
            neutron = Particle('neutron', self.position, direction_neutron, emit_time)
            alpha = Particle('alpha', self.position, direction_alpha, emit_time)
            return [neutron, alpha]
        except Exception as e:
            print(f"Ошибка при испускании частиц: {e}")
            return []
