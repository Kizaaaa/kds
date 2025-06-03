import tkinter as tk
from tkinter import ttk
from simulation import simulate

def start_gui():
    def run_simulation():
        params = {label: int(entry.get()) for label, entry in entries.items()}
        navigation_enabled = nav_var.get()
        root.destroy()
        simulate(
            grid_size=params["Ukuran Laut"],
            initial_prey=params["Banyak Mangsa di Awal"],
            initial_predators=params["Banyak Predator di Awal"],
            prey_reproduce_interval=params["Waktu untuk Reproduksi Mangsa"],
            predator_reproduce_interval=params["Waktu untuk Reproduksi Predator"],
            predator_initial_energy=params["Energi Awal Predator"],
            energy_gain=params["Energi yang Didapat Saat Makan"],
            energy_loss=params["Energi Hilang Dalam Satu Waktu"],
            max_steps=params["Waktu Simulasi Maksimum"],
            enable_navigation=navigation_enabled
        )

    def center_window(window, width=500, height=600):
        # Get screen dimensions
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        
        # Calculate position coordinates
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        
        # Set window geometry
        window.geometry(f"{width}x{height}+{x}+{y}")

    root = tk.Tk()
    root.title("🌊 Simulasi Interaksi Predator-Mangsa")
    
    # Center the window
    center_window(root, 550, 650)
    
    # Configure ocean blue theme
    root.configure(bg="#0B2F52")  # Deep ocean blue
    
    # Create and configure style
    style = ttk.Style()
    style.theme_use('clam')
    
    # Configure styles with ocean theme
    style.configure('Ocean.TLabel', 
                   background="#0B2F52", 
                   foreground="#E6F3FF",  # Light blue text
                   font=('Segoe UI', 10, 'bold'))
    
    style.configure('Ocean.TEntry',
                   fieldbackground="#1E4A72",  # Medium ocean blue
                   foreground="#FFFFFF",
                   bordercolor="#4A90E2",
                   lightcolor="#4A90E2",
                   darkcolor="#2C5F85",
                   font=('Segoe UI', 10))
    
    style.configure('Ocean.TCheckbutton',
                #    background="#0B2F52",
                #    foreground="#E6F3FF",
                #    focuscolor="#4A90E2",
                #    indicatorforeground="#FFFFFF",  # White checkmark
                #    indicatorbackground="#1E4A72",  # Dark blue background for checkbox
                   font=('Segoe UI', 10))
    
    # Map checkbutton states for better visibility
    style.map('Ocean.TCheckbutton',
             indicatorforeground=[('selected', '#00FF7F'),  # Bright green checkmark when selected
                                ('!selected', '#FFFFFF')],   # White when not selected
             indicatorbackground=[('selected', '#1E4A72'),   # Dark blue when selected
                                ('!selected', '#2C5F85')])   # Slightly lighter when not selected
    
    style.configure('Ocean.TButton',
                   background="#1E90FF",  # Bright ocean blue
                   foreground="#FFFFFF",
                   bordercolor="#4A90E2",
                   lightcolor="#5BA0F2",
                   darkcolor="#1E4A72",
                   font=('Segoe UI', 12, 'bold'))
    
    style.map('Ocean.TButton',
             background=[('active', '#87CEEB'),      # Light blue on hover - much more readable
                        ('pressed', '#1E4A72')],     # Dark blue when pressed
             foreground=[('active', '#000080'),      # Dark blue text on hover for readability
                        ('pressed', '#FFFFFF')])

    # Create main frame with padding
    main_frame = tk.Frame(root, bg="#0B2F52", padx=30, pady=30)
    main_frame.pack(fill='both', expand=True)
    
    # Add title
    title_label = tk.Label(main_frame, 
                          text="🌊 Simulasi Interaksi Predator-Mangsa 🐠",
                          font=('Segoe UI', 16, 'bold'),
                          bg="#0B2F52",
                          fg="#87CEEB")  # Sky blue
    title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))

    entries = {}
    defaults = {
        "Ukuran Laut": 50,
        "Banyak Mangsa di Awal": 250,
        "Banyak Predator di Awal": 200,
        "Waktu untuk Reproduksi Mangsa": 5,
        "Waktu untuk Reproduksi Predator": 8,
        "Energi Awal Predator": 20,
        "Energi yang Didapat Saat Makan": 15,
        "Energi Hilang Dalam Satu Waktu": 1,
        "Waktu Simulasi Maksimum": 100
    }

    # Create parameter inputs with ocean styling
    for i, (label, default) in enumerate(defaults.items()):
        ttk.Label(main_frame, text=label + ":", style='Ocean.TLabel').grid(
            row=i+1, column=0, padx=10, pady=8, sticky="e")
        
        entry = ttk.Entry(main_frame, style='Ocean.TEntry', width=15)
        entry.insert(0, str(default))
        entry.grid(row=i+1, column=1, padx=10, pady=8, sticky="w")
        entries[label] = entry

    # Add navigation mode checkbox with ocean styling
    nav_var = tk.BooleanVar(value=True)
    nav_checkbox = ttk.Checkbutton(main_frame, 
                                  text="🧭 Aktifkan Mode Navigasi (bisa maju/mundur)", 
                                  variable=nav_var, 
                                  style='Ocean.TCheckbutton')
    nav_checkbox.grid(row=len(defaults)+1, column=0, columnspan=2, pady=15, sticky="w")

    # Add start button with ocean styling
    start_button = ttk.Button(main_frame, 
                             text="🚀 Mulai Simulasi", 
                             command=run_simulation, 
                             style='Ocean.TButton')
    start_button.grid(row=len(defaults)+2, column=0, columnspan=2, pady=20)
    
    # Add a subtle separator line
    separator = tk.Frame(main_frame, height=2, bg="#4A90E2")
    separator.grid(row=len(defaults)+3, column=0, columnspan=2, sticky="ew", pady=10)
    
    # Add footer text
    footer_label = tk.Label(main_frame, 
                           text="Kelompok 10 - K1",
                           font=('Segoe UI', 9,),
                           bg="#0B2F52",
                           fg="#87CEEB")
    footer_label.grid(row=len(defaults)+4, column=0, columnspan=2, pady=(10, 0))

    # Configure grid weights for better centering
    main_frame.grid_columnconfigure(0, weight=1)
    main_frame.grid_columnconfigure(1, weight=1)
    
    # Make window non-resizable for consistent appearance
    root.resizable(False, False)
    
    # Set window icon (if you have an icon file)
    try:
        root.iconbitmap("ocean_icon.ico")  # Optional: add your icon file
    except:
        pass  # Ignore if icon file doesn't exist
    
    root.mainloop()