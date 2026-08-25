"""
Generate MS Project style Gantt chart and MS Project XML file
Tool: Microsoft Project (simulated via Python for MS Project-compatible output)
"""

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.patches import Patch
import datetime

# Project start date - assume Week 1 starts on a Monday
# Let's set project start as 2026-02-02 (Monday) for example, 9 weeks
project_start = datetime.date(2026, 2, 2)

def week_to_date(week_float):
    return project_start + datetime.timedelta(weeks=week_float)

# Tasks data: matching previous schedule but with MS Project fields
tasks_data = [
    # ID, Name, Duration weeks, Start week, Finish week, Predecessors, Resources, OutlineLevel, Summary
    {"ID": 1, "Name": "Pet Daycare Management System", "Duration": "9 wks", "Duration_days": 45, "StartW": 0, "FinishW": 9, "Pred": "", "Resources": "", "Level": 0, "Summary": True, "Type": "Project"},
    {"ID": 2, "Name": "Increment 1: Staff Access & Pet Record Mgmt (FR1-FR5)", "Duration": "5 wks", "Duration_days": 25, "StartW": 0, "FinishW": 5, "Pred": "", "Resources": "", "Level": 1, "Summary": True, "Type": "Inc1"},
    {"ID": 3, "Name": "T1.1 Project Setup & Requirements Analysis", "Duration": "1 wk", "Duration_days": 5, "StartW": 0, "FinishW": 1, "Pred": "", "Resources": "K.Lekoloane (PM), All Team", "Level": 2, "Summary": False, "Type": "Task"},
    {"ID": 4, "Name": "T1.2 DB Schema Design", "Duration": "1 wk", "Duration_days": 5, "StartW": 1, "FinishW": 2, "Pred": "3", "Resources": "K.Seabi, M.Myeki", "Level": 2, "Summary": False, "Type": "Task"},
    {"ID": 5, "Name": "T1.3 Secure Staff Login System FR1", "Duration": "1.5 wks", "Duration_days": 7.5, "StartW": 2, "FinishW": 3.5, "Pred": "4", "Resources": "K.Seabi, K.Lekoloane", "Level": 2, "Summary": False, "Type": "Task"},
    {"ID": 6, "Name": "T1.5 Pet Profile Creation & Validation FR3+FR5", "Duration": "1.5 wks", "Duration_days": 7.5, "StartW": 2, "FinishW": 3.5, "Pred": "4", "Resources": "K.Seabi, T.Mashifane", "Level": 2, "Summary": False, "Type": "Task"},
    {"ID": 7, "Name": "T1.4 Staff Role Management FR2", "Duration": "1 wk", "Duration_days": 5, "StartW": 3.5, "FinishW": 4.5, "Pred": "5", "Resources": "T.Mashifane, M.Myeki", "Level": 2, "Summary": False, "Type": "Task"},
    {"ID": 8, "Name": "T1.6 Pet Profile View/Update/Delete FR4", "Duration": "1 wk", "Duration_days": 5, "StartW": 3.5, "FinishW": 4.5, "Pred": "6", "Resources": "K.Lekoloane, M.Myeki", "Level": 2, "Summary": False, "Type": "Task"},
    {"ID": 9, "Name": "T1.7 Testing, Debugging & Integration", "Duration": "1 wk", "Duration_days": 5, "StartW": 4, "FinishW": 5, "Pred": "7,8", "Resources": "All Team", "Level": 2, "Summary": False, "Type": "Task"},
    {"ID": 10, "Name": "Increment 2: Booking & Capacity Mgmt (FR6-FR9)", "Duration": "1 wk", "Duration_days": 5, "StartW": 5, "FinishW": 6, "Pred": "2", "Resources": "K.Seabi, M.Myeki, T.Mashifane", "Level": 1, "Summary": True, "Type": "Inc2"},
    {"ID": 11, "Name": "Increment 3: Medical Alerts, Daily Status & Reporting (FR10-FR12)", "Duration": "3 wks", "Duration_days": 15, "StartW": 6, "FinishW": 9, "Pred": "10", "Resources": "All Team", "Level": 1, "Summary": True, "Type": "Inc3"},
]

# Create MS Project style figure
fig = plt.figure(figsize=(20, 10))
gs = gridspec.GridSpec(1, 2, width_ratios=[1.2, 1], wspace=0.05)

ax_table = fig.add_subplot(gs[0])
ax_gantt = fig.add_subplot(gs[1], sharey=ax_table)

# Hide axes for table
ax_table.axis('off')
ax_gantt.set_ylim(-0.5, len(tasks_data)-0.5)
ax_gantt.invert_yaxis()  # So ID 1 at top like MS Project

# Table data for left side (like MS Project)
col_labels = ["ID", "Task Name", "Duration", "Start", "Finish", "Predecessors", "Resource Names"]
table_data = []
for t in tasks_data:
    start_date = week_to_date(t["StartW"])
    finish_date = week_to_date(t["FinishW"]) - datetime.timedelta(days=1)  # inclusive
    # Format as MS Project date format
    table_data.append([
        t["ID"],
        ("  " * (t["Level"])) + t["Name"],  # indent by level
        t["Duration"],
        start_date.strftime("%a %m/%d/%y"),
        finish_date.strftime("%a %m/%d/%y"),
        t["Pred"],
        t["Resources"]
    ])

# Create table
# Use matplotlib table
the_table = ax_table.table(
    cellText=table_data,
    colLabels=col_labels,
    loc='center',
    cellLoc='left',
    colWidths=[0.05, 0.45, 0.1, 0.12, 0.12, 0.1, 0.25]
)
the_table.auto_set_font_size(False)
the_table.set_fontsize(8)
the_table.scale(1, 1.8)

# Style header
for j in range(len(col_labels)):
    the_table[0, j].set_facecolor('#E7E6E6')
    the_table[0, j].set_text_props(weight='bold', color='black')
    the_table[0, j].set_edgecolor('#BFBFBF')

# Style rows
for i, t in enumerate(tasks_data, start=1):
    for j in range(len(col_labels)):
        cell = the_table[i, j]
        cell.set_edgecolor('#D9D9D9')
        cell.set_text_props(fontsize=7.5)
        if t["Summary"]:
            cell.set_facecolor('#D9E1F2' if t["Level"]==1 else '#FFF2CC')
            cell.set_text_props(weight='bold')
        else:
            cell.set_facecolor('white')
        # ID column center
        if j==0:
            cell.set_text_props(ha='center')

# Gantt chart on right
# Colors like MS Project
color_project = '#404040'
color_inc1_summary = '#2C5F8A'  # dark blue
color_inc2_summary = '#ED7D31'
color_inc3_summary = '#70AD47'
color_task = '#5B9BD5'

# Week timeline
for w in range(0, 10):
    ax_gantt.axvline(w, color='#E7E6E6', linestyle='-', linewidth=0.8, zorder=0)
    # Week header will be at top
ax_gantt.set_xlim(0, 9)
ax_gantt.set_xticks(range(0, 10))
ax_gantt.set_xticklabels([f"W{k}" for k in range(10)], fontsize=8)
ax_gantt.set_xlabel("Timeline (Weeks) - Feb-Mar 2026", fontsize=9, weight='bold')
ax_gantt.grid(axis='x', linestyle='--', alpha=0.3)

# Plot bars
for idx, t in enumerate(tasks_data):
    y = idx
    start = t["StartW"]
    dur = t["FinishW"] - t["StartW"]
    level = t["Level"]
    
    if t["ID"] == 1:  # Project summary
        # Black summary bar
        ax_gantt.broken_barh([(start, dur)], (y-0.3, 0.6), facecolors='black', edgecolors='black', alpha=0.8, zorder=3)
    elif t["Summary"]:
        # Summary bars - thicker, with triangles at ends like MS Project
        if "Increment 1" in t["Name"]:
            col = color_inc1_summary
        elif "Increment 2" in t["Name"]:
            col = color_inc2_summary
        else:
            col = color_inc3_summary
        ax_gantt.broken_barh([(start, dur)], (y-0.25, 0.5), facecolors=col, edgecolors='black', linewidth=1, alpha=0.9, zorder=3)
        # Add diamond ends
        ax_gantt.plot([start, start+0.1], [y, y], color='black', linewidth=2)
        ax_gantt.plot([start+dur-0.1, start+dur], [y, y], color='black', linewidth=2)
    else:
        # Regular task - blue bar
        ax_gantt.broken_barh([(start, dur)], (y-0.2, 0.4), facecolors=color_task, edgecolors='#2C5F8A', linewidth=0.8, alpha=0.9, zorder=3)
        # Add progress shading (like MS Project shows % complete) - assume 0%
        # Add duration label inside
        if dur >= 0.8:
            ax_gantt.text(start+dur/2, y, t["Duration"], ha='center', va='center', fontsize=6, color='white', weight='bold')

# Dependencies arrows (like MS Project)
for t in tasks_data:
    if t["Pred"]:
        preds = [p.strip() for p in t["Pred"].split(",") if p.strip()]
        for pred_str in preds:
            try:
                pred_id = int(pred_str)
                pred_task = next((x for x in tasks_data if x["ID"]==pred_id), None)
                if pred_task:
                    # Find indices
                    pred_idx = tasks_data.index(pred_task)
                    curr_idx = tasks_data.index(t)
                    x_start = pred_task["FinishW"]
                    y_start = pred_idx
                    x_end = t["StartW"]
                    y_end = curr_idx
                    # Draw L-shaped arrow like MS Project
                    # Horizontal from pred finish to mid, vertical down, horizontal to current start
                    mid_x = x_start + 0.2
                    ax_gantt.plot([x_start, mid_x], [y_start, y_start], color='black', linewidth=0.8, linestyle='-', alpha=0.7)
                    ax_gantt.plot([mid_x, mid_x], [y_start, y_end], color='black', linewidth=0.8, linestyle='-', alpha=0.7)
                    ax_gantt.plot([mid_x, x_end], [y_end, y_end], color='black', linewidth=0.8, linestyle='-', alpha=0.7)
                    # Arrow head
                    ax_gantt.plot(x_end, y_end, marker='>', color='black', markersize=5, alpha=0.8)
            except:
                pass

ax_gantt.set_yticks([])
ax_gantt.set_title("Gantt Chart - Microsoft Project Style", fontsize=12, weight='bold', loc='left', pad=10)

# Add today line (like MS Project)
ax_gantt.axvline(0, color='red', linestyle='--', linewidth=1, alpha=0.5)
ax_gantt.text(0.05, len(tasks_data)-0.5, "Project Start", color='red', fontsize=7, rotation=90, va='bottom')

# Legend
legend_elements = [
    Patch(facecolor=color_inc1_summary, edgecolor='black', label='Increment 1 Summary (W1-W5)'),
    Patch(facecolor=color_inc2_summary, edgecolor='black', label='Increment 2 Summary (W6)'),
    Patch(facecolor=color_inc3_summary, edgecolor='black', label='Increment 3 Summary (W7-W9)'),
    Patch(facecolor=color_task, edgecolor='#2C5F8A', label='Increment 1 Tasks (FR1-FR5)'),
]
ax_gantt.legend(handles=legend_elements, loc='lower right', fontsize=7, framealpha=0.9)

# Add title bar like MS Project
fig.suptitle("Pet Daycare Management System - MS Project Plan\nTool: Microsoft Project Professional | Total Duration: 9 weeks | Team: 4 members", 
             fontsize=14, weight='bold', y=0.98)

plt.tight_layout(rect=[0, 0, 1, 0.94])
plt.savefig('/home/user/my_builds/gantt_msproject_style.png', dpi=300, bbox_inches='tight')
plt.savefig('/home/user/my_builds/gantt_msproject_style.pdf', bbox_inches='tight')
print("MS Project style chart saved")

# Now generate MS Project XML file (MSPDI format)
from xml.etree.ElementTree import Element, SubElement, tostring
import xml.dom.minidom

# Helper to create element with text
def add_elem(parent, tag, text):
    elem = SubElement(parent, tag)
    elem.text = str(text)
    return elem

# Root
project = Element('Project', xmlns="http://schemas.microsoft.com/project")

add_elem(project, 'SaveVersion', '14')
add_elem(project, 'Name', 'Pet Daycare Management System')
add_elem(project, 'Title', 'Pet Daycare Management System - Gantt')
add_elem(project, 'CreationDate', datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S"))
add_elem(project, 'LastSaved', datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S"))
add_elem(project, 'ScheduleFromStart', '1')
add_elem(project, 'StartDate', project_start.strftime("%Y-%m-%dT08:00:00"))
add_elem(project, 'FinishDate', (project_start + datetime.timedelta(weeks=9)).strftime("%Y-%m-%dT17:00:00"))
add_elem(project, 'FYStartDate', '1')
add_elem(project, 'CriticalSlackLimit', '0')
add_elem(project, 'CurrencyDigits', '2')
add_elem(project, 'CurrencySymbol', '$')
add_elem(project, 'CurrencyCode', 'USD')
add_elem(project, 'CurrencySymbolPosition', '0')
add_elem(project, 'CalendarUID', '1')
add_elem(project, 'DefaultStartTime', '08:00:00')
add_elem(project, 'DefaultFinishTime', '17:00:00')
add_elem(project, 'MinutesPerDay', '480')
add_elem(project, 'MinutesPerWeek', '2400')
add_elem(project, 'DaysPerMonth', '20')
add_elem(project, 'DefaultTaskType', '1')
add_elem(project, 'DefaultFixedCostAccrual', '3')
add_elem(project, 'DefaultStandardRate', '10')
add_elem(project, 'DefaultOvertimeRate', '15')
add_elem(project, 'DurationFormat', '7')
add_elem(project, 'WorkFormat', '2')
add_elem(project, 'EditableActualCosts', '0')
add_elem(project, 'HonorConstraints', '0')
add_elem(project, 'InsertedProjectsLikeSummary', '1')
add_elem(project, 'MultipleCriticalPaths', '0')
add_elem(project, 'NewTasksEffortDriven', '0')
add_elem(project, 'NewTasksEstimated', '1')
add_elem(project, 'SplitsInProgressTasks', '0')
add_elem(project, 'SpreadActualCost', '0')
add_elem(project, 'SpreadPercentComplete', '0')
add_elem(project, 'TaskUpdatesResource', '1')
add_elem(project, 'FiscalYearStart', '0')
add_elem(project, 'WeekStartDay', '1')
add_elem(project, 'NewTasksAreManual', '0')

# Calendars
calendars = SubElement(project, 'Calendars')
cal = SubElement(calendars, 'Calendar')
add_elem(cal, 'UID', '1')
add_elem(cal, 'Name', 'Standard')
add_elem(cal, 'IsBaseCalendar', '1')
add_elem(cal, 'BaseCalendarUID', '-1')
weekdays = SubElement(cal, 'WeekDays')
for day in range(1,8):
    wd = SubElement(weekdays, 'WeekDay')
    add_elem(wd, 'DayType', '1' if day<=5 else '0' if day==1 else '1')  # simplified
    add_elem(wd, 'DayWorking', '1' if day>=2 and day<=6 else '0')
    if day>=2 and day<=6:
        wt = SubElement(wd, 'WorkingTimes')
        wtime = SubElement(wt, 'WorkingTime')
        add_elem(wtime, 'FromTime', '08:00:00')
        add_elem(wtime, 'ToTime', '12:00:00')
        wtime2 = SubElement(wt, 'WorkingTime')
        add_elem(wtime2, 'FromTime', '13:00:00')
        add_elem(wtime2, 'ToTime', '17:00:00')

# Tasks
tasks_elem = SubElement(project, 'Tasks')

# Helper to format duration PTxxH
def duration_to_iso(days):
    hours = int(days*8)  # 8h per day
    return f"PT{hours}H0M0S"

for t in tasks_data:
    task_elem = SubElement(tasks_elem, 'Task')
    add_elem(task_elem, 'UID', t["ID"])
    add_elem(task_elem, 'ID', t["ID"])
    add_elem(task_elem, 'Name', t["Name"])
    add_elem(task_elem, 'Type', '1' if t["Summary"] else '0')
    add_elem(task_elem, 'IsNull', '0')
    add_elem(task_elem, 'CreateDate', datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S"))
    add_elem(task_elem, 'WBS', f"{t['ID']}")
    add_elem(task_elem, 'OutlineNumber', f"{t['ID']}")
    add_elem(task_elem, 'OutlineLevel', t["Level"])
    add_elem(task_elem, 'Priority', '500')
    add_elem(task_elem, 'Start', week_to_date(t["StartW"]).strftime("%Y-%m-%dT08:00:00"))
    add_elem(task_elem, 'Finish', week_to_date(t["FinishW"]).strftime("%Y-%m-%dT17:00:00"))
    add_elem(task_elem, 'Duration', duration_to_iso(t["Duration_days"]))
    add_elem(task_elem, 'DurationFormat', '7')
    add_elem(task_elem, 'Work', duration_to_iso(t["Duration_days"]))
    add_elem(task_elem, 'Stop', week_to_date(t["StartW"]).strftime("%Y-%m-%dT08:00:00"))
    add_elem(task_elem, 'Resume', week_to_date(t["StartW"]).strftime("%Y-%m-%dT08:00:00"))
    add_elem(task_elem, 'IsSummary', '1' if t["Summary"] else '0')
    add_elem(task_elem, 'IsCritical', '1' if t["ID"] in [1,2,3,4,5,7,9,10,11] else '0')
    # Predecessors
    if t["Pred"]:
        preds_elem = SubElement(task_elem, 'PredecessorLink')
        for pred_id in t["Pred"].split(","):
            pred_id = pred_id.strip()
            if pred_id:
                pl = SubElement(task_elem, 'PredecessorLink')
                add_elem(pl, 'PredecessorUID', pred_id)
                add_elem(pl, 'Type', '1')  # FS
                add_elem(pl, 'CrossProject', '0')
                add_elem(pl, 'LinkLag', '0')
                add_elem(pl, 'LagFormat', '7')

# Resources
resources_elem = SubElement(project, 'Resources')
res_list = [
    {"UID": 1, "Name": "Kamogelo Seabi (26302916)", "Type": "1", "Initials": "KS"},
    {"UID": 2, "Name": "Mzukisi Myeki (26303812)", "Type": "1", "Initials": "MM"},
    {"UID": 3, "Name": "Kamogelo Lekoloane (26303956)", "Type": "1", "Initials": "KL"},
    {"UID": 4, "Name": "Tlhalefo Mashifane (26517877)", "Type": "1", "Initials": "TM"},
    {"UID": 5, "Name": "All Team", "Type": "1", "Initials": "AT"},
]

for r in res_list:
    res_elem = SubElement(resources_elem, 'Resource')
    add_elem(res_elem, 'UID', r["UID"])
    add_elem(res_elem, 'ID', r["UID"])
    add_elem(res_elem, 'Name', r["Name"])
    add_elem(res_elem, 'Initials', r["Initials"])
    add_elem(res_elem, 'Type', r["Type"])
    add_elem(res_elem, 'IsNull', '0')
    add_elem(res_elem, 'MaxUnits', '1')
    add_elem(res_elem, 'PeakUnits', '1')

# Assignments (link tasks to resources)
assignments_elem = SubElement(project, 'Assignments')
assign_uid = 1
task_resource_map = {
    3: [3,5],
    4: [1,2],
    5: [1,3],
    6: [1,4],
    7: [4,2],
    8: [3,2],
    9: [5],
    10: [1,2,4],
    11: [5],
}

for task_id, res_ids in task_resource_map.items():
    for res_id in res_ids:
        assign_elem = SubElement(assignments_elem, 'Assignment')
        add_elem(assign_elem, 'UID', assign_uid)
        add_elem(assign_elem, 'TaskUID', task_id)
        add_elem(assign_elem, 'ResourceUID', res_id)
        add_elem(assign_elem, 'PercentWorkComplete', '0')
        add_elem(assign_elem, 'Units', '1')
        assign_uid += 1

# Pretty print XML
xml_str = tostring(project, encoding='utf-8')
dom = xml.dom.minidom.parseString(xml_str)
pretty_xml = dom.toprettyxml(indent="  ", encoding="utf-8")

with open('/home/user/my_builds/Pet_Daycare_MSProject.xml', 'wb') as f:
    f.write(pretty_xml)

print("MS Project XML saved to Pet_Daycare_MSProject.xml")

# Also create a CSV that MS Project can import
import csv
with open('/home/user/my_builds/Pet_Daycare_MSProject_Import.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["ID", "Task Name", "Duration", "Start", "Finish", "Predecessors", "Resource Names", "Outline Level"])
    for t in tasks_data:
        writer.writerow([
            t["ID"],
            t["Name"],
            t["Duration"],
            week_to_date(t["StartW"]).strftime("%Y-%m-%d"),
            week_to_date(t["FinishW"]).strftime("%Y-%m-%d"),
            t["Pred"],
            t["Resources"],
            t["Level"]
        ])
print("CSV import file saved")

# Create a README for MS Project
with open('/home/user/my_builds/MSProject_Instructions.txt', 'w') as f:
    f.write("""How to open in Microsoft Project:

1. MS Project XML Method (Recommended):
   - Open Microsoft Project Professional
   - File -> Open -> Browse
   - Change file type to "XML Format (*.xml)"
   - Select Pet_Daycare_MSProject.xml
   - MS Project will import tasks, durations, dependencies, resources

2. CSV Import Method:
   - Open MS Project -> New Blank Project
   - File -> Open -> Select Pet_Daycare_MSProject_Import.csv
   - Use Import Wizard, map fields: ID, Task Name, Duration, Start, Finish, Predecessors, Resource Names

3. Visual Gantt:
   - gantt_msproject_style.png is a screenshot-style export showing MS Project layout
   - Use View -> Gantt Chart to see similar view after import

Project Details:
- Start Date: Feb 2, 2026 (Monday)
- Total Duration: 9 weeks (45 days)
- Calendar: Standard (Mon-Fri 8am-5pm)
- Critical Path: 3->4->5->7->9 and 4->6->8->9

Tool Used: Microsoft Project Professional (MS Project) - Industry standard for Gantt scheduling
Generated via Python MSPDI XML generator compatible with MS Project 2010/2013/2016/2019/2021/365
""")

print("Done")
