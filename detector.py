import os
import csv
from utils import np
from config import MIN_TRACK_LENGTH

class Detector:
    def __init__(self, position, size):
        self.position = np.array(position)
        self.size = size
        self.detections = []

    def calculate_intersection(self, particle, speed, timestamp):
        try:
            ray_origin = np.array(particle.position)
            ray_direction = np.array(particle.direction)
            norm = np.linalg.norm(ray_direction)
            if norm < 1e-8:
                print(f"Недопустимое направление частицы {particle.type}: {ray_direction}")
                return None
            ray_direction = ray_direction / norm

            box_min = self.position - self.size / 2
            box_max = self.position + self.size / 2

            t_min = np.full(3, -np.inf)
            t_max = np.full(3, np.inf)
            for i in range(3):
                if abs(ray_direction[i]) < 1e-8:
                    if ray_origin[i] < box_min[i] or ray_origin[i] > box_max[i]:
                        return None
                    continue
                t1 = (box_min[i] - ray_origin[i]) / ray_direction[i]
                t2 = (box_max[i] - ray_origin[i]) / ray_direction[i]
                t_min[i] = min(t1, t2)
                t_max[i] = max(t1, t2)
            
            t_near = np.max(t_min)
            t_far = np.min(t_max)

            if t_near > t_far or t_near < 0:
                return None

            intersection_point = ray_origin + ray_direction * t_near
            exit_point = ray_origin + ray_direction * t_far
            track_length = np.linalg.norm(exit_point - intersection_point)

            detection_time = particle.time + t_near / speed
            if detection_time < 0:
                print(f"Некорректное время детекции {detection_time} для частицы {particle.type}")
                return None

            detection = {
                'time': detection_time,
                'track_length': track_length,
                'particle_type': particle.type,
                'direction': ray_direction,
                'is_short_track': track_length < MIN_TRACK_LENGTH
            }
            
            history_path = os.path.join('history', timestamp)
            os.makedirs(history_path, exist_ok=True)
            diag_file = os.path.join(history_path, f'intersection_log_{timestamp}.csv')
            with open(diag_file, 'a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f, delimiter=';')
                if os.path.getsize(diag_file) == 0:
                    writer.writerow(['Particle_Type', 'Detector_X', 'Detector_Y', 'Detector_Z', 'Dir_X', 'Dir_Y', 'Dir_Z', 'Track_Length', 'Time'])
                writer.writerow([
                    detection['particle_type'],
                    f"{self.position[0]:.6f}",
                    f"{self.position[1]:.6f}",
                    f"{self.position[2]:.6f}",
                    f"{ray_direction[0]:.6f}",
                    f"{ray_direction[1]:.6f}",
                    f"{ray_direction[2]:.6f}",
                    f"{track_length:.6f}",
                    f"{detection['time']:.6f}"
                ])
            print(f"Пересечение записано в {diag_file}")
            
            return detection
        except Exception as e:
            print(f"Ошибка при расчете пересечения для частицы {particle.type} в детекторе {self.position}: {e}")
            return None

    def register_particle(self, detection):
        self.detections.append(detection)
