import tkinter as tk
import customtkinter
from statblock_scraper import get_statblock
import asyncio


class MonsterWindow(customtkinter.CTk):
    def __init__(self, parent, callback):
        super().__init__()
        self.skills = {}
        self.title("Add Monster")

        self.monster_frame = customtkinter.CTkFrame(
            self, width=400, height=200, corner_radius=0
        )
        self.monster_frame.grid(row=0, column=0, sticky="nsew", padx=30, pady=10)

        self.monster_name_entry = customtkinter.CTkEntry(
            self.monster_frame, placeholder_text="Monster Name"
        )
        self.monster_name_entry.grid(row=1, column=0, sticky="nsew", padx=30, pady=10)
        self.monster_name_entry.bind("<KeyRelease>", self.show_import_button)
        self.monster_name_entry.bind("<Return>", self.on_enter)
        self.after(100, self.monster_name_entry.focus_force)

        # Import button (initially hidden)
        self.import_button = customtkinter.CTkButton(
            self.monster_frame, text="Import Monster", command=self.import_monster
        )
        self.import_button.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)
        self.import_button.grid_remove()  # Initially hide the button

        self.initiative_modifier_entry = customtkinter.CTkEntry(
            self.monster_frame, placeholder_text="Initiative"
        )
        self.initiative_modifier_entry.grid(
            row=2, column=0, sticky="nsew", padx=30, pady=10
        )

        self.num_monsters_entry = customtkinter.CTkEntry(
            self.monster_frame,
            placeholder_text="How many?",
        )
        self.num_monsters_entry.grid(row=3, column=0, sticky="nsew", padx=30, pady=10)
        self.num_monsters_entry.bind("<Return>", self.on_enter_with_filled_form)

        self.average_health_entry = customtkinter.CTkEntry(
            self.monster_frame,
            placeholder_text="Average Health",
        )
        self.average_health_entry.grid(row=4, column=0, sticky="nsew", padx=30, pady=10)

        self.armor_class_entry = customtkinter.CTkEntry(
            self.monster_frame,
            placeholder_text="Armor Class",
        )
        self.armor_class_entry.grid(row=5, column=0, sticky="nsew", padx=30, pady=10)

        self.speed_entry = customtkinter.CTkEntry(
            self.monster_frame, placeholder_text="Speed"
        )
        self.speed_entry.grid(row=6, column=0, sticky="nsew", padx=30, pady=10)

        self.resistances_entry = customtkinter.CTkEntry(
            self.monster_frame, placeholder_text="Resistances"
        )
        self.resistances_entry.grid(row=7, column=0, sticky="nsew", padx=30, pady=10)

        self.damage_immunities_entry = customtkinter.CTkEntry(
            self.monster_frame, placeholder_text="Damage Immunities"
        )
        self.damage_immunities_entry.grid(
            row=8, column=0, sticky="nsew", padx=30, pady=10
        )

        self.damage_vulnerabilities_entry = customtkinter.CTkEntry(
            self.monster_frame, placeholder_text="Damage Vulnerabilities"
        )
        self.damage_vulnerabilities_entry.grid(
            row=9, column=0, sticky="nsew", padx=30, pady=10
        )

        self.condition_immunities_entry = customtkinter.CTkEntry(
            self.monster_frame, placeholder_text="Condition Immunities"
        )
        self.condition_immunities_entry.grid(
            row=10, column=0, sticky="nsew", padx=30, pady=10
        )

        self.monstertyp_auswahl_frame = customtkinter.CTkFrame(self)
        self.monstertyp_auswahl_frame.grid(
            row=0, column=1, sticky="nsew", padx=30, pady=10
        )
        self.type_var = tk.StringVar()

        self.monstertyp_auswahl_frame_label = customtkinter.CTkLabel(
            master=self.monstertyp_auswahl_frame, text="Choose the monster type:"
        )
        self.monstertyp_auswahl_frame_label.grid(
            row=0, column=0, sticky="nsew", padx=30, pady=10
        )

        self.humanoid_button = customtkinter.CTkRadioButton(
            master=self.monstertyp_auswahl_frame,
            text="Humanoid",
            variable=self.type_var,
            value="humanoid",
        )
        self.humanoid_button.grid(row=1, column=0, sticky="nsew", padx=30, pady=10)

        self.tier_button = customtkinter.CTkRadioButton(
            master=self.monstertyp_auswahl_frame,
            text="Tier",
            variable=self.type_var,
            value="beast",
        )
        self.tier_button.grid(row=2, column=0, sticky="nsew", padx=30, pady=10)

        self.untot_button = customtkinter.CTkRadioButton(
            master=self.monstertyp_auswahl_frame,
            text="Untot",
            variable=self.type_var,
            value="undead",
        )
        self.untot_button.grid(row=3, column=0, sticky="nsew", padx=30, pady=10)

        self.maschine_button = customtkinter.CTkRadioButton(
            master=self.monstertyp_auswahl_frame,
            text="Maschine",
            variable=self.type_var,
            value="construct",
        )
        self.maschine_button.grid(row=4, column=0, sticky="nsew", padx=30, pady=10)

        self.schleim_button = customtkinter.CTkRadioButton(
            master=self.monstertyp_auswahl_frame,
            text="Schleim",
            variable=self.type_var,
            value="ooze",
        )
        self.schleim_button.grid(row=5, column=0, sticky="nsew", padx=30, pady=10)

        self.celestial_button = customtkinter.CTkRadioButton(
            master=self.monstertyp_auswahl_frame,
            text="Celestial",
            variable=self.type_var,
            value="celestial",
        )
        self.celestial_button.grid(row=6, column=0, sticky="nsew", padx=30, pady=10)

        self.drache_button = customtkinter.CTkRadioButton(
            master=self.monstertyp_auswahl_frame,
            text="Drache",
            variable=self.type_var,
            value="dragon",
        )
        self.drache_button.grid(row=7, column=0, sticky="nsew", padx=30, pady=10)

        self.element_button = customtkinter.CTkRadioButton(
            master=self.monstertyp_auswahl_frame,
            text="Elementar",
            variable=self.type_var,
            value="elemental",
        )
        self.element_button.grid(row=8, column=0, sticky="nsew", padx=30, pady=10)

        self.aberration_button = customtkinter.CTkRadioButton(
            master=self.monstertyp_auswahl_frame,
            text="Aberration",
            variable=self.type_var,
            value="aberration",
        )
        self.aberration_button.grid(row=9, column=0, sticky="nsew", padx=30, pady=10)

        self.fey_button = customtkinter.CTkRadioButton(
            master=self.monstertyp_auswahl_frame,
            text="Fee",
            variable=self.type_var,
            value="fey",
        )
        self.fey_button.grid(row=10, column=0, sticky="nsew", padx=30, pady=10)

        self.fiend_button = customtkinter.CTkRadioButton(
            master=self.monstertyp_auswahl_frame,
            text="Fiend",
            variable=self.type_var,
            value="fiend",
        )
        self.fiend_button.grid(row=1, column=1, sticky="nsew", padx=30, pady=10)

        self.giant_button = customtkinter.CTkRadioButton(
            master=self.monstertyp_auswahl_frame,
            text="Riese",
            variable=self.type_var,
            value="giant",
        )
        self.giant_button.grid(row=2, column=1, sticky="nsew", padx=30, pady=10)

        self.monstrosity_button = customtkinter.CTkRadioButton(
            master=self.monstertyp_auswahl_frame,
            text="Monstrosität",
            variable=self.type_var,
            value="monstrosity",
        )
        self.monstrosity_button.grid(row=3, column=1, sticky="nsew", padx=30, pady=10)

        self.plant_button = customtkinter.CTkRadioButton(
            master=self.monstertyp_auswahl_frame,
            text="Pflanze",
            variable=self.type_var,
            value="plant",
        )
        self.plant_button.grid(row=4, column=1, sticky="nsew", padx=30, pady=10)
        # create Submit button frame
        self.submit_button_frame = customtkinter.CTkFrame(self)
        self.submit_button_frame.grid(
            row=1, column=0, sticky="nsew", padx=30, pady=10, columnspan=3
        )
        self.submit_button_frame.grid_rowconfigure(2, weight=1)
        self.submit_button = customtkinter.CTkButton(
            master=self.submit_button_frame, text="Submit", command=self.submit
        )
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
            self.import_button.configure(
                text=f"Import {monster_name}"
            )  # Update button text
        else:
            self.import_button.grid_remove()  # Hide the button if the entry is cleared
            self.import_button.configure(text="Import Monster")  # Reset button text

    def import_monster(self):
        monster_name = self.monster_name_entry.get()
        monster_statblock = asyncio.run(get_statblock(monster_name))
        print(monster_statblock)
        possible_types = [
            "aberration",
            "humanoid",
            "beast",
            "undead",
            "construct",
            "ooze",
            "celestial",
            "dragon",
            "elemental",
            "fey",
            "fiend",
            "giant",
            "monstrosity",
            "plant",
        ]

        if monster_statblock:
            dex_score_string = monster_statblock.get("ability_scores", {}).get(
                "DEX", "0 (0)"
            )
            dex_modifier = dex_score_string.split("(")[-1].strip(")")

            self.initiative_modifier_entry.delete(0, tk.END)
            self.initiative_modifier_entry.insert(0, dex_modifier)

            hit_points = monster_statblock.get("important_info", {}).get(
                "Hit Points", "0 (0)"
            )
            average_health = hit_points.split("(")[-1].strip(")")

            self.average_health_entry.delete(0, tk.END)
            self.average_health_entry.insert(0, average_health)

            armor_class = monster_statblock.get("important_info", {}).get(
                "Armor Class", "0"
            )
            speed = monster_statblock.get("important_info", {}).get("Speed", "0")
            self.armor_class_entry.delete(0, tk.END)
            self.armor_class_entry.insert(0, armor_class)
            self.speed_entry.delete(0, tk.END)
            self.speed_entry.insert(0, speed)

            # Set new fields with default values for None
            self.resistances_entry.delete(0, tk.END)
            self.resistances_entry.insert(
                0,
                monster_statblock.get("important_info", {}).get(
                    "Damage Resistances", "None"
                ),
            )

            self.damage_immunities_entry.delete(0, tk.END)
            self.damage_immunities_entry.insert(
                0,
                monster_statblock.get("important_info", {}).get(
                    "Damage Immunities", "None"
                ),
            )

            self.damage_vulnerabilities_entry.delete(0, tk.END)
            self.damage_vulnerabilities_entry.insert(
                0,
                monster_statblock.get("important_info", {}).get(
                    "Damage Vulnerabilities", "None"
                ),
            )

            self.condition_immunities_entry.delete(0, tk.END)
            self.condition_immunities_entry.insert(
                0,
                monster_statblock.get("important_info", {}).get(
                    "Condition Immunities", "None"
                ),
            )
            split_monster_type = (
                monster_statblock.get("creature_type").replace(",", " ").split()
            )
            found_types = [
                word for word in split_monster_type if word in possible_types
            ]
            if found_types:
                self.type_var.set(found_types[0])
            skills_string = monster_statblock.get("important_info", {}).get(
                "Skills", "None"
            )
            if skills_string != "None":
                # Split the string by commas to separate each skill
                skills_list = skills_string.split(", ")

                # Iterate over the list to populate the dictionary
                for skill in skills_list:
                    # Split each skill into its name and value
                    name, value = skill.split(" ")
                    # Add to the dictionary
                    self.skills[name] = value
            self.after(100, self.num_monsters_entry.focus_force)

    def on_enter(self, event):
        if self.monster_name_entry.get():
            self.import_monster()

    def on_enter_with_filled_form(self, event):
        # Check if all necessary fields are filled
        if (
            self.monster_name_entry.get()
            and self.initiative_modifier_entry.get()
            and self.num_monsters_entry.get()
            and self.average_health_entry.get()
            and self.type_var.get()
        ):
            self.submit()

    def submit(self):
        monster_name = self.monster_name_entry.get()
        initiative_modifier = int(self.initiative_modifier_entry.get())
        num_monsters = int(self.num_monsters_entry.get())
        average_health = self.average_health_entry.get()
        monster_type = self.type_var.get()
        armor_class = self.armor_class_entry.get() or None
        speed = self.speed_entry.get() or None
        resistances = self.resistances_entry.get() or None
        damage_immunities = self.damage_immunities_entry.get() or None
        damage_vulnerabilities = self.damage_vulnerabilities_entry.get() or None
        condition_immunities = self.condition_immunities_entry.get() or None
        monster_skills = self.skills or None
        self.callback(
            monster_name,
            initiative_modifier,
            num_monsters,
            average_health,
            monster_type,
            armor_class,
            speed,
            resistances,
            damage_immunities,
            damage_vulnerabilities,
            condition_immunities,
            monster_skills,
        )
        self.destroy()
