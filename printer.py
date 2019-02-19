#!/usr/bin/env python3
# -*-coding:utf-8 -*-
import os
import time
from colorama import init
from termcolor import cprint


init()


class Printer:
    instance = None

    def __new__(cls):
        if not cls.instance:
            cls.instance = super().__new__(cls)
        return cls.instance

    @staticmethod
    def current_time():
        return "[" + str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))) + "]"

    def printer(self, _msg, _type, _color, log=True):
        msg = ("{:<22}{:<10}{:<20}".format(self.current_time(), "[" + str(_type) + "]", str(_msg)))
        cprint(msg, _color)
        if log:
            log_file = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'log', 'log.log')
            with open(log_file, "a+", encoding="utf-8")as f:
                print(msg, file=f, flush=True)  # f.write(msg + "\n")

    def info(self, _msg, log=False):
        self.printer(_msg, 'Info', 'green', log)

    def error(self, _msg, log=False):
        self.printer(_msg, 'Error', 'red', log)

    def warning(self, _msg, log=False):
        self.printer(_msg, 'Warning', 'yellow', log)

    def lottery(self, _msg, log=False):
        self.printer(_msg, 'Lottery', 'cyan', log)
