import random
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
from matplotlib.patches import Patch

from agents import Prey, Predator


class SimulationViewer:
    def __init__(self, history, grid_size):
        self.history = history
        self.grid_size = grid_size
        self.current_step = 0
        self.max_step = len(history) - 1
        
        # Create figure and axis with better styling
        self.fig, self.ax = plt.subplots(figsize=(14, 10))
        mng = self.fig.canvas.manager
        mng.window.state('zoomed')
        plt.subplots_adjust(bottom=0.15, right=0.8, top=0.9)
        
        # Set figure background color
        self.fig.patch.set_facecolor('lightblue')
        
        # Create navigation buttons
        ax_prev = plt.axes([0.25, 0.02, 0.08, 0.04])
        ax_next = plt.axes([0.34, 0.02, 0.08, 0.04])
        ax_first = plt.axes([0.1, 0.02, 0.08, 0.04])
        ax_last = plt.axes([0.55, 0.02, 0.08, 0.04])
        ax_play = plt.axes([0.43, 0.02, 0.08, 0.04])
        
        self.btn_prev = Button(ax_prev, '<- Sebelumnya')
        self.btn_next = Button(ax_next, 'Sesudah ->')
        self.btn_first = Button(ax_first, '<< Pertama')
        self.btn_last = Button(ax_last, 'Terakhir >>')
        self.btn_play = Button(ax_play, '> Mulai')
        
        # Connect button events
        self.btn_prev.on_clicked(self.prev_step)
        self.btn_next.on_clicked(self.next_step)
        self.btn_first.on_clicked(self.first_step)
        self.btn_last.on_clicked(self.last_step)
        self.btn_play.on_clicked(self.toggle_play)
        
        # Add keyboard navigation
        self.fig.canvas.mpl_connect('key_press_event', self.on_key_press)
        
        # Animation state
        self.playing = False
        self.animation_timer = None
        
        # Initial plot
        self.update_plot()
        
    def update_plot(self):
        self.ax.clear()
        
        if self.current_step < len(self.history):
            prey_list, predator_list = self.history[self.current_step]
            
            # Create grid with ocean gradient effect
            grid = np.full((self.grid_size, self.grid_size, 3), [20, 105, 200], dtype=int)
            
            # Add some variation to make it look more like ocean
            for i in range(self.grid_size):
                for j in range(self.grid_size):
                    # Add subtle random variation to ocean color
                    variation = random.randint(-15, 15)
                    grid[i, j] = [
                        max(0, min(255, 20 + variation)),
                        max(0, min(255, 105 + variation//2)),
                        max(0, min(255, 200 + variation//3))
                    ]
            
            # Add prey (bright green) and predators (bright red)
            for prey in prey_list:
                grid[prey.y, prey.x] = [50, 255, 50]  # Bright green for prey
            for predator in predator_list:
                grid[predator.y, predator.x] = [255, 50, 50]  # Bright red for predators
            
            self.ax.imshow(grid)
            
            # Enhanced title with more information
            total_animals = len(prey_list) + len(predator_list)
            prey_percentage = (len(prey_list) / total_animals * 100) if total_animals > 0 else 0
            predator_percentage = (len(predator_list) / total_animals * 100) if total_animals > 0 else 0
            
            title = f"Simulasi Interaksi Predator-Mangsa\n"
            title += f"Waktu: {self.current_step + 1}/{len(self.history)} | "
            title += f"Mangsa: {len(prey_list)} ({prey_percentage:.1f}%) | "
            title += f"Predator: {len(predator_list)} ({predator_percentage:.1f}%)"
            
            self.ax.set_title(title, fontsize=12, fontweight='bold', pad=20)
            self.ax.axis('off')
            
            # Enhanced legend with more details
            legend_elements = [
                Patch(facecolor='#1469C8', label=f'Laut'),
                Patch(facecolor='#32FF32', label=f'Mangsa - {len(prey_list)}'),
                Patch(facecolor='#FF3232', label=f'Predator - {len(predator_list)}')
            ]
            
            # Add ecosystem status
            if len(prey_list) == 0:
                legend_elements.append(Patch(facecolor='gray', label='⚠️ Mangsa Punah'))
            elif len(predator_list) == 0:
                legend_elements.append(Patch(facecolor='gray', label='⚠️ Predator Punah'))
            
            self.ax.legend(handles=legend_elements, loc='center left', bbox_to_anchor=(1.02, 0.5), 
                          fontsize=10, title="Legenda", title_fontsize=12)
            
        # Update button states
        self.btn_prev.ax.set_facecolor('lightgray' if self.current_step == 0 else 'white')
        self.btn_next.ax.set_facecolor('lightgray' if self.current_step == self.max_step else 'white')
        
        plt.draw()
    
    def prev_step(self, event):
        if self.current_step > 0:
            self.current_step -= 1
            self.update_plot()
    
    def next_step(self, event):
        if self.current_step < self.max_step:
            self.current_step += 1
            self.update_plot()
    
    def first_step(self, event):
        self.current_step = 0
        self.update_plot()
    
    def last_step(self, event):
        self.current_step = self.max_step
        self.update_plot()
    
    def toggle_play(self, event):
        if self.playing:
            self.stop_animation()
        else:
            self.start_animation()
    
    def start_animation(self):
        self.playing = True
        self.btn_play.label.set_text('|| Pause')
        self.animate_step()
    
    def stop_animation(self):
        self.playing = False
        self.btn_play.label.set_text('> Play')
        if self.animation_timer:
            self.animation_timer.stop()
            self.animation_timer = None
    
    def animate_step(self):
        if self.playing and self.current_step < self.max_step:
            self.current_step += 1
            self.update_plot()
            # Schedule next step
            self.animation_timer = self.fig.canvas.new_timer(interval=500)  # 500ms delay
            self.animation_timer.single_shot = True
            self.animation_timer.add_callback(self.animate_step)
            self.animation_timer.start()
        else:
            self.stop_animation()
    
    def on_key_press(self, event):
        if event.key == 'left':
            self.prev_step(None)
        elif event.key == 'right':
            self.next_step(None)
        elif event.key == 'home':
            self.first_step(None)
        elif event.key == 'end':
            self.last_step(None)
        elif event.key == ' ':
            self.toggle_play(None)


def plot_grid(grid_size, prey_list, predator_list, step):
    # Enhanced real-time plotting function - fixed to use single persistent figure
    grid = np.full((grid_size, grid_size, 3), [20, 105, 200], dtype=int)  # Ocean blue background
    
    # Add prey (bright green) and predators (bright red)
    for prey in prey_list:
        grid[prey.y, prey.x] = [50, 255, 50]  # Bright green for prey
    for predator in predator_list:
        grid[predator.y, predator.x] = [255, 50, 50]  # Bright red for predators

    # Create figure only once and reuse it
    if not hasattr(plot_grid, 'fig'):
        plot_grid.fig, plot_grid.ax = plt.subplots(figsize=(12, 8))
        mng = plot_grid.fig.canvas.manager
        mng.window.state('zoomed')
        plt.subplots_adjust(right=0.8)
        plot_grid.fig.patch.set_facecolor('lightblue')
    
    # Clear the axis and redraw
    plot_grid.ax.clear()
    plot_grid.ax.imshow(grid)
    
    # Enhanced title
    total_animals = len(prey_list) + len(predator_list)
    prey_percentage = (len(prey_list) / total_animals * 100) if total_animals > 0 else 0
    predator_percentage = (len(predator_list) / total_animals * 100) if total_animals > 0 else 0
    
    title = f"Simulasi Interaksi Predator-Mangsa\n"
    title += f"Waktu: {step} | Mangsa: {len(prey_list)} ({prey_percentage:.1f}%) | "
    title += f"Predator: {len(predator_list)} ({predator_percentage:.1f}%)"
    
    plot_grid.ax.set_title(title, fontsize=12, fontweight='bold', pad=20)
    plot_grid.ax.axis('off')
    
    # Enhanced legend
    legend_elements = [
        Patch(facecolor='#1469C8', label='Laut'),
        Patch(facecolor='#32FF32', label=f'Mangsa - {len(prey_list)}'),
        Patch(facecolor='#FF3232', label=f'Predator - {len(predator_list)}')
    ]
    
    # Add ecosystem status for real-time mode too
    if len(prey_list) == 0:
        legend_elements.append(Patch(facecolor='gray', label='⚠️ Mangsa Punah'))
    elif len(predator_list) == 0:
        legend_elements.append(Patch(facecolor='gray', label='⚠️ Predator Punah'))
    
    plot_grid.ax.legend(handles=legend_elements, loc='center left', bbox_to_anchor=(1.02, 0.5), 
                       fontsize=10, title="Legenda", title_fontsize=12)
    
    plt.draw()
    plt.pause(0.1)


def simulate(grid_size, initial_prey, initial_predators, prey_reproduce_interval,
             predator_reproduce_interval, predator_initial_energy, energy_gain,
             energy_loss, max_steps, enable_navigation=True):

    prey_list = [Prey(random.randrange(grid_size), random.randrange(grid_size)) for _ in range(initial_prey)]
    predator_list = [Predator(random.randrange(grid_size), random.randrange(grid_size), predator_initial_energy) for _ in range(initial_predators)]

    # Store simulation history if navigation is enabled
    history = []
    if enable_navigation:
        # Store initial state
        import copy
        history.append((copy.deepcopy(prey_list), copy.deepcopy(predator_list)))

    for step in range(1, max_steps + 1):
        occupied = {}
        for agent in prey_list + predator_list:
            occupied.setdefault((agent.x, agent.y), []).append(agent)

        # Prey actions
        new_prey = []
        for prey in prey_list:
            child = prey.step(grid_size, prey_reproduce_interval, occupied)
            if child:
                new_prey.append(child)
        prey_list.extend(new_prey)

        prey_positions = {(prey.x, prey.y) for prey in prey_list}
        occupied_positions = {(agent.x, agent.y) for agent in prey_list + predator_list}

        # Predator actions
        new_predators = []
        for predator in predator_list:
            child, ate = predator.step(grid_size, prey_positions, energy_gain, energy_loss, predator_reproduce_interval, occupied_positions)
            if ate:
                prey_list = [pr for pr in prey_list if not (pr.x == predator.x and pr.y == predator.y)]
                prey_positions.discard((predator.x, predator.y))
            if child:
                new_predators.append(child)
        predator_list.extend(new_predators)
        predator_list = [pred for pred in predator_list if pred.energy > 0]

        print(f"Langkah {step}: Mangsa = {len(prey_list)}, Predator = {len(predator_list)}")
        
        if enable_navigation:
            # Store current state for navigation
            import copy
            history.append((copy.deepcopy(prey_list), copy.deepcopy(predator_list)))
        else:
            # Use original real-time plotting
            plot_grid(grid_size, prey_list, predator_list, step)

        if not prey_list or not predator_list:
            print("Salah satu populasi telah punah, simulasi dihentikan.")
            break
    
    # Show navigation interface if enabled
    if enable_navigation:
        print(f"Simulasi selesai. Menampilkan {len(history)} langkah dengan kontrol navigasi.")
        print("Kontrol: ← → (navigasi), Home/End (awal/akhir), Spacebar (play/pause)")
        viewer = SimulationViewer(history, grid_size)
        plt.show()
    else:
        plt.show()