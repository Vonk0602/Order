import matplotlib.pyplot as plt
import numpy as np
import os
from datetime import datetime
from mpl_toolkits.mplot3d import Axes3D

def visualize_3d(detectors, generator_pos, particles, timestamp, distance, angle):
    plt.close('all')
    fig = plt.figure(figsize=(14, 12))
    ax = fig.add_subplot(111, projection='3d')
    
    detector_positions = np.array([detector.position for detector in detectors])
    x = detector_positions[:, 0]
    y = detector_positions[:, 1]
    z = detector_positions[:, 2]
    
    x_min, x_max = min(x) - 0.2, max(x) + 0.2
    y_min, y_max = min(y) - 0.2, max(y) + 0.2
    z_min, z_max = min(z) - 0.2, max(z) + 0.2
    
    for s, e in [(x_min, x_max), (x_max, x_max), (x_max, x_min), (x_min, x_min)]:
        ax.plot3D([s, e], [y_min, y_min], [z_min, z_min], 'k-', linewidth=1.5)
        ax.plot3D([s, e], [y_max, y_max], [z_min, z_min], 'k-', linewidth=1.5)
        ax.plot3D([s, e], [y_min, y_min], [z_max, z_max], 'k-', linewidth=1.5)
        ax.plot3D([s, e], [y_max, y_max], [z_max, z_max], 'k-', linewidth=1.5)
    for s, e in [(y_min, y_max), (y_max, y_max), (y_max, y_min), (y_min, y_min)]:
        ax.plot3D([x_min, x_min], [s, e], [z_min, z_min], 'k-', linewidth=1.5)
        ax.plot3D([x_max, x_max], [s, e], [z_min, z_min], 'k-', linewidth=1.5)
        ax.plot3D([x_min, x_min], [s, e], [z_max, z_max], 'k-', linewidth=1.5)
        ax.plot3D([x_max, x_max], [s, e], [z_max, z_max], 'k-', linewidth=1.5)
    for s, e in [(z_min, z_max), (z_max, z_max), (z_max, z_min), (z_min, z_min)]:
        ax.plot3D([x_min, x_min], [y_min, y_min], [s, e], 'k-', linewidth=1.5)
        ax.plot3D([x_max, x_max], [y_min, y_min], [s, e], 'k-', linewidth=1.5)
        ax.plot3D([x_min, x_min], [y_max, y_max], [s, e], 'k-', linewidth=1.5)
        ax.plot3D([x_max, x_max], [y_max, y_max], [s, e], 'k-', linewidth=1.5)
    
    u = np.linspace(0, 2 * np.pi, 50)
    v = np.linspace(0, np.pi, 50)
    sphere_x = generator_pos[0] + 0.1 * np.outer(np.cos(u), np.sin(v))
    sphere_y = generator_pos[1] + 0.1 * np.outer(np.sin(u), np.sin(v))
    sphere_z = generator_pos[2] + 0.1 * np.outer(np.ones(np.size(u)), np.cos(v))
    ax.plot_surface(sphere_x, sphere_y, sphere_z, color='#2ecc71', alpha=0.8, edgecolor='none', label='Генератор')
    
    for particle in particles:
        if particle.type == 'neutron':
            start = particle.position
            direction = particle.direction
            length = 1.5
            end_x = start[0] + direction[0] * length
            end_y = start[1] + direction[1] * length
            end_z = start[2] + direction[2] * length
            ax.plot3D([start[0], end_x], [start[1], end_y], [start[2], end_z], color='#e74c3c', linewidth=1.5)
    
    ax.scatter(x, y, z, c='#3498db', s=50, marker='s', label='Детекторы')
    
    ax.grid(True, linestyle='--', alpha=0.7)
    ax.set_xlabel('X (м)', fontsize=14, labelpad=12)
    ax.set_ylabel('Y (м)', fontsize=14, labelpad=12)
    ax.set_zlabel('Z (м)', fontsize=14, labelpad=12)
    
    max_range = max(x_max - x_min, y_max - y_min, z_max - z_min) * 1.5
    mid_x = (x_max + x_min) * 0.5
    mid_y = (y_max + y_min) * 0.5
    mid_z = (z_max + z_min) * 0.5
    ax.set_xlim(mid_x - max_range, mid_x + max_range)
    ax.set_ylim(mid_y - max_range, mid_y + max_range)
    ax.set_zlim(mid_z - max_range, mid_z + max_range)
    
    ax.set_title(f'Визуализация установки\nРасстояние: {distance:.1f} м, Угол: {angle}°', fontsize=16, pad=20)
    ax.legend(fontsize=12)
    
    history_path = os.path.join('history', timestamp)
    os.makedirs(history_path, exist_ok=True)
    filename = os.path.join(history_path, f'setup_{distance:.1f}m_{angle}deg_{timestamp}.png')
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    print(f"Визуализация сохранена в {filename}")
    plt.close()

def visualize_angular_distribution(results, timestamp):
    plt.close('all')
    fig = plt.figure(figsize=(12, 10))
    
    neutron_theta = []
    neutron_phi = []
    alpha_theta = []
    alpha_phi = []
    for detection in results:
        direction = np.array(detection['particle_direction'])
        theta = np.arccos(direction[2])
        phi = np.arctan2(direction[1], direction[0])
        if detection['particle_type'] == 'neutron':
            neutron_theta.append(np.rad2deg(theta))
            neutron_phi.append(np.rad2deg(phi % (2 * np.pi)))
        else:
            alpha_theta.append(np.rad2deg(theta))
            alpha_phi.append(np.rad2deg(phi % (2 * np.pi)))
    
    print(f"Количество записей в results: {len(results)}")
    print(f"Количество нейтронов: {len(neutron_theta)}")
    print(f"Количество альфа-частиц: {len(alpha_theta)}")
    if neutron_theta:
        print(f"Уникальные theta нейтронов: {np.unique(neutron_theta)[:5]}...")
        print(f"Уникальные phi нейтронов: {np.unique(neutron_phi)[:5]}...")
    if alpha_theta:
        print(f"Уникальные theta альфа-частиц: {np.unique(alpha_theta)[:5]}...")
        print(f"Уникальные phi альфа-частиц: {np.unique(alpha_phi)[:5]}...")
    
    ax1 = fig.add_subplot(221)
    hist_neutron, xedges, yedges = np.histogram2d(neutron_theta, neutron_phi, bins=[20, 20], range=[[0, 180], [0, 360]])
    if hist_neutron.sum() > 0:
        hist_neutron = hist_neutron / hist_neutron.max()
    else:
        hist_neutron = np.zeros_like(hist_neutron)
    im1 = ax1.imshow(hist_neutron.T, cmap='viridis', aspect='auto', extent=[0, 180, 0, 360], origin='lower')
    ax1.set_xlabel('Полярный угол (градусы)', fontsize=10)
    ax1.set_ylabel('Азимутальный угол (градусы)', fontsize=10)
    ax1.set_title('Нейтроны (2D гистограмма)', fontsize=12)
    cbar1 = plt.colorbar(im1, ax=ax1)
    cbar1.set_label('Нормированная плотность', size=10)
    cbar1.ax.tick_params(labelsize=10)
    
    ax2 = fig.add_subplot(222)
    hist_alpha, _, _ = np.histogram2d(alpha_theta, alpha_phi, bins=[20, 20], range=[[0, 180], [0, 360]])
    if hist_alpha.sum() > 0:
        hist_alpha = hist_alpha / hist_alpha.max()
    else:
        hist_alpha = np.zeros_like(hist_alpha)
    im2 = ax2.imshow(hist_alpha.T, cmap='viridis', aspect='auto', extent=[0, 180, 0, 360], origin='lower')
    ax2.set_xlabel('Полярный угол (градусы)', fontsize=10)
    ax2.set_ylabel('Азимутальный угол (градусы)', fontsize=10)
    ax2.set_title('Альфа-частицы (2D гистограмма)', fontsize=12)
    cbar2 = plt.colorbar(im2, ax=ax2)
    cbar2.set_label('Нормированная плотность', size=10)
    cbar2.ax.tick_params(labelsize=10)
    
    ax3 = fig.add_subplot(223)
    if neutron_phi:
        plt.hist(neutron_phi, bins=50, range=[0, 360], density=True, color='#e74c3c', alpha=0.7, label='Нейтроны')
    if alpha_phi:
        plt.hist(alpha_phi, bins=50, range=[0, 360], density=True, color='#9b59b6', alpha=0.7, label='Альфа-частицы')
    ax3.set_xlabel('Азимутальный угол (градусы)', fontsize=10)
    ax3.set_ylabel('Нормированная плотность', fontsize=10)
    ax3.set_title('1D гистограмма по φ', fontsize=12)
    ax3.legend(fontsize=10)
    
    ax4 = fig.add_subplot(224, projection='polar')
    if neutron_phi:
        phi_rad = np.deg2rad(neutron_phi)
        hist_n, bins = np.histogram(phi_rad, bins=50, range=[0, 2 * np.pi], density=True)
        centers = (bins[:-1] + bins[1:]) / 2
        width = np.diff(bins)
        ax4.bar(centers, hist_n, width=width, color='#e74c3c', alpha=0.7, label='Нейтроны')
    if alpha_phi:
        phi_rad = np.deg2rad(alpha_phi)
        hist_a, bins = np.histogram(phi_rad, bins=50, range=[0, 2 * np.pi], density=True)
        centers = (bins[:-1] + bins[1:]) / 2
        width = np.diff(bins)
        ax4.bar(centers, hist_a, width=width, color='#9b59b6', alpha=0.7, label='Альфа-частицы')
    ax4.set_title('Полярный график по φ', fontsize=12, pad=20)
    ax4.legend(fontsize=10)
    
    print(f"Сумма гистограммы нейтронов: {hist_neutron.sum()}")
    print(f"Максимум гистограммы нейтронов: {hist_neutron.max()}")
    print(f"Уникальные значения в гистограмме нейтронов: {np.unique(hist_neutron)[:5]}...")
    print(f"Сумма гистограммы альфа-частиц: {hist_alpha.sum()}")
    print(f"Максимум гистограммы альфа-частиц: {hist_alpha.max()}")
    print(f"Уникальные значения в гистограмме альфа-частиц: {np.unique(hist_alpha)[:5]}...")
    
    history_path = os.path.join('history', timestamp)
    os.makedirs(history_path, exist_ok=True)
    filename = os.path.join(history_path, f'angular_profile_{timestamp}.png')
    plt.tight_layout()
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    print(f"Угловая гистограмма сохранена в {filename}")
    plt.close()

def visualize_3d_trajectories(timestamp):
    plt.close('all')
    fig = plt.figure(figsize=(12, 5))
    
    ax1 = fig.add_subplot(121, projection='3d')
    x = np.linspace(-1, 1, 100)
    y = np.zeros(100)
    z = np.linspace(-1, 1, 100)
    inside = (z >= -0.5) & (z <= 0.5)
    ax1.plot(x[:50], y[:50], z[:50], 'b-', label='Вход', linewidth=1.5)
    ax1.plot(x[50:], y[50:], z[50:], 'r-', label='Выход', linewidth=1.5)
    
    x_min, x_max = -1.5, 1.5
    y_min, y_max = -1.5, 1.5
    z_min, z_max = -1.5, 1.5
    for s, e in [(x_min, x_max), (x_max, x_max), (x_max, x_min), (x_min, x_min)]:
        ax.plot3D([s, e], [y_min, y_min], [z_min, z_min], 'k-', linewidth=1.5)
        ax.plot3D([s, e], [y_max, y_max], [z_min, z_min], 'k-', linewidth=1.5)
        ax.plot3D([s, e], [y_min, y_min], [z_max, z_max], 'k-', linewidth=1.5)
        ax.plot3D([s, e], [y_max, y_max], [z_max, z_max], 'k-', linewidth=1.5)
    for s, e in [(y_min, y_max), (y_max, y_max), (y_max, y_min), (y_min, y_min)]:
        ax.plot3D([x_min, x_min], [s, e], [z_min, z_min], 'k-', linewidth=1.5)
        ax.plot3D([x_max, x_max], [s, e], [z_min, z_min], 'k-', linewidth=1.5)
        ax.plot3D([x_min, x_min], [s, e], [z_max, z_max], 'k-', linewidth=1.5)
        ax.plot3D([x_max, x_max], [s, e], [z_max, z_max], 'k-', linewidth=1.5)
    for s, e in [(z_min, z_max), (z_max, z_max), (z_max, z_min), (z_min, z_min)]:
        ax.plot3D([x_min, x_min], [y_min, y_min], [s, e], 'k-', linewidth=1.5)
        ax.plot3D([x_max, x_max], [y_min, y_min], [s, e], 'k-', linewidth=1.5)
        ax.plot3D([x_min, x_min], [y_max, y_max], [s, e], 'k-', linewidth=1.5)
        ax.plot3D([x_max, x_max], [y_max, y_max], [s, e], 'k-', linewidth=1.5)
    
    ax1.set_xlabel('X', fontsize=12)
    ax1.set_ylabel('Y', fontsize=12)
    ax1.set_zlabel('Z', fontsize=12)
    ax1.legend(fontsize=10)
    ax1.grid(True, linestyle='--', alpha=0.7)
    
    ax2 = fig.add_subplot(122, projection='3d')
    for s, e in [(x_min, x_max), (x_max, x_max), (x_max, x_min), (x_min, x_min)]:
        ax2.plot3D([s, e], [y_min, y_min], [z_min, z_min], 'k-', linewidth=1.5)
        ax2.plot3D([s, e], [y_max, y_max], [z_min, z_min], 'k-', linewidth=1.5)
        ax2.plot3D([s, e], [y_min, y_min], [z_max, z_max], 'k-', linewidth=1.5)
        ax2.plot3D([s, e], [y_max, y_max], [z_max, z_max], 'k-', linewidth=1.5)
    for s, e in [(y_min, y_max), (y_max, y_max), (y_max, y_min), (y_min, y_min)]:
        ax2.plot3D([x_min, x_min], [s, e], [z_min, z_min], 'k-', linewidth=1.5)
        ax2.plot3D([x_max, x_max], [s, e], [z_min, z_min], 'k-', linewidth=1.5)
        ax2.plot3D([x_min, x_min], [s, e], [z_max, z_max], 'k-', linewidth=1.5)
        ax2.plot3D([x_max, x_max], [s, e], [z_max, z_max], 'k-', linewidth=1.5)
    for s, e in [(z_min, z_max), (z_max, z_max), (z_max, z_min), (z_min, z_min)]:
        ax2.plot3D([x_min, x_min], [y_min, y_min], [s, e], 'k-', linewidth=1.5)
        ax2.plot3D([x_max, x_max], [y_min, y_min], [s, e], 'k-', linewidth=1.5)
        ax2.plot3D([x_min, x_min], [y_max, y_max], [s, e], 'k-', linewidth=1.5)
        ax2.plot3D([x_max, x_max], [y_max, y_max], [s, e], 'k-', linewidth=1.5)
    
    ax2.set_xlabel('X', fontsize=12)
    ax2.set_ylabel('Y', fontsize=12)
    ax2.set_zlabel('Z', fontsize=12)
    ax2.grid(True, linestyle='--', alpha=0.7)
    
    history_path = os.path.join('history', timestamp)
    os.makedirs(history_path, exist_ok=True)
    filename = os.path.join(history_path, f'trajectories_3d_{timestamp}.png')
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    print(f"3D траектории сохранены в {filename}")
    plt.close()
