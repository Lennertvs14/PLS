import os
import json
from datetime import date


class Backup:
    location = "Backup/Backups.json"

    def __init__(self, description=""):
        self.id = id(self)
        self.date = str(date.today())
        self.file_name = self.date + "-" + str(self.id)
        self.description = description
        self.data = {}
        self.backup()

    def backup(self):
        self.data = self.__get_data_to_backup()
        current_backups = self.get_existing_backups()
        current_backups.append(self.__dict__)
        if not os.path.exists("Backup"):
            os.makedirs("Backup")
        with open(self.location, "w") as file:
            json.dump(current_backups, file, indent=4)
        self.validate_backup()

    def __get_data_to_backup(self):
        data_folder = "Data"
        data_dict = {}
        for file_name in os.listdir(data_folder):
            if file_name.endswith(".json"):
                file_path = os.path.join(data_folder, file_name)
                try:
                    with open(file_path, "r") as file:
                        data = json.load(file)
                except Exception as e:
                    data = None
                data_dict[file_name[:-5]] = data
        return data_dict

    def get_existing_backups(self):
        return self.get_data(self.location)

    def validate_backup(self):
        assert os.path.exists(self.location)
        try:
            with open(self.location, 'r') as file:
                data = json.load(file)
        except FileNotFoundError:
            print("The backup was not successful.")
            return False
        print("The backup was successful.")
        return True

    @staticmethod
    def restore_backup(delete_backup_after=False):
        current_backups = Backup.get_data(Backup.location)
        if current_backups:
            backup_to_restore = Backup.get_backup_to_restore_by_user_input(current_backups)
            backup_data = backup_to_restore['data']
            if backup_data:
                for file_name, data in backup_data.items():
                    file_path = os.path.join('Data', file_name + '.json')
                    with open(file_path, 'w') as file:
                        json.dump(data, file, indent=4)
                if delete_backup_after:
                    backups = [backup for backup in current_backups if backup['file_name'] != backup_to_restore['file_name']]
                    with open(Backup.location, "w") as file:
                        json.dump(backups, file, indent=4)
                print("Restoring the backup was successful.")
                return True
            else:
                print("Restoring the backup was not successful.")
                return False
        else:
            print("There are no backups found to restore.")

    @staticmethod
    def get_backup_to_restore_by_user_input(backups=None):
        if backups is None:
            backups = Backup.get_data(Backup.location)
        print("Backups to restore (from old to new):")
        count = 1
        for backup in backups:
            print(f"    [{count}] Backup {backup['description']} made at {backup['date']}.")
            count += 1
        user_input = input("Enter a digit to choose: ").strip()
        if user_input.isdigit() and 0 < int(user_input) <= len(backups):
            return backups[int(user_input)-1]
        else:
            print("Invalid input, please try again.\n")
            return Backup.get_backup_to_restore_by_user_input()

    @staticmethod
    def get_data(file_path):
        try:
            with open(file_path, "r") as file:
                data = json.load(file)
        except Exception as e:
            data = []
        return data
