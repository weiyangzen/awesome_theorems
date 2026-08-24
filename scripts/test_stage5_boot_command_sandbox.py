#!/usr/bin/env python3
"""Independent conformance tests for the Stage5 BOOT command sandbox."""

from __future__ import annotations

import base64
import hashlib
import json
import os
from pathlib import Path
import signal
import sys
import tempfile
import unittest
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import stage5_boot_command_sandbox as sandbox


CONFORMANCE_ID = "stage5-boot-manager-conformance-v1"
PYTHON = "/usr/bin/python3.12"


class Stage5BootCommandSandboxTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory(
            prefix="stage5-boot-command-sandbox-test-"
        )
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name) / "repo"
        self.root.mkdir()
        self.probe = self.root / "probe.py"
        self.probe.write_text(
            "import sys\n"
            "sys.stdout.buffer.write(b'stdout-evidence\\n')\n"
            "sys.stderr.buffer.write(b'stderr-evidence\\n')\n",
            encoding="utf-8",
        )

    def manifest(self) -> dict[str, object]:
        return sandbox.seal_snapshot_manifest(
            self.root,
            ["probe.py"],
            executable_paths={PYTHON: sandbox.PINNED_HOST_TOOLS[PYTHON]},
        )

    def command(self, manifest: dict[str, object]) -> dict[str, object]:
        return sandbox.make_command_spec(
            manifest,
            command_id="manager-conformance",
            argv=[PYTHON, "-I", "-B", "probe.py"],
            timeout_seconds=10,
            conformance_id=CONFORMANCE_ID,
        )

    def test_manifest_and_command_spec_are_closed_and_fail_closed(self) -> None:
        manifest = self.manifest()
        spec = self.command(manifest)
        self.assertEqual(set(spec), sandbox._COMMAND_FIELDS)
        self.assertEqual(spec["argv"], [PYTHON, "-I", "-B", "probe.py"])
        self.assertEqual(spec["cwd"], ".")
        self.assertIs(spec["shell"], False)
        self.assertEqual(spec["stdin"], "devnull")
        self.assertEqual(spec["timeout_seconds"], 10.0)
        self.assertEqual(spec["max_output_bytes"], sandbox.MAX_OUTPUT_BYTES)
        self.assertEqual(spec["conformance_id"], CONFORMANCE_ID)
        self.assertRegex(str(spec["snapshot_manifest_sha256"]), r"^[0-9a-f]{64}$")
        self.assertRegex(str(spec["authority_sha256"]), r"^[0-9a-f]{64}$")

        invalid = (
            {"command_id": "../alias"},
            {"argv": ["python3", "probe.py"]},
            {"argv": ["/bin/sh", "probe.py"]},
            {"argv": [PYTHON, "-c", "print('not a sealed input')"]},
            {"argv": [PYTHON, "-m", "unsealed_module"]},
            {"timeout_seconds": 0},
            {"timeout_seconds": sandbox.MAX_TIMEOUT_SECONDS + 1},
            {"conformance_id": "producer-self-test"},
        )
        baseline = {
            "command_id": "manager-conformance",
            "argv": [PYTHON, "-I", "-B", "probe.py"],
            "timeout_seconds": 10,
            "conformance_id": CONFORMANCE_ID,
        }
        for mutation in invalid:
            with self.subTest(mutation=mutation), self.assertRaises(
                sandbox.SandboxError
            ):
                sandbox.make_command_spec(manifest, **{**baseline, **mutation})

    def test_snapshot_input_drift_is_rejected_before_any_spawn(self) -> None:
        manifest = self.manifest()
        spec = self.command(manifest)
        self.probe.write_text("raise SystemExit(0)\n", encoding="utf-8")
        with (
            mock.patch.object(
                sandbox.subprocess,
                "Popen",
                side_effect=AssertionError("spawn occurred before snapshot check"),
            ) as popen,
            self.assertRaisesRegex(sandbox.SandboxError, "snapshot|drift|sha256"),
        ):
            sandbox.run_suite(self.root, manifest, [spec])
        popen.assert_not_called()

    def test_success_result_is_closed_and_contains_complete_output_evidence(
        self,
    ) -> None:
        manifest = self.manifest()
        spec = self.command(manifest)
        try:
            result = sandbox.run_suite(self.root, manifest, [spec])
        except sandbox.SandboxError as exc:
            if "systemd" in str(exc).lower() and any(
                word in str(exc).lower()
                for word in ("unavailable", "permission", "connect", "establish")
            ):
                self.skipTest(f"systemd sandbox is unavailable: {exc}")
            raise

        self.assertEqual(
            set(result),
            {
                "schema_version",
                "snapshot_manifest_sha256",
                "sandbox_policy_sha256",
                "commands",
                "suite_conformance_id",
                "side_effects_absent",
                "authority_sha256",
            },
        )
        self.assertEqual(result["suite_conformance_id"], CONFORMANCE_ID)
        self.assertIs(result["side_effects_absent"], True)
        self.assertEqual(len(result["commands"]), 1)
        command = result["commands"][0]
        self.assertEqual(command["command_id"], "manager-conformance")
        self.assertEqual(command["exit_code"], 0)
        self.assertIs(command["timed_out"], False)
        self.assertIs(command["descendants_absent"], True)
        expected = {"stdout": b"stdout-evidence\n", "stderr": b"stderr-evidence\n"}
        for stream, raw in expected.items():
            with self.subTest(stream=stream):
                encoded = command[f"{stream}_base64"]
                self.assertEqual(base64.b64decode(encoded, validate=True), raw)
                self.assertEqual(command[f"{stream}_size"], len(raw))
                self.assertEqual(
                    command[f"{stream}_sha256"], hashlib.sha256(raw).hexdigest()
                )
                self.assertIs(command[f"{stream}_complete"], True)

    def test_read_only_compile_helper_does_not_write_snapshot(self) -> None:
        helper = self.root / "compile_check.py"
        helper.write_text(
            "from pathlib import Path\n"
            "source=Path('probe.py').read_text(encoding='utf-8')\n"
            "compile(source,'probe.py','exec',dont_inherit=True,optimize=0)\n",
            encoding="utf-8",
        )
        manifest = sandbox.seal_snapshot_manifest(
            self.root,
            ["compile_check.py", "probe.py"],
            executable_paths={PYTHON: sandbox.PINNED_HOST_TOOLS[PYTHON]},
        )
        spec = sandbox.make_command_spec(
            manifest,
            command_id="read-only-compile",
            argv=[PYTHON, "-I", "-B", "compile_check.py"],
            timeout_seconds=10,
            conformance_id=CONFORMANCE_ID,
        )
        result = sandbox.run_suite(self.root, manifest, [spec])
        self.assertEqual(result["commands"][0]["exit_code"], 0)
        self.assertFalse((self.root / "__pycache__").exists())
        self.assertFalse((self.root / "probe.pyc").exists())

    def run_fixture(self, source: str, *, timeout: float = 10) -> dict[str, object]:
        self.probe.write_text(source, encoding="utf-8")
        manifest = self.manifest()
        spec = sandbox.make_command_spec(
            manifest,
            command_id="fixture",
            argv=[PYTHON, "-I", "-B", "probe.py"],
            timeout_seconds=timeout,
            conformance_id=CONFORMANCE_ID,
        )
        return sandbox.run_suite(self.root, manifest, [spec])

    def test_candidate_cannot_mutate_live_tree_host_tmp_or_open_network(self) -> None:
        sentinel = self.root / "sentinel"
        sentinel.write_bytes(b"canonical\n")
        marker = f"stage5-boot-malicious-{os.getpid()}"
        source = f'''import json,os,socket
attempts={{}}
for name,path in [
 ("live", {str(sentinel)!r}),
 ("runtime", {str(self.root / ".ops/escape")!r}),
 ("host_tmp", {str(Path("/tmp") / marker)!r}),
]:
 try:
  os.makedirs(os.path.dirname(path),exist_ok=True)
  with open(path,"wb") as stream:stream.write(b"escape")
  attempts[name]=False
 except OSError:attempts[name]=True
for name,family in [("inet",socket.AF_INET),("inet6",socket.AF_INET6)]:
 try:s=socket.socket(family,socket.SOCK_STREAM);s.close();attempts[name]=False
 except OSError:attempts[name]=True
print(json.dumps(attempts,sort_keys=True))
'''
        result = self.run_fixture(source)
        observed = json.loads(
            base64.b64decode(result["commands"][0]["stdout_base64"], validate=True)
        )
        self.assertEqual(observed, {
            "host_tmp": True, "inet": True, "inet6": True,
            "live": True, "runtime": True,
        })
        self.assertEqual(sentinel.read_bytes(), b"canonical\n")
        self.assertFalse((self.root / ".ops").exists())
        self.assertFalse((Path("/tmp") / marker).exists())

    def test_output_overflow_fails_closed_with_bounded_evidence(self) -> None:
        self.probe.write_text(
            f"import os\nos.write(1,b'x'*{sandbox.MAX_OUTPUT_BYTES + 1})\n",
            encoding="utf-8",
        )
        manifest = self.manifest()
        spec = self.command(manifest)
        with self.assertRaisesRegex(sandbox.SandboxError, "output bound") as raised:
            sandbox.run_suite(self.root, manifest, [spec])
        evidence = raised.exception.evidence
        self.assertIsNotNone(evidence)
        assert evidence is not None
        self.assertIs(evidence["output_overflow"], True)
        self.assertIs(evidence["stdout_complete"], False)
        self.assertLessEqual(evidence["stdout_size"], sandbox.MAX_OUTPUT_BYTES)

    def test_timeout_kills_complete_service_cgroup(self) -> None:
        # The child ignores TERM and outlives its parent unless the controller
        # kills the complete transient-service cgroup.
        source = '''import os,signal,time
pid=os.fork()
if pid==0:
 signal.signal(signal.SIGTERM,signal.SIG_IGN)
 while True:time.sleep(1)
while True:time.sleep(1)
'''
        self.probe.write_text(source, encoding="utf-8")
        manifest = self.manifest()
        spec = sandbox.make_command_spec(
            manifest,
            command_id="timeout",
            argv=[PYTHON, "-I", "-B", "probe.py"],
            timeout_seconds=0.2,
            conformance_id=CONFORMANCE_ID,
        )
        with self.assertRaisesRegex(sandbox.SandboxError, "timed out") as raised:
            sandbox.run_suite(self.root, manifest, [spec])
        evidence = raised.exception.evidence
        self.assertIsNotNone(evidence)
        assert evidence is not None
        self.assertIs(evidence["timed_out"], True)
        self.assertIs(evidence["descendants_absent"], True)


if __name__ == "__main__":
    unittest.main()
