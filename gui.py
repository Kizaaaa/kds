import tkinter as tk
from tkinter import ttk
from simulation import simulate

def start_gui():
    def run_simulation():
        params = {label: int(entry.get()) for label, entry in entries.items()}
        float_params = {label: float(entry.get()) for label, entry in float_entries.items()}
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
            food_density=float_params["Kepadatan Makanan (0.0-1.0)"],
            enable_navigation=navigation_enabled
        )

    def center_window(window, width=500, height=750):
        # Get screen dimensions
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        
        # Calculate position coordinates
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        
        # Set window geometry
        window.geometry(f"{width}x{height}+{x}+{y}")

    def validate_float_input(value):
        """Validate float input for density parameter"""
        if value == "":
            return True
        try:
            float_val = float(value)
            return 0.0 <= float_val <= 1.0
        except ValueError:
            return False

    root = tk.Tk()
    root.title("🌊 Simulasi Interaksi Predator-Mangsa dengan Sistem Energi")
    
    # Center the window with increased height
    center_window(root, 580, 780)
    
    # Configure ocean blue theme
    root.configure(bg="#0B2F52")  # Deep ocean blue
    
    # Create and configure style
    style = ttk.Style()
    style.theme_use('clam')
    
    # Configure styles with ocean theme
    style.configure('Ocean.TLabel', 
                   background="#0B2F52", 
                   foreground="#E6F3FF",  # Light blue text
                   font=('Segoe UI', 9, 'bold'))
    
    style.configure('Ocean.TEntry',
                   fieldbackground="#1E4A72",  # Medium ocean blue
                   foreground="#FFFFFF",
                   bordercolor="#4A90E2",
                   lightcolor="#4A90E2",
                   darkcolor="#2C5F85",
                   font=('Segoe UI', 9))
    
    style.configure('Ocean.TCheckbutton',
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
             background=[('active', '#87CEEB'),      # Light blue on hover
                        ('pressed', '#1E4A72')],     # Dark blue when pressed
             foreground=[('active', '#000080'),      # Dark blue text on hover for readability
                        ('pressed', '#FFFFFF')])

    # Create main frame with padding
    main_frame = tk.Frame(root, bg="#0B2F52", padx=30, pady=20)
    main_frame.pack(fill='both', expand=True)
    
    # Add title
    title_label = tk.Label(main_frame, 
                          text="🌊 Simulasi Interaksi Predator-Mangsa 🐠\ndengan Sistem Energi dan Makanan",
                          font=('Segoe UI', 14, 'bold'),
                          bg="#0B2F52",
                          fg="#87CEEB",  # Sky blue
                          justify='center')
    title_label.grid(row=0, column=0, columnspan=2, pady=(0, 15))

    # Create scrollable frame for parameters
    canvas = tk.Canvas(main_frame, bg="#0B2F52", highlightthickness=0)
    scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg="#0B2F52")

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    # Configure mouse wheel scrolling
    def _on_mousewheel(event):
        canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    canvas.bind_all("<MouseWheel>", _on_mousewheel)

    entries = {}
    float_entries = {}
    
    # Enhanced parameters with new energy and food system values
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
    
    # Float parameters (for food density)
    float_defaults = {
        "Kepadatan Makanan (0.0-1.0)": 0.1
    }

    # Parameter descriptions for tooltips
    descriptions = {
        "Ukuran Laut": "Ukuran grid simulasi (NxN)",
        "Banyak Mangsa di Awal": "Jumlah mangsa pada awal simulasi",
        "Banyak Predator di Awal": "Jumlah predator pada awal simulasi", 
        "Waktu untuk Reproduksi Mangsa": "Interval reproduksi mangsa (langkah)",
        "Waktu untuk Reproduksi Predator": "Interval reproduksi predator (langkah)",
        "Energi Awal Predator": "Energi awal setiap predator",
        "Energi yang Didapat Saat Makan": "Energi yang didapat predator saat makan mangsa",
        "Energi Hilang Dalam Satu Waktu": "Energi yang hilang per langkah waktu",
        "Waktu Simulasi Maksimum": "Durasi maksimum simulasi",
        "Kepadatan Makanan (0.0-1.0)": "Proporsi sel yang berisi makanan (0.0 = tidak ada, 1.0 = penuh)"
    }

    # Add section headers and organize parameters
    current_row = 1
    
    # Environment section
    env_header = tk.Label(scrollable_frame, 
                         text="🌍 Pengaturan Lingkungan",
                         font=('Segoe UI', 11, 'bold'),
                         bg="#0B2F52",
                         fg="#FFD700")  # Gold color
    env_header.grid(row=current_row, column=0, columnspan=2, pady=(10, 5), sticky="w")
    current_row += 1
    
    env_params = ["Ukuran Laut", "Kepadatan Makanan (0.0-1.0)", "Waktu Simulasi Maksimum"]
    
    # Environment parameters
    for param in env_params:
        if param in defaults:
            ttk.Label(scrollable_frame, text=param + ":", style='Ocean.TLabel').grid(
                row=current_row, column=0, padx=10, pady=6, sticky="e")
            
            entry = ttk.Entry(scrollable_frame, style='Ocean.TEntry', width=15)
            entry.insert(0, str(defaults[param]))
            entry.grid(row=current_row, column=1, padx=10, pady=6, sticky="w")
            entries[param] = entry
        else:  # Float parameter
            ttk.Label(scrollable_frame, text=param + ":", style='Ocean.TLabel').grid(
                row=current_row, column=0, padx=10, pady=6, sticky="e")
            
            # Register validation function
            vcmd = (root.register(validate_float_input), '%P')
            entry = ttk.Entry(scrollable_frame, style='Ocean.TEntry', width=15, 
                             validate='key', validatecommand=vcmd)
            entry.insert(0, str(float_defaults[param]))
            entry.grid(row=current_row, column=1, padx=10, pady=6, sticky="w")
            float_entries[param] = entry
        current_row += 1
    
    # Population section
    pop_header = tk.Label(scrollable_frame, 
                         text="🐟 Pengaturan Populasi",
                         font=('Segoe UI', 11, 'bold'),
                         bg="#0B2F52",
                         fg="#FFD700")
    pop_header.grid(row=current_row, column=0, columnspan=2, pady=(15, 5), sticky="w")
    current_row += 1
    
    pop_params = ["Banyak Mangsa di Awal", "Banyak Predator di Awal"]
    
    for param in pop_params:
        ttk.Label(scrollable_frame, text=param + ":", style='Ocean.TLabel').grid(
            row=current_row, column=0, padx=10, pady=6, sticky="e")
        
        entry = ttk.Entry(scrollable_frame, style='Ocean.TEntry', width=15)
        entry.insert(0, str(defaults[param]))
        entry.grid(row=current_row, column=1, padx=10, pady=6, sticky="w")
        entries[param] = entry
        current_row += 1
    
    # Reproduction section
    repro_header = tk.Label(scrollable_frame, 
                           text="🥚 Pengaturan Reproduksi",
                           font=('Segoe UI', 11, 'bold'),
                           bg="#0B2F52",
                           fg="#FFD700")
    repro_header.grid(row=current_row, column=0, columnspan=2, pady=(15, 5), sticky="w")
    current_row += 1
    
    repro_params = ["Waktu untuk Reproduksi Mangsa", "Waktu untuk Reproduksi Predator"]
    
    for param in repro_params:
        ttk.Label(scrollable_frame, text=param + ":", style='Ocean.TLabel').grid(
            row=current_row, column=0, padx=10, pady=6, sticky="e")
        
        entry = ttk.Entry(scrollable_frame, style='Ocean.TEntry', width=15)
        entry.insert(0, str(defaults[param]))
        entry.grid(row=current_row, column=1, padx=10, pady=6, sticky="w")
        entries[param] = entry
        current_row += 1
    
    # Energy system section
    energy_header = tk.Label(scrollable_frame, 
                            text="⚡ Sistem Energi",
                            font=('Segoe UI', 11, 'bold'),
                            bg="#0B2F52",
                            fg="#FFD700")
    energy_header.grid(row=current_row, column=0, columnspan=2, pady=(15, 5), sticky="w")
    current_row += 1
    
    energy_params = ["Energi Awal Predator", "Energi yang Didapat Saat Makan", "Energi Hilang Dalam Satu Waktu"]
    
    for param in energy_params:
        ttk.Label(scrollable_frame, text=param + ":", style='Ocean.TLabel').grid(
            row=current_row, column=0, padx=10, pady=6, sticky="e")
        
        entry = ttk.Entry(scrollable_frame, style='Ocean.TEntry', width=15)
        entry.insert(0, str(defaults[param]))
        entry.grid(row=current_row, column=1, padx=10, pady=6, sticky="w")
        entries[param] = entry
        current_row += 1

    # Add navigation mode checkbox with enhanced styling
    nav_var = tk.BooleanVar(value=True)
    nav_checkbox = ttk.Checkbutton(scrollable_frame, 
                                  text="🧭 Aktifkan Mode Navigasi\n    (bisa maju/mundur dalam simulasi)", 
                                  variable=nav_var, 
                                  style='Ocean.TCheckbutton')
    nav_checkbox.grid(row=current_row, column=0, columnspan=2, pady=15, sticky="w")
    current_row += 1

    # Add informational text
    info_text = tk.Label(scrollable_frame,
                        text="ℹ️ Sistem Energi Baru:\n" +
                             "• Mangsa memiliki energi dan perlu makanan untuk bertahan hidup\n" +
                             "• Predator kehilangan energi setiap langkah dan mendapat energi dari memakan mangsa\n" +
                             "• Makanan (plankton/vegetasi) tersebar di laut dan dapat regenerasi\n" +
                             "• Reproduksi memerlukan energi minimum",
                        font=('Segoe UI', 8),
                        bg="#0B2F52",
                        fg="#E6F3FF",
                        justify='left',
                        wraplength=500)
    info_text.grid(row=current_row, column=0, columnspan=2, pady=10, sticky="w")
    current_row += 1

    # Configure canvas and scrollbar in main_frame
    canvas.grid(row=1, column=0, columnspan=2, sticky="nsew", pady=10)
    scrollbar.grid(row=1, column=2, sticky="ns", pady=10)

    # Configure grid weights
    main_frame.grid_rowconfigure(1, weight=1)
    main_frame.grid_columnconfigure(0, weight=1)

    # Add start button outside the scrollable area
    button_frame = tk.Frame(main_frame, bg="#0B2F52")
    button_frame.grid(row=2, column=0, columnspan=2, pady=15)
    
    start_button = ttk.Button(button_frame, 
                             text="🚀 Mulai Simulasi", 
                             command=run_simulation, 
                             style='Ocean.TButton')
    start_button.pack()
    
    # Add a subtle separator line
    separator = tk.Frame(main_frame, height=2, bg="#4A90E2")
    separator.grid(row=3, column=0, columnspan=2, sticky="ew", pady=5)
    
    # Add footer text
    footer_label = tk.Label(main_frame, 
                           text="Kelompok 10 - K1\nSimulasi Predator-Mangsa dengan Sistem Energi",
                           font=('Segoe UI', 9),
                           bg="#0B2F52",
                           fg="#87CEEB",
                           justify='center')
    footer_label.grid(row=4, column=0, columnspan=2, pady=(5, 0))

    # Make window resizable for better usability with more parameters
    root.resizable(True, True)
    root.minsize(580, 650)
    
    # Set window icon (if you have an icon file)
    try:
        root.iconbitmap("ocean_icon.ico")  # Optional: add your icon file
    except:
        pass  # Ignore if icon file doesn't exist
    
    root.mainloop()