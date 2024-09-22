import tkinter as tk
from tkinter import ttk
import random
import customtkinter
import os
#TODO from Dateiname, import meine FUnktion
#TODO webscraper für https://5ecompendium.github.io/bestiary/creature/aboleth-nihilith
    # TODO eine FUnction in add monster window wo ich den namne eingeben kann mit autofill
# TODO getrollte Strings mit nem klick markieren
# Strings eventuell direkt aus ChatGPT holen
#TODO Die Ordnung einzelner participants z.b. bei gleicher initative ändern können
#TODO ELemental String list adden
#'TODO BUG: Es scheint so, als ob wenn ich rows lösche alles andere wieder anfangs hp ist
customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"
customtkinter.set_widget_scaling(.9)

class InitiativeTracker(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("D&D INitiative Tracker")
        self.geometry(f"{1400}x{1000}")

        # configure grid layout (4x4)
        self.grid_columnconfigure( 1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

       

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=5, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(5, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Add Monsters or Players", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.add_monster_button = customtkinter.CTkButton(self.sidebar_frame, text= "Add Monsters", command=self.open_monster_window, text_color = "black", fg_color = "red")
        self.add_monster_button.grid(row=1, column=0, padx=20, pady=10)
        self.add_player_button = customtkinter.CTkButton(self.sidebar_frame,text = "Add Player", command= self.add_player)
        self.add_player_button.grid(row=2, column=0, padx=20, pady=10)

        # setup and hide the main frame for later use
        self.main_frame = customtkinter.CTkScrollableFrame(self, width=140, corner_radius=0)
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx = 30, pady = 20)
        self.main_frame.grid_rowconfigure(5, weight=1)
        self.main_frame.grid_forget()

        # defining the input variables for the players
        self.participant_name_entry = tk.StringVar()
        self.participant_initiative_entry = tk.StringVar()
        self.participant_health_entry = tk.StringVar()
        
        self.participant_name_entry = customtkinter.CTkEntry(self.sidebar_frame, placeholder_text="Player Name",)
        self.participant_name_entry.grid(row=3, column=0, padx=20, pady=10)

        self.participant_initiative_entry = customtkinter.CTkEntry(self.sidebar_frame, placeholder_text="Player Initiative", )
        self.participant_initiative_entry.grid(row=4, column=0, padx=20, pady=10)

        self.participant_health_entry = customtkinter.CTkEntry(self.sidebar_frame, placeholder_text="Player Health", )
        self.participant_health_entry.grid(row=5, column=0, padx=20, pady=10, sticky = "n")

        # Creating the appearance mode widget
        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=6, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 10))

        # creating the Scalingwidget
        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=9, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"],
                                                               command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=10, column=0, padx=20, pady=(10, 20))

        # set default values for SCaling and Appearence
        self.appearance_mode_optionemenu.set("Dark")
        self.scaling_optionemenu.set("100%")
        #self.textbox.insert("0.0", "CTkTextbox\n\n" + "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua.\n\n" * 20)
        
        # Initializing the required lists
        self.initial_values = []
        self.status_lists = {}
        self.current_health = {}
        """self.humanoid_status_list = []
        self.tier_status_list =[]
        self.untot_status_list = []
        self.maschine_status_list = []
        self.schleim_status_list = []
        self.celestial_status_list = []
        self.drache_status_list = []"""
        self.passive_perception_list = []

    """def get_list_name(self, monster_type):
        #list_name = f"self.{monster_type.lower()}_status_list"
        return self.status_lists.get(monster_type.lower(), [])"""
        
    
    def get_file_name(self, monster_type):
        file_name = f"{monster_type.lower()}_status.txt"
        return file_name
    
    def get_file_directory(self, monster_type):
        file_name = self.get_file_name(monster_type)
        file_directory = os.path.join(os.path.dirname(__file__), "monster_status_strings",  file_name)
        return file_directory
    
    def fill_status_lists(self, zahl, line, monster_type):
        if monster_type.lower() not in self.status_lists:
            # If not, create a new key-value pair with an empty list
            self.status_lists[monster_type.lower()] = []

        #status_list = self.get_list_name(monster_type)
        self.status_lists[monster_type.lower()].append((zahl, f"{line}"))
        print("calling the fill_status_lists function, this is the dict", self.status_lists)
        #self.status_lists[monster_type.lower()] = status_list
        #self.get_list_name(monster_type).append((zahl, f"{line}"))
        #self.humanoid_status_list = [(zahl,line) for zahl, line in self.humanoid_status_list if pline != "0-20" or line != "20-40" or line != "40-60" or line != "60-80" and line != "80-100""]
        


    def read_data_file(self, monster_type):
    
        """Method to read in data from the to the monster_type corresponding txt file. The txt file should have
        lines saying 0-20, 20-40, 40-60, 80-100. After the line 0-20 and before the line 20-40, the file should contain
        lines describing the status of the monster for a condition between 0 and 20% of its hitpoints.
        The strings are stored in the corresponding list. 
                
        Args:
            file_name (string): name of a file to read from
        
        Returns:
            None
        
        """

        with open(self.get_file_directory(monster_type), encoding= "utf8") as file:
            line = file.readline()
            while line:
                line = line.strip()
                if "0-20" in line:
                    zahl = 0
                elif "20-40" in line:
                    zahl = 20
                elif "40-60" in line:
                    zahl = 40
                elif "60-80" in line:
                    zahl = 60
                elif "80-100" in line:
                    zahl = 80
                # DONE: Versuchen in eine Methode auszulagern
                print("calling the read_data_file function, infos passed:", zahl, line, monster_type)
                if line not in ["0-20", "20-40", "40-60", "60-80", "80-100"]:
                    self.fill_status_lists(zahl, line, monster_type)
                line = file.readline()
                    
                #self.get_list_name(monster_type).append((zahl, f"line"))
           

        file.close()

    """Method to add a player after the entry widgets on the main window of the Initiative Tracker have been filled. At the moment, all players are identified as Humanoids"""
    def add_player(self):
        participant = self.participant_name_entry.get()     
        initiative = int(self.participant_initiative_entry.get())
        health = int(self.participant_health_entry.get())
        type = "Humanoid"
    
        # Check if participant already exists in the initial_values
        for i, (existing_participant, existing_initiative, existing_health, monster_type) in enumerate(self.initial_values):
            if existing_participant == participant:
                self.initial_values[i] = (participant, initiative, health, type)
                break
        else:
            self.initial_values.append((participant, initiative, health, type))

        self.initial_values.sort(key=lambda x: x[1], reverse=True)
        #print(self.initial_values)
        self.main_frame.destroy()
        self.update_initiative_text()
    
    """ Method for displaying the information in the initial_values tuple list as widgets in the main_frame of the Initiative_Tracker window"""
    def update_initiative_text(self):
        

        self.main_frame = customtkinter.CTkScrollableFrame(self, width=1000, height= 1000, corner_radius=0)
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx = 30, pady = 20, rowspan = 5)
        self.main_frame.grid_rowconfigure(5, weight=1)

        
        
        customtkinter.CTkLabel(master=self.main_frame, text ="Participant").grid(column=1, row =0, sticky = "w", padx = 5, pady = 5)
        customtkinter.CTkLabel(master=self.main_frame, text ="Initiative").grid(column=2, row =0, padx = 5, pady = 5)
        customtkinter.CTkLabel(master=self.main_frame, text ="Health").grid(column=3, row =0, padx = 5, pady = 5)
        customtkinter.CTkLabel(master=self.main_frame, text ="Health Status").grid(column=4, row =0, padx = 5, pady = 5)
        customtkinter.CTkLabel(master=self.main_frame, text ="Delete Button").grid(column=5, row =0, padx = 5, pady = 5)
        row_count = 1
        for i, (participant, initiative, health, type) in enumerate(self.initial_values):
            row_count += 1
            # Input Participant, initiative in the mainframe
            customtkinter.CTkLabel(master=self.main_frame, text =participant).grid(column=1, row =i+1, sticky = "w", padx = 5, pady = 5)
            customtkinter.CTkLabel(master=self.main_frame, text =initiative).grid(column=2, row =i+1, padx = 5, pady = 5)
            #create health_entry widget
            health_entry = tk.StringVar()
            health_entry_widget = customtkinter.CTkEntry(master = self.main_frame, textvariable= health_entry, width = 50)
            if participant in self.current_health:
                health_entry_widget.insert(0, str(self.current_health[participant]))
                row = i
                self.check_health_status(participant, row)


            if participant not in self.current_health:
                health_entry_widget.insert(0, str(health))
            health_entry_widget.grid(column=3, row=i+1, padx = 5, pady = 5)
            self.delayed_health_callback_id = None
            health_entry.trace_add(mode="write", callback=lambda *args, p=participant, h=health_entry, row = i: self.delayed_check_health_status(p, h, row))
            if participant not in self.current_health:
                customtkinter.CTkLabel(master=self.main_frame, text = "Full HP", fg_color = "green").grid(column=4, row =i+1, sticky = "w", padx = 5, pady = 5)
            # create Delete Button
            customtkinter.CTkButton(self.main_frame, text= "Delete this row", width = 60, command=lambda p=participant, row=i: self.delete_entry(row, p)).grid(column =5, row =i+1, padx = 5, pady = 5)

        #print("row_count =", row_count)
#TODO: Scrolbar Vertikal implementieren
        """main_frame_scrollbar = customtkinter.CTkScrollbar (self, command = tk.textbox.yview)
        main_frame_scrollbar.grid(row = 0, column = 3, sticky = "ew")
        self.main_frame.configure (xscrollcommand=main_frame_scrollbar.set)"""

    """ Method that is being called by the delete Button. It takes in the participants name of the row the delete button is clicked, creates a new dict without the tuple containing that participant and calls the update_initiative_text method"""
    def delete_entry(self, row, p):
        print(f"Deleting entry for row: {row}")
        self.initial_values.pop(row)
        print(self.current_health)
        if p in self.current_health:
            del(self.current_health[p])
        print(self.current_health)
        #self.initial_values = [(p, i, h, t) for p, i, h, t in self.initial_values if p != participant]
        self.update_initiative_text()
        #print("Entry deleted. Updated values:", self.initial_values)

    """method for changing the appearance of the window"""
    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)
    """method for changing the scaling"""
    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    """method for delaying a function being executed"""

    


    """method for delaying a function being executed"""

    def delayed_check_health_status(self, participant, health_entry, row):
        # Cancel the previous scheduled callback
        if self.delayed_health_callback_id:
            self.main_frame.after_cancel(self.delayed_health_callback_id)

        # Schedule a new callback after 200 milliseconds
        self.delayed_health_callback_id = self.main_frame.after(200, lambda: self.write_current_health(participant, health_entry, row)) #health_entry.get()))

    """ method to calculate the health_percentage for every participant.. It uses the health_entry in the initial_values list as well as the Number in the health_entry widget.
    Then it evaluates the type of the participant and, depending on the type, takes a random string from the list that corresponds to that type and 
    displays the string into the main_Frame widget"""

    def write_current_health(self, participant, health_entry, row):
        if health_entry != " ":
            print(f"calling write_current_health_function for participant{participant} with health:{health_entry.get()}")
            self.current_health[participant] = health_entry.get()
            print(self.current_health)
            self.check_health_status(participant, row)
        else:
            pass


    def check_health_status(self, participant, row):
        for participant_tuple in self.initial_values:
            participant_name, initiative, tuple_health, type = participant_tuple
            if participant_name == participant:
                if tuple_health != "":
                    try:
                        tuple_health = int(tuple_health)
                        current_health = int(self.current_health[participant])
                        health_percentage = (current_health / tuple_health) * 100
                        print(f"for {participant} in row {row} health_percentage={health_percentage}")
                    except (ValueError, ZeroDivisionError) as e:
                        print(f"Error calculating health percentage for {participant} in row {row}: {e}")
                        health_percentage = 0  # Assign a default value if there's an error
                else:
                    print(f"No health data available for {participant} in row {row}")
                    health_percentage = 0  # Assign a default value when tuple_health is empty

        widget = self.main_frame.grid_slaves(row+1, 4) 
        for w in widget: 
            print(f"destroying widget{w}")
            w.destroy()

        health_status = self.random_status_string(health_percentage, type)[0]
        color = self.random_status_string(health_percentage, type)[1]
        #if len(health_status):
        customtkinter.CTkLabel(master=self.main_frame, text = health_status, fg_color = color).grid(column=4, row = row+1, sticky = "w", padx = 5, pady = 5)


    def random_status_string (self, health_percentage, type):
        type = type.lower()
        #print( "SO sieht gerade das dictionary aus:", self.status_lists)
        #print("This is the type:", type)
        liste = self.status_lists[type]
        #print(f"Dies ist in der Liste: {self.status_lists[type]}")
        #print ("Dis ist in der Liste:", liste)
        if health_percentage >= 80:
            number = random.randint(sum(1 for tuple in liste if tuple[0] ==0 or tuple[0] == 20 or tuple[0] == 40 or tuple[0] == 60), sum(1 for tuple in liste if tuple[0] ==0 or tuple[0] == 20 or tuple[0] == 40 or tuple[0] == 60 or tuple[0] == 80)-1)
            health_status = liste[number][1]
            color = "chartreuse4"
                
            
        elif health_percentage >=60 and health_percentage < 80:
            number = random.randint(sum(1 for tuple in liste if tuple[0] ==0 or tuple[0] == 20 or tuple[0] == 40),sum(1 for tuple in liste if tuple[0] ==0 or tuple[0] == 20 or tuple[0] == 40 or tuple[0] == 60)-1)
            health_status = liste[number][1]
            color = "chartreuse1"
                
                
        elif health_percentage >= 40 and health_percentage < 60:
            number = random.randint(sum(1 for tuple in liste if tuple[0] == 20 or tuple[0] ==0),sum(1 for tuple in liste if tuple[0] ==0 or tuple[0] == 20 or tuple[0] == 40)-1)
            health_status = liste[number][1]
            color = "orange"
                               

        elif health_percentage >= 20 and health_percentage < 40:
            number = random.randint(sum(1 for tuple in liste if tuple[0] == 0), sum(1 for tuple in liste if tuple[0] == 20 or tuple[0] ==0)-1)
            health_status = liste[number][1]
            color = "firebrick1"
                        

        elif health_percentage >= 0 and health_percentage < 20:
            number = random.randint(0,sum(1 for tuple in liste if tuple[0] == 0)-1)
            health_status = liste[number][1]
            color = "firebrick4"
        
        #self.display_passive_perception()




        return health_status, color
        # TODO: FUnktion schreiben
    
    def get_url(self, monster_name):
        url = f"https://5ecompendium.github.io/bestiary/creature/{monster_name}"
        return url
    
    #TODO hier noch vernünftige Logik reinklashcen
    
    """def fetch_and_display_data(self, url):

        try:
            # Make a request to the website
            response = requests.get(url)
            response.raise_for_status()  # Raise an exception for bad requests

            # Parse the HTML content of the page
            soup = BeautifulSoup(response.text, 'html.parser')

            # Extract the data you want from the parsed HTML
            # For example, let's assume the data is inside a div with class 'data-container'
            data_container = soup.find('div', class_='data-container')

            # Get the text content from the data container
            data_text = data_container.get_text() if data_container else 'Data not found'

            # Display the data in a Tkinter window
            result_window = tk.Toplevel(root)
            result_window.title('Fetched Data')
            result_label = tk.Label(result_window, text=data_text, wraplength=400)
            result_label.pack(padx=20, pady=20)

        except requests.exceptions.RequestException as e:
            # Handle request exceptions (e.g., network error)
            error_message = f'Error fetching data: {str(e)}'
            error_label = tk.Label(root, text=error_message, fg='red')
            error_label.pack(padx=20, pady=20)"""

    """def display_passive_perception(self):
        self.passive_perception_frame = customtkinter.CTkFrame(self, width=200, height= 500, corner_radius=0)
        self.passive_perception_frame.grid(row=0, column=2, sticky="nsew", padx = 30, pady = 20, rowspan = 5)
        #self.passive_perception_frame.grid_rowconfigure(5, weight=1)

        with open(f"{os.path.join(os.path.dirname(__file__),'player_passive_perception.txt')}", encoding= "utf8") as file:
            line = str(file.readline())
            line = line.strip("\n")
            line = line.split(":")
            print("this is the display-passive_perception line", line)
            customtkinter.CTkLabel(master=self.passive_perception_frame, text = line[0], fg_color = color).grid(column=0, row =0, sticky = "w", padx = 5, pady = 5)
            customtkinter.CTkLabel(master=self.passive_perception_frame, text = line[1], fg_color = color).grid(column=1, row =0, sticky = "w", padx = 5, pady = 5)"""
           
       

    

    """method that is being called by the monster_button. It initializes the MonsterWindow class"""

    def open_monster_window(self):
        monster_window = MonsterWindow(self, self.add_monster)
        monster_window.mainloop()

        '''method that uses the values put in by the Monsterwindow Class, calculates the HP for a specific monster based on the average HP,
        rolls for the initiative of the individual monster. IT does this for every time the monster is being added and continues to number the monsters. It also calls the read_data_file method for the corresponding monster_type, 
         appends the data as tuples into the initial_values list, sorts it in descending order, destroys the current main_frame to then call the update_initiative_text method to rebuild it '''
    def add_monster(self, monster_name, initiative_modifier, num_monsters, average_health, monster_type):
        number = 0
        while number == 0:
            number = random.randint(-1, 1)
        for i in range(1, num_monsters + 1):
            monster = f"{monster_name}{i}"
            if number < 0:
                health = int(average_health) - int(((average_health / 100) * random.randint(1, 40)))
            elif number > 0:
                health = int(average_health) + int(((average_health / 100) * random.randint(1, 40)))
            initiative = random.randint(1, 20) + initiative_modifier
            self.initial_values.append((monster, initiative, health, monster_type))
        
        print("adding monster with the name {}, initiative {}, number {}, health {} and type {}".format(monster_name, initiative_modifier, num_monsters, average_health, monster_type))
        # hier will ich prüfen, ob die Liste im dictionary bereits iexistiert und falls nicht, die Liste erstellen.
        if self.status_lists.get(monster_type.lower()) is None:
            self.read_data_file(monster_type)
            #print("CPndition one works")
            #self.read_data_file(monster_type)
            #print(f"Lists have been initialized. THis is the list: {self.get_list_name(monster_type)}")
       

        self.initial_values.sort(key=lambda x: x[1], reverse=True)
        self.main_frame.destroy()
        self.update_initiative_text()

    
"""this class generates a window that asks the user to input a monster name, monster initiative, monster average health and the numbers of monsters the user wants to add.
It also asks the user to specify which type the monster is so it can later use corresponding strings"""

class MonsterWindow(customtkinter.CTk):
    def __init__(self, parent, callback):
        super().__init__()
        self.title("Add Monster")       

        self.monster_frame = customtkinter.CTkFrame(self, width=400, height= 200, corner_radius=0)
        self.monster_frame.grid(row=0, column=0, sticky="nsew", padx = 30, pady = 10)  

        
        self.monster_name_entry = customtkinter.CTkEntry(self.monster_frame, placeholder_text="Monster Name",)
        self.monster_name_entry.grid(row=1, column= 0, sticky="nsew", padx = 30, pady = 10)

        self.initiative_modifier_entry = customtkinter.CTkEntry(self.monster_frame, placeholder_text="Initiative")
        self.initiative_modifier_entry.grid(row=2, column=0, sticky="nsew", padx = 30, pady = 10)

        self.num_monsters_entry = customtkinter.CTkEntry(self.monster_frame, placeholder_text="How many?",)
        self.num_monsters_entry.grid(row=3, column=0, sticky="nsew", padx = 30, pady = 10)
       
        self.average_health_entry = customtkinter.CTkEntry(self.monster_frame, placeholder_text="Average Health",)
        self.average_health_entry.grid(row=4, column=0, sticky="nsew", padx = 30, pady = 10)


        self.monstertyp_auswahl_frame = customtkinter.CTkFrame(self)
        self.monstertyp_auswahl_frame.grid(row=0, column=1, sticky="nsew", padx = 30, pady = 10)
        self.type_var = tk.StringVar()

        self.monstertyp_auswahl_frame_label = customtkinter.CTkLabel(master=self.monstertyp_auswahl_frame, text="Choose the monster type:")
        self.monstertyp_auswahl_frame_label.grid(row=0, column=0, sticky="nsew", padx = 30, pady = 10)

#TODO die Buttons dynamisch machen
        self.humanoid_button = customtkinter.CTkRadioButton(master=self.monstertyp_auswahl_frame, text = "Humanoid" ,variable=self.type_var, value= "Humanoid")
        self.humanoid_button.grid(row=1, column=0, sticky="nsew", padx = 30, pady = 10)
        self.tier_button = customtkinter.CTkRadioButton(master=self.monstertyp_auswahl_frame, text = "Tier", variable=self.type_var, value= "Tier")
        self.tier_button.grid(row=2, column=0, sticky="nsew", padx = 30, pady = 10)
        self.untot_button = customtkinter.CTkRadioButton(master=self.monstertyp_auswahl_frame,text = "Untot", variable=self.type_var, value= "Untot")
        self.untot_button.grid(row=3, column=0, sticky="nsew", padx = 30, pady = 10)
        self.maschine_button = customtkinter.CTkRadioButton(master=self.monstertyp_auswahl_frame,text = "Maschine", variable=self.type_var, value= "Maschine")
        self.maschine_button.grid(row=4, column=0, sticky="nsew", padx = 30, pady = 10)
        self.schleim_button = customtkinter.CTkRadioButton(master=self.monstertyp_auswahl_frame,text = "Schleim", variable=self.type_var, value= "Schleim")
        self.schleim_button.grid(row=5, column=0, sticky="nsew", padx = 30, pady = 10)
        self.celestial_button = customtkinter.CTkRadioButton(master=self.monstertyp_auswahl_frame,text = "Celestial",  variable=self.type_var, value= "Celestial")
        self.celestial_button.grid(row=6, column=0, sticky="nsew", padx = 30, pady = 10)
        self.drache_button = customtkinter.CTkRadioButton(master=self.monstertyp_auswahl_frame,text = "Drache",  variable=self.type_var, value= "Drache")
        self.drache_button.grid(row=7, column=0, sticky="nsew", padx = 30, pady = 10)
        self.element_button = customtkinter.CTkRadioButton(master=self.monstertyp_auswahl_frame,text = "Elementar",  variable=self.type_var, value= "Elementar")
        self.element_button.grid(row=8, column=0, sticky="nsew", padx = 30, pady = 10)

        # create Submit button frame
        self.submit_button_frame = customtkinter.CTkFrame(self)
        self.submit_button_frame.grid(row=1, column=0, sticky="nsew", padx = 30, pady = 10, columnspan = 3)
        self.submit_button_frame.grid_rowconfigure (2, weight = 1)
        self.submit_button = customtkinter.CTkButton(master = self.submit_button_frame, text = "Submit", command = self.submit)
        self.submit_button.grid(row=0, column=0, padx = 30, pady = 10)
        

        #TODO: rausfinden wie man in einer FUnktion variablen generierne, die in self zur Verfügung stehen, EIngabefeld für Spieler mit Typ und default = HUmanoid,

        self.callback = callback
    """this method defines the behaviour of the submit button which is used in the MonsterWIndow class. It reads out the values in the EntryWidgets, the radiobutton which was ticked and passes the values to the add_monster Method"""
    def submit(self):
        monster_name = self.monster_name_entry.get()
        initiative_modifier = int(self.initiative_modifier_entry.get())
        num_monsters = int(self.num_monsters_entry.get())
        average_health = int(self.average_health_entry.get())
        monster_type = self.type_var.get()

        self.callback(monster_name, initiative_modifier, num_monsters, average_health, monster_type)
        self.destroy()


if __name__ == "__main__":
    app = InitiativeTracker()
    app.after(0, lambda:app.state('zoomed'))
    app.mainloop()