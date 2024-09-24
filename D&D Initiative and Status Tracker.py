import tkinter as tk
import random
import customtkinter

from add_monster_window import MonsterWindow
from utils.file_import import read_data_file
from get_status_string import get_random_status_string
from utils.health_status_helpers import delayed_check_health_status, get_status_string_and_color, get_health_status_color_indicator
from utils.calculate_health import calculate_health
from status_window import open_status_window

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"
customtkinter.set_widget_scaling(.9)

class InitiativeTracker(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("D&D Initiative Tracker")
        self.geometry(f"{1400}x{1000}")

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=5, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(5, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Add Monsters or Players", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.add_monster_button = customtkinter.CTkButton(self.sidebar_frame, text="Add Monsters",
                                                          command=self.open_monster_window, text_color="black", fg_color="red")
        self.add_monster_button.grid(row=1, column=0, padx=20, pady=10)
        self.add_player_button = customtkinter.CTkButton(self.sidebar_frame, text="Add Player", command=self.add_player)
        self.add_player_button.grid(row=2, column=0, padx=20, pady=10)

        # setup and hide the main frame for later use
        self.main_frame = customtkinter.CTkScrollableFrame(self, width=140, corner_radius=0)
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=30, pady=20)
        self.main_frame.grid_rowconfigure(5, weight=1)
        self.main_frame.grid_forget()

        # defining the input variables for the players
        self.participant_name_entry = customtkinter.CTkEntry(self.sidebar_frame, placeholder_text="Player Name")
        self.participant_name_entry.grid(row=3, column=0, padx=20, pady=10)

        self.participant_initiative_entry = customtkinter.CTkEntry(self.sidebar_frame, placeholder_text="Player Initiative")
        self.participant_initiative_entry.grid(row=4, column=0, padx=20, pady=10)

        self.participant_health_entry = customtkinter.CTkEntry(self.sidebar_frame, placeholder_text="Player Health")
        self.participant_health_entry.grid(row=5, column=0, padx=20, pady=10, sticky="n")

        # Creating the appearance mode widget
        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=6, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 10))

        # creating the Scaling widget
        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=9, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"],
                                                               command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=10, column=0, padx=20, pady=(10, 20))

        # set default values for Scaling and Appearance
        self.appearance_mode_optionemenu.set("Dark")
        self.scaling_optionemenu.set("100%")

        # Initializing the required dictionaries
        self.initial_values = {}  # dictionary with the following strucutre: {"name": (initiative, maximum_health, monster_type)}
        self.status_lists = {}
        self.current_health = {}
        self.passive_perception_list = []

        self.status_labels = {}  # Store references to status labels

    def add_player(self):
        participant = self.participant_name_entry.get()
        initiative = int(self.participant_initiative_entry.get())
        health = int(self.participant_health_entry.get())
        type = "humanoid"

        # Update or add participant in the initial_values dictionary
        self.initial_values[participant] = {
            "initiative": initiative,
            "health": health,
            "type": type
        }
        self.current_health[participant] = health

        # Sort the dictionary by initiative and convert back to a sorted list
        sorted_initial_values = sorted(self.initial_values.items(), key=lambda x: x[1][0], reverse=True)

        self.main_frame.destroy()
        self.update_initiative_text(sorted_initial_values)

    def update_initiative_text(self, sorted_initial_values):
        self.main_frame = customtkinter.CTkScrollableFrame(self, width=1000, height=1000, corner_radius=0)
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=30, pady=20, rowspan=5)
        self.main_frame.grid_rowconfigure(5, weight=1)
        customtkinter.CTkLabel(master=self.main_frame, text="Participant").grid(column=1, row=0, sticky="w", padx=5,
                                                                                pady=5)
        customtkinter.CTkLabel(master=self.main_frame, text="Initiative").grid(column=2, row=0, padx=5, pady=5)
        customtkinter.CTkLabel(master=self.main_frame, text="Health").grid(column=3, row=0, padx=5, pady=5)
        customtkinter.CTkLabel(master=self.main_frame, text="Health Status").grid(column=4, row=0, padx=5, pady=5)
        customtkinter.CTkLabel(master=self.main_frame, text="Delete Button").grid(column=5, row=0, padx=5, pady=5)

        row_count = 1
        for participant, attributes in sorted_initial_values:
            row_count += 1
            initiative = attributes["initiative"]
            health = attributes["health"]
            monster_type = attributes["type"]
            customtkinter.CTkLabel(master=self.main_frame, text=participant).grid(column=1, row=row_count, sticky="w",
                                                                                  padx=5, pady=5)
            customtkinter.CTkLabel(master=self.main_frame, text=initiative).grid(column=2, row=row_count, padx=5,
                                                                                 pady=5)

            # Health entry widget
            health_entry = tk.StringVar()
            health_entry_widget = customtkinter.CTkEntry(master=self.main_frame, textvariable=health_entry, width=50)
            if participant in self.current_health:
                health_entry_widget.insert(0, str(self.current_health[participant]))
            else:
                health_entry_widget.insert(0, str(health))
            health_entry_widget.grid(column=3, row=row_count, padx=5, pady=5)

            # Status label reference
            status_label = customtkinter.CTkButton(
                master=self.main_frame,
                text="HP Indicator",
                command=lambda p=participant: open_status_window(p, self.current_health, self.initial_values,
                                                                 self.status_lists)
            )
            status_label.grid(column=4, row=row_count, sticky="w", padx=5, pady=5)

            # Set initial color
            status_color = get_health_status_color_indicator(
                self.current_health.get(participant, health),
                health
            )
            status_label.configure(fg_color=status_color)

            # Attach callback for health_entry change
            health_entry.trace_add(
                mode="write",
                callback=lambda mode, name, index, p=participant, he=health_entry, sl=status_label: (
                    delayed_check_health_status(self, p, he, self.current_health, sl, self.initial_values))
            )

            # Create Delete Button
            customtkinter.CTkButton(self.main_frame, text="Delete this row", width=60,
                                    command=lambda p=participant: self.delete_entry(p)).grid(column=5, row=row_count,
                                                                                             padx=5, pady=5)



    def delete_entry(self, participant):
        if participant in self.initial_values:
            del self.initial_values[participant]
        if participant in self.current_health:
            del self.current_health[participant]
        sorted_initial_values = sorted(self.initial_values.items(), key=lambda x: x[1]["initiative"], reverse=True)
        self.update_initiative_text(sorted_initial_values)

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def open_monster_window(self):
        monster_window = MonsterWindow(self, self.add_monster)
        monster_window.mainloop()

    def add_monster(self, monster_name, initiative_modifier, num_monsters, average_health, monster_type, armor_class=None,
                    speed=None, resistances=None,
                    damage_immunities=None, damage_vulnerabilities=None,
                    condition_immunities=None):
        for i in range(1, num_monsters + 1):
            monster = f"{monster_name}{i}"
            health = calculate_health(average_health)
            initiative = random.randint(1, 20) + initiative_modifier

            # Using a dictionary to store monster attributes
            monster_attributes = {
                "initiative": initiative,
                "health": health,
                "type": monster_type,
                "armor_class": armor_class,
                "speed": speed,
                "resistances": resistances,
                "damage_immunities": damage_immunities,
                "damage_vulnerabilities": damage_vulnerabilities,
                "condition_immunities": condition_immunities
            }

            self.initial_values[monster] = monster_attributes
            print(self.initial_values[monster])
            self.current_health[monster] = health

        if self.status_lists.get(monster_type.lower()) is None:
            read_data_file(monster_type, self.status_lists)

        sorted_initial_values = sorted(self.initial_values.items(), key=lambda x: x[1]["initiative"], reverse=True)
        self.update_initiative_text(sorted_initial_values)

if __name__ == "__main__":
    app = InitiativeTracker()
    app.after(0, lambda: app.state('zoomed'))
    app.mainloop()
