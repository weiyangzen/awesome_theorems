#!/usr/bin/env python3
"""Run the Stage1 rev-5.6 Lean 4 execution queue safely.

The requirements source is ``Docs/Stage1_Blueprint_rev-5.6.md``.  Its generated
execution appendix is a rendering of the typed execution-state DAG in
``Docs/Stage1_Execution_DAG_rev-5.6.json``.  The JSON is deliberately kept in
the repository, rather than in `.cron`, so worker state, dependencies, and
acceptance history are reviewable and reproducible.

This program owns scheduler-only state below `.cron/stage1-rev56/`, which is
gitignored.  A worker never writes an accepted state: it produces a self-test
manifest and its isolated clone is queued for the integration owner.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import time
from collections import Counter, deque
from typing import Any, NoReturn


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "Docs"
BLUEPRINT = DOCS / "Stage1_Blueprint_rev-5.6.md"
TARGETS = DOCS / "Stage1_Targets_rev-5.6.json"
DAG = DOCS / "Stage1_Execution_DAG_rev-5.6.json"
RUNTIME = ROOT / ".cron" / "stage1-rev56"
CHECKLIST_BEGIN = "<!-- STAGE1-EXECUTION-CHECKLIST:BEGIN -->"
CHECKLIST_END = "<!-- STAGE1-EXECUTION-CHECKLIST:END -->"
PHASES = (
    ("intake", "Create the theorem dossier, scope map, and source-statement crosswalk."),
    ("statement", "Elaborate the exact Lean 4 target with the minimal pinned imports."),
    ("anchor_audit", "Audit mathlib and external Lean 4 candidates at immutable revisions."),
    ("obligation_tree", "Freeze the obligation registry and typed proof/provenance/workflow graphs."),
    ("proof", "Implement or pin/import the required proof bodies without placeholders."),
    ("validation", "Run hermetic kernel, trust, provenance, and independent validation gates."),
    ("release", "Reconcile evidence and decide the exact theorem-completion verdict."),
)
VALID_STATES = {"[ ]", "[_]", "[x]"}
MAX_WORKERS = 12


def fail(message: str) -> NoReturn:
    raise SystemExit(f"stage1_execution_cron: {message}")


def run(command: list[str], *, cwd: Path = ROOT, check: bool = True) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(command, cwd=cwd, text=True, capture_output=True)
    if check and result.returncode:
        detail = (result.stderr or result.stdout).strip()
        fail(f"command failed ({' '.join(command)}): {detail}")
    return result


def atomic_write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(text, encoding="utf-8")
    temporary.replace(path)


def read_json(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"cannot read {path.relative_to(ROOT)}: {exc}")
    if not isinstance(data, dict):
        fail(f"{path.relative_to(ROOT)} must contain a JSON object")
    return data


def target_rows() -> list[dict[str, Any]]:
    manifest = read_json(TARGETS)
    targets = manifest.get("targets")
    if not isinstance(targets, list) or len(targets) != 1546:
        fail("target manifest must contain exactly 1546 targets")
    if [target.get("execution_rank") for target in targets] != list(range(1, 1547)):
        fail("target manifest execution ranks are not contiguous")
    return targets


def task_id(theorem_id: str, phase: str) -> str:
    return f"S56-{theorem_id.removeprefix('THM-')}-{phase.upper()}"


def make_item(target: dict[str, Any], phase_index: int) -> dict[str, Any]:
    theorem_id = target["theorem_id"]
    phase, description = PHASES[phase_index]
    dependencies = [] if phase_index == 0 else [task_id(theorem_id, PHASES[phase_index - 1][0])]
    instance_dir = f"Stage1_Instances/{theorem_id}"
    return {
        "id": task_id(theorem_id, phase),
        "theorem_id": theorem_id,
        "execution_rank": target["execution_rank"],
        "phase": phase,
        "layer": phase_index,
        "state": "[ ]",
        "depends_on": dependencies,
        "owned_paths": [instance_dir],
        "deliverable": description,
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0,
        "children": [],
    }


def new_dag() -> dict[str, Any]:
    targets = target_rows()
    items = [make_item(target, phase) for target in targets for phase in range(len(PHASES))]
    ids = "\n".join(sorted(target["theorem_id"] for target in targets)) + "\n"
    return {
        "schema_version": "stage1-execution-dag/1.0",
        "requirements_source": "Docs/Stage1_Blueprint_rev-5.6.md",
        "target_manifest": "Docs/Stage1_Targets_rev-5.6.json",
        "target_id_set_sha256": hashlib.sha256(ids.encode()).hexdigest(),
        "state_protocol": {"not_done": "[ ]", "worker_self_tested": "[_]", "master_accepted": "[x]"},
        "items": items,
    }


def topological_order(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_id = {item.get("id"): item for item in items}
    if len(by_id) != len(items) or None in by_id:
        fail("execution DAG has duplicate or missing item ids")
    indegree = {item_id: 0 for item_id in by_id}
    children: dict[str, list[str]] = {item_id: [] for item_id in by_id}
    for item in items:
        dependencies = item.get("depends_on")
        if not isinstance(dependencies, list):
            fail(f"{item['id']} has invalid dependency list")
        for dependency in dependencies:
            if dependency not in by_id:
                fail(f"{item['id']} depends on missing item {dependency}")
            indegree[item["id"]] += 1
            children[dependency].append(item["id"])
    ready = deque(sorted((item_id for item_id, degree in indegree.items() if degree == 0), key=lambda i: (by_id[i]["layer"], by_id[i]["execution_rank"], i)))
    ordered: list[dict[str, Any]] = []
    while ready:
        item_id = ready.popleft()
        ordered.append(by_id[item_id])
        for child in sorted(children[item_id], key=lambda i: (by_id[i]["layer"], by_id[i]["execution_rank"], i)):
            indegree[child] -= 1
            if indegree[child] == 0:
                ready.append(child)
    if len(ordered) != len(items):
        fail("execution DAG contains a cycle")
    return ordered


def validate_dag(data: dict[str, Any]) -> list[dict[str, Any]]:
    if data.get("schema_version") != "stage1-execution-dag/1.0":
        fail("unsupported execution DAG schema")
    if data.get("requirements_source") != "Docs/Stage1_Blueprint_rev-5.6.md":
        fail("execution DAG requirements source is not the rev-5.6 blueprint")
    items = data.get("items")
    if not isinstance(items, list) or len(items) != 1546 * len(PHASES):
        fail(f"execution DAG must contain exactly {1546 * len(PHASES)} phase items")
    targets = target_rows()
    target_ids = {target["theorem_id"] for target in targets}
    items_by_target: dict[str, list[dict[str, Any]]] = {}
    for item in items:
        if not isinstance(item, dict) or item.get("state") not in VALID_STATES:
            fail("execution DAG contains an invalid item state")
        theorem_id = item.get("theorem_id")
        if theorem_id not in target_ids:
            fail(f"execution DAG item has unknown target {theorem_id}")
        if not isinstance(item.get("owned_paths"), list) or not item["owned_paths"]:
            fail(f"{item.get('id')} has no owned paths")
        items_by_target.setdefault(theorem_id, []).append(item)
    if set(items_by_target) != target_ids or any(len(group) != len(PHASES) for group in items_by_target.values()):
        fail("every target must have exactly one item per execution phase")
    for theorem_id, group in items_by_target.items():
        by_phase = {item.get("phase"): item for item in group}
        if set(by_phase) != {phase for phase, _ in PHASES}:
            fail(f"{theorem_id} has an invalid phase set")
        for index, (phase, _) in enumerate(PHASES):
            item = by_phase[phase]
            if item.get("id") != task_id(theorem_id, phase) or item.get("layer") != index:
                fail(f"{theorem_id}/{phase} has unstable identity or layer")
            expected = [] if index == 0 else [task_id(theorem_id, PHASES[index - 1][0])]
            if item.get("depends_on") != expected:
                fail(f"{theorem_id}/{phase} has invalid dependencies")
            if item["state"] == "[x]" and any(by_phase[prior]["state"] != "[x]" for prior, _ in PHASES[:index]):
                fail(f"{item['id']} is accepted before a dependency")
    return topological_order(items)


def render_checklist(items: list[dict[str, Any]]) -> str:
    lines = [
        CHECKLIST_BEGIN,
        "## 13. Generated 1546-Target Execution Checklist",
        "",
        "This appendix is generated by `scripts/stage1_execution_cron.py --bootstrap`. The typed DAG at",
        "`Docs/Stage1_Execution_DAG_rev-5.6.json` is the execution-state authority; this Markdown rendering",
        "is retained in the normative blueprint for inspection. Do not edit either surface by hand.",
        "",
        "Every target is expanded into seven dependency-ordered phases: intake, statement, anchor audit,",
        "obligation tree, proof, validation, and release. `[ ]` and `[_]` are unfinished; only the master",
        "integration lane may render `[x]` after all rev-5.6 receipts and gates pass.",
        "",
    ]
    for item in sorted(items, key=lambda row: (row["execution_rank"], row["layer"])):
        depends = ", ".join(f"`{dependency}`" for dependency in item["depends_on"]) or "none"
        paths = ", ".join(f"`{path}`" for path in item["owned_paths"])
        lines.append(
            f"- {item['state']} `{item['id']}` / `{item['theorem_id']}` / `{item['phase']}`: {item['deliverable']}"
        )
        lines.append(f"  Depends: {depends}. Owned paths: {paths}. Gate: {item['completion_gate']}.")
    lines.extend(["", CHECKLIST_END, ""])
    return "\n".join(lines)


def write_projection(data: dict[str, Any]) -> None:
    items = validate_dag(data)
    blueprint = BLUEPRINT.read_text(encoding="utf-8")
    rendered = render_checklist(items)
    if CHECKLIST_BEGIN in blueprint or CHECKLIST_END in blueprint:
        if CHECKLIST_BEGIN not in blueprint or CHECKLIST_END not in blueprint:
            fail("blueprint has malformed execution checklist markers")
        pattern = re.escape(CHECKLIST_BEGIN) + r".*?" + re.escape(CHECKLIST_END) + r"\n?"
        blueprint, count = re.subn(pattern, rendered, blueprint, count=1, flags=re.DOTALL)
        if count != 1:
            fail("blueprint execution checklist markers are ambiguous")
    else:
        blueprint = blueprint.rstrip() + "\n\n" + rendered
    atomic_write(BLUEPRINT, blueprint)


def bootstrap() -> None:
    data = read_json(DAG) if DAG.exists() else new_dag()
    validate_dag(data)
    atomic_write(DAG, json.dumps(data, ensure_ascii=False, indent=2) + "\n")
    write_projection(data)
    print(f"bootstrapped {len(data['items'])} phase items for 1546 targets")


def load_dag() -> tuple[dict[str, Any], list[dict[str, Any]]]:
    if not DAG.exists():
        fail("execution DAG is missing; run --bootstrap first")
    data = read_json(DAG)
    return data, validate_dag(data)


def runtime_path(name: str) -> Path:
    RUNTIME.mkdir(parents=True, exist_ok=True)
    return RUNTIME / name


def load_claims() -> list[dict[str, Any]]:
    path = runtime_path("claims.json")
    if not path.exists():
        return []
    claims = read_json(path).get("claims", [])
    if not isinstance(claims, list):
        fail("claim ledger is malformed")
    return [claim for claim in claims if isinstance(claim, dict)]


def save_claims(claims: list[dict[str, Any]]) -> None:
    atomic_write(runtime_path("claims.json"), json.dumps({"claims": claims}, indent=2) + "\n")


def pid_alive(pid: Any) -> bool:
    return isinstance(pid, int) and pid > 0 and Path(f"/proc/{pid}").exists()


def session_is_live(session: Any) -> bool:
    if not isinstance(session, str):
        return False
    result = run(["tmux", "list-panes", "-t", session, "-F", "#{pane_dead}"], check=False)
    return result.returncode == 0 and any(line.strip() == "0" for line in result.stdout.splitlines())


def refresh_claims(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    states = {item["id"]: item["state"] for item in items}
    kept: list[dict[str, Any]] = []
    released: list[dict[str, Any]] = []
    for claim in load_claims():
        if states.get(claim.get("item_id")) == "[x]":
            claim["released_at"] = dt.datetime.now(dt.timezone.utc).isoformat()
            claim["release_reason"] = "master_accepted"
            released.append(claim)
        elif claim.get("status") == "live" and (not pid_alive(claim.get("pid")) or not session_is_live(claim.get("session"))):
            session = claim.get("session")
            if isinstance(session, str):
                run(["tmux", "kill-session", "-t", session], check=False)
            manifest = Path(claim.get("workspace", "")) / ".stage1-worker-selftest.json"
            if manifest.exists():
                claim["status"] = "finished"
                claim["selftest_manifest"] = str(manifest.relative_to(ROOT)) if manifest.is_relative_to(ROOT) else str(manifest)
                kept.append(claim)
            else:
                claim["released_at"] = dt.datetime.now(dt.timezone.utc).isoformat()
                claim["release_reason"] = "worker_exited_without_selftest"
                released.append(claim)
        else:
            kept.append(claim)
    if released:
        audit = runtime_path("released_claims.jsonl")
        with audit.open("a", encoding="utf-8") as handle:
            for claim in released:
                handle.write(json.dumps(claim) + "\n")
    save_claims(kept)
    return kept


def trim_file(path: Path, max_bytes: int) -> None:
    if path.exists() and path.stat().st_size > max_bytes:
        with path.open("rb") as handle:
            handle.seek(-max_bytes, os.SEEK_END)
            tail = handle.read()
        temporary = path.with_suffix(path.suffix + ".tmp")
        temporary.write_bytes(tail)
        temporary.replace(path)


def space_guard(claims: list[dict[str, Any]]) -> None:
    min_free_gb = int(os.environ.get("MIN_FREE_GB", "30"))
    danger_free_gb = int(os.environ.get("DANGER_FREE_GB", "15"))
    max_log_mb = int(os.environ.get("MAX_LOG_MB", "20"))
    max_keepalive_mb = int(os.environ.get("MAX_KEEPALIVE_MB", "5"))
    max_root_gb = int(os.environ.get("MAX_CRON_ROOT_GB", "30"))
    retention_days = int(os.environ.get("LOG_RETENTION_DAYS", "3"))
    RUNTIME.mkdir(parents=True, exist_ok=True)
    now = time.time()
    for path in RUNTIME.rglob("*"):
        if not path.is_file():
            continue
        if path.name == "keepalive.log":
            trim_file(path, max_keepalive_mb * 1024 * 1024)
        elif path.suffix in {".log", ".out", ".err"}:
            if now - path.stat().st_mtime > retention_days * 86400:
                path.unlink(missing_ok=True)
            else:
                trim_file(path, max_log_mb * 1024 * 1024)
    usage = shutil.disk_usage(ROOT)
    free_gb = usage.free // (1024**3)
    root_bytes = sum(path.stat().st_size for path in RUNTIME.rglob("*") if path.is_file())
    state = {"free_gb": free_gb, "cron_root_gb": round(root_bytes / 1024**3, 3), "checked_at": dt.datetime.now(dt.timezone.utc).isoformat()}
    atomic_write(runtime_path("space_guard.json"), json.dumps(state, indent=2) + "\n")
    if free_gb < danger_free_gb:
        fail(f"blocked_disk_space: only {free_gb} GiB free (danger threshold {danger_free_gb})")
    if free_gb < min_free_gb:
        fail(f"blocked_disk_space: only {free_gb} GiB free (minimum {min_free_gb})")
    if root_bytes > max_root_gb * 1024**3:
        fail(f"blocked_disk_space: cron root exceeds {max_root_gb} GiB")


def sync_guard() -> None:
    status = run(["git", "status", "--porcelain"], check=True).stdout
    if status.strip():
        fail("blocked_sync: tracked or untracked local changes exist; refuse to stash user work automatically")
    run(["git", "fetch", "--prune", "origin"])
    upstream = run(["git", "rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}"]).stdout.strip()
    head = run(["git", "rev-parse", "HEAD"]).stdout.strip()
    remote = run(["git", "rev-parse", upstream]).stdout.strip()
    if head != remote:
        run(["git", "merge", "--ff-only", upstream])
        head = run(["git", "rev-parse", "HEAD"]).stdout.strip()
    if head != remote:
        fail("blocked_sync: local HEAD does not match remote tracking HEAD")


def task_prompt(item: dict[str, Any], workspace: Path) -> str:
    item_json = json.dumps(item, ensure_ascii=False, indent=2)
    return f"""You are Stage1 rev-5.6 worker for exactly one Lean 4 theorem execution task.

Repository root: {workspace}
Work only inside this worker automation clone: {workspace}
Do not edit the scheduler's authoritative checkout directly: {ROOT}

Active /goal: fully and truthfully expand and validate all 1546 metadata-screened Lean 4 targets under Docs/Stage1_Blueprint_rev-5.6.md. Do not claim theorem completion without every rev-5.6 gate and kernel evidence.

Your assigned item is the only item you may claim:
{item_json}

Required work:
1. Read Docs/Stage1_Blueprint_rev-5.6.md, skills/execute-stage1-rev56/SKILL.md, and the target manifest entry.
2. Complete the assigned phase with real source, Lean, and/or evidence artifacts under the item's owned path. You may inspect shared read-only sources, but never modify another target's owned path. Never use sorry, axiom, placeholder, fake results, or a broadened/substituted theorem.
3. Run the smallest real validation available and record exact commands/results in the owned artifact.
4. Do not edit Docs/Stage1_Execution_DAG_rev-5.6.json, the generated blueprint checklist, or any item state. You are a worker, never the master.
5. If and only if your assigned phase is genuinely self-tested, write `.stage1-worker-selftest.json` at the workspace root with item_id, changed_paths, commands, output_summary, base_revision, known_failures, and `state: "[_]"`. Otherwise leave no self-test manifest and explain the blocker in an owned artifact.
6. Do not commit, push, or modify unrelated targets. The integration lane will inspect this clone.
"""


def worker_command(workspace: Path, prompt_path: Path, output_path: Path) -> str:
    model = os.environ.get("CODEX_MODEL", "gpt-5.6-sol")
    effort = os.environ.get("CODEX_REASONING_EFFORT", "low")
    service_tier = os.environ.get("CODEX_SERVICE_TIER", "fast")
    return (
        f"cd {shlex_quote(str(workspace))} && "
        f"codex exec --cd {shlex_quote(str(workspace))} --model {shlex_quote(model)} "
        f"-c features.code_mode_host=false -c model_reasoning_effort={shlex_quote(effort)} "
        f"-c service_tier={shlex_quote(service_tier)} "
        f"--sandbox danger-full-access "
        f"< {shlex_quote(str(prompt_path))} > {shlex_quote(str(output_path))} 2>&1"
    )


def shlex_quote(value: str) -> str:
    import shlex

    return shlex.quote(value)


def prepare_workspace(slot: int) -> Path:
    workspace = RUNTIME / "workers" / f"slot{slot}"
    if workspace.exists():
        shutil.rmtree(workspace)
    workspace.parent.mkdir(parents=True, exist_ok=True)
    # Shared clones would inherit the 7.5 GiB local Lean build tree.  Create a lightweight
    # source-only worktree instead and let workers inspect the canonical local toolchain read-only.
    run([
        "git", "clone", "--no-checkout", "--filter=blob:none", "--reference-if-able", str(ROOT),
        str(ROOT), str(workspace),
    ], cwd=ROOT)
    run(["git", "checkout", "--detach", "HEAD"], cwd=workspace)
    for relative in (
        "Docs/Stage1_Blueprint_rev-5.6.md", "Docs/Stage1_Execution_DAG_rev-5.6.json",
        "Docs/Stage1_Targets_rev-5.6.json", "skills/execute-stage1-rev56/SKILL.md",
    ):
        source, destination = ROOT / relative, workspace / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)
    return workspace


def write_todo(data: dict[str, Any], ordered: list[dict[str, Any]], claims: list[dict[str, Any]]) -> Path:
    counts = Counter(item["state"] for item in ordered)
    claim_by_item = {claim.get("item_id"): claim for claim in claims}
    ready = []
    workers = []
    for item in ordered:
        claim = claim_by_item.get(item["id"])
        claim_state = "unclaimed" if claim is None else f"{claim.get('status')}:{claim.get('session', 'unknown')}"
        deps_done = all(next(row for row in ordered if row["id"] == dependency)["state"] == "[x]" for dependency in item["depends_on"])
        if item["state"] == "[_]":
            ready.append((item, claim_state, deps_done))
        elif item["state"] == "[ ]" and claim is None:
            workers.append((item, claim_state, deps_done))
    today = dt.date.today().strftime("%Y%m%d")
    path = DOCS / f"todos_{today}.md"
    lines = [
        "# Stage1 rev-5.6 Execution Todo",
        "",
        "Source: `Docs/Stage1_Blueprint_rev-5.6.md`; typed state: `Docs/Stage1_Execution_DAG_rev-5.6.json`.",
        f"Not done: {counts['[ ]']}",
        f"Worker self-tested: {counts['[_]']}",
        f"Master accepted: {counts['[x]']}",
        f"Unfinished: {counts['[ ]'] + counts['[_]']}",
        "DAG cycle check: passed.",
        f"Claim ledger: `.cron/stage1-rev56/claims.json`; live worker claims: {sum(c.get('status') == 'live' for c in claims)}.",
        "",
        "## Worker Claim Frontier",
        "",
        "| Item | Target | Phase | Dependencies accepted | Claim | Owned path |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for item, claim_state, deps_done in workers:
        lines.append(f"| `{item['id']}` | `{item['theorem_id']}` | {item['phase']} | {deps_done} | {claim_state} | `{item['owned_paths'][0]}` |")
    lines.extend(["", "## Master Integration Frontier", "", "| Item | Dependencies accepted | Claim |", "| --- | --- | --- |"])
    for item, claim_state, deps_done in ready:
        lines.append(f"| `{item['id']}` | {deps_done} | {claim_state} |")
    lines.append("")
    atomic_write(path, "\n".join(lines))
    return path


def validate_only() -> None:
    data, ordered = load_dag()
    claims = refresh_claims(ordered)
    space_guard(claims)
    todo = write_todo(data, ordered, claims)
    print("validate-only: ok")
    print(f"requirements_source=Docs/Stage1_Blueprint_rev-5.6.md")
    print(f"items={len(ordered)} targets=1546 states={dict(Counter(item['state'] for item in ordered))}")
    print(
        "platform=codex "
        f"model={os.environ.get('CODEX_MODEL', 'gpt-5.6-sol')} "
        f"reasoning_effort={os.environ.get('CODEX_REASONING_EFFORT', 'low')} "
        f"service_tier={os.environ.get('CODEX_SERVICE_TIER', 'fast')}"
    )
    print(f"todo={todo.relative_to(ROOT)}")


def integrate(limit: int) -> int:
    """Verify worker handoffs and advance only the worker cursor to `[_]`."""
    if limit < 1 or limit > MAX_WORKERS:
        fail(f"--limit must be in 1..{MAX_WORKERS}")
    data, ordered = load_dag()
    claims = refresh_claims(ordered)
    by_id = {item["id"]: item for item in data["items"]}
    ready = [claim for claim in claims if claim.get("status") == "finished"][:limit]
    accepted: list[str] = []
    rejected: list[dict[str, str]] = []
    queue: list[dict[str, Any]] = []
    for claim in ready:
        item = by_id.get(claim.get("item_id"))
        workspace = Path(str(claim.get("workspace", "")))
        handoff = workspace / ".stage1-worker-selftest.json"
        try:
            if item is None:
                raise ValueError("claim refers to unknown item")
            packet = json.loads(handoff.read_text(encoding="utf-8"))
            changed_paths = packet.get("changed_paths")
            owner = item["owned_paths"][0] + "/"
            if packet.get("item_id") != item["id"] or packet.get("state") != "[_]":
                raise ValueError("worker packet identity/state mismatch")
            if not isinstance(changed_paths, list) or not changed_paths:
                raise ValueError("worker packet lacks changed paths")
            allowed_worker_metadata = {".stage1-worker-selftest.json"}
            if any(
                not isinstance(path, str)
                or (not path.startswith(owner) and path not in allowed_worker_metadata)
                or ".." in Path(path).parts
                for path in changed_paths
            ):
                raise ValueError("worker paths escape the assigned ownership scope")
            source = workspace / item["owned_paths"][0]
            destination = ROOT / item["owned_paths"][0]
            if not source.is_dir() or destination.exists():
                raise ValueError("worker source missing or main owned path conflicts")
            records = [*source.rglob("*.json"), *source.rglob("*.yaml"), *source.rglob("*.yml")]
            if not records or not any(item["theorem_id"] in record.read_text(encoding="utf-8", errors="ignore") for record in records):
                raise ValueError("no target-identifying structured evidence record")
            shutil.copytree(source, destination)
            item["state"] = "[_]"
            item["attempts"] = int(item.get("attempts", 0)) + 1
            claim["status"] = "finished_integrated"
            claim["integrated_at"] = dt.datetime.now(dt.timezone.utc).isoformat()
            accepted.append(item["id"])
            queue.append({"item_id": item["id"], "theorem_id": item["theorem_id"], "state": "[_]", "owned_paths": item["owned_paths"], "changed_paths": changed_paths, "commands": packet.get("commands", []), "known_failures": packet.get("known_failures", [])})
        except (OSError, ValueError, json.JSONDecodeError) as exc:
            claim["status"] = "rejected"
            claim["rejected_at"] = dt.datetime.now(dt.timezone.utc).isoformat()
            # Preserve the reason in the durable claim ledger as well as the
            # per-tick queue, which is deliberately overwritten on each run.
            claim["rejection_reason"] = str(exc)
            rejected.append({"item_id": str(claim.get("item_id")), "reason": str(exc)})
    if accepted:
        run(["python3", "Docs/tools/check_stage1_standard.py"])
        run(["python3", "scripts/stage1_target.py", "check"])
        atomic_write(DAG, json.dumps(data, ensure_ascii=False, indent=2) + "\n")
        write_projection(data)
    save_claims(claims)
    atomic_write(runtime_path("integration_queue.json"), json.dumps({"queued": queue, "rejected": rejected}, ensure_ascii=False, indent=2) + "\n")
    todo = write_todo(data, validate_dag(data), claims)
    print(f"integrate: worker-self-tested={len(accepted)} rejected={len(rejected)} todo={todo.relative_to(ROOT)}")
    return len(accepted)


def checkpoint_integration() -> None:
    """Checkpoint a verified worker-cursor batch before refilling worker slots."""
    run(["git", "add", "Docs/Stage1_Blueprint_rev-5.6.md", "Docs/Stage1_Execution_DAG_rev-5.6.json", "Stage1_Instances"])
    staged = run(["git", "diff", "--cached", "--name-only"]).stdout.splitlines()
    if not staged:
        return
    forbidden = [path for path in staged if path.startswith((".cron/", ".ops/", "tests/", "spec/"))]
    if forbidden:
        fail(f"checkpoint refuses private/test paths: {forbidden}")
    if any(
        not path.startswith("Stage1_Instances/")
        and path not in {"Docs/Stage1_Blueprint_rev-5.6.md", "Docs/Stage1_Execution_DAG_rev-5.6.json"}
        for path in staged
    ):
        fail("checkpoint includes a path outside the Stage1 integration surface")
    run(["git", "commit", "-m", "Integrate Stage1 worker evidence batch"])
    run(["git", "push", "origin", "main"])
    sync_guard()


def launch(max_workers: int) -> None:
    if max_workers < 1 or max_workers > MAX_WORKERS:
        fail(f"--workers must be in 1..{MAX_WORKERS}")
    # A tick begins clean/synced, then drains handoffs, checkpoints them, and only then
    # refills worker capacity. This preserves the worker/master dual cursor across cron ticks.
    sync_guard()
    integrated = integrate(max_workers)
    if integrated:
        checkpoint_integration()
    data, ordered = load_dag()
    claims = refresh_claims(ordered)
    space_guard(claims)
    live = [claim for claim in claims if claim.get("status") == "live"]
    # A slot owns its clone.  Never derive a slot from the count of live claims:
    # claims can finish out of order, leaving holes, and reusing an occupied slot
    # would make two Codex processes write the same worker checkout/manifest.
    occupied_slots = {
        claim.get("slot")
        for claim in live
        if isinstance(claim.get("slot"), int) and 1 <= claim["slot"] <= max_workers
    }
    available_slots = [slot for slot in range(1, max_workers + 1) if slot not in occupied_slots]
    capacity = len(available_slots)
    if capacity <= 0:
        print(f"tick: saturated ({len(live)}/{max_workers} live workers)")
        write_todo(data, ordered, claims)
        return
    claimed_ids = {
        claim.get("item_id")
        for claim in claims
        if claim.get("status") in {"live", "finished", "finished_integrated"}
    }
    candidates = [item for item in ordered if item["state"] == "[ ]" and item["id"] not in claimed_ids]
    selected = candidates[:capacity]
    if not selected:
        print("tick: no unclaimed work")
        write_todo(data, ordered, claims)
        return
    timestamp = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    for slot, item in zip(available_slots, selected):
        workspace = prepare_workspace(slot)
        prompt = RUNTIME / "prompts" / f"{item['id']}.txt"
        output = RUNTIME / "logs" / f"{item['id']}.out"
        prompt.parent.mkdir(parents=True, exist_ok=True)
        output.parent.mkdir(parents=True, exist_ok=True)
        atomic_write(prompt, task_prompt(item, workspace))
        session = f"stage1r56-{slot}-{item['execution_rank']:04d}"
        run(["tmux", "kill-session", "-t", session], check=False)
        command = worker_command(workspace, prompt, output)
        run(["tmux", "new-session", "-d", "-s", session, "bash", "-lc", command])
        pid_result = run(["tmux", "list-panes", "-t", session, "-F", "#{pane_pid}"], check=False)
        pid_text = pid_result.stdout.strip()
        claims.append({
            "item_id": item["id"], "theorem_id": item["theorem_id"], "depends_on": item["depends_on"],
            "owned_paths": item["owned_paths"], "session": session, "slot": slot, "workspace": str(workspace),
            "status": "live", "pid": int(pid_text) if pid_text.isdigit() else None, "claimed_at": timestamp,
        })
    save_claims(claims)
    todo = write_todo(data, ordered, claims)
    print(f"tick: launched {len(selected)} worker(s), live={len(live) + len(selected)}/{max_workers}, todo={todo.relative_to(ROOT)}")


def cleanup() -> None:
    data, ordered = load_dag()
    claims = refresh_claims(ordered)
    counts = Counter(item["state"] for item in ordered)
    todo = DOCS / f"todos_{dt.date.today():%Y%m%d}.md"
    unfinished_zero = todo.exists() and "Unfinished: 0" in todo.read_text(encoding="utf-8")
    if counts["[ ]"] or counts["[_]"] or claims or not unfinished_zero:
        fail("cleanup refused: unfinished work, active/pending claims, or stale todo remains")
    cron = run(["crontab", "-l"], check=False)
    lines = [line for line in cron.stdout.splitlines() if "stage1_execution_cron.py" not in line]
    subprocess.run(["crontab", "-"], input="\n".join(lines) + "\n", text=True, check=True)
    atomic_write(runtime_path("cleanup.json"), json.dumps({"state": "completed", "at": dt.datetime.now(dt.timezone.utc).isoformat()}, indent=2) + "\n")
    print("cleanup: removed Stage1 execution cron entry")


def install(schedule: str) -> None:
    if not re.fullmatch(r"[^\n]+", schedule):
        fail("schedule must be one crontab line prefix")
    command = f"{schedule} cd {ROOT} && {ROOT / 'scripts' / 'stage1_execution_cron.py'} --tick --workers {MAX_WORKERS} >> {RUNTIME / 'keepalive.log'} 2>&1 # stage1_execution_cron.py"
    current = run(["crontab", "-l"], check=False).stdout.splitlines()
    current = [line for line in current if "stage1_execution_cron.py" not in line]
    subprocess.run(["crontab", "-"], input="\n".join(current + [command]) + "\n", text=True, check=True)
    print("install: cron entry installed")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    modes = parser.add_mutually_exclusive_group(required=True)
    modes.add_argument("--bootstrap", action="store_true", help="generate the typed 1546-target execution DAG and blueprint appendix")
    modes.add_argument("--validate-only", action="store_true", help="validate DAG, state, budgets, and todo without syncing or spawning workers")
    modes.add_argument("--integrate", action="store_true", help="verify completed worker handoffs and advance them to worker-self-tested")
    modes.add_argument("--tick", action="store_true", help="sync, refill the tmux Codex worker lanes, and refresh todo")
    modes.add_argument("--cleanup", action="store_true", help="remove the cron entry only after every completion gate is true")
    modes.add_argument("--install", action="store_true", help="install a bounded scheduler cron entry")
    parser.add_argument("--workers", type=int, default=MAX_WORKERS, help=f"maximum concurrent tmux Codex workers (1..{MAX_WORKERS})")
    parser.add_argument("--limit", type=int, default=MAX_WORKERS, help=f"maximum worker handoffs integrated by --integrate (1..{MAX_WORKERS})")
    parser.add_argument("--schedule", default="*/10 * * * *", help="crontab schedule used by --install")
    args = parser.parse_args()
    if args.bootstrap:
        bootstrap()
    elif args.validate_only:
        validate_only()
    elif args.integrate:
        integrate(args.limit)
    elif args.tick:
        launch(args.workers)
    elif args.cleanup:
        cleanup()
    else:
        install(args.schedule)


if __name__ == "__main__":
    main()
