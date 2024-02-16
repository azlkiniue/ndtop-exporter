# This file is part of nvitop, the interactive NVIDIA-GPU process viewer.
#
# Copyright 2021-2024 Xuehai Pan. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
"""Utility functions for ``nvitop-exporter``."""

import socket
import docker


__all__ = ['get_ip_address', 'get_container_id', 'get_container_info']


# Reference: https://stackoverflow.com/a/28950776
def get_ip_address() -> str:
    """Get the IP address of the current machine."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(0.0)
    try:
        # Doesn't even have to be reachable
        s.connect(('10.254.254.254', 1))
        ip_address = s.getsockname()[0]
    except Exception:  # noqa: BLE001 # pylint: disable=broad-except
        ip_address = '127.0.0.1'
    finally:
        s.close()
    return ip_address

def get_container_id(searched_pid: str) -> str:
    docker_client = docker.from_env()
    """Get list of all containers"""
    containers = docker_client.containers.list()
    # iterate trough the list of containers
    for container in containers:
        # get the list of processes running inside the container
        processes = docker_client.api.top(container.id)
        list_of_processes = processes["Processes"]
        # iterate through the list of processes
        for process in list_of_processes:
            pid = process[1]
            # check if the pid is the searched_pid
            if pid == searched_pid:
                return container.id
            
def get_container_info(container_id: str) -> tuple:
    docker_client = docker.from_env()
    container = docker_client.containers.get(container_id)
    return container.attrs["Name"].lstrip("/"), container.attrs["Config"]["Image"]