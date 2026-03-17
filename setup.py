import sys
import subprocess
from pathlib import Path
from setuptools import setup
from setuptools.command.build_py import build_py as _build_py
from setuptools.command.develop import develop as _develop

# Clear up old generated protos before regenerating
for pyi_file in Path("src/ark_msgs").rglob("*.pyi"):
    if pyi_file.name.endswith("_pb2.pyi") or pyi_file.name.endswith("_pb2_grpc.pyi"):
        pyi_file.unlink()
for py_file in Path("src/ark_msgs").rglob("*.py"):
    if py_file.name.endswith("_pb2.py") or py_file.name.endswith("_pb2_grpc.py"):
        py_file.unlink()

PKG_PROTO_ROOT = Path("proto")


def compile_protos() -> None:
    protos = sorted(PKG_PROTO_ROOT.rglob("*.proto"))
    if not protos:
        return

    cmd = [
        sys.executable,
        "-m",
        "grpc_tools.protoc",
        f"-I{PKG_PROTO_ROOT}",
        f"--python_out=src",
        f"--pyi_out=src",
        *[str(p) for p in protos],
    ]
    subprocess.check_call(cmd)


class build_py(_build_py):
    def run(self):
        compile_protos()
        super().run()


class develop(_develop):
    def run(self):
        compile_protos()
        super().run()


setup(
    cmdclass={"build_py": build_py, "develop": develop},
)
