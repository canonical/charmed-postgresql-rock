import yaml
import subprocess


def test_upload():
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


def test_all_apps():
    with open("rockcraft.yaml") as file:
        rockcraft = yaml.safe_load(file)
        name = rockcraft["name"]
        version = rockcraft["version"]
        major_version = version.split(".")[0]

        override = {
            "pgbackrest": "version",
        }

        apps = [
            "/usr/bin/createuser",
            "/usr/bin/pg_archivecleanup",
            "/usr/bin/pg_isready",
            "/usr/bin/pg_restore",
            "/usr/bin/pg_config",
            "/usr/bin/pg_dump",
            "/usr/bin/pg_recvlogical",
            "/usr/bin/pg_basebackup",
            f"/usr/lib/postgresql/{major_version}/bin/pg_ctl",
            "/usr/bin/pg_dumpall",
            "/usr/bin/pg_receivewal",
            "/usr/bin/pgbackrest",
            "/usr/bin/pgbench",
            "/usr/sbin/pgbouncer",
            "/usr/bin/psql",
            "/usr/bin/syncobj_admin",
        ]

        for app in apps:
            print(f"Running {app}...")
            try:
                subprocess.check_output(
                    [
                        "docker",
                        "run",
                        "--entrypoint",
                        app,
                        f"{name}:test",
                        override.get(app, "--help"),
                    ]
                )
            except subprocess.CalledProcessError as e:
                print(e)
                raise e


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
