#!/usr/bin/env python

import settings
from python_example import get_status, install_ssh_keys
from time import sleep

SSH_KEY = 'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDTWaa3Z89mPAxm4WbXWrjuiPKGFHF1zAAkEvOolVY8BSPJaWlSnFmreQtiTe6aZr7QeSgLZAM5QPQbGP9xDg8IGIa/wdyt2KHRguYyfbzqU7U295USWnnS+LkfbU0l3clxSSXgUhToW0CKRuMo6W/HGxjupsV2JqPGZ34XR1WBPJkfLbmAu0HxD9OccVBoSFnsSao0VbqLDCxIVDg4EOOBCPs09YKZfCp8qXrlT8DuKs2voRLqJ3KNWT3ODNrH4RSOal5tGLhPjFK1iLGANqU6sVgTMwhY6EgGFo4VhUGHlEqtAb/8F3x6OLkJkxQdCub4KizhNLjba0yGQ5/Rwgmp mvip@hax0rbook4.local'


def create_docker_nodes(max_retries=100):
    tasks = []

    for node in settings.NODES:
        tasks.append(install_ssh_keys(
            ip=node['ip'],
            username=node['username'],
            password=node['password'],
            ssh_user='vagrant',
            ssh_keys=[SSH_KEY],
        ))

    while max_retries > 0:
        max_retries -= 1

        if len(tasks) < 1:
            return True

        for task in tasks:
            status = get_status(task)
            print 'Task docker ({}) status is {}'.format(
                task,
                status['status']
            )
            if status['status'] in settings.EXIT_STATUS:
                print 'Task weave ({}) exited.'.format(task)
                tasks.remove(task)
        error_msg = status['msg']
        if error_msg:
            print error_msg
        sleep(5)
    else:
        return False


def main():
    create_docker_nodes()

if __name__ == "__main__":
    main()
