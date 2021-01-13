from flask import Blueprint, render_template, request, redirect, url_for, abort, flash
from ..repositories import deskRepository

deskRep = deskRepository.deskRepository()
desk_page = Blueprint("desks", __name__, url_prefix="/desks")

@desk_page.route("", methods=['GET'])
def getAllDesks():
    desks = deskRep.getAllDesks()
    return render_template("desks/desks.html", desks = desks)

@desk_page.route("/<name>", methods=['GET'])
def getDeskByName(name):
    desk = deskRep.getDeskByName(name)
    if desk:
        return render_template("desks/desk.html", desk = desk)
    abort(404, "No desk with such name")

@desk_page.route("/delete", methods=['POST'])
def deleteDeskByName():
    name = request.form["name"]
    deskRep.deleteDeskByName(name)
    return redirect(url_for('.getAllDesks'))

@desk_page.route("/new", methods=['POST'])
def createNewDesk():
    name = request.form["name"]
    if name:
        if not deskRep.addDesk(name):
            flash(message="Desk with such name is already exists")
    return redirect(url_for('.getAllDesks'))

@desk_page.route("/update", methods=["POST"])
def updateDesk():
    old_name = request.form["old_name"]
    new_name = request.form["new_name"]
    if deskRep.updateDeskByName(old_name, new_name):
        return redirect(url_for('.getAllDesks'))
    abort(404, "No desk with such name")