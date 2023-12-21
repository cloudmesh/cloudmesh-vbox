from cloudmesh.abstract.ComputeNodeABC import ComputeNodeABC
import subprocess
import json
import re
import time
import json


class Vbox(ComputeNodeABC):
    def __init__(self):
        """
        Initialize the Vbox class.
        """
        super().__init__()

    def _run(self, command):
        """
        Run a shell command.

        Args:
            command (list): The command to run as a list of strings.

        Returns:
            str: The output of the command.
        """
        result = subprocess.run(command, capture_output=True, text=True)
        return result.stdout

    def list(self, **kwargs):
        """
        List all VMs.

        Args:
            kwargs (dict): Additional keyword arguments.

        Returns:
            str: A JSON string representing the list of VMs.
        """
        output = self._run(["VBoxManage", "list", "vms"])
        lines = output.splitlines()
        vms = []
        for line in lines:
            match = re.match(r'^"(.+)" {(.+)}$', line)
            if match:
                vms.append(
                    {
                        "name": match.group(1),
                        "UUID": match.group(2),
                    }
                )
        return json.dumps(vms)

    def start(self, name=None):
        """
        Start a VM.

        Args:
            name (str, optional): The name of the VM. Defaults to None.

        Returns:
            str: The output of the VBoxManage startvm command.
        """
        if name is None:
            raise ValueError("VM name must be provided")

        return self._run(["VBoxManage", "startvm", name])

    def stop(self, name=None):
        """
        Stop a VM.

        Args:
            name (str, optional): The name of the VM. Defaults to None.

        Returns:
            str: The output of the VBoxManage controlvm command.
        """
        if name is None:
            raise ValueError("VM name must be provided")

        return self._run(["VBoxManage", "controlvm", name, "poweroff"])

    def info(self, name=None):
        """
        Get information about a VM.

        Args:
            name (str, optional): The name of the VM. Defaults to None.

        Returns:
            str: A JSON string representing the information about the VM.
        """
        if name is None:
            raise ValueError("VM name must be provided")

        output = self._run(["VBoxManage", "showvminfo", name, "--machinereadable"])
        lines = output.splitlines()
        info = {}
        for line in lines:
            match = re.match(r'^"?(.+?)"?="?(.*?)"?$', line)
            if match:
                info[match.group(1)] = match.group(2)
        return json.dumps(info)

    def suspend(self, name=None):
        """
        Suspend a VM.

        Args:
            name (str, optional): The name of the VM. Defaults to None.

        Returns:
            str: The output of the VBoxManage controlvm command.
        """
        if name is None:
            raise ValueError("VM name must be provided")

        return self._run(["VBoxManage", "controlvm", name, "savestate"])

    def resume(self, name=None):
        """
        Resume a VM.

        Args:
            name (str, optional): The name of the VM. Defaults to None.

        Returns:
            str: The output of the VBoxManage startvm command.
        """
        if name is None:
            raise ValueError("VM name must be provided")

        return self._run(["VBoxManage", "startvm", name])

    def reboot(self, name=None):
        """
        Reboot a VM.

        Args:
            name (str, optional): The name of the VM. Defaults to None.

        Returns:
            str: The output of the VBoxManage controlvm command.
        """
        if name is None:
            raise ValueError("VM name must be provided")

        return self._run(["VBoxManage", "controlvm", name, "reset"])

    def create(self, name=None, image=None, size=None, timeout=360, **kwargs):
        """
        Create a new VM.

        Args:
            name (str, optional): The name of the VM. Defaults to None.
            image (str, optional): The image to use for the VM. Defaults to None.
            size (str, optional): The size of the VM. Defaults to None.
            timeout (int, optional): The timeout for creating the VM. Defaults to 360.
            kwargs (dict): Additional keyword arguments.
        """
        pass

    def rename(self, name=None, destination=None):
        """
        Rename a VM.

        Args:
            name (str, optional): The current name of the VM. Defaults to None.
            destination (str, optional): The new name for the VM. Defaults to None.

        Returns:
            str: The output of the VBoxManage modifyvm command.
        """
        if name is None or destination is None:
            raise ValueError("Both current and new VM names must be provided")

        return self._run(["VBoxManage", "modifyvm", name, "--name", destination])

    def destroy(self, name=None):
        """
        Destroy a VM.

        Args:
            name (str, optional): The name of the VM. Defaults to None.

        Returns:
            str: The output of the VBoxManage unregistervm command.
        """
        if name is None:
            raise ValueError("VM name must be provided")

        return self._run(["VBoxManage", "unregistervm", name, "--delete"])

    def get_server_metadata(self, name):
        """
        gets the metadata for the server

        :param name: name of the fm
        :return:
        """
        raise NotImplementedError

    def set_server_metadata(self, name=None, **metadata):
        """
        Set metadata for a VM.

        Args:
            name (str, optional): The name of the VM. Defaults to None.
            metadata (dict): The metadata to set.
        """
        pass

    def delete_server_metadata(self, name=None, **metadata):
        """
        Delete metadata from a VM.

        Args:
            name (str, optional): The name of the VM. Defaults to None.
            metadata (dict): The metadata to delete.
        """
        pass

    def ssh(self, vm=None, username=None, command=None):
        """
        SSH into a VM.

        Args:
            vm (str, optional): The IP address of the VM to SSH into. Defaults to None.
            username (str, optional): The username to use for SSH. Defaults to None.
            command (str, optional): The command to run. Defaults to None.

        Returns:
            str: The output of the SSH command.
        """
        if vm is None or username is None:
            raise ValueError("Both VM IP address and username must be provided")

        ssh_command = ["ssh", f"{username}@{vm}"]
        if command:
            ssh_command.append(command)

        result = subprocess.run(ssh_command, capture_output=True, text=True)
        return result.stdout

    def run(self, vm=None, command=None):
        """
        Run a command on a VM.

        Args:
            vm (str, optional): The VM to run the command on. Defaults to None.
            command (str, optional): The command to run. Defaults to None.

        Returns:
            str: The output of the command.
        """
        if vm is None or command is None:
            raise ValueError("Both VM and command must be provided")

        ssh_command = ["ssh", f"{self.username}@{vm}", command]
        result = subprocess.run(ssh_command, capture_output=True, text=True)
        return result.stdout

    def console(self, vm=None):
        raise
        """
        Open a console to a VM.

        Args:
            vm (str, optional): The VM to open a console to. Defaults to None.
        """
        pass

    def log(self, vm=None):
        """
        Get the log for a VM.

        Args:
            vm (str, optional): The VM to get the log for. Defaults to None.

        Returns:
            str: The output of the log.
        """
        if vm is None:
            raise ValueError("VM name must be provided")

        output = self.run(vm, "VBoxManage showvminfo --machinereadable")
        for line in output.split("\n"):
            if "Logfile" in line:
                logfile = line.split("=")[1].strip().strip('"')
                return self.run(vm, f"cat {logfile}")

        return "No log file found"

    def script(self, vm=None, script=None):
        """
        Run a script on a VM.

        Args:
            vm (str, optional): The VM to run the script on. Defaults to None.
            script (str, optional): The script to run. Defaults to None.

        Returns:
            str: The output of the script.
        """
        if vm is None or script is None:
            raise ValueError("Both VM and script must be provided")

        commands = script.split("\n")
        output = ""

        for command in commands:
            if command.strip():  # Ignore empty lines
                output += self.run(vm, command)

        return output

    def wait(self, vm=None, state=None, interval=5, timeout=60):
        """
        Wait for a VM to reach a certain state.

        Args:
            vm (str, optional): The VM to wait for. Defaults to None.
            state (str, optional): The state to wait for. Defaults to None.
            interval (int, optional): The interval to wait between checks. Defaults to 5.
            timeout (int, optional): The maximum time to wait. Defaults to 60.

        Returns:
            str: The output in JSON format.
        """
        if vm is None or state is None:
            raise ValueError("Both VM and state must be provided")

        start_time = time.time()
        while True:
            current_state = self.status(vm)
            if current_state == state:
                output = {"vm": vm, "state": state, "status": "reached"}
                return json.dumps(output)
            elif time.time() - start_time > timeout:
                output = {"vm": vm, "state": state, "status": "timeout"}
                return json.dumps(output)

            time.sleep(interval)

    def status(self, vm=None):
        """
        Get the status of a VM.

        Args:
            vm (str, optional): The name of the VM. Defaults to None.

        Returns:
            str: The status of the VM.
        """
        if vm is None:
            raise ValueError("VM name must be provided")

        output = self._run(["VBoxManage", "showvminfo", vm])
        for line in output.split("\n"):
            if "State:" in line:
                return line.split(":")[1].strip()

        return "Unknown"

    def keys(self):
        """
        Lists the keys on the cloud

        :return: dict
        """
        raise NotImplementedError

    def key_upload(self, key=None):
        """
        uploads the key specified in the yaml configuration to the cloud
        :param key:
        :return:
        """
        raise NotImplementedError

    def key_delete(self, name=None):
        """
        deletes the key with the given name
        :param name: The name of the key
        :return:
        """
        raise NotImplementedError

    def images(self, **kwargs):
        """
        Lists the images on the cloud
        :return: dict
        """
        raise NotImplementedError

    def image(self, name=None):
        """
        Gets the image with a given nmae
        :param name: The name of the image
        :return: the dict of the image
        """
        raise NotImplementedError

    def flavors(self, **kwargs):
        """
        Lists the flavors on the cloud

        :return: dict of flavors
        """
        raise NotImplementedError

    def flavor(self, name=None):
        """
        Gets the flavor with a given name
        :param name: The name of the flavor
        :return: The dict of the flavor
        """
        raise NotImplementedError

    def reboot(self, name=None):
        """
        Reboot a list of nodes with the given names

        :param name: A list of node names
        :return:  A list of dict representing the nodes
        """
        raise NotImplementedError

    def attach_public_ip(self, name=None, ip=None):
        """
        adds a public ip to the named vm

        :param name: Name of the vm
        :param ip: The ip address
        :return:
        """
        raise NotImplementedError

    def detach_public_ip(self, name=None, ip=None):
        """
        adds a public ip to the named vm

        :param name: Name of the vm
        :param ip: The ip address
        :return:
        """
        raise NotImplementedError

    def delete_public_ip(self, ip=None):
        """
        Deletes the ip address

        :param ip: the ip address, if None than all will be deleted
        :return:
        """
        raise NotImplementedError

    def list_public_ips(self, available=False):
        """
        Lists the public ip addresses.

        :param available: if True only those that are not allocated will be
            returned.

        :return:
        """
        raise NotImplementedError

    def create_public_ip(self):
        """
        Creates a new public IP address to use

        :return: The ip address information
        """
        raise NotImplementedError

    def find_available_public_ip(self):
        """
        Returns a single public available ip address.

        :return: The ip
        """
        raise NotImplementedError

    def get_public_ip(self, name=None):
        """
        returns the public ip

        :param name: name of the server
        :return:
        """
        raise NotImplementedError

    def list_secgroups(self, name=None):
        """
        List the named security group

        :param name: The name of the group, if None all will be returned
        :return:
        """

    def list_secgroup_rules(self, name="default"):
        """
        List the named security group

        :param name: The name of the group, if None all will be returned
        :return:
        """
        raise NotImplementedError

    def upload_secgroup(self, name=None):
        raise NotImplementedError

    def add_secgroup(self, name=None, description=None):
        raise NotImplementedError

    def add_secgroup_rule(
        self, name=None, port=None, protocol=None, ip_range=None  # group name
    ):
        raise NotImplementedError

    def remove_secgroup(self, name=None):
        raise NotImplementedError

    def add_rules_to_secgroup(self, name=None, rules=None):
        raise NotImplementedError

    def remove_rules_from_secgroup(self, name=None, rules=None):
        raise NotImplementedError
