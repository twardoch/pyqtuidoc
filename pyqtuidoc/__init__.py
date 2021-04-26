#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
pyhecate
--------
Copyright (c) 2021 Adam Twardoch <adam+github@twardoch.com>
MIT license. Python 3.8+
"""
__version__ = "0.1.0"

__all__ = ['__main__']

import os
import shutil
import glob
import logging
import json
import subprocess
import tempfile
import time
import ffmpeg
from send2trash import send2trash

