import numpy as np
import json
import csv
import os
from generator import Generator
from detector import Detector
from config import DETECTOR_POSITIONS, SIMULATION_TIME, DETECTOR_SIZE, PARTICLE_SPEED, TRAJECTORY

class Simulation:
    def __init__(self):
        self.generator = Generator()
        self.detectors = [Detector(pos, DETECTOR_SIZE) for pos in DETECTOR_POSITIONS]
        self.time = 0
        self.results = []
        print(f"Симуляция инициализирована с {len(self.detectors)} детекторами")

    def move_detectors(self, trajectory_point):
        try:
            for i, detector in enumerate(self.detectors):
                original_pos = np.array(DETECTOR_POSITIONS[i])
                detector.position = original_pos + np.array(trajectory_point)
            print(f"Детекторы перемещены в {trajectory_point} в момент {self.time}")
        except Exception as e:
            print(f"Ошибка при перемещении детекторов: {e}")

    def run(self):
        print(f"Запуск симуляции на {SIMULATION_TIME} шагов")
        while self.time < SIMULATION_TIME:
            traj_point = TRAJECTORY(self.time)
            self.move_detectors(traj_point)
            particles = self.generator.emit_particles(self.time)
            for particle in particles:
                self.simulate_particle(particle)
            self.time += 1
        self.stitch_results()
        neutron_count = sum(1 for r in self.results if r['particle_type'] == 'neutron')
        alpha_count = sum(1 for r in self.results if r['particle_type'] == 'alpha')
        print(f"Симуляция завершена. Зарегистрировано {len(self.results)} пересечений: {neutron_count} нейтронов, {alpha_count} альфа-частиц.")

    def simulate_particle(self, particle):
        for detector in self.detectors:
            detection = detector.calculate_intersection(particle, PARTICLE_SPEED)
            if detection:
                detector.register_particle(detection)
                self.results.append({
                    'detector_pos': tuple(detector.position),
                    'time': detection['time'],
                    'particle_type': detection['particle_type'],
                    'track_length': detection['track_length'],
                    'particle_direction': tuple(detection['direction'])
                })
                print(f"Пересечение зарегистрировано: {detection}")

    def stitch_results(self):
        stitched = {}
        for result in self.results:
            pos = result['detector_pos']
            if pos not in stitched:
                stitched[pos] = []
            stitched[pos].append(result)
        self.stitched_results = stitched
        print("Сшивка результатов завершена")

    def export_results(self, filename, timestamp):
        history_path = os.path.join('history', timestamp)
        os.makedirs(history_path, exist_ok=True)
        filepath = os.path.join(history_path, filename)
        if filename.endswith('.json'):
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(self.stitched_results, f, default=lambda x: list(x) if isinstance(x, tuple) else x)
            print(f"Результаты экспортированы в {filepath} в формате JSON")
        elif filename.endswith('.csv'):
            with open(filepath, 'w', newline='', encoding='utf-8-sig') as f:
                writer = csv.writer(f, delimiter=';')
                writer.writerow(['Детектор_X', 'Детектор_Y', 'Детектор_Z', 'Время', 'Тип_частицы', 'Длина_пробега'])
                for pos, detections in self.stitched_results.items():
                    for detection in detections:
                        writer.writerow([
                            f"{pos[0]:.6f}",
                            f"{pos[1]:.6f}",
                            f"{pos[2]:.6f}",
                            f"{detection['time']:.6f}",
                            detection['particle_type'],
                            f"{detection['track_length']:.6f}"
                        ])
            print(f"Результаты экспортированы в {filepath} в формате CSV")
        else:
            print("Неподдерживаемый формат файла. Используйте .json или .csv")
