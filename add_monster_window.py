import tkinter as tk
import customtkinter
from statblock_scraper import get_statblock
import asyncio

class MonsterWindow(customtkinter.CTk):
    def __init__(self, parent, callback):
        super().__init__()
        self.title("Add Monster")

        self.monster_frame = customtkinter.CTkFrame(self, width=400, height=200, corner_radius=0)
        self.monster_frame.grid(row=0, column=0, sticky="nsew", padx=30, pady=10)

        self.monster_name_entry = customtkinter.CTkEntry(self.monster_frame, placeholder_text="Monster Name" )
        self.monster_name_entry.grid(row=1, column=0, sticky="nsew", padx=30, pady=10)
        self.monster_name_entry.bind("<KeyRelease>", self.show_import_button)

        # Import button (initially hidden)
        self.import_button = customtkinter.CTkButton(self.monster_frame, text="Import Monster",
                                                     command=self.import_monster)
        self.import_button.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)
        self.import_button.grid_remove()  # Initially hide the button

        self.initiative_modifier_entry = customtkinter.CTkEntry(self.monster_frame, placeholder_text="Initiative")
        self.initiative_modifier_entry.grid(row=2, column=0, sticky="nsew", padx=30, pady=10)

        self.num_monsters_entry = customtkinter.CTkEntry(self.monster_frame, placeholder_text="How many?", )
        self.num_monsters_entry.grid(row=3, column=0, sticky="nsew", padx=30, pady=10)

        self.average_health_entry = customtkinter.CTkEntry(self.monster_frame, placeholder_text="Average Health", )
        self.average_health_entry.grid(row=4, column=0, sticky="nsew", padx=30, pady=10)

        self.armor_class_entry = customtkinter.CTkEntry(self.monster_frame, placeholder_text="Armor Class",
                                                        )
        self.armor_class_entry.grid(row=5, column=0, sticky="nsew", padx=30, pady=10)

        self.speed_entry = customtkinter.CTkEntry(self.monster_frame, placeholder_text="Speed")
        self.speed_entry.grid(row=6, column=0, sticky="nsew", padx=30, pady=10)

        self.monstertyp_auswahl_frame = customtkinter.CTkFrame(self)
        self.monstertyp_auswahl_frame.grid(row=0, column=1, sticky="nsew", padx=30, pady=10)
        self.type_var = tk.StringVar()

        self.monstertyp_auswahl_frame_label = customtkinter.CTkLabel(master=self.monstertyp_auswahl_frame,
                                                                     text="Choose the monster type:")
        self.monstertyp_auswahl_frame_label.grid(row=0, column=0, sticky="nsew", padx=30, pady=10)

        self.humanoid_button = customtkinter.CTkRadioButton(master=self.monstertyp_auswahl_frame, text="Humanoid",
                                                            variable=self.type_var, value="Humanoid")
        self.humanoid_button.grid(row=1, column=0, sticky="nsew", padx=30, pady=10)
        self.tier_button = customtkinter.CTkRadioButton(master=self.monstertyp_auswahl_frame, text="Tier",
                                                        variable=self.type_var, value="Tier")
        self.tier_button.grid(row=2, column=0, sticky="nsew", padx=30, pady=10)
        self.untot_button = customtkinter.CTkRadioButton(master=self.monstertyp_auswahl_frame, text="Untot",
                                                         variable=self.type_var, value="Untot")
        self.untot_button.grid(row=3, column=0, sticky="nsew", padx=30, pady=10)
        self.maschine_button = customtkinter.CTkRadioButton(master=self.monstertyp_auswahl_frame, text="Maschine",
                                                            variable=self.type_var, value="Maschine")
        self.maschine_button.grid(row=4, column=0, sticky="nsew", padx=30, pady=10)
        self.schleim_button = customtkinter.CTkRadioButton(master=self.monstertyp_auswahl_frame, text="Schleim",
                                                           variable=self.type_var, value="Schleim")
        self.schleim_button.grid(row=5, column=0, sticky="nsew", padx=30, pady=10)
        self.celestial_button = customtkinter.CTkRadioButton(master=self.monstertyp_auswahl_frame, text="Celestial",
                                                             variable=self.type_var, value="Celestial")
        self.celestial_button.grid(row=6, column=0, sticky="nsew", padx=30, pady=10)
        self.drache_button = customtkinter.CTkRadioButton(master=self.monstertyp_auswahl_frame, text="Drache",
                                                          variable=self.type_var, value="Drache")
        self.drache_button.grid(row=7, column=0, sticky="nsew", padx=30, pady=10)
        self.element_button = customtkinter.CTkRadioButton(master=self.monstertyp_auswahl_frame, text="Elementar",
                                                           variable=self.type_var, value="Elementar")
        self.element_button.grid(row=8, column=0, sticky="nsew", padx=30, pady=10)

        # create Submit button frame
        self.submit_button_frame = customtkinter.CTkFrame(self)
        self.submit_button_frame.grid(row=1, column=0, sticky="nsew", padx=30, pady=10, columnspan=3)
        self.submit_button_frame.grid_rowconfigure(2, weight=1)
        self.submit_button = customtkinter.CTkButton(master=self.submit_button_frame, text="Submit",
                                                     command=self.submit)
        self.submit_button.grid(row=0, column=0, padx=30, pady=10)


        # TODO: rausfinden wie man in einer FUnktion variablen generierne, die in self zur Verfügung stehen, EIngabefeld für Spieler mit Typ und default = HUmanoid,

        self.callback = callback

    """this method defines the behaviour of the submit button which is used in the MonsterWIndow class. It reads out the values in the EntryWidgets, the radiobutton which was ticked and passes the values to the add_monster Method"""

    def show_import_button(self, *args):
        # Get the current text from the monster name entry
        monster_name = self.monster_name_entry.get()

        # Show the Import button only if the monster name entry is not empty
        if monster_name:
            self.import_button.grid()  # Make the button visible
            self.import_button.configure(text=f"Import {monster_name}")  # Update button text
        else:
            self.import_button.grid_remove()  # Hide the button if the entry is cleared
            self.import_button.configure(text="Import Monster")  # Reset button text

    def import_monster(self):
        monster_name = self.monster_name_entry.get()
        monster_statblock = asyncio.run(get_statblock(monster_name))
        print(monster_statblock)
        if monster_statblock:
            dex_score_string = monster_statblock['ability_scores']['DEX']
            dex_modifier = dex_score_string.split('(')[-1].strip(')')

            self.initiative_modifier_entry.delete(0, tk.END)
            self.initiative_modifier_entry.insert(0, dex_modifier)

            hit_points = monster_statblock['important_info']['Hit Points']
            average_health = hit_points.split('(')[-1].strip(')')

            self.average_health_entry.delete(0, tk.END)
            self.average_health_entry.insert(0, average_health)

            # Set armor class and speed
            armor_class = monster_statblock['important_info']['Armor Class']
            speed = monster_statblock['important_info']['Speed']

            self.armor_class_entry.delete(0, tk.END)
            self.armor_class_entry.insert(0, armor_class)

            self.speed_entry.delete(0, tk.END)
            self.speed_entry.insert(0, speed)

            # Update creature name and type if needed...
            # (omitted for brevity)

            print(f"Importing monster: {monster_name}, this is the statblock: {monster_statblock}")
        else:
            print(f"Failed to import monster: {monster_name}")

    def submit(self):
        monster_name = self.monster_name_entry.get()
        initiative_modifier = int(self.initiative_modifier_entry.get())
        num_monsters = int(self.num_monsters_entry.get())
        average_health = self.average_health_entry.get()
        monster_type = self.type_var.get()

        self.callback(monster_name, initiative_modifier, num_monsters, average_health, monster_type)
        self.destroy()