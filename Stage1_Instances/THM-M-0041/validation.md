# Intake validation

Base revision: `dc2eb1390c8f2a88e7afcbdbd35f92ab43f64fb8` (tree
`25138aaafcff80ee47bf04805bccd804978e6754`). Validation date: 2026-07-13
(Asia/Shanghai).

This validation covers manifest membership, the planned dossier, selected scope and explicit
ambiguity boundary, source-statement crosswalk, six-node open task DAG, JSON/scoped invariants, and
a narrow pinned Lean candidate API and axiom probe. It does not validate a canonical Cayley-Hamilton
Lean target or proof because the statement gate, exact source transport, body provenance, and trust
closure remain open. The automation-provided canonical `.lake` symlink was pre-existing and used
read-only; no dependency update, build, clone, fetch, or other `.lake` mutation was performed. This
dirty worker evidence is nonrelease evidence.

## Environment

- Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, target
  `x86_64-unknown-linux-gnu`.
- Lake `5.0.0-src+98dc76e`.
- Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; package source status was clean.
- `lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

## Commands and results

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | all 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0041` | 0 | rank 1081, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| `git status --short --untracked-files=all` | 0 | preflight contained only the automation-provided untracked `Formalizations/Lean/.lake` symlink |
| `git blame -L 314,319 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog lines originate at commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `curl -L --fail --silent --show-error --max-time 20 https://api.crossref.org/works/10.1098/rstl.1858.0002` | 0 | identified Cayley's 1858 primary-publication lead and abstract; no immutable theorem/proof passage or H0 packet accepted |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | 0 | versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | 0 | pinned revision and tree recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | 0 | empty output |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | 0 | hashes recorded above |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0041/IntakeProbe.lean)` | 0 | eight matrix/polynomial/linear-map APIs elaborated; both candidate axiom reports were `[propext, Classical.choice, Quot.sound]` |
| `python3 -m json.tool` on `instance.json`, `task-dag.json`, `intake-receipt.json`, and `.stage1-worker-selftest.json` | 0 | all finalized structured artifacts are valid JSON |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0041-pycache python3 -m py_compile Stage1_Instances/THM-M-0041/check_intake.py` | 0 | scoped validator compiled without generated files in the owned path |
| `python3 -B Stage1_Instances/THM-M-0041/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | manifest/DAG identity, planned H1/M3/R3 boundary, source and pin hashes, exact artifact inventory, receipt packet, and six open tasks agree |
| prohibited Lean construct scan over the owned path | 1 | expected no-match exit; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| `git diff --check -- Stage1_Instances/THM-M-0041 .stage1-worker-selftest.json` plus scoped new-file checks | 0 | no whitespace diagnostics |

## Known downstream failures

- No immutable primary theorem/proof passage has been admitted and independently reviewed with
  coefficient-domain, definition, assumption, conclusion, attribution, proof-boundary, and errata
  mapping.
- The conventional commutative-ring finite square-matrix scope is selected but not yet ratified by
  a source packet; empty index, zero ring, characteristic-polynomial convention, and matrix-algebra
  evaluation remain statement-gate decisions.
- No canonical Lean expression or environment fingerprint, checked matrix/endomorphism transport,
  or four-class statement mutation has been accepted.
- Formal anchor and terminal-body provenance audit, discovery protocol, obligation registry, typed
  graphs, composition, readable reconstruction, hermetic replay, deterministic bundle, independent
  verification, master acceptance, audit completion, and theorem completion remain open.

These failures do not invalidate a truthful, self-tested `planned` intake. Only the integration lane
may accept the provisional node receipt.
