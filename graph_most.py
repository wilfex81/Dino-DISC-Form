import numpy as np
import matplotlib.pyplot as plt

def plot_disc_graph_most(values, ax):
    # Data points and labels
    labels = ['D', 'I', 'S', 'C']
    
    # Transform values to match form grid (0-20 scale)
    mapped_values = [v * 2 for v in values]

    # Plot setup
    positions = np.arange(len(labels))
    
    # Setup the grid first - match exact scale from form
    ax.set_ylim(-0.5, 20.5)  # Extended to show full grid
    ax.set_xlim(-0.8, len(labels) - 0.2)
    
    # Add all grid numbers from 0 to 20
    for i in range(21):
        # Draw light gray horizontal grid lines
        alpha = 0.3 if i % 4 == 0 else 0.15  # Make major gridlines more visible
        linewidth = 0.8 if i % 4 == 0 else 0.5
        ax.axhline(y=i, color='gray', linestyle='-', alpha=alpha, linewidth=linewidth)
        
        # Add left-side numbers with correct alignment and spacing
        if i % 2 == 0:  # Show even numbers
            ax.text(-0.6, i, str(i), ha='right', va='center', fontsize=6)
    
    # Add vertical dotted lines at specific positions
    for x in positions:
        ax.axvline(x=x, color='lightgray', linestyle=':', alpha=0.2, linewidth=0.5)
    
    # Add segment labels (H, MH, M, ML, L) - match exact position and style
    segments = ['H', 'MH', 'M', 'ML', 'L']
    y_positions = [18, 14, 10, 6, 2]
    for label, y in zip(segments, y_positions):
        ax.text(-0.75, y, label, ha='right', va='center', fontsize=7, fontweight='bold')

    # Plot data points and lines - match exact style
    ax.plot(positions, mapped_values, 'ko-', linewidth=0.8, markersize=4, markerfacecolor='white', markeredgewidth=0.8)
    ax.plot(positions, mapped_values, 'ko', markersize=2, markerfacecolor='black')

    # Set up axis
    ax.set_xticks(positions)
    ax.set_xticklabels(labels, fontsize=9, fontweight='bold')
    ax.set_yticks([])  # Remove y-axis ticks
    
    # Title exactly as in form - match font and spacing
    ax.set_title("Graph 1 MOST\nMask, Public Self", pad=10, fontsize=8, fontweight='bold')
    
    # Clean up spines
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(True)
    ax.spines['bottom'].set_visible(True)
    ax.spines['left'].set_linewidth(0.5)
    ax.spines['bottom'].set_linewidth(0.5)

    return ax