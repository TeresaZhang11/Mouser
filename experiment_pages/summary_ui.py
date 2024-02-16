'''Summary UI at the end of making a new experiment.'''
from tkinter import *
from tkinter.ttk import *
from tkinter.filedialog import *
import os
import tempfile
from tk_models import *
from scrollable_frame import ScrolledFrame
from experiment_pages.experiment import Experiment
from experiment_pages.experiment_menu_ui import ExperimentMenuUI
from experiment_pages.password_utils import PasswordManager

class CreateExperimentButton(Button):
    '''Button to save a new experiment.'''
    def __init__(self, experiment: Experiment, page: Frame, menu_page: Frame):
        super().__init__(page, text="Create", compound=TOP,
                         width=15, command=lambda: [self.create_experiment()])
        self.place(relx=0.85, rely=0.15, anchor=CENTER)
        self.experiment = experiment
        self.next_page = menu_page

    def create_experiment(self):
        '''Saves an experiment as a new .mouser file.'''
        directory = askdirectory()
        if directory:
            self.experiment.save_to_database(directory)
            if self.experiment.get_password():
                password = self.experiment.get_password()
                file = directory + '/' + self.experiment.get_name() + '_Protected.mouser'
                manager = PasswordManager(password)
                decrypted_data = manager.decrypt_file(file)
                temp_folder_name = "Mouser"
                temp_folder_path = os.path.join(tempfile.gettempdir(), temp_folder_name)
                os.makedirs(temp_folder_path, exist_ok=True)
                temp_file_name = self.experiment.get_name() + '_Protected.mouser'
                temp_file_path = os.path.join(temp_folder_path, temp_file_name)
                if os.path.exists(temp_file_path):
                    os.remove(temp_file_path)

                with open(temp_file_path, "wb") as temp_file:
                    temp_file.write(decrypted_data)
                    temp_file.seek(0)
                    root= self.winfo_toplevel() #pylint: disable= redefined-outer-name
                    page = ExperimentMenuUI(root, temp_file.name)
                    page.tkraise()
            else:
                file = directory + '/' + self.experiment.get_name() + '.mouser'
                root= self.winfo_toplevel()
                page = ExperimentMenuUI(root, file)
                page.tkraise()

class SummaryUI(MouserPage): # pylint: disable=undefined-variable
    '''Summary User Interface.'''
    def __init__(self, experiment: Experiment, parent:Tk, prev_page: Frame, menu_page: Frame):
        super().__init__(parent, "New Experiment - Summary", prev_page)

        self.input = experiment
        self.menu = menu_page

        CreateExperimentButton(experiment, self, menu_page)

        scroll_canvas = ScrolledFrame(self)
        scroll_canvas.place(relx=0.10, rely=0.25, relheight=0.7, relwidth=0.8)

        self.main_frame = Frame(scroll_canvas)
        self.main_frame.pack(side=LEFT, expand=True)

    def update_page(self):
        '''Updates the frame.'''
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        self.create_summary_frame()

    def create_summary_frame(self):
        '''Creates and populates summary frame.'''
        pad_x, pad_y = 10, 10
        labels, inputs = [], []

        label_style = Style()
        label_style.configure('Summary.TLabel', font=('Arial', '10', 'bold'))

        name_label = Label(self.main_frame, text='Experiment Name:', style='Summary.TLabel')
        name_input = Label(self.main_frame, text=self.input.get_name())
        labels.append(name_label)
        inputs.append(name_input)

        names = ''
        for name in self.input.get_investigators():
            names += name + ',\n'
        invest_label = Label(self.main_frame, text='Investigators:', style='Summary.TLabel')
        if len(names) >= 2:
            invest_input = Label(self.main_frame, text=names[:-2])
        else:
            invest_input = Label(self.main_frame, text=names)
        labels.append(invest_label)
        inputs.append(invest_input)

        species_label = Label(self.main_frame, text='Species:', style='Summary.TLabel')
        species_input = Label(self.main_frame, text=self.input.get_species())
        labels.append(species_label)
        inputs.append(species_input)

        items = ''
        for item in self.input.get_measurement_items():
            items += item + ',\n'
        items_label = Label(self.main_frame, text='Measurement Items:', style='Summary.TLabel')
        if len(items) >= 2:
            items_input = Label(self.main_frame, text=items[:-2])
        else:
            items_input = Label(self.main_frame, text=items)
        labels.append(items_label)
        inputs.append(items_input)

        animals = self.input.get_num_animals() + ' ' + self.input.get_species()
        animal_label = Label(self.main_frame, text='Number of Animals:', style='Summary.TLabel')
        animal_input = Label(self.main_frame, text=animals)
        labels.append(animal_label)
        inputs.append(animal_input)

        cage_label = Label(self.main_frame, text='Animals per Cage:', style='Summary.TLabel')
        cage_input = Label(self.main_frame, text=self.input.get_max_animals())
        labels.append(cage_label)
        inputs.append(cage_input)

        groups = self.input.get_group_names()
        group_names = ''
        for group in groups:
            group_names += group + ',\n'

        group_label = Label(self.main_frame, text='Group Names:', style='Summary.TLabel')
        if len(group_names) >= 2:
            group_input = Label(self.main_frame, text=group_names[:-2])
        else:
            group_input = Label(self.main_frame, text=group_names)
        labels.append(group_label)
        inputs.append(group_input)

        rfid = str(self.input.uses_rfid())
        rfid_label = Label(self.main_frame, text='Uses RFID:', style='Summary.TLabel')
        rfid_input = Label(self.main_frame, text=rfid)
        labels.append(rfid_label)
        inputs.append(rfid_input)
        # pylint: disable= consider-using-enumerate
        for index in range(0, len(labels)):
            labels[index].grid(row=index, column=0, padx= pad_x, pady= pad_y, sticky=NW)
            inputs[index].grid(row=index, column=1, padx= pad_x, pady= pad_y, sticky=NW)

            self.main_frame.grid_rowconfigure(index, weight=1)
            self.main_frame.grid_columnconfigure(index, weight=1)
        # pylint: enable= consider-using-enumerate
