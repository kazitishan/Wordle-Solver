import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

class DataVisualizationOverlay:
    def __init__(self, parent, data, possible_words, close_callback):
        self.parent = parent
        self.data = data  # This is now the dictionary from fetchData()
        self.possible_words = possible_words
        self.close_callback = close_callback
        
        # Create the overlay frame
        self.create_overlay()
        
    def create_overlay(self):
        # Create a full-screen frame overlay
        self.overlay = tk.Frame(self.parent, bg="#121213")
        self.overlay.place(x=0, y=0, relwidth=1, relheight=1)
        
        # Create header with title and close button
        header_frame = tk.Frame(self.overlay, bg="#121213")
        header_frame.pack(fill=tk.X, padx=20, pady=20)
        
        # Add a close button (X) at the top left
        close_button = tk.Button(
            header_frame, 
            text="X", 
            font=('Inter', 14, 'bold'), 
            bg="#818384", 
            fg="#000000",
            command=self.close_callback,
            width=2,
            height=1
        )
        close_button.pack(side=tk.LEFT)
        
        # Add title
        title = tk.Label(
            header_frame, 
            text="Possible Word Data Analysis", 
            font=('Inter', 20, 'bold'), 
            bg="#121213", 
            fg="#ffffff"
        )
        title.pack(side=tk.LEFT, padx=20)
        
        # Create content area
        content_frame = tk.Frame(self.overlay, bg="#121213")
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Create tabs for visualizations
        tab_control = ttk.Notebook(content_frame)
        
        # Apply a dark theme to the notebook
        style = ttk.Style()
        style.theme_use('default')
        style.configure("TNotebook", background="#121213", borderwidth=0)
        style.configure("TNotebook.Tab", background="#3a3a3c", foreground="#ffffff", padding=[10, 5])
        style.map("TNotebook.Tab", background=[("selected", "#538d4e")])
        
        # Create tabs
        letter_freq_tab = tk.Frame(tab_control, bg="#121213")
        position_freq_tab = tk.Frame(tab_control, bg="#121213")
        letter_occurrences_tab = tk.Frame(tab_control, bg="#121213")
        
        tab_control.add(letter_freq_tab, text="Letter Frequency")
        tab_control.add(position_freq_tab, text="Position Analysis")
        tab_control.add(letter_occurrences_tab, text="Letter Occurrences")
        
        tab_control.pack(expand=1, fill="both")
        
        # Fill tabs with content
        self.create_letter_frequency_tab(letter_freq_tab)
        self.create_position_frequency_tab(position_freq_tab)
        self.create_letter_occurrences_tab(letter_occurrences_tab)
    
    def create_letter_frequency_tab(self, parent):
        # Create a frame for the chart
        chart_frame = tk.Frame(parent, bg="#121213")
        chart_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create description
        description = tk.Label(
            chart_frame,
            text="This chart shows the frequency of each letter across all positions.",
            font=('Inter', 12),
            bg="#121213",
            fg="#ffffff",
            wraplength=1000,
            anchor="w",
            justify="left"
        )
        description.pack(pady=(0, 10), anchor="w")
        
        # Use frequencies from fetchData()
        letter_counts = self.data['frequencies']
        
        # Sort by frequency
        sorted_letters = sorted(letter_counts.items(), key=lambda x: x[1], reverse=True)
        letters = [item[0] for item in sorted_letters]
        counts = [item[1] for item in sorted_letters]
        
        # Create figure and plot
        fig, ax = plt.subplots(figsize=(12, 6))
        fig.patch.set_facecolor('#121213')
        ax.set_facecolor('#121213')
        
        bars = ax.bar(letters, counts, color='#538d4e')
        
        # Styling
        ax.set_title('Letter Frequency in Possible Words', color='white', fontsize=16)
        ax.set_xlabel('Letters', color='white', fontsize=14)
        ax.set_ylabel('Frequency', color='white', fontsize=14)
        ax.tick_params(axis='x', colors='white')
        ax.tick_params(axis='y', colors='white')
        
        # Add value labels on top of each bar
        for bar in bars:
            height = bar.get_height()
            ax.annotate(f'{height}',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom',
                        color='white')
        
        # Change spines color
        for spine in ax.spines.values():
            spine.set_color('#3a3a3c')
        
        # Embed the plot in Tkinter
        canvas = FigureCanvasTkAgg(fig, master=chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    def create_letter_occurrences_tab(self, parent):
        # Create a frame for the chart
        chart_frame = tk.Frame(parent, bg="#121213")
        chart_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create description
        description = tk.Label(
            chart_frame,
            text="This chart shows the number of words containing each letter.",
            font=('Inter', 12),
            bg="#121213",
            fg="#ffffff",
            wraplength=1000,
            anchor="w",
            justify="left"
        )
        description.pack(pady=(0, 10), anchor="w")
        
        # Use occurrences from fetchData()
        letter_occurrences = self.data['occurrences']
        
        # Sort by occurrences
        sorted_letters = sorted(letter_occurrences.items(), key=lambda x: x[1], reverse=True)
        letters = [item[0] for item in sorted_letters]
        counts = [item[1] for item in sorted_letters]
        
        # Create figure and plot
        fig, ax = plt.subplots(figsize=(12, 6))
        fig.patch.set_facecolor('#121213')
        ax.set_facecolor('#121213')
        
        bars = ax.bar(letters, counts, color='#3a7ca5')  # Different color to distinguish from frequency
        
        # Styling
        ax.set_title('Letter Occurrences in Possible Words', color='white', fontsize=16)
        ax.set_xlabel('Letters', color='white', fontsize=14)
        ax.set_ylabel('Number of Words', color='white', fontsize=14)
        ax.tick_params(axis='x', colors='white')
        ax.tick_params(axis='y', colors='white')
        
        # Add value labels on top of each bar
        for bar in bars:
            height = bar.get_height()
            ax.annotate(f'{height}',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom',
                        color='white')
        
        # Change spines color
        for spine in ax.spines.values():
            spine.set_color('#3a3a3c')
        
        # Embed the plot in Tkinter
        canvas = FigureCanvasTkAgg(fig, master=chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    def create_position_frequency_tab(self, parent):
        # Create a frame for the chart
        chart_frame = tk.Frame(parent, bg="#121213")
        chart_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create description
        description = tk.Label(
            chart_frame,
            text="This heatmap shows the frequency of each letter at each position in the word.",
            font=('Inter', 12),
            bg="#121213",
            fg="#ffffff",
            wraplength=1000,
            anchor="w",
            justify="left"
        )
        description.pack(pady=(0, 10), anchor="w")
        
        # Use position data from fetchData()
        position_freq = self.data['positions']
        
        # Get all unique letters
        all_letters = sorted(list(position_freq.keys()))
        
        # Create a matrix for heatmap
        matrix = np.zeros((5, len(all_letters)))
        for i, letter in enumerate(all_letters):
            for pos in range(5):
                matrix[pos, i] = position_freq[letter][pos]
        
        # Create figure and plot
        fig, ax = plt.subplots(figsize=(12, 8))
        fig.patch.set_facecolor('#121213')
        ax.set_facecolor('#121213')
        
        # Create horizontal heatmap
        im = ax.imshow(matrix, cmap='YlGnBu', aspect='auto', origin='lower')
        
        # Styling
        ax.set_title('Letter Frequency by Position', color='white', fontsize=16)
        ax.set_ylabel('Position (0-indexed)', color='white', fontsize=14)
        ax.set_xlabel('Letter', color='white', fontsize=14)
        ax.set_yticks(np.arange(5))
        ax.set_xticks(np.arange(len(all_letters)))
        ax.set_xticklabels(all_letters, rotation=45, ha='right')
        ax.tick_params(axis='x', colors='white')
        ax.tick_params(axis='y', colors='white')
        
        # Add colorbar
        cbar = plt.colorbar(im, ax=ax)
        cbar.ax.tick_params(colors='white')
        cbar.set_label('Frequency', color='white')
        
        # Loop over data dimensions and create text annotations
        for i in range(5):
            for j in range(len(all_letters)):
                if matrix[i, j] > 0:
                    # Adjust text color based on background intensity
                    text_color = "black" if matrix[i, j] < matrix.max()/2 else "white"
                    ax.text(j, i, int(matrix[i, j]),
                            ha="center", va="center", color=text_color,
                            fontweight='bold')
        
        # Change spines color
        for spine in ax.spines.values():
            spine.set_color('#3a3a3c')
        
        plt.tight_layout()
        
        # Create a new Tkinter canvas
        canvas = FigureCanvasTkAgg(fig, master=chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    def destroy(self):
        self.overlay.destroy()