import random

class Process:
    def __init__(self, process_id):
        self.process_id = process_id
        self.active = True

    def crash(self):
        self.active = False
        print(f"Process {self.process_id} crashed.")

    def activate(self):
        self.active = True
        print(f"Process {self.process_id} activated.")

class RingAlgorithm:
    def __init__(self, num_processes):
        self.processes = [Process(i) for i in range(1, num_processes + 1)]
        self.coordinator = max(p.process_id for p in self.processes)
        print(f"Initial Coordinator is Process {self.coordinator}")
    
    def start_election(self):
        active_processes = [p.process_id for p in self.processes if p.active]
        if active_processes:
            self.coordinator = max(active_processes)
            print(f"New Coordinator is Process {self.coordinator}")
        else:
            print("No active processes remaining.")
    
    def display_coordinator(self):
        print(f"Current Coordinator: Process {self.coordinator}")
    
    def display_active_processes(self):
        active_count = sum(p.active for p in self.processes)
        print(f"Number of active processes: {active_count}")

def main():
    num_processes = 5
    system = RingAlgorithm(num_processes)
    
    while True:
        print("\n1. Crash a Process\n2. Activate a Process\n3. Display Coordinator\n4. Display Active Processes\n5. Exit")
        choice = input("Enter choice: ")
        
        if choice == '1':
            pid = int(input("Enter Process ID to crash: "))
            process = next((p for p in system.processes if p.process_id == pid), None)
            if process:
                process.crash()
                if pid == system.coordinator:
                    print("Coordinator crashed! Starting new election...")
                    system.start_election()
        elif choice == '2':
            pid = int(input("Enter Process ID to activate: "))
            process = next((p for p in system.processes if p.process_id == pid), None)
            if process:
                process.activate()
                system.start_election()
        elif choice == '3':
            system.display_coordinator()
        elif choice == '4':
            system.display_active_processes()
        elif choice == '5':
            print("Exiting...")
            break
        else:
            print("Invalid choice, try again.")

if __name__ == "__main__":
    main()
