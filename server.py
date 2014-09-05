from bottle import route, run, static_file, get, post, request, jinja2_view
import config
from task import TaskManager, Task

task_manager = TaskManager()


@route('/static/:filename')
def server_static(filename):
    return static_file(filename, root='./static')


@post('/api/tasks')
def tasks_create():
    task = Task(**request.json)
    task_manager.add_task(task)
    return "success"


@get('/api/tasks')
def tasks_list():
    return task_manager.tasks()


@get('/')
@jinja2_view('index.html', template_lookup=['templates'])
def index():
    return task_manager.tasks()


if __name__ == "__main__":
    run(host=config.HOSTNAME, port=config.PORT)
