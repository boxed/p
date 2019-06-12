#!/usr/bin/env python3
import sys, yaml
from CLI.CLI import CLI


class Packages(CLI):
    """
Usage:
p-packages.py create <packagename> <(r)match> <commands>
    """
    def __init__(self):
        super().__init__("","create")

    def create(self,args):
        packagename = args[0]
        match = args[1] if args
