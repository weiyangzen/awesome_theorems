# Intake validation

Base revision: `fb0baac89ea0633612be3b47448464b4b8e4bef7`; base tree:
`018557070da18ea1733a82de81a238750c59aa84`.

This validation covers target membership, the planned dossier, source and scope discrimination,
the open downstream task DAG, pinned environment identity, adjacent Lean API elaboration, bounded
local name search, JSON and scoped invariants, proof-escape hygiene, and whitespace. Because the
repository record supplies no stable proposition, no canonical target, expression hash, statement
mutation, source acceptance, or proof is claimed.

The automation-provided `Formalizations/Lean/.lake` symlink to canonical pinned artifacts was
present before edits and used read-only. No `lake update`, `lake build`, dependency clone or fetch,
or other `.lake` mutation was performed. The symlink makes this nonrelease worker evidence.

## Environment

- Platform: Linux 7.0.0-27-generic, x86_64; Lean target `x86_64-unknown-linux-gnu`.
- Lean: `4.29.0`, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`.
- Lake: `5.0.0-src+98dc76e`.
- Pinned mathlib: `8a178386ffc0f5fef0b77738bb5449d50efeea95`; tree
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; package worktree clean.
- `Formalizations/Lean/lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `Formalizations/Lean/lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

## Commands and results

| Command (repository root unless noted) | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0932` | 0 | rank 1471, planned, L0/rework_required, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| initial `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the pre-existing `.lake` symlink; base revision and tree recorded above |
| `git blame -L 6812,6817 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog fields originate at commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| Crossref and Elsevier core metadata inspection for DOI `10.1016/j.exmath.2006.07.002` | 0 | Gao-Geroldinger 2006 subject-reference lead identified; metadata digests recorded; no exact proposition or H0 credited |
| `lake env lean --version`; `lake --version` (`cwd=Formalizations/Lean`) | 0 | pinned Lean and Lake versions above; no update or build run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned revision/tree above; package source clean |
| `LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0932/IntakeProbe.lean` (`cwd=Formalizations/Lean`) | 0 | nine adjacent sequence/EGZ interfaces elaborated; two excluded-neighbor axiom reports list only `propext`, `Classical.choice`, and `Quot.sound`; complete output SHA-256 `f11cc398...afe3`; no target declaration or proof body |
| bounded case-insensitive `rg` for zero-sum-sequence, Davenport-constant, and Olson-constant Lean declarations | 1 (expected no match) | no exact-topic declaration in repo-local or pinned-mathlib Lean; discovery-only, not an exhaustive external audit |
| `python3 -m json.tool` on all structured owned artifacts and the root worker packet | 0 | valid JSON |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0932-pycache python3 -m py_compile Stage1_Instances/THM-M-0932/check_intake.py` | 0 | scoped checker compiled without generated owned files |
| `python3 -B Stage1_Instances/THM-M-0932/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | target/DAG identity, pins, H5/M4/R4 null target, inventory, receipt, packet, blocker, and six open tasks agree |
| `python3 -B Stage1_Instances/THM-M-0932/check_intake.py` | 0 | public replay mode passed without the scheduler-only packet |
| prohibited Lean construct scan over the owned path | 1 (expected no match) | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| per-new-file whitespace checks and `git diff --check -- Stage1_Instances/THM-M-0932 .stage1-worker-selftest.json` | 0 aggregate | no whitespace diagnostics |

## Known open gates

An approved canonical root, immutable pinpoint source, exact incorporated definitions, binders,
hypotheses, conclusion, proof boundary, corrections, errata, and independent source review remain
open. So do the canonical Lean target and minimal imports, expression and environment fingerprints,
checked transports, four statement mutations, exhaustive anchor audit, obligation registry, typed
graphs, proof and composition, source/provenance/trust closure, readable reconstruction, hermetic
replay, deterministic bundle, independent verification, and master acceptance. These downstream
failures do not invalidate a truthful self-tested `planned` intake.

## Status boundary

This is provisional worker self-test evidence for `S56-M-0932-INTAKE` only. It supports a planned
dossier, not an accepted node receipt. No canonical statement, H0 source closure, proof, audit
completion, theorem completion, or master acceptance is claimed.
