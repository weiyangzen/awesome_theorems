# Intake validation

Validation date: 2026-07-13 (Asia/Shanghai).
Base revision: `0e5ae82e6d507ee607c3f011900571ffd8096800`.
Base tree: `400e6edf1f69b971b60a367e3ea29be359b07907`.

This validation covers target membership, the planned dossier and open task DAG, repository-source
provenance, statement-ambiguity and neighbor boundaries, JSON and scoped invariants, a narrow
pinned Lean API/axiom probe, prohibited-construct hygiene, and whitespace. It does not validate a
canonical theorem statement or proof.

The preflight worktree contained only the automation-provided untracked
`Formalizations/Lean/.lake` symlink to canonical pinned artifacts. It was used read-only. No
`lake update`, `lake build`, dependency clone or fetch, network-triggering Lake operation, or other
`.lake` mutation was performed. The owned intake files and worker packet make the final snapshot
dirty and nonrelease.

## Environment

- Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, target
  `x86_64-unknown-linux-gnu`.
- Lake `5.0.0-src+98dc76e`.
- Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; package status was clean.
- `lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

## Commands and results

Commands without an explicit working directory ran at repository root.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0635` | 0 | rank 1328; planned; no legacy slot; legacy artifacts unaccepted; theorem_complete false |
| `git status --short --untracked-files=all` (preflight) | 0 | only `?? Formalizations/Lean/.lake`; preserved read-only |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base revision and tree shown above |
| `git blame -L 4706,4711 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| scoped inspection of the rev-5.6 standard, skill, manifest, DAG, catalog, Stage0 projection, and neighboring targets | 0 | compact-domain two-sided extrema family identified; nonemptiness, domain, codomain, continuity encoding, binders, and exact conclusion remain source decisions |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | versions recorded above; no update or build run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | 0 | pinned revision and tree recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | 0 | empty output; package worktree clean |
| bounded `rg` search for extreme-value and compact-extremum interfaces in repo-local Lean and pinned mathlib | 0 | direct generic `IsCompact.exists_isMinOn` and `IsCompact.exists_isMaxOn` leads found; no THM-M-0635 root found; intake discovery only |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0635/IntakeProbe.lean` | 0 | nine adjacent APIs elaborated; both proof-bearing leads report `[propext, Classical.choice, Quot.sound]`; stdout SHA-256 `ed046c98...9b929`; no target theorem declared |
| `python3 -m json.tool` on `instance.json`, `task-dag.json`, `intake-receipt.json`, and `.stage1-worker-selftest.json` | 0 | all finalized structured artifacts are valid JSON |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0635-pycache python3 -m py_compile Stage1_Instances/THM-M-0635/check_intake.py` | 0 | scoped validator compiled without generated files under the owned path |
| `python3 -B Stage1_Instances/THM-M-0635/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | manifest/DAG identity, planned H1/M3/R4 boundary, null root, source and pin hashes, artifact packet, and six open tasks agree |
| `python3 -B Stage1_Instances/THM-M-0635/check_intake.py` | 0 | packet-free public replay passed |
| prohibited Lean construct scan over the owned path | 1 (expected no match) | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| `git diff --check -- Stage1_Instances/THM-M-0635 .stage1-worker-selftest.json` plus scoped new-file checks | 0 | no whitespace, final-newline, CR, NUL, or trailing-space defect |

## Known open gates

No immutable primary or authoritative proof source, exact theorem and incorporated-definition
locator, assumption/proof-boundary/translation/errata crosswalk, or independent source review has
been admitted. The exact canonical human proposition, minimal Lean imports, combined root
expression, expression and environment fingerprints, checked transports, and statement mutations
remain open.

The direct pinned mathlib candidates establish useful `M3` formal support only. Exhaustive
repo-local, mathlib, and external anchor inventory, source identity, terminal-body provenance,
obligation registry, typed graphs, proof integration, composition, trust closure, readable
reconstruction, hermetic replay, deterministic bundle, independent verification, master
acceptance, audit completion, and theorem completion remain open. These failures do not invalidate
a truthful self-tested `planned` intake.
