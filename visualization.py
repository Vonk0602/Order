import os
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap, Normalize
from utils import np

def visualize_3d(detectors, generator_pos, particles, timestamp, distance, angle):
    if not particles:
        print("Нет частиц для визуализации")
        return
    
    try:
        fig = plt.figure(figsize=(10, 8))
        ax = fig.add_subplot(111, projection='3d')
        
        for detector in detectors:
            pos = detector.position
            size = detector.size
            x = [pos[0] - size/2, pos[0] + size/2]
            y = [pos[1] - size/2, pos[1] + size/2]
            z = [pos[2] - size/2, pos[2] + size/2]
            for i in range(2):
                for j in range(2):
                    ax.plot3D([x[i], x[i]], [y[j], y[j]], [z[0], z[1]], 'b')
                    ax.plot3D([x[i], x[i]], [y[0], y[1]], [z[j], z[j]], 'b')
                    ax.plot3D([x[0], x[1]], [y[i], y[i]], [z[j], z[j]], 'b')
        
        ax.scatter(generator_pos[0], generator_pos[1], generator_pos[2], c='r', marker='*', s=200, label='Генератор')
        
        for particle in particles:
            start = np.array(particle.position)
            direction = np.array(particle.direction)
            end = start + direction * 2.0
            ax.plot3D([start[0], end[0]], [start[1], end[1]], [start[2], end[2]], 'g' if particle.type == 'neutron' else 'm', label=particle.type if particle == particles[0] else '')
        
        ax.set_xlabel('X, м')
        ax.set_ylabel('Y, м')
        ax.set_zlabel('Z, м')
        ax.legend()
        ax.set_title(f'Траектории частиц (d={distance} м, α={angle}°)')
        
        history_path = os.path.join('history', timestamp)
        os.makedirs(history_path, exist_ok=True)
        filepath = os.path.join(history_path, f'3d_visualization_d{distance}_a{angle}_{timestamp}.png')
        try:
            plt.savefig(filepath, dpi=600, bbox_inches='tight')
            print(f"3D визуализация сохранена в {filepath}")
        except PermissionError as e:
            print(f"Ошибка записи файла {filepath}: Отказано в доступе ({e}). Визуализация не сохранена.")
        plt.close()
    except Exception as e:
        print(f"Ошибка при визуализации 3D: {e}")

def visualize_angular_distribution(results, timestamp):
    if not results:
        print("Нет данных для визуализации углового распределения")
        return
    
    try:
        theta_angles = []
        phi_angles = []
        for result in results:
            dir_x, dir_y, dir_z = result['particle_direction']
            theta = np.arctan2(np.sqrt(dir_x**2 + dir_y**2), dir_z) * 180 / np.pi
            phi = np.arctan2(dir_y, dir_x) * 180 / np.pi
            theta_angles.append(theta)
            phi_angles.append(phi)
        
        if not theta_angles or not phi_angles:
            print("Нет углов для визуализации")
            return
        
        plt.figure(figsize=(12, 10))
        cmap = LinearSegmentedColormap.from_list('custom', ['#0000FF', '#00FFFF', '#FFFF00', '#FF0000'], N=256)
        hist, xedges, yedges = np.histogram2d(theta_angles, phi_angles, bins=(100, 100), range=((0, 180), (-180, 180)), density=True)
        hist_max = np.max(hist)
        print(f"Максимальное значение плотности: {hist_max}")
        if hist_max == 0:
            print("Гистограмма пуста или содержит нулевые значения")
            hist = np.zeros_like(hist)
        else:
            hist /= hist_max
        
        norm = Normalize(vmin=0, vmax=1)
        img = plt.pcolormesh(xedges, yedges, hist.T, cmap=cmap, norm=norm)
        cbar = plt.colorbar(img, label='Нормированная плотность', pad=0.02, ticks=[0.0, 0.2, 0.4, 0.6, 0.8, 1.0])
        cbar.ax.tick_params(labelsize=14)
        cbar.ax.set_ylabel('Нормированная плотность', fontsize=14, labelpad=10)
        
        plt.title('Угловое распределение нейтронов (2D гистограмма)', fontsize=16, pad=15)
        plt.xlabel('Полярный угол θ (градусы)', fontsize=14)
        plt.ylabel('Азимутальный угол φ (градусы)', fontsize=14)
        plt.xticks(np.arange(0, 181, 30), fontsize=12)
        plt.yticks(np.arange(-180, 181, 60), fontsize=12)
        plt.grid(True, linestyle='--', alpha=0.3)
        plt.tight_layout()
        
        history_path = os.path.join('history', timestamp)
        os.makedirs(history_path, exist_ok=True)
        filepath = os.path.join(history_path, f'angular_distribution_{timestamp}.png')
        try:
            plt.savefig(filepath, dpi=600, bbox_inches='tight')
            print(f"Тепловая карта углового распределения сохранена в {filepath}")
        except PermissionError as e:
            print(f"Ошибка записи файла {filepath}: Отказано в доступе ({e}). Визуализация не сохранена.")
        plt.close()
    except Exception as e:
        print(f"Ошибка при визуализации углового распределения: {e}")
