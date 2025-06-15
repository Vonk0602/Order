from utils import np

class Particle:
    def __init__(self, type, position, direction, time):
        self.type = type
        self.position = np.array(position)
        norm = np.linalg.norm(direction)
        if norm == 0:
            raise ValueError("Направление частицы не может быть нулевым")
        self.direction = np.array(direction) / norm
        self.time = time
