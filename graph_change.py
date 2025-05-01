import numpy as np
import matplotlib.pyplot as plt

def plot_disc_graph_change(values, ax):
    # Data points and labels
    labels = ['D', 'I', 'S', 'C']
    
    # Plot setup
    positions = np.arange(len(labels))
    
    # Setup the grid - match exact scale from form
    ax.set_ylim(-20.5, 20.5)  # Extended to show full grid
    ax.set_xlim(-0.8, len(labels) - 0.2)
    
    # Add all grid lines from -20 to +20
    for i in range(-20, 21):
        # Draw light gray horizontal grid lines
        alpha = 0.3 if i == 0 else 0.15  # Make zero line more visible
        linewidth = 0.8 if i == 0 else 0.5  # Make zero line thicker
        ax.axhline(y=i, color='gray', linestyle='-', alpha=alpha, linewidth=linewidth)
        
        # Add left-side numbers with correct alignment and spacing
        if i != 0 and i % 2 == 0:  # Only show even numbers
            ax.text(-0.6, i, f"{'+' if i > 0 else ''}{i}", ha='right', va='center', fontsize=6)
    
    # Add vertical dotted lines at specific positions
    for x in positions:
        ax.axvline(x=x, color='lightgray', linestyle=':', alpha=0.2, linewidth=0.5)
    
    # Add segment labels with +/- prefixes - match exact position and style
    pos_segments = ['+H', '+MH', '+M', '+ML', '+L']
    pos_y_positions = [18, 14, 10, 6, 2]
    neg_segments = ['-L', '-ML', '-M', '-MH', '-H']
    neg_y_positions = [-2, -6, -10, -14, -18]
    
    for label, y in zip(pos_segments, pos_y_positions):
        ax.text(-0.75, y, label, ha='right', va='center', fontsize=7, fontweight='bold')
    for label, y in zip(neg_segments, neg_y_positions):
        ax.text(-0.75, y, label, ha='right', va='center', fontsize=7, fontweight='bold')

    # Plot data points and lines - match exact style
    ax.plot(positions, values, 'ko-', linewidth=0.8, markersize=4, markerfacecolor='white', markeredgewidth=0.8)
    ax.plot(positions, values, 'ko', markersize=2, markerfacecolor='black')

    # Set up axis
    ax.set_xticks(positions)
    ax.set_xticklabels(labels, fontsize=9, fontweight='bold')
    ax.set_yticks([])  # Remove y-axis ticks
    
    # Title exactly as in form - match font and spacing
    ax.set_title("Graph 3 CHANGE\nMirror, Perceived Self", pad=10, fontsize=8, fontweight='bold')
    
    # Clean up spines
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(True)
    ax.spines['bottom'].set_visible(True)
    ax.spines['left'].set_linewidth(0.5)
    ax.spines['bottom'].set_linewidth(0.5)
    
    # Add thicker lines at specific intervals (-16, -12, -8, -4, 0, 4, 8, 12, 16)
    highlight_vals = [-16, -12, -8, -4, 4, 8, 12, 16]
    for y in highlight_vals:
        ax.axhline(y=y, color='gray', linestyle='-', alpha=0.3, linewidth=0.8)

    return ax