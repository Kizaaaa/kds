import random
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
from matplotlib.patches import Patch

# Import the enhanced agents (you'll need to use the updated agents.py)
from agents import Prey, Predator, Food


class SimulationViewer:
    def __init__(self, history, grid_size):
        self.history = history
        self.grid_size = grid_size
        self.current_step = 0
        self.max_step = len(history) - 1
        
        # Create figure and axis with better styling
        self.fig, (self.ax_main, self.ax_stats) = plt.subplots(1, 2, figsize=(18, 10), 
                                                              gridspec_kw={'width_ratios': [2, 1]})
        mng = self.fig.canvas.manager
        mng.window.state('zoomed')
        plt.subplots_adjust(bottom=0.15, right=0.95, top=0.9)
        
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
        self.ax_main.clear()
        self.ax_stats.clear()
        
        if self.current_step < len(self.history):
            prey_list, predator_list, food_list, stats = self.history[self.current_step]
            
            # Create grid with ocean gradient effect
            grid = np.full((self.grid_size, self.grid_size, 3), [20, 105, 200], dtype=int)
            
            # Add food sources (yellow/green)
            for food in food_list:
                if food.available:
                    grid[food.y, food.x] = [100, 200, 50]  # Light green for available food
                else:
                    grid[food.y, food.x] = [139, 69, 19]   # Brown for consumed food
            
            # Add prey (bright green) with energy-based intensity
            for prey in prey_list:
                energy_ratio = min(1.0, prey.energy / 30.0)  # Normalize to max energy
                green_intensity = int(150 + 105 * energy_ratio)  # Brighter green for higher energy
                grid[prey.y, prey.x] = [50, green_intensity, 50]
            
            # Add predators (bright red) with energy-based intensity
            for predator in predator_list:
                energy_ratio = min(1.0, predator.energy / 50.0)  # Normalize to reasonable max
                red_intensity = int(150 + 105 * energy_ratio)  # Brighter red for higher energy
                grid[predator.y, predator.x] = [red_intensity, 50, 50]
            
            self.ax_main.imshow(grid)
            
            # Enhanced title with more information
            total_animals = len(prey_list) + len(predator_list)
            prey_percentage = (len(prey_list) / total_animals * 100) if total_animals > 0 else 0
            predator_percentage = (len(predator_list) / total_animals * 100) if total_animals > 0 else 0
            
            title = f"Simulasi Interaksi Predator-Mangsa dengan Sistem Energi\n"
            title += f"Waktu: {self.current_step + 1}/{len(self.history)} | "
            title += f"Mangsa: {len(prey_list)} ({prey_percentage:.1f}%) | "
            title += f"Predator: {len(predator_list)} ({predator_percentage:.1f}%)"
            
            self.ax_main.set_title(title, fontsize=12, fontweight='bold', pad=20)
            self.ax_main.axis('off')
            
            # Enhanced legend
            legend_elements = [
                Patch(facecolor='#1469C8', label='Laut'),
                Patch(facecolor='#64C832', label=f'Makanan - {sum(1 for f in food_list if f.available)}'),
                Patch(facecolor='#32FF32', label=f'Mangsa - {len(prey_list)}'),
                Patch(facecolor='#FF3232', label=f'Predator - {len(predator_list)}')
            ]
            
            # Add ecosystem status
            if len(prey_list) == 0:
                legend_elements.append(Patch(facecolor='gray', label='⚠️ Mangsa Punah'))
            elif len(predator_list) == 0:
                legend_elements.append(Patch(facecolor='gray', label='⚠️ Predator Punah'))
            
            self.ax_main.legend(handles=legend_elements, loc='center left', bbox_to_anchor=(1.02, 0.5), 
                               fontsize=10, title="Legenda", title_fontsize=12)
            
            # Plot statistics
            steps = list(range(len(self.history[:self.current_step + 1])))
            prey_counts = [len(h[0]) for h in self.history[:self.current_step + 1]]
            predator_counts = [len(h[1]) for h in self.history[:self.current_step + 1]]
            
            if len(steps) > 1:
                self.ax_stats.plot(steps, prey_counts, 'g-', linewidth=2, label='Mangsa')
                self.ax_stats.plot(steps, predator_counts, 'r-', linewidth=2, label='Predator')
                self.ax_stats.set_xlabel('Waktu')
                self.ax_stats.set_ylabel('Populasi')
                self.ax_stats.set_title('Dinamika Populasi')
                self.ax_stats.legend()
                self.ax_stats.grid(True, alpha=0.3)
            
            # Add energy statistics if available
            if stats and 'avg_prey_energy' in stats:
                avg_prey_energy = stats['avg_prey_energy']
                avg_predator_energy = stats['avg_predator_energy']
                
                # Add energy info to the plot
                energy_text = f"Rata-rata Energi:\nMangsa: {avg_prey_energy:.1f}\nPredator: {avg_predator_energy:.1f}"
                self.ax_stats.text(0.02, 0.98, energy_text, transform=self.ax_stats.transAxes, 
                                  verticalalignment='top', fontsize=10, 
                                  bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
        
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
            self.animation_timer = self.fig.canvas.new_timer(interval=500)
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


def simulate(grid_size, initial_prey, initial_predators, prey_reproduce_interval,
             predator_reproduce_interval, predator_initial_energy, energy_gain,
             energy_loss, max_steps, enable_navigation=True, food_density=0.1):

    # Create initial populations
    prey_list = [Prey(random.randrange(grid_size), random.randrange(grid_size)) 
                 for _ in range(initial_prey)]
    predator_list = [Predator(random.randrange(grid_size), random.randrange(grid_size), predator_initial_energy) 
                     for _ in range(initial_predators)]
    
    # Create food sources
    num_food = int(grid_size * grid_size * food_density)
    food_list = []
    for _ in range(num_food):
        x, y = random.randrange(grid_size), random.randrange(grid_size)
        food_list.append(Food(x, y))

    # Store simulation history if navigation is enabled
    history = []
    if enable_navigation:
        import copy
        # Calculate initial stats
        avg_prey_energy = sum(p.energy for p in prey_list) / len(prey_list) if prey_list else 0
        avg_predator_energy = sum(p.energy for p in predator_list) / len(predator_list) if predator_list else 0
        stats = {'avg_prey_energy': avg_prey_energy, 'avg_predator_energy': avg_predator_energy}
        history.append((copy.deepcopy(prey_list), copy.deepcopy(predator_list), 
                       copy.deepcopy(food_list), stats))

    for step in range(1, max_steps + 1):
        # Update food regeneration
        for food in food_list:
            food.step()
        
        # Get available food positions
        food_positions = {(f.x, f.y) for f in food_list if f.available}
        
        # Create occupied positions map
        occupied = {}
        for agent in prey_list + predator_list:
            occupied.setdefault((agent.x, agent.y), []).append(agent)

        # Prey actions with energy system
        new_prey = []
        for prey in prey_list[:]:  # Use slice to avoid modification during iteration
            child = prey.step(grid_size, prey_reproduce_interval, occupied, food_positions)
            if child:
                new_prey.append(child)
        
        # Remove dead prey (those with no energy)
        prey_list = [prey for prey in prey_list if prey.is_alive()]
        prey_list.extend(new_prey)

        # Consume food where prey are located
        for prey in prey_list:
            for food in food_list:
                if food.x == prey.x and food.y == prey.y and food.available:
                    food.consume()
                    break

        prey_positions = {(prey.x, prey.y) for prey in prey_list}
        occupied_positions = {(agent.x, agent.y) for agent in prey_list + predator_list}

        # Predator actions
        new_predators = []
        for predator in predator_list:
            child, ate = predator.step(grid_size, prey_positions, energy_gain, energy_loss, 
                                     predator_reproduce_interval, occupied_positions)
            if ate:
                # Remove eaten prey
                prey_list = [pr for pr in prey_list if not (pr.x == predator.x and pr.y == predator.y)]
                prey_positions.discard((predator.x, predator.y))
            if child:
                new_predators.append(child)
        
        predator_list.extend(new_predators)
        predator_list = [pred for pred in predator_list if pred.is_alive()]

        # Calculate statistics
        avg_prey_energy = sum(p.energy for p in prey_list) / len(prey_list) if prey_list else 0
        avg_predator_energy = sum(p.energy for p in predator_list) / len(predator_list) if predator_list else 0
        available_food = sum(1 for f in food_list if f.available)
        
        print(f"Langkah {step}: Mangsa = {len(prey_list)} (Energi rata-rata: {avg_prey_energy:.1f}), "
              f"Predator = {len(predator_list)} (Energi rata-rata: {avg_predator_energy:.1f}), "
              f"Makanan tersedia = {available_food}")
        
        if enable_navigation:
            import copy
            stats = {
                'avg_prey_energy': avg_prey_energy, 
                'avg_predator_energy': avg_predator_energy,
                'available_food': available_food
            }
            history.append((copy.deepcopy(prey_list), copy.deepcopy(predator_list), 
                           copy.deepcopy(food_list), stats))

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