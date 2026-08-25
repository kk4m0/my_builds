import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch

# Setup style
plt.style.use('default')
fig, ax = plt.subplots(figsize=(14, 9))

# Define colors
color_inc1 = '#2C5F8A'  # dark blue for increment 1 phase
color_inc1_tasks = '#5B9BD5'  # lighter blue for tasks
color_inc2 = '#ED7D31'  # orange
color_inc3 = '#70AD47'  # green
color_milestone = '#404040'

# Tasks: (label, start_week, duration, y_position, color)
# y positions from top to bottom (higher y = higher on chart)
tasks = [
    # Increment 3 (top if we want chronological bottom to top, but let's put Increment1 at top for readability)
    # We'll order y from 10 down to 0
    ("Increment 3: Medical alerts, daily status & reporting (Weeks 7-9)", 6, 3, 9, color_inc3),
    ("Increment 2: Booking & capacity management (Week 6)", 5, 1, 8, color_inc2),
    ("Increment 1: Staff Access & Pet Record Management (Weeks 1-5) [FR1-FR5]", 0, 5, 7, color_inc1),
    ("T1.7: Testing, Debugging & Integration (W5, 1wk) - All Team [Dep: T1.4,T1.6]", 4, 1, 5.5, '#A5C7E8'),
    ("T1.6: Pet Profile View/Update/Delete FR4 (W4-W5, 1wk) - K.Lekoloane + M.Myeki [Dep: T1.5]", 3.5, 1, 4.5, '#8AB4E0'),
    ("T1.5: Pet Profile Creation & Validation FR3+FR5 (W3-W4, 1.5wk) - K.Seabi + T.Mashifane [Dep: T1.2]", 2, 1.5, 3.5, '#7AA9D6'),
    ("T1.4: Staff Role Management FR2 (W4, 1wk) - T.Mashifane + M.Myeki [Dep: T1.3]", 3.5, 1, 2.5, '#8AB4E0'),
    ("T1.3: Secure Staff Login System FR1 (W2-W4, 1.5wk) - K.Seabi + K.Lekoloane [Dep: T1.2]", 2, 1.5, 1.5, '#7AA9D6'),
    ("T1.2: DB Schema Design (W2, 1wk) - K.Seabi + M.Myeki [Dep: T1.1]", 1, 1, 0.5, '#B9D3EE'),
    ("T1.1: Project Setup & Requirements Analysis (W1, 1wk) - K.Lekoloane (PM) + All", 0, 1, -0.5, '#B9D3EE'),
]

# Plot bars
for label, start, duration, y, color in tasks:
    ax.broken_barh([(start, duration)], (y-0.35, 0.7), facecolors=color, edgecolors='black', linewidth=0.8, alpha=0.9)
    # Add duration text inside bar if enough space
    if duration >= 1:
        ax.text(start + duration/2, y, f"{duration} wk", ha='center', va='center', fontsize=8, color='white', weight='bold')
    
# Add dependencies arrows for Increment 1 tasks
# Define positions for arrows: from end of predecessor to start of successor
# We'll use y positions
deps = [
    # (from_task_index, to_task_index)
    # T1.1 -> T1.2
    (9, 8),
    # T1.2 -> T1.3
    (8, 7),
    # T1.2 -> T1.5
    (8, 5),
    # T1.3 -> T1.4
    (7, 6),
    # T1.5 -> T1.6
    (5, 4),
    # T1.4 -> T1.7 and T1.6 -> T1.7
    (6, 3),
    (4, 3),
]

# Map task index in list to actual y
# tasks list order as defined
for from_idx, to_idx in deps:
    from_task = tasks[from_idx]
    to_task = tasks[to_idx]
    # from: end x = start+duration, y = from_task y
    # to: start x, y = to_task y
    x_start = from_task[1] + from_task[2]
    y_start = from_task[3]
    x_end = to_task[1]
    y_end = to_task[3]
    # Draw arrow with slight curve
    # Use FancyArrowPatch
    arrow = FancyArrowPatch((x_start, y_start), (x_end, y_end),
                            connectionstyle="arc3,rad=0.2",
                            arrowstyle='->', color='#404040', linewidth=1, linestyle='--', alpha=0.7,
                            mutation_scale=10)
    ax.add_patch(arrow)

# Formatting
ax.set_xlim(0, 9)
ax.set_ylim(-1.2, 10)
ax.set_xlabel('Project Timeline (Weeks)', fontsize=12, weight='bold')
ax.set_ylabel('Phases / Tasks', fontsize=12, weight='bold')
ax.set_title('Pet Daycare Management System - Project Gantt Chart\nIncrements 1-3 (Total 9 Weeks)', fontsize=14, weight='bold', pad=20)

# X ticks for weeks
ax.set_xticks(range(0, 10))
ax.set_xticklabels([f'W{i}' if i==0 else f'W{i}\n(Week {i})' for i in range(0,10)], fontsize=9)
ax.grid(axis='x', linestyle='--', alpha=0.5)

# Y ticks
y_labels = [t[0] for t in tasks]
y_pos = [t[3] for t in tasks]
ax.set_yticks(y_pos)
ax.set_yticklabels(y_labels, fontsize=8.5)

# Add vertical lines for week boundaries
for w in range(0, 10):
    ax.axvline(w, color='gray', linestyle=':', alpha=0.3)

# Add legend
legend_patches = [
    mpatches.Patch(color=color_inc1, label='Increment 1 Phase (W1-W5)'),
    mpatches.Patch(color=color_inc1_tasks, label='Increment 1 Tasks (FR1-FR5)'),
    mpatches.Patch(color=color_inc2, label='Increment 2 Phase (W6)'),
    mpatches.Patch(color=color_inc3, label='Increment 3 Phase (W7-W9)'),
]
ax.legend(handles=legend_patches, loc='lower right', fontsize=9, framealpha=0.9)

# Add team info box
team_text = "Team:\nK.Seabi (26302916) - Coding, Debugging, Productivity\nM.Myeki (26303812) - Coding, Testing\nK.Lekoloane (26303956) - PM, Debugging, Testing\nT.Mashifane (26517877) - Testing, HTML"
fig.text(0.02, 0.02, team_text, fontsize=7, bbox=dict(facecolor='lightyellow', alpha=0.8, boxstyle='round'))

plt.tight_layout()
plt.savefig('/home/user/my_builds/gantt_chart.png', dpi=300, bbox_inches='tight')
plt.savefig('/home/user/my_builds/gantt_chart.pdf', bbox_inches='tight')
print("Gantt chart saved to gantt_chart.png and pdf")

# Also create a second simpler overview chart (just 3 increments)
fig2, ax2 = plt.subplots(figsize=(12, 4))
overview = [
    ("Increment 1: Staff Access & Pet Records (Due End of Week 5) - FR1-FR5", 0, 5, 2, color_inc1),
    ("Increment 2: Booking & Capacity Mgmt (Due End of Week 6) - FR6-FR9", 5, 1, 1, color_inc2),
    ("Increment 3: Alerts, Daily Status & Reporting (Due End of Week 9) - FR10-FR12", 6, 3, 0, color_inc3),
]
for label, start, dur, y, col in overview:
    ax2.broken_barh([(start, dur)], (y-0.35, 0.7), facecolors=col, edgecolors='black', linewidth=1)
    ax2.text(start+dur/2, y, f"Weeks {int(start+1)}-{int(start+dur)} | {dur} week{'s' if dur>1 else ''}", ha='center', va='center', color='white', weight='bold', fontsize=10)

ax2.set_xlim(0,9)
ax2.set_ylim(-0.8, 2.8)
ax2.set_xticks(range(0,10))
ax2.set_xticklabels([f'Week {i}' if i>0 else 'Start' for i in range(10)])
ax2.set_yticks([0,1,2])
ax2.set_yticklabels([o[0] for o in overview], fontsize=9)
ax2.set_xlabel('Timeline (Weeks 1-9)')
ax2.set_title('High-Level Phases Overview - Pet Daycare System', weight='bold')
ax2.grid(axis='x', linestyle='--', alpha=0.5)
plt.tight_layout()
plt.savefig('/home/user/my_builds/gantt_overview.png', dpi=300, bbox_inches='tight')
print("Overview saved")
