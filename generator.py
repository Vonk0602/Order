import numpy as np
from particle import Particle
from config import GENERATOR_POSITION, GENERATOR_PULSE_DISTRIBUTION, GENERATOR_PULSE_MEAN, GENERATOR_PULSE_STD, GENERATOR_PULSE_UNIFORM_MIN, GENERATOR_PULSE_UNIFORM_MAX

class Generator:
    def __init__(self):
        self.position = np.array(GENERATOR_POSITION)
        print(f"Генератор инициализирован в {self.position}")

    def emit_particles(self, current_time, num_neutrons=10):
        try:
            particles = []
            for _ in range(num_neutrons):
                theta = np.random.uniform(0, 2 * np.pi)
                phi = np.random.uniform(0, np.pi)
                direction = np.array([np.sin(phi) * np.cos(theta), np.sin(phi) * np.sin(theta), np.cos(phi)])
                if GENERATOR_PULSE_DISTRIBUTION == 'gaussian':
                    time_offset = np.random.normal(GENERATOR_PULSE_MEAN, GENERATOR_PULSE_STD)
                elif GENERATOR_PULSE_DISTRIBUTION == 'uniform':
                    time_offset = np.random.uniform(GENERATOR_PULSE_UNIFORM_MIN, GENERATOR_PULSE_UNIFORM_MAX)
                else:
                    print(f"Неизвестное распределение импульсов: {GENERATOR_PULSE_DISTRIBUTION}. Используется нулевое смещение")
                    time_offset = 0
                emit_time = current_time + time_offset
                neutron = Particle('neutron', self.position, direction, emit_time)
                particles.append(neutron)
                print(f"Сгенерирован нейтрон с направлением {direction} в {emit_time}")
            return particles
        except Exception as e:
            print(f"Ошибка при испускании частиц: {e}")
            return []
