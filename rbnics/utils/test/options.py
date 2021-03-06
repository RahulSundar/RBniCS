# Copyright (C) 2015-2020 by the RBniCS authors
#
# This file is part of RBniCS.
#
# SPDX-License-Identifier: LGPL-3.0-or-later

import os
import tempfile
try:
    import git
except ImportError:
    # Minimal support to be able to do a git clone
    class git(object):
        class Repo(object):
            @classmethod
            def clone_from(cls, url, to_path):
                os.system("git clone " + url + " " + to_path)
from rbnics.utils.test.patch_initialize_testing_training_set import patch_initialize_testing_training_set


def add_gold_options(parser, subdirectory):
    available_options = [name for opt in parser._anonymous.options for name in opt.names()]
    # Comparison to gold files in methodology tests and tutorials
    if "--action" not in available_options:
        parser.addoption("--action", action="store", default=None)
    if "--data-dir" not in available_options:
        data_dir_default = os.environ.get("RBNICS_TEST_DATA", None)
        if data_dir_default is not None:
            data_dir_default = os.path.join(data_dir_default, subdirectory)
        else:
            data_dir_default = "git@gitlab.com:RBniCS-test-data/" + subdirectory + ".git"
        parser.addoption("--data-dir", action="store", default=data_dir_default)


def add_performance_options(parser):
    available_options = [name for opt in parser._anonymous.options for name in opt.names()]
    # Comparison to previous performance tests
    if "--overhead-speedup-storage" not in available_options:
        parser.addoption("--overhead-speedup-storage", action="store", default=".benchmarks")


def process_gold_options(config):
    if config.option.action is not None:
        if config.option.data_dir.startswith("git@gitlab.com:RBniCS-test-data"):
            assert config.option.action != "regold", "Please provide a data directory"
            data_dir = tempfile.mkdtemp()
            git.Repo.clone_from(config.option.data_dir, data_dir)
            config.option.data_dir = data_dir
        patch_initialize_testing_training_set(config.option.action)
