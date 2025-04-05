import tkinter as tk
from tkinter import messagebox
import math

class Process:
    def __init__(self, process_id):
        self.process_id = process_id
        self.active = True

    def crash(self):
        self.active = False

    def activate(self):
        self.active = True
        
class RingApp:
    def __init__(self, root, system):
        self.root = root
        self.system = system
        self.root.title("Ring Algorithm - Circular View")

        self.canvas = tk.Canvas(self.root, width=400, height=400, bg="white")
        self.canvas.pack()

        self.selection_frame = tk.Frame(self.root)
        self.selection_frame.pack(pady=10)

        self.selected_pid = tk.IntVar()
        self.selected_pid.set(1)

        self.process_menu = tk.OptionMenu(
            self.selection_frame,
            self.selected_pid,
            *[p.process_id for p in self.system.processes]
        )
        self.process_menu.pack(side="left")

        self.crash_btn = tk.Button(self.selection_frame, text="Crash", command=self.crash_selected)
        self.crash_btn.pack(side="left", padx=5)

        self.activate_btn = tk.Button(self.selection_frame, text="Activate", command=self.activate_selected)
        self.activate_btn.pack(side="left", padx=5)

        self.show_coord_btn = tk.Button(self.selection_frame, text="Display Coordinator", command=self.show_coordinator)
        self.show_coord_btn.pack(side="left", padx=5)

        self.show_active_btn = tk.Button(self.selection_frame, text="Active Processes", command=self.show_active_count)
        self.show_active_btn.pack(side="left", padx=5)

        self.exit_btn = tk.Button(self.selection_frame, text="Exit", command=self.root.destroy)
        self.exit_btn.pack(side="left", padx=5)

        self.draw_ring()
        
    def crash_selected(self):
        pid = self.selected_pid.get()
        process = self.system.get_process_by_id(pid)
        if process and process.active:
            process.crash()
            if pid == self.system.coordinator:
                self.system.start_election()
            messagebox.showinfo("Process Crashed", f"Process {pid} crashed.")
            self.draw_ring()
        else:
            messagebox.showwarning("Invalid", f"Process {pid} is already crashed.")

    def activate_selected(self):
        pid = self.selected_pid.get()
        process = self.system.get_process_by_id(pid)
        if process and not process.active:
            process.activate()
            self.system.start_election()
            messagebox.showinfo("Process Activated", f"Process {pid} activated.")
            self.draw_ring()
        else:
            messagebox.showwarning("Invalid", f"Process {pid} is already active.")

class RingAlgorithm:
    def __init__(self, num_processes):
        self.processes = [Process(i) for i in range(1, num_processes + 1)]
        self.coordinator = max(p.process_id for p in self.processes)

    def start_election(self):
        active_ids = [p.process_id for p in self.processes if p.active]
        self.coordinator = max(active_ids) if active_ids else None

    def get_active_processes(self):
        return [p for p in self.processes if p.active]

    def get_process_by_id(self, pid):
        for p in self.processes:
            if p.process_id == pid:
                return p
        return None

# --- GUI with circular layout ---
class RingApp:
    def __init__(self, root, system):
        self.root = root
        self.system = system
        self.root.title("Ring Algorithm - Circular View")

        self.canvas = tk.Canvas(self.root, width=400, height=400, bg="white")
        self.canvas.pack()

        self.status_label = tk.Label(self.root, text="")
        self.status_label.pack(pady=10)

        self.coord_button = tk.Button(self.root, text="Show Coordinator", command=self.show_coordinator)
        self.coord_button.pack(pady=5)

        self.count_button = tk.Button(self.root, text="Show Active Count", command=self.show_active_count)
        self.count_button.pack(pady=5)

        self.draw_ring()

    def draw_ring(self):
        self.canvas.delete("all")
        center_x, center_y = 200, 200
        radius = 120
        angle_gap = 360 / len(self.system.processes)
        self.buttons = []

        for i, process in enumerate(self.system.processes):
            angle_deg = angle_gap * i
            angle_rad = math.radians(angle_deg)
            x = center_x + radius * math.cos(angle_rad)
            y = center_y + radius * math.sin(angle_rad)

            color = "lightgreen" if process.active else "tomato"
            btn = tk.Button(
                self.canvas,
                text=f"P{process.process_id}",
                bg=color,
                command=lambda p=process: self.toggle_process(p)
            )
            # Create a window to place the button at x, y
            self.canvas.create_window(x, y, window=btn)
            self.buttons.append(btn)

    def toggle_process(self, process):
        if process.active:
            process.crash()
            msg = f"Process {process.process_id} crashed."
            if process.process_id == self.system.coordinator:
                msg += " Coordinator crashed. Starting election..."
                self.system.start_election()
        else:
            process.activate()
            msg = f"Process {process.process_id} activated. Starting election..."
            self.system.start_election()

        messagebox.showinfo("Status", msg)
        self.draw_ring()

    def show_coordinator(self):
        if self.system.coordinator:
            messagebox.showinfo("Coordinator", f"Current Coordinator: Process {self.system.coordinator}")
        else:
            messagebox.showwarning("Coordinator", "No active coordinator found!")

    def show_active_count(self):
        count = len(self.system.get_active_processes())
        messagebox.showinfo("Active Processes", f"Number of active processes: {count}")

# --- Main ---
if __name__ == "__main__":
    num_processes = 8  # Adjust as needed
    system = RingAlgorithm(num_processes)

    root = tk.Tk()
    app = RingApp(root, system)
    root.mainloop()
