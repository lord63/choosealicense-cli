#!/usr/bin/env python
# -*- coding: utf-8 -*-

from invoke import task, run


@task
def test():
    run("py.test choosealicense/test/")


@task
def clean():
    run("rm -rf build")
    run("rm -rf dist")
    run("rm -rf choosealicense_cli.egg-info")
    print("Cleaned up.")


@task
def publish(test=False):
    if test:
        run("python setup.py register -r test sdist upload -r test")
    else:
        run("python setup.py register -r sdist upload")
