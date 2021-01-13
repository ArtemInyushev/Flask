from flask import Blueprint, render_template, request, redirect, url_for, abort, flash
from ..repositories import taskRepository, deskRepository

taskRep = taskRepository.taskRepository()
deskRep = deskRepository.deskRepository()

task_page = Blueprint("tasks", __name__, url_prefix="/tasks")

@task_page.route("", methods=['GET'])
def getAllTasks():
    filters = ["all"]
    for desk in deskRep.getAllDesks():
        filters.append(desk.name)

    filter = request.args.get("filter")
    if not filter:
        filter = "all"
    filters.remove(filter)

    tasks = []
    if filter == "all":
        tasks = taskRep.getAllTasks()
    else:
        tasks = taskRep.getAllTasksByDesk(filter)

    return render_template("tasks/tasks.html", 
                            tasks = tasks, 
                            filters = filters, 
                            main_filter = filter)

@task_page.route("/<title>", methods=['GET'])
def getTaskByTitle(title):
    task = taskRep.getTaskByTitle(title)
    if task:
        return render_template("tasks/task.html", task = task)
    abort(404, "No task with such title")

@task_page.route("/delete", methods=['POST'])
def deleteTask():
    title = request.form["title"]
    taskRep.deleteTaskByTitle(title)
    return redirect(url_for('.getAllTasks'))

@task_page.route("/update", methods=['POST'])
def updateTask():
    old_title = request.form["old_title"]
    new_title = request.form["new_title"]
    status = False
    if request.form.get("status") == "done":
        status = True
    desc = request.form["desc"]
    if taskRep.updateTaskByTitle(old_title, new_title, status, desc):
        return redirect(url_for('.getAllTasks'))
    abort(404, "No task with such title")
