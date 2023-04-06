import os
import json
from datetime import date


class Backup:
    def __init__(self):
        self.id = id(self)
        self.location = "Backup/Backups.json"
        self.date = str(date.today())
        self.name = self.date + "-" + str(self.id)
        self.data = {}
        self.backup()

    def backup(self):
        self.data = self.__get_data_to_backup()
        current_backups = self.__get_existing_backups()
        current_backups.append(self.__dict__)
        if not os.path.exists("Backup"):
            os.makedirs("Backup")
        with open(self.location, "w") as file:
            json.dump(current_backups, file, indent=4)
        self.backup_validation()

    def __get_data_to_backup(self):
        data_folder = "Data"
        data_dict = {}
        for file_name in os.listdir(data_folder):
            if file_name.endswith(".json"):
                file_path = os.path.join(data_folder, file_name)
                try:
                    with open(file_path, "r") as file:
                        data = json.load(file)
                except FileNotFoundError:
                    data = None
                data_dict[file_name[:-5]] = data
        return data_dict

    def __get_existing_backups(self):
        current_backups = []
        current_backups = self.get_data(self.location)
        return current_backups

