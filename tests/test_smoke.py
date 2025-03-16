import yaml
import subprocess
import pytest


def test_install():
    with open("rockcraft.yaml") as file:
        rockcraft = yaml.safe_load(file)
        name = rockcraft["name"]
        version = rockcraft["version"]

        subprocess.run(
            [
                "skopeo",
                "copy",
                f"oci-archive:{name}_{version}_amd64.rock",
                f"docker-daemon:{name}:test",
            ]
        )


@pytest.mark.run(after="test_install")
def test_all_apps():
    pass


@pytest.mark.run(after="test_install")
def test_all_services():
    pass


@pytest.mark.run(after="test_install")
def test_version():
    with open("rockcraft.yaml") as file:
        rockcraft = yaml.safe_load(file)
        name = rockcraft["name"]
        version = rockcraft["version"]
        app_version = (
            subprocess.check_output(
                [
                    "docker",
                    "run",
                    "--entrypoint",
                    "/usr/bin/pg_isready",
                    f"{name}:test",
                    "--version",
                ]
            )
            .decode()
            .split(" ")[2]
        )
        assert version == app_version
