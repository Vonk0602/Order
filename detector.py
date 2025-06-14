import numpy as np
from config import DETECTOR_SIZE, MIN_TRACK_LENGTH

class Detector:
    def __init__(self, position, size=DETECTOR_SIZE):
        self.position = np.array(position)
        self.size = size
        self.detections = []
        print(f"Детектор инициализирован в {self.position}")

    def calculate_intersection(self, particle, speed):
        try:
            ray_origin = np.array(particle.position)
            ray_direction = np.array(particle.direction)
            box_min = self.position - self.size / 2
            box_max = self.position + self.size / 2

            t_min = (box_min - ray_origin) / ray_direction
            t_max = (box_max - ray_origin) / ray_direction
            t_near = np.max(np.minimum(t_min, t_max))
            t_far = np.min(np.maximum(t_min, t_max))

            if t_near > t_far:
                return None

            intersection_point = ray_origin + ray_direction * t_near
            exit_point = ray_origin + ray_direction * t_far
            track_length = np.linalg.norm(exit_point - intersection_point)

            if track_length < MIN_TRACK_LENGTH:
                return None

            return {
                'time': particle.time + t_near / speed,
                'track_length': track_length,
                'particle_type': particle.type,
                'direction': particle.direction
            }
        except Exception as e:
            print(f"Ошибка при расчете пересечения: {e}")
            return None

    def register_particle(self, detection):
        self.detections.append(detection)
        print(f"Детектор на {self.position} зарегистрировал {detection['particle_type']} с пробегом {detection['track_length']} в момент {detection['time']}")
