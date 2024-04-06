from flask import request, jsonify
from .models import Task, Event, Subcategory, Category, User
from flask import Blueprint
from .app import db
from datetime import datetime, timezone, timedelta


app_routes = Blueprint('routes', __name__, url_prefix='/')
TIME_FORMAT = '%Y-%m-%d %H:%M'


# sanity check route
@app_routes.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify('pong!')

# @app_routes.route('/login', methods=['POST'])
# def login():
#     try:
#         data = request.get_json()
#         name = data['name']
#         username = data['username']
#         password = data['password']
#         print(data)
#         db.session.add(event)
#         db.session.commit()
#     except Exception as e:
#         print(str(e))
#         return jsonify(
#             {
#                 "message": "An error has occured while logging the user in",
#                 "error": str(e)
#             }
#         ), 500
    
    # return jsonify(
    #     {
    #         "data": user.to_dict()
    #     }
    # ), 201

# USERS
# Creating and sending a new user to the database
@app_routes.route("/users", methods=['POST'])
def addUser():
    try:
        data = request.get_json()
        user = User(**data)
        print(data)
        db.session.add(user)
        db.session.commit()
    except Exception as e:
        print(str(e))
        return jsonify(
            {
                "message": "An error has occured while creating a new user",
                "error": str(e)
            }
        ), 500
    
    return jsonify(
        {
            "data": user.to_dict()
        }
    ), 201

# Retreiving users from the database
@app_routes.route("/users")
def getUsers():
    user_list = User.query.all()
    if len(user_list) != 0:
        return jsonify(
            {
                "data": {
                    "users": [user.to_dict() for user in user_list]
                }
            }
        ), 200
    return jsonify(
        {
            "message": "No users found."
        }
    )


# Retreiving users from the database
@app_routes.route("/user/<int:user_id>")
def getUser(user_id):
    user = (db.session.query(User)
            .filter(User.user_id == user_id).one_or_none())
    if user:
        return jsonify(
            {
                "data": {
                    "user": user.to_dict()
                }
            }
        ), 200
    return jsonify(
        {
            "message": "No users found."
        }
    ), 204


# EVENTS
# Creating and sending an event to the database
@app_routes.route("/events", methods=['POST'])
def addEvent():
    try:
        data = request.get_json()
        event = Event(**data)
        print(data)
        created_event = event.add()
    except Exception as e:
        print(str(e))
        return jsonify(
            {
                "message": "An error has occured while creating an event",
                "error": str(e)
            }
        ), 500
    
    return jsonify(
        {
            "data": event.to_dict()
        }
    ), 201

# Retreiving events from the database
@app_routes.route("/events")
def getEvents():
    event_list = Event.query.all()
    for event in event_list:
        print(event.start_time)
        print(type(event.start_time))
    if len(event_list) != 0:
        return jsonify(
            {
                "data": {
                    "events": [event.to_dict() for event in event_list]
                }
            }
        ), 200
    return jsonify(
        {
            "message": "No events found."
        }
    ), 204


# Retreiving event by Id from the database
@app_routes.route("/event/<int:event_id>", methods=['GET', 'PUT', 'DELETE'])
def getEventById(event_id):
    event = (db.session.query(Event)
             .filter(Event.event_id == event_id).one_or_none())
    if not event:
        return jsonify(
            {
                "message": "No event found."
            }
        ), 204

    if request.method == 'GET':
        subcat = (db.session.query(Subcategory)
                  .filter(Subcategory.subcategory_id == event.subcategory_id)
                  .one())
        event_dict = event.to_dict()
        event_dict['subcategory'] = subcat.name
        print(event_dict)
        return jsonify(
            {
                "data": {
                    "event": event_dict
                }
            }
        ), 200

    if request.method == 'PUT':
        data = request.get_json()
        event.name = data['name']
        event.subcategory_id = data['subcategory_id']
        event.date = data['date']
        event.start_time = data['start_time']
        event.end_time = data['end_time']
        event.location = data['location']
        event.details = data['details']
        db.session.commit()
        return jsonify(
            {
                "data": {
                    "event": event.to_dict()
                }
            }
        ), 200

    db.session.delete(event)
    db.session.commit()
    return jsonify(
        {
            "message": "Event deleted successfully."
        }
    ), 200


# TASKS
# Creating and sending a task to the database
@app_routes.route("/tasks", methods=['POST'])
def addTask():
    try:
        data = request.get_json()
        task = Task(**data)
        # db.session.add(task)
        # db.session.commit()
        task.add()
    except Exception as e:
        print(str(e))
        return jsonify(
            {
                "message": "An error has occured while creating an task",
                "error": str(e)
            }
        ), 500
    
    return jsonify(
        {
            "data": task.to_dict()
        }
    ), 201

# Retreiving tasks from the database
@app_routes.route("/tasks")
def getTasks():
    task_list = Task.query.all()
    if len(task_list) != 0:
        return jsonify(
            {
                "data": {
                    "tasks": [task.to_dict() for task in task_list]
                }
            }
        ), 200
    return jsonify(
        {
            "message": "No tasks found."
        }
    ), 204


# Retreiving task by Id from the database
@app_routes.route("/task/<int:task_id>", methods=['GET', 'PUT', 'DELETE'])
def taskById(task_id):
    task = (db.session.query(Task)
            .filter(Task.task_id == task_id).one_or_none())
    if not task:
        return jsonify(
            {
                "message": "No task found."
            }
        ), 204

    if request.method == 'GET':
        subcat = (db.session.query(Subcategory)
                  .filter(Subcategory.subcategory_id == task.subcategory_id)
                  .one())
        task_dict = task.to_dict()
        task_dict['subcategory'] = subcat.name
        task_dict['end_time'] = getTaskEnd(task).split("T")[1]
        print(task_dict)
        return jsonify(
            {
                "data": {
                    "task": task_dict
                }
            }
        ), 200

    if request.method == 'PUT':
        data = request.get_json()
        task.name = data['name']
        task.subcategory_id = data['subcategory_id']
        task.date = data['date']
        task.duration = data['duration']
        task.start_time = data['start_time']
        task.details = data['details']
        db.session.commit()
        return jsonify(
            {
                "data": {
                    "event": task.to_dict()
                }
            }
        ), 200

    db.session.delete(task)
    db.session.commit()
    return jsonify(
        {
            "message": "Task deleted successfully."
        }
    ), 200


# CATEGORIES
# Creating and sending a category to the database
@app_routes.route("/categories", methods=['POST'])
def addCategory():
    try:
        data = request.get_json()
        category = Category(**data)
        category.add()
    except Exception as e:
        return jsonify(
            {
                "message": "An error has occured while creating a category",
                "error": str(e)
            }
        ), 500

    return jsonify(
        {
            "data": category.to_dict()
        }
    ), 201

# Retreiving categories from the database
@app_routes.route("/categories")
def getCategories():
    category_list = Category.query.all()
    if len(category_list) != 0:
        return jsonify(
            {
                "data": {
                    "categories": [category.to_dict() for category in category_list]
                }
            }
        ), 200
    return jsonify(
        {
            "message": "No categories found."
        }
    )


# Retreiving task by Id from the database
@app_routes.route("/category/<int:category_id>", methods=['PUT', 'DELETE'])
def categoryById(category_id):
    category = (db.session.query(Category)
                .filter(Category.category_id == category_id)
                .one_or_none())

    if not category:
        return jsonify(
            {
                "message": "No category found."
            }
        ), 204

    if request.method == 'PUT':
        data = request.get_json()
        category.name = data['name']
        db.session.commit()
        return jsonify(
            {
                "data": {
                    "category": category.to_dict()
                }
            }
        ), 200

    db.session.delete(category)
    db.session.commit()
    return jsonify(
        {
            "message": "Category deleted successfully."
        }
    ), 200


# SUBCATEGORIES
# Creating and sending a subcategory to the database
@app_routes.route("/subcategories", methods=['POST'])
def addSubcategory():
    try:
        data = request.get_json()
        print(data)
        subcategory = Subcategory(**data)
        subcategory.add()
    except Exception as e:
        print(str(e))
        return jsonify(
            {
                "message": "An error has occured while creating a subcategory",
                "error": str(e)
            }
        ), 500
    
    return jsonify(
        {
            "data": subcategory.to_dict()
        }
    ), 201

# Retreiving subcategories from the database
@app_routes.route("/subcategories")
def getSubcategories():
    subcategory_list = Subcategory.query.all()
    if len(subcategory_list) != 0:
        return jsonify(
            {
                "data": {
                    "subcategories": [subcategory.to_dict() for subcategory in subcategory_list]
                }
            }
        ), 200
    return jsonify(
        {
            "message": "No subcategories found."
        }
    ), 204


# Retreiving task by Id from the database
@app_routes.route("/subcategory/<int:subcategory_id>",
                  methods=['PUT', 'DELETE'])
def subcategoryById(subcategory_id):
    subcategory = (db.session.query(Subcategory)
                   .filter(Subcategory.subcategory_id == subcategory_id)
                   .one_or_none())

    if not subcategory:
        return jsonify(
            {
                "message": "No subcategory found."
            }
        ), 204

    if request.method == 'PUT':
        data = request.get_json()
        subcategory.name = data['name']
        subcategory.cateogry_id = data['category_id']
        subcategory.color = data['color']
        db.session.commit()
        return jsonify(
            {
                "data": {
                    "subcategory": subcategory.to_dict()
                }
            }
        ), 200

    db.session.delete(subcategory)
    db.session.commit()
    return jsonify(
        {
            "message": "Subcategory deleted successfully."
        }
    ), 200


# Retreiving dictionary of subcategories names to id from the database
@app_routes.route("/subcategoriesNameId/<int:user_id>")
def getSubcategoriesNameId(user_id):
    cat_list = (db.session.query(Category)
                .filter(Category.user_id == user_id).all())

    subcat_list = (db.session.query(Subcategory)
                   .filter(Subcategory.cateogry_id
                   .in_([cat.category_id for cat in cat_list])).all())

    if len(subcat_list) != 0:
        return jsonify(
            {
                "data": {
                    "subcategories": [
                        {
                            "text": subcategory.name,
                            "value": subcategory.subcategory_id,
                            "color": subcategory.color
                        } for subcategory in subcat_list]
                }
            }
        ), 200
    return jsonify(
        {
            "message": "No subcategories found."
        }
    ), 204


# Retreiving dictionary of categories names to id from the database
@app_routes.route("/categoriesNameId/<int:user_id>")
def getCategoriesNameId(user_id):
    print('in categories name id')
    cat_list = (db.session.query(Category)
                .filter(Category.user_id == user_id).all())

    if len(cat_list) != 0:
        return jsonify(
            {
                "data": {
                    "categories": [
                        {
                            "text": category.name,
                            "value": category.category_id
                        } for category in cat_list]
                }
            }
        ), 200
    return jsonify(
        {
            "message": "No categories found."
        }
    ), 204


@app_routes.route("/eventsWithParams", methods=['POST'])
def getEventsWithParams():
    print(request.data)
    data = request.get_json()
    start_time = data['start_time']
    start_date = (datetime.strptime(start_time, '%Y-%m-%d').date())
    end_time = data['end_time']
    end_date = (datetime.strptime(end_time, '%Y-%m-%d').date())
    print(start_date, end_date)
    user = data['user']
    events_list = (db.session.query(Event).filter(Event.user_id == user)
                   .filter(Event.date >= start_date)
                   .filter(Event.date <= end_date).all())
    colors = {}
    subcat_names = {}
    for event in events_list:
        event_subcat = event.subcategory_id
        if event_subcat not in colors:
            subcat = (db.session.query(Subcategory)
                      .filter(Subcategory.subcategory_id == event_subcat)
                      .one())
            colors[event_subcat] = subcat.color
            subcat_names[event_subcat] = subcat.name
    print(events_list)
    if len(events_list) != 0:
        return jsonify(
            {
                "data": {
                    "events": [
                        {
                            "event": event.event_id,
                            "name": event.name,
                            "start": (str(event.date) +
                                      "T" + str(event.start_time)),
                            "end": str(event.date) + "T" + str(event.end_time),
                            "location": event.location,
                            "details": event.details,
                            "color": (colors[event.subcategory_id].lower() +
                                      " darken-1"),
                            "subcategory": subcat_names[event.subcategory_id]
                        } for event in events_list
                    ]
                }
            }
        ), 200
    return jsonify(
        {
            "message": "No events found."
        }
    ), 204


@app_routes.route("/tasksWithParams", methods=['POST'])
def getTasksWithParams():
    print(request.data)
    data = request.get_json()
    start_time = data['start_time']
    start_date = (datetime.strptime(start_time, '%Y-%m-%d').date())
    user = data['user']
    tasks_list = (db.session.query(Task).filter(Task.user_id == user)
                  .filter(Task.date == start_date).all())
    colors = {}
    subcat_names = {}
    for task in tasks_list:
        task_subcat = task.subcategory_id
        if task_subcat not in colors:
            subcat = (db.session.query(Subcategory)
                      .filter(Subcategory.subcategory_id == task_subcat).one())
            colors[task_subcat] = subcat.color
            subcat_names[task_subcat] = subcat.name
    print(tasks_list)
    if len(tasks_list) != 0:
        return jsonify(
            {
                "data": {
                    "tasks": [
                        {
                            "task_id": task.task_id,
                            "name": task.name,
                            "start": (str(task.date) + " " +
                                      task.start_time.strftime(TIME_FORMAT)),
                            "end": getTaskEnd(task),
                            "details": task.details,
                            "color": (colors[task.subcategory_id].lower()
                                      + " lighten-2"),
                            "subcategory": subcat_names[task.subcategory_id]
                        } for task in tasks_list
                    ]
                }
            }
        ), 200
    return jsonify(
        {
            "message": "No events found."
        }
    ), 204


@app_routes.route("/eventsAndTasksWithParams", methods=['POST'])
def getEventsAndTasksWithParams():
    print('events and tasks')
    print(request.data)
    data = request.get_json()
    start_time = data['start_time']
    start_date = (datetime.strptime(start_time, '%Y-%m-%d').date())
    print(start_date)
    end_time = data['end_time']
    end_date = (datetime.strptime(end_time, '%Y-%m-%d').date())
    print(end_date)
    
    user = data['user']

    events_list = (db.session.query(Event).filter(Event.user_id == user)
                   .filter(Event.date >= start_date)
                   .filter(Event.date <= end_date).all())

    tasks_list = (db.session.query(Task).filter(Task.user_id == user)
                  .filter(Task.date == start_date).all())

    colors = {}
    subcat_names = {}
    for task in tasks_list:
        task_subcat = task.subcategory_id
        if task_subcat not in colors:
            subcat = (db.session.query(Subcategory)
                      .filter(Subcategory.subcategory_id == task_subcat).one())
            colors[task_subcat] = subcat.color
            subcat_names[task_subcat] = subcat.name

    tasks_dict = [{
                    "task_id": task.task_id,
                    "name": task.name,
                    "start": (str(task.date) + "T" +
                              str(task.start_time)),
                    "end": getTaskEnd(task),
                    "details": task.details,
                    "color": (colors[task.subcategory_id].lower()
                              + " lighten-2"),
                    "subcategory": subcat_names[task.subcategory_id]
                } for task in tasks_list]

    for event in events_list:
        event_subcat = event.subcategory_id
        if event_subcat not in colors:
            subcat = (db.session.query(Subcategory)
                      .filter(Subcategory.subcategory_id == event_subcat)
                      .one())
            colors[event_subcat] = subcat.color
            subcat_names[event_subcat] = subcat.name

    events_dict = [{
                    "event_id": event.event_id,
                    "name": event.name,
                    "start": (str(event.date) +
                              "T" + str(event.start_time)),
                    "end": str(event.date) + "T" + str(event.end_time),
                    "location": event.location,
                    "details": event.details,
                    "color": (colors[event.subcategory_id].lower() +
                              " darken-1"),
                    "subcategory": subcat_names[event.subcategory_id]
                } for event in events_list]

    print(tasks_list)
    print(events_list)
    if len(tasks_list) != 0 or len(events_list) != 0:
        return jsonify(
            {
                "data": tasks_dict + events_dict
            }
        ), 200
    return jsonify(
        {
            "message": "No events found."
        }
    ), 204


def getTaskEnd(task):
    start_time = task.start_time
    date = task.date
    start_datetime = datetime.combine(date, start_time)
    end_time = start_datetime + timedelta(minutes=task.duration)
    return end_time.strftime('%Y-%m-%dT%H:%M:%S')


@app_routes.route("/getCategoryByUserId/<int:user_id>")
def getCategoryByUserId(user_id):
    cat_list = (db.session.query(Category)
                .filter(Category.user_id == user_id).all())

    subcat_list = (db.session.query(Subcategory).all())

    if len(cat_list) != 0:
        return jsonify({
            "data": {
                "categories": [
                    {
                        "category_id": category.category_id,
                        "name": category.name,
                        "subcategories": [
                            {
                                "subcategory_id": subcategory.subcategory_id,
                                "name": subcategory.name,
                                "category_id": subcategory.cateogry_id,
                                "color": subcategory.color.lower()
                            } for subcategory in subcat_list if
                            subcategory.cateogry_id == category.category_id
                        ]
                    } for category in cat_list
                ]
            }
        }), 200
    return jsonify(
        {
            "message": "No categories found"
        }
    ), 204


@app_routes.route("/getSubategoryByUserId/<int:user_id>")
def getSubategoryByUserId(user_id):
    cat_list = (db.session.query(Category)
                .filter(Category.user_id == user_id).all())

    subcat_list = (db.session.query(Subcategory)
                   .filter(Subcategory.category_id
                   .in_([cat.category_id for cat in cat_list])).all())

    if len(subcat_list) != 0:
        return jsonify(
            {
                "data": {
                    "subcategories": [
                        {
                            "subcategory_id": subcategory.subcategory_id,
                            "name": subcategory.name,
                            "category_id": subcategory.category_id,
                            "color": subcategory.color.lower()
                        } for subcategory in cat_list
                    ]
                }
            }
        ), 200
    return jsonify(
        {
            "message": "No subcategories found."
        }
    ), 204


@app_routes.route("/eventsAndTasksBySubcategory", methods=['POST'])
def getEventsAndTasksBySubcategory():
    data = request.get_json()
    start_time = data['start_time']
    start_date = (datetime.strptime(start_time, '%Y-%m-%d').date())
    end_time = data['end_time']
    end_date = (datetime.strptime(end_time, '%Y-%m-%d').date())
    user = data['user']
    subcategory = data['subcategory']

    events_list = (db.session.query(Event).filter(Event.user_id == user)
                   .filter(Event.date >= start_date)
                   .filter(Event.date <= end_date)
                   .filter(Event.subcategory_id == subcategory).all())

    tasks_list = (db.session.query(Task).filter(Task.user_id == user)
                  .filter(Task.date == start_date)
                  .filter(Task.subcategory_id == subcategory).all())

    subcat_obj = (db.session.query(Subcategory)
                    .filter(Subcategory.subcategory_id == subcategory).one())
    color = subcat_obj.color
    subcat_name = subcat_obj.name

    tasks_dict = [{
        "task_id": task.task_id,
        "name": task.name,
        "start": (str(task.date) + "T" + str(task.start_time)),
        "end": getTaskEnd(task),
        "details": task.details,
        "color": color.lower() + " lighten-2",
        "subcategory": subcat_name
    } for task in tasks_list]

    events_dict = [{
        "event_id": event.event_id,
        "name": event.name,
        "start": (str(event.date) + "T" + str(event.start_time)),
        "end": str(event.date) + "T" + str(event.end_time),
        "location": event.location,
        "details": event.details,
        "color": color + " darken-1",
        "subcategory": subcat_name
    } for event in events_list]

    print(tasks_list)
    print(events_list)
    if len(tasks_list) != 0 or len(events_list) != 0:
        return jsonify(
            {
                "data": tasks_dict + events_dict
            }
        ), 200
    return jsonify(
        {
            "message": "No events found."
        }
    ), 204


@app_routes.route("/eventsBySubcategory", methods=['POST'])
def getEventsBySubcategory():
    data = request.get_json()
    start_time = data['start_time']
    start_date = (datetime.strptime(start_time, '%Y-%m-%d').date())
    end_time = data['end_time']
    end_date = (datetime.strptime(end_time, '%Y-%m-%d').date())
    user = data['user']
    subcategory = data['subcategory']

    events_list = (db.session.query(Event).filter(Event.user_id == user)
                   .filter(Event.date >= start_date)
                   .filter(Event.date <= end_date)
                   .filter(Event.subcategory_id <= subcategory).all())

    subcat_obj = (db.session.query(Subcategory)
                    .filter(Subcategory.subcategory_id == subcategory).one())
    color = subcat_obj.color
    subcat_name = subcat_obj.name

    if len(events_list) != 0:
        return jsonify({
            "data": {
                "events": [{
                    "event": event.event_id,
                    "name": event.name,
                    "start": (str(event.date) +
                                "T" + str(event.start_time)),
                    "end": str(event.date) + "T" + str(event.end_time),
                    "location": event.location,
                    "details": event.details,
                    "color": color.lower() + " darken-1",
                    "subcategory": subcat_name
                } for event in events_list]
            }
        }), 200
    return jsonify(
        {
            "message": "No events found."
        }
    ), 204

# @app_routes.route("/addData")
# def addData():
#     db.create_all()
#     return jsonify(), 200


# @app_routes.route("/deleteData")
# def deleteData():
#     d = db.session.query(Category).filter(Category.category_id == 5)
#     d.delete()
#     db.session.commit()
#     return jsonify(), 200
