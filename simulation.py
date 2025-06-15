import os
import json
import csv
from datetime import datetime
from utils import np
from scipy.spatial import cKDTree
from generator import Generator
from detector import Detector
from config import DETECTOR_POSITIONS, DETECTOR_SIZE, SIMULATION_TIME, PARTICLE_SPEED, MIN_TRACK_LENGTH, TRAJECTORY

class Simulation:
    def __init__(self):
        if PARTICLE_SPEED <= 0:
            raise ValueError("Скорость частиц должна быть положительной")
        if DETECTOR_SIZE <= 0:
            raise ValueError("Размер детектора должен быть положительным")
        if MIN_TRACK_LENGTH <= 0:
            raise ValueError("Минимальная длина пробега должна быть положительной")
        self.generator = Generator()
        self.detectors = [Detector(pos, DETECTOR_SIZE) for pos in DETECTOR_POSITIONS]
        self.detector_positions = np.array([d.position for d in self.detectors])
        self.kdtree = cKDTree(self.detector_positions)
        self.time = 0
        self.results = []
        self.missed_intersections = 0
        self.stitched_results = {}
        print(f"Симуляция инициализирована с {len(self.detectors)} детекторами")

    def move_detectors(self, traj_point):
        pass

    def simulate_particle(self, particle, timestamp):
        indices = self.kdtree.query_ball_point(particle.position, r=3.0)
        for idx in indices:
            detector = self.detectors[idx]
            detection = detector.calculate_intersection(particle, PARTICLE_SPEED, timestamp)
            if detection:
                if np.linalg.norm(detection['direction']) == 0:
                    print("Направление частицы не может быть нулевым")
                    continue
                detector.register_particle(detection)
                self.results.append({
                    'detector_pos': tuple(np.round(detector.position, 6)),
                    'time': detection['time'],
                    'particle_type': detection['particle_type'],
                    'track_length': detection['track_length'],
                    'particle_direction': tuple(detection['direction'])
                })
                print(f"Пересечение зарегистрировано: {detection}")
            else:
                self.missed_intersections += 1

    def run(self):
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        time_step = 0.1
        print(f"Запуск симуляции на {SIMULATION_TIME} секунд с шагом {time_step} с, временной штамп {timestamp}")
        while self.time < SIMULATION_TIME:
            traj_point = TRAJECTORY(self.time)
            self.move_detectors(traj_point)
            particles = self.generator.emit_particles(self.time, timestamp)
            for particle in particles:
                self.simulate_particle(particle, timestamp)
            self.time += time_step
        self.stitch_results()
        neutron_count = sum(1 for r in self.results if r['particle_type'] == 'neutron')
        alpha_count = sum(1 for r in self.results if r['particle_type'] == 'alpha')
        print(f"Симуляция завершена. Зарегистрировано {len(self.results)} пересечений: {neutron_count} нейтронов, {alpha_count} альфа-частиц. Пропущено пересечений: {self.missed_intersections}")
        return timestamp

    def stitch_results(self):
        self.stitched_results = {}
        for result in self.results:
            pos = result['detector_pos']
            if pos not in self.stitched_results:
                self.stitched_results[pos] = []
            self.stitched_results[pos].append({
                'time': result['time'],
                'particle_type': result['particle_type'],
                'track_length': result['track_length'],
                'particle_direction': result['particle_direction']
            })

    def export_results(self, filename, timestamp):
        history_path = os.path.join('history', timestamp)
        os.makedirs(history_path, exist_ok=True)
        filepath = os.path.join(history_path, filename)
        
        if os.path.exists(filepath):
            print(f"Файл {filepath} уже существует, создается резервная копия")
            os.rename(filepath, filepath + '.bak')
        
        if filename.endswith('.json'):
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(self.stitched_results, f, default=lambda x: list(x) if isinstance(x, tuple) else x)
            print(f"Результаты экспортированы в {filepath} в формате JSON")
        
        elif filename.endswith('.csv'):
            with open(filepath, 'w', newline='', encoding='utf-8-sig') as f:
                writer = csv.writer(f, delimiter=';')
                writer.writerow(['Детектор_X', 'Детектор_Y', 'Детектор_Z', 'Время', 'Тип_частицы', 'Длина_пробега', 'Dir_X', 'Dir_Y', 'Dir_Z'])
                for pos, detections in self.stitched_results.items():
                    for detection in detections:
                        writer.writerow([
                            f"{pos[0]:.6f}",
                            f"{pos[1]:.6f}",
                            f"{pos[2]:.6f}",
                            f"{detection['time']:.6f}",
                            detection['particle_type'],
                            f"{detection['track_length']:.6f}",
                            f"{detection['particle_direction'][0]:.2f}",
                            f"{detection['particle_direction'][1]:.2f}",
                            f"{detection['particle_direction'][2]:.2f}"
                        ])
            print(f"Результаты экспортированы в {filepath} в формате CSV")
        
        else:
            print("Неподдерживаемый формат файла. Используйте .json или .csv")
