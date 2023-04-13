# Copyright 2023, NVIDIA CORPORATION & AFFILIATES. All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#  * Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
#  * Neither the name of NVIDIA CORPORATION nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS ``AS IS'' AND ANY
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE ARE DISCLAIMED.  IN NO EVENT SHALL THE COPYRIGHT OWNER OR
# CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
# PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY
# OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import os

#
# Helper functions for reading/writing state to disk
#


def read_int_from_txt_file(filename):
    full_path = os.path.join(os.environ["MODEL_LOG_DIR"], filename)
    try:
        with open(full_path, mode="r", encoding="utf-8", errors="strict") as f:
            txt = f.read()
    except FileNotFoundError:
        txt = "0"
    return int(txt)


def write_int_to_txt_file(filename, number):
    full_path = os.path.join(os.environ["MODEL_LOG_DIR"], filename)
    txt = str(number)
    with open(full_path, mode="w", encoding="utf-8", errors="strict") as f:
        f.write(txt)


#
# Functions for communicating initialize and finalize count between the model
# and test
#


def get_count(filename):
    count = read_int_from_txt_file(filename)
    return count


def inc_count(filename):
    count = read_int_from_txt_file(filename)
    count += 1
    write_int_to_txt_file(filename, count)
    return count


def reset_count(filename):
    count = 0
    write_int_to_txt_file(filename, count)
    return count


def get_initialize_count():
    return get_count("instance_init_del_initialize_count.txt")


def inc_initialize_count():
    return inc_count("instance_init_del_initialize_count.txt")


def reset_initialize_count():
    return reset_count("instance_init_del_initialize_count.txt")


def get_finalize_count():
    return get_count("instance_init_del_finalize_count.txt")


def inc_finalize_count():
    return inc_count("instance_init_del_finalize_count.txt")


def reset_finalize_count():
    return reset_count("instance_init_del_finalize_count.txt")


#
# Functions for communicating varies of delay (in seconds) to the model
#


def get_initialize_delay():
    delay = read_int_from_txt_file("instance_init_del_initialize_delay.txt")
    return delay


def set_initialize_delay(delay):
    write_int_to_txt_file("instance_init_del_initialize_delay.txt", delay)
    return delay


def get_infer_delay():
    delay = read_int_from_txt_file("instance_init_del_infer_delay.txt")
    return delay


def set_infer_delay(delay):
    write_int_to_txt_file("instance_init_del_infer_delay.txt", delay)
    return delay


#
# Functions for modifying the model
#


def update_instance_group(instance_group_str):
    full_path = os.path.join(os.path.dirname(__file__), "config.pbtxt")
    with open(full_path, mode="r+", encoding="utf-8", errors="strict") as f:
        txt = f.read()
        txt = txt.split("instance_group [")[0]
        txt += "instance_group [\n"
        txt += instance_group_str
        txt += "\n]\n"
        f.truncate(0)
        f.seek(0)
        f.write(txt)
    return txt


def update_model_file():
    full_path = os.path.join(os.path.dirname(__file__), "1", "model.py")
    with open(full_path, mode="a", encoding="utf-8", errors="strict") as f:
        f.write("\n# dummy model file update\n")


def enable_batching():
    full_path = os.path.join(os.path.dirname(__file__), "config.pbtxt")
    with open(full_path, mode="r+", encoding="utf-8", errors="strict") as f:
        txt = f.read()
        txt = txt.replace("max_batch_size: 0", "max_batch_size: 2")
        f.truncate(0)
        f.seek(0)
        f.write(txt)
    return txt


def disable_batching():
    full_path = os.path.join(os.path.dirname(__file__), "config.pbtxt")
    with open(full_path, mode="r+", encoding="utf-8", errors="strict") as f:
        txt = f.read()
        txt = txt.replace("max_batch_size: 2", "max_batch_size: 0")
        f.truncate(0)
        f.seek(0)
        f.write(txt)
    return txt
