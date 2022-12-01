from tkinter import *
from tkinter.ttk import *
from tk_models import *
from ExperimentDatabase import ExperimentDatabase


class CageConfigurationUI(MouserPage):
    def __init__(self, database, parent:Tk, prev_page: Frame = None):
        super().__init__(parent, "Group Configuration", prev_page)

        file = str(database) + '.db'
        self.db = ExperimentDatabase(file)

        # unchanging data for stuff:
        self.groups = self.db.get_all_groups()

        self.main_frame = Frame(self)
        self.main_frame.grid(row=2, column=3, sticky='NESW')
        self.main_frame.place(relx=0.05, rely=0.20)

        move_frame = Frame(self.main_frame, relief=RIDGE)
        move_frame.grid(row=0, column=3, padx=10, pady=10)

        auto_button = Button(self.main_frame, text='Auto Group', width=15, 
                            command= lambda: self.auto_group())
        save_button = Button(self.main_frame, text='Save', width=15, 
                            command= lambda: self.save_to_database())
        move_button = Button(move_frame, text='Move', width=15, 
                            command= lambda: self.check_move_input())

        auto_button.grid(row=0, column=0, padx=10, pady=10)
        save_button.grid(row=0, column=4, padx=10, pady=10)
        move_button.grid(row=0, column=2, padx=5, pady=5)

        self.id_input = Entry(move_frame, width=10)
        self.cage_input = Entry(move_frame, width=10)

        self.id_input.insert(END, 'animal id')
        self.cage_input.insert(END, 'cage id')

        self.id_input.bind("<Button-1>", lambda event, arg='id': self.clear_entry(event, arg))
        self.cage_input.bind("<Button-1>", lambda event, arg='cage': self.clear_entry(event, arg))

        self.id_input.grid(row=0, column=0, padx=5, pady=10)
        self.cage_input.grid(row=0, column=1, padx=5, pady=10)

        self.config_frame = Frame(self.main_frame)
        self.config_frame.grid(row=1, column=0, columnspan=3)

        self.update_frame()



    def create_group_frame(self):
        # use group frame (is on main)
        
        index = 0
        for group in self.groups:
            frame = Frame(self.config_frame, relief='ridge')
            frame.grid(row=index, column=0, padx=10, pady=10)
            Label(frame, text=group).grid(row=0, column=0, padx=10, pady=10)
            index += 1



        animals = self.db.get_animals()
        for anim in animals:

            # make list of groups

            # call create cage frame
            anim_frame = self.create_cage_frame(anim)

            # anim_frame.grid()
            # place cage frame on group frame



    def create_cage_frame(self, animal):
        # use cage frame (is on group)

        # cage_frame = Frame(self.group_frame)
        # self.create_animal_frame(animal)
        # place animal frame on cage frame
        # return cage frame

        pass


    def create_animal_frame(self, animal, frame):
        # use anim frame (is on cage)
        
        # anim_frame = Frame()
        # return an animal frame  
        pass


    def update_frame(self):
        for widget in self.config_frame.winfo_children():
            widget.destroy()
        self.cage_frames = []
        self.anim_frames = []
        self.create_group_frame()


    def clear_entry(self, event, input):
        if input == 'id':
            self.id_input.delete(0, END)
        else:
            self.cage_input.delete(0, END)


    def auto_group(self):
        # TO-DO : re-group by weight
        self.update_frame()
        pass

    
    def move_animal(self, id: int, cage: int):
        # TO-DO : change in temp variable

        self.clear_entry(None, 'cage')
        self.clear_entry(None, 'id')

        self.update_frame()


    def raise_warning(self, option: int):
        message = Tk()
        message.title("WARNING")
        message.geometry('320x100')
        message.resizable(False, False)

        if option == 1:
            label = Label(message, text='Animal ID and Cage ID must be integers.')
            label.grid(row=0, column=0, padx=10, pady=10)
        elif option == 2:
            label = Label(message, text='Not a valid Animal ID.')
            label.grid(row=0, column=0, padx=10, pady=10)
        elif option == 3:
            label = Label(message, text='Not a valid Cage ID.')
            label.grid(row=0, column=0, padx=10, pady=10)

        ok_button = Button(message, text="OK", width=10, 
                        command= lambda: [message.destroy()])
        ok_button.grid(row=2, column=0, padx=10, pady=10)

        message.mainloop()


    def check_move_input(self):
        # valid_animal = False
        # valid_cage = False
        valid_animal = True
        valid_cage = True

        # TO-DO : call database/local variable check if valid

        if self.id_input.get() == '' or self.cage_input.get() == '':
            self.raise_warning(1)
        elif isinstance(int(self.id_input.get()), int) == False or isinstance(int(self.cage_input.get()), int) == False:
            self.raise_warning(1)
        elif valid_animal == False:
            self.raise_warning(2)
        elif valid_cage == False:
            self.raise_warning(3)
        elif  isinstance(int(self.id_input.get()), int) and isinstance(int(self.cage_input.get()), int) and valid_animal and valid_cage:
            self.move_animal(self.id_input.get(), self.cage_input.get())


    def save_to_database(self):
        # TO-DO : save to database
        # TO-DO : return to menu

        self.db.close()
        pass

