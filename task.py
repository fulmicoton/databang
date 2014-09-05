import datetime
from Queue import Queue
import threading
import subprocess
import config
from os import mkdir
from os import path as osp
import shutil

GIT_COMMAND = ["git", "--git-dir=./sandbox/.git", "--work-tree=./sandbox", ]

STATUS = (
    PENDING,
    RUNNING,
    SUCCESS,
    ERROR
) = (
    "PENDING",
    "RUNNING",
    "SUCCESS",
    "ERROR"
)


class Task(object):

    __slots__ = ('hash_rev', 'status', 'author', 'commit_msg', 'datetime', 'result_directory')

    def __init__(self,
                 hash_rev=None,
                 author=None,
                 commit_msg=None):
        self.status = PENDING
        self.hash_rev = hash_rev
        self.author = author
        self.commit_msg = commit_msg
        self.datetime = datetime.datetime.now()
        self.result_directory = None

    def checkout(self,):
        subprocess.check_call(GIT_COMMAND + ["fetch", "origin"])
        subprocess.check_call(GIT_COMMAND + ["checkout", self.hash_rev])

    def __respath_candidates(self,):
        filepath = osp.join("results", self.hash_rev)
        for i in range(1000):
            yield filepath + "-" + str(i).rjust(4, "0")

    def get_result_directory(self,):
        candidate = None
        if self.result_directory is None:
            for filepath in self.__respath_candidates():
                if not osp.exists(filepath):
                    candidate = filepath
                    break
            print "mkdir", candidate
            mkdir(candidate)
            self.result_directory = candidate
        if self.result_directory is None:
            raise Exception("Could not create directory.")
        return self.result_directory
                    

class TaskRunner(threading.Thread):

    def __init__(self, pending):
        threading.Thread.__init__(self,)
        self.pending = pending
        self.worker_pool = Queue()

    def run(self,):
        while True:
            task = self.pending.get(True)
            try:
                print "Running task", task
                task.status = RUNNING
                self.run_task(task)
                self.copy_task(task)
                task.status = SUCCESS
            except Exception as e:
                print "Error ", e
                task.status = ERROR

    def run_task(self, task):
        task.checkout()
        print "call"
        subprocess.check_call("./run.sh")
        print "done"
        self.copy_task(task)

    def copy_task(self, task):
        result_dir = task.get_result_directory()
        for fruit in config.FRUITS:
            print "copy", fruit
            src_file = osp.join("sandbox", fruit)
            dest_file = osp.join(result_dir, fruit)
            shutil.copyfile(src_file, dest_file)

    def make(self,):
        subprocess.check_call("run.sh")


class TaskManager(object):

    def __init__(self,):
        self.pending = Queue()
        self.tasks = []
        self.runner = TaskRunner(self.pending)
        self.runner.daemon = True
        self.runner.start()

    def add_task(self, task):
        self.pending.put(task)
        self.tasks.append(task)
