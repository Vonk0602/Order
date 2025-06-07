import matplotlib.pyplot as plt
import os

def visualize_3d(detectors, timestamp):
    plt.close('all')
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    
    x = [detector.position[0] for detector in detectors]
    y = [detector.position[1] for detector in detectors]
    z = [detector.position[2] for detector in detectors]
    
    for pos in zip(x, y, z):
        print(f"Позиция детектора: {pos}")
    
    ax.scatter(x, y, z, c='blue', marker='o')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    
    ax.set_xlim(min(x) - 0.5, max(x) + 0.5)
    ax.set_ylim(min(y) - 0.5, max(y) + 0.5)
    ax.set_zlim(min(z) - 0.5, max(z) + 0.5)
    
    history_path = os.path.join('history', timestamp)
    os.makedirs(history_path, exist_ok=True)
    filename = os.path.join(history_path, f'detectors_3d_{timestamp}.png')
    plt.savefig(filename)
    plt.show()

def visualize_angular_distribution(angles, timestamp):
    plt.close('all')
    plt.figure()
    plt.hist(angles, bins=30, color='green', alpha=0.7)
    plt.xlabel('Угол (градусы)')
    plt.ylabel('Количество')
    plt.title('Угловое распределение потока')
    
    history_path = os.path.join('history', timestamp)
    os.makedirs(history_path, exist_ok=True)
    filename = os.path.join(history_path, f'angular_distribution_{timestamp}.png')
    plt.savefig(filename)
    plt.show()

def visualize_particle_trajectories(particles, timestamp, particle_type='all'):
    plt.close('all')
    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    for particle in particles:
        if particle_type == 'all' or particle.type == particle_type:
            color = 'red' if particle.type == 'neutron' else 'blue'
            ax.quiver(particle.position[0], particle.position[1], particle.position[2],
                      particle.direction[0], particle.direction[1], particle.direction[2],
                      length=1.0, normalize=True, color=color, label=particle.type)
    
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_xlim(-1.5, 1.5)
    ax.set_ylim(-1.5, 1.5)
    ax.set_zlim(-1.5, 1.5)
    ax.view_init(elev=20, azim=45)
    ax.legend()
    
    history_path = os.path.join('history', timestamp)
    os.makedirs(history_path, exist_ok=True)
    filename = os.path.join(history_path, f'particle_trajectories_{particle_type}_{timestamp}.png')
    plt.savefig(filename)
    plt.show()
