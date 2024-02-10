import csv
import uuid
from datetime import date
from database_apis.experiment_database import ExperimentDatabase
from database_apis.experiment_database import ExperimentDatabase
from datetime import date
from .password_utils import PasswordManager

class Experiment():
    def __init__(self):

        self.name = ''
        self.investigators = []
        self.species = ''
        self.items = []
        self.id = ''
        self.rfid = False
        self.num_animals = ''
        self.num_groups = '0'
        self.max_per_cage = ''
        self.animals_per_group = ''
        self.group_names = []
        self.data_collect_type = []
        self.date_created = str(date.today())
        self.password = None

        self.group_num_changed = False
        self.measurement_items_changed = False


    def set_name(self, name):
        self.name = name


    def set_investigators(self, invest):
        self.investigators = invest


    def set_species(self, species):
        self.species = species


    def set_measurement_items(self, items):
        if self.items != items:
            self.measurement_items_changed = True
            self.items = items.copy()


    def set_uses_rfid(self, rfid):
        self.rfid = rfid


    def set_num_animals(self, num):
        self.num_animals = num


    def set_num_groups(self, num):
        if self.num_groups != num:
            self.num_groups = num
            self.group_num_changed = True


    def set_max_animals(self, num):
        self.max_per_cage = num
    
    def set_unique_id(self):
        unique_id = uuid.uuid1()
        self.id = str(unique_id)

    
    def set_group_names(self, names):
        self.group_names = names


    def set_collection_types(self, type):
        self.data_collect_type = type


    def set_animals_per_group(self, num):
        self.animals_per_group = num


    def set_password(self, password):
        self.password = password


    def set_group_num_changed_false(self):
        self.group_num_changed = False


    def set_measurement_items_changed_false(self):
        self.measurement_items_changed = False


    def get_name(self):
        return self.name


    def get_investigators(self):
        return self.investigators


    def get_species(self):
        return self.species


    def get_measurement_items(self):
        return self.items


    def uses_rfid(self):
        return self.rfid


    def get_num_animals(self):
        return self.num_animals


    def get_num_groups(self):
        return self.num_groups


    def get_max_animals(self):
        return self.max_per_cage

    
    def get_group_names(self):
        return self.group_names


    def get_collection_types(self):
        return self.data_collect_type


    def get_password(self):
        return self.password


    def check_num_groups_change(self):
        return self.group_num_changed
    

    def check_measurement_items_changed(self):
        return self.measurement_items_changed

    def save_to_database(self, directory: str):
        if(self.password):
            file = directory + '/' + self.name + '_Protected.mouser'
        else:
            file = directory + '/' + self.name + '.mouser'
        db = ExperimentDatabase(file)
        db.setup_experiment(self.name, self.species, self.rfid, self.num_animals, 
                            self.num_groups, self.max_per_cage, self.id)
        db.setup_groups(self.group_names)
        db.setup_cages(self.num_animals, self.num_groups, self.max_per_cage)
        db.setup_measurement_items(self.data_collect_type)
        if(self.password):
            manager = PasswordManager(self.password)
            manager.encrypt_file(file)
        
        # TO:DO save date created to db

        