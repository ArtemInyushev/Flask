import json
from datetime import datetime, date
from ..models.task import Task

class taskRepository:

    def saveAllTasks(self, tasks_list):
        obj = {"tasks": [ob.__dict__ for ob in tasks_list]}
        new_json = json.dumps(obj, indent=4)
        
        with open('api/data/tasks.json', 'w') as fout:
            fout.writelines(new_json)

    def getAllTasks(self):
        tasks_list = []
        with open('api/data/tasks.json', 'r') as fin:
            tasks = json.load(fin)

            for obj in tasks["tasks"]:
                dateOfCreate = obj["dateOfCreate"]
                dateOfMod = obj["dateOfMod"]
                title = obj["title"]
                status = obj["status"]
                desc = obj["desc"]
                desk_name = obj["desk_name"]
                tasks_list.append(Task(dateOfCreate, dateOfMod, title, status, desc, desk_name))
        return tasks_list

    def getTaskByTitle(self, title):
        tasks_list = self.getAllTasks()
        for task in tasks_list:
            if task.title == title:
                return task

    def updateTaskByTitle(self, old_title, new_title, status, desc):
        tasks_list = self.getAllTasks()
        for task in tasks_list:
            if task.title == old_title:
                now = date.today().strftime("%d-%m-%Y")
                task.title = new_title
                task.status = status
                task.desc = desc
                task.dateOfMod = now
                self.saveAllTasks(tasks_list)
                return True
        return False

    def deleteTaskByTitle(self, title):
        tasks_list = self.getAllTasks()
        for task in tasks_list:
            if task.title == title:
                tasks_list.remove(task)
                self.saveAllTasks(tasks_list)
                return True
        return False

    def getAllTasksByDesk(self, desk_name):
        tasks_list = self.getAllTasks()
        res = []
        for task in tasks_list:
            if task.desk_name == desk_name:
                res.append(task)
        return res

    def deleteAllTasksByDesk(self, desk_name):
        tasks_list = self.getAllTasks()
        tasks_list = list(filter(lambda x: x.desk_name != desk_name, tasks_list))
        self.saveAllTasks(tasks_list)
