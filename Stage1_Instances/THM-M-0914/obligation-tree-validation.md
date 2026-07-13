# THM-M-0914 obligation-tree validation

Item: `S56-M-0914-OBLIGATION_TREE`.

Base revision: `f023dbc3411d83201065d1a1156d7406b81135d4`.

Base tree: `3b3a73ec19293a2a9b8d9c7e67f0d25da2a511b4`.

Validation date: `2026-07-13` (`Asia/Shanghai`).

## Result

Registry version 1 freezes 19 stable semantic obligations and 45 directed
edges across separate proof, refinement, provenance, evidence, trust,
documentation, and workflow graphs. Every `proof_requires` edge has a
reciprocal `composes` edge, the exact root reaches all ten mathematical route
nodes, and aliases and wrapper/terminal identities are deduplicated.

`instance.json` binds registry id `THM-M-0914-OBLIGATIONS-v1`, version 1,
denominator `5a421bbb...f3ce`, and all nine obligation-tree artifact roles. It
does not change lifecycle, accepted task state, root debt, or completion flags.

The architecture exposes the concrete `Fin` cardinal normalization, the
finite-type wrapper, the substantive finite-set terminal, the cardinal
injectivity bridge, and the terminal contradiction logic. All leaves have
substantive ledgers of at most 100 steps. Construction, extra branch,
computation, and transport-back exclusions are explicit and await independent
approval.

The checker composes `Statement.lean` with `ObligationTree.lean` in a temporary
file because the statement phase intentionally has no compiled local module.
The canonical root identity is checked by `rfl`. Thirteen local declarations
are machine-reported sorry-free; the conditional closure covers 1,897
declarations, reports only `propext`, `Classical.choice`, and `Quot.sound`, and
finds no bodyless nonaxiom or unsafe declaration. The pinned candidates remain
separate from the conditional root certificate.

The owned `ObligationTree.lean` also elaborates directly under the pinned Lake
environment. The actual-canonical identity is injected only by the composed
validator harness because the standalone file deliberately does not invent or
import an unbuilt local `Statement` module.

## Commands and results

All Lean validation reused the automation-provided canonical `.lake` symlink
read-only. No `lake update`, `lake build`, dependency clone/fetch, checkout,
installation, or `.lake` mutation ran.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | rev-5.6 structure and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique ordered targets passed |
| `python3 scripts/stage1_target.py show THM-M-0914` | 0 | rank 1456; planned; L0/rework-required; theorem incomplete |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base `f023dbc3...35d4`; tree `3b3a73ec...11b4` |
| `git status --short` before editing | 0 | only the pre-existing automation-provided `Formalizations/Lean/.lake` symlink was untracked |
| `python3 -B Stage1_Instances/THM-M-0914/build_obligation_artifacts.py` | 0 | wrote 19 obligations and 45 typed edges; denominator `5a421bbb...f3ce` |
| `LC_ALL=C TZ=UTC python3 -B Stage1_Instances/THM-M-0914/check_obligation_tree.py` | 0 | deterministic generation, schema, graphs, pins, source markers, Lean composition, receipt, and open-root boundary passed |
| `cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0914/ObligationTree.lean` | 0 | standalone conditional architecture passed with 12 sorry-free declarations and no missing local module |
| checker-composed `cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean <temporary>.lean` | 0 | exact statement identity and conditional composition passed; output SHA-256 `2d956604...30cb` |
| `python3 -m json.tool` on the registry, graph bundle, validation specs, receipt, and worker packet | 0 | all structured artifacts parsed |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0914-obligation-pycache python3 -m py_compile` on generator and checker | 0 | both Python files compiled without writing into the owned path |
| scoped comment/string-aware prohibited-construct scan | 1 (expected no match) | no placeholder, bodyless declaration, unsafe/opaque construct, oracle, external-code hook, or generated proof shortcut |
| scoped whitespace and text-byte checks | 0 | no trailing whitespace, CR, NUL, or missing final newline |
| `git diff --check -- Stage1_Instances/THM-M-0914 .stage1-worker-selftest.json` plus new-file checks | 0 / 1 expected | no whitespace diagnostics; no-index exits 1 only because each file is new |

The historical `check_statement.py` hard-codes the pre-anchor file inventory,
and `check_anchor_audit.py` expects the predecessor worker packet at the root.
Neither is an aggregate post-phase validator. This phase instead rechecks the
frozen statement and anchor hashes, actual canonical expression, immutable
mathlib pins and source markers, and the composed Lean declaration directly.

## Status boundary

This is provisional worker self-test evidence pending dependency-ordered master
acceptance. It freezes architecture and validates conditional interfaces only.
It does not install or accept the pinned proof bodies, promote `M0-W`, close
H0/R0 or release trust, finish `AUDIT-Z`, or complete the theorem. The accepted
root vector remains `[H1, M3, R4]`.
