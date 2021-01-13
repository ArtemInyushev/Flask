import json
from datetime import datetime, date
from ..models.desk import Desk
from api.repositories.taskRepository import taskRepository

taskRep = taskRepository()

class deskRepository:
    
    def saveAllDesks(self, desks_list):
        obj = {"desks": [ob.__dict__ for ob in desks_list]}
        new_json = json.dumps(obj, indent=4)
        
        with open('api/data/desks.json', 'w') as fout:
            fout.writelines(new_json)

    def getAllDesks(self):
        desks_list = []
        with open('api/data/desks.json', 'r') as fin:
            desks = json.load(fin)

            for obj in desks["desks"]:
                dateOfCreate = obj["dateOfCreate"]
                dateOfMod = obj["dateOfMod"]
                name = obj["name"]
                desks_list.append(Desk(dateOfCreate, dateOfMod, name))
        return desks_list

    def getDeskByName(self, name):
        desks_list = self.getAllDesks()
        for desk in desks_list:
            if desk.name == name:
                return desk

    def addDesk(self, name):
        desks_list = self.getAllDesks()
        for desk in desks_list:
            if desk.name == name:
                return False

        now = date.today().strftime("%d-%m-%Y")
        new_desk = Desk(now, now, name)
        desks_list.append(new_desk)

        self.saveAllDesks(desks_list)
        return True

    def updateDeskByName(self, old_name, new_name):
        desks_list = self.getAllDesks()
        for desk in desks_list:
            if desk.name == old_name:
                now = date.today().strftime("%d-%m-%Y")
                desk.name = new_name
                desk.dateOfMod = now
                self.saveAllDesks(desks_list)
                return True
        return False

    def deleteDeskByName(self, name):
        desks_list = self.getAllDesks()
        for desk in desks_list:
            if desk.name == name:
                taskRep.deleteAllTasksByDesk(name)
                desks_list.remove(desk)
                self.saveAllDesks(desks_list)
                return True
        return False
