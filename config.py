import numpy as np

# Размер детектора (в метрах)
DETECTOR_SIZE = 0.1

# Позиции детекторов в матрице 6x6 (x, y, z координаты)
DETECTOR_POSITIONS = [(x, y, 0) for x in range(6) for y in range(6)]

# Позиция генератора (x, y, z координаты)
GENERATOR_POSITION = (0, 0, 0)

# Режим работы генератора ('pulse' для импульсного режима)
GENERATOR_MODE = 'pulse'

# Тип временного распределения импульсов ('gaussian' или 'uniform')
GENERATOR_PULSE_DISTRIBUTION = 'gaussian'

# Среднее значение времени для гауссовского распределения (в секундах)
GENERATOR_PULSE_MEAN = 0

# Стандартное отклонение для гауссовского распределения (в секундах)
GENERATOR_PULSE_STD = 0.5

# Минимальное значение для равномерного распределения (в секундах)
GENERATOR_PULSE_UNIFORM_MIN = -1

# Максимальное значение для равномерного распределения (в секундах)
GENERATOR_PULSE_UNIFORM_MAX = 1

# Минимальная длина пробега частицы в детекторе для регистрации (в метрах)
MIN_TRACK_LENGTH = 0.1

# Время симуляции (в секундах)
SIMULATION_TIME = 1000

# Скорость частиц (в метрах в секунду)
PARTICLE_SPEED = 1.0

# Скорость движения траектории детекторов
TRAJECTORY_SPEED = 0.02

# Функция траектории движения детекторной матрицы (зависит от времени t)
TRAJECTORY = lambda t: (np.cos(t * TRAJECTORY_SPEED) * 2, np.sin(t * TRAJECTORY_SPEED) * 2, 0)

# Угол наклона детекторной матрицы (в градусах)
TILT = 10
