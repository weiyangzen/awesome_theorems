# Intake validation

Base revision: `fb0baac89ea0633612be3b47448464b4b8e4bef7`; base tree:
`018557070da18ea1733a82de81a238750c59aa84`. Validation date: 2026-07-13
(Asia/Shanghai).

The preflight worktree contained only the automation-provided untracked
`Formalizations/Lean/.lake` symlink to canonical pinned artifacts. It was used read-only. No
`lake update`, `lake build`, dependency clone/fetch, or `.lake` mutation was performed. The new
target-owned dossier and root worker packet make this nonrelease dirty worker evidence.

Validation covers target-set consistency, planned dossier structure and scope invariants,
repository provenance, an open downstream task DAG, a narrow pinned Lean exact-topic interface and
axiom probe, prohibited-construct hygiene, and whitespace. It does not validate a canonical
statement, human-source fidelity, terminal proof body, exhaustive anchor inventory, audit
completion, or theorem completion.

## Source boundary

The repository supplies only the uncited six-line catalog record at
`Docs/researches/math_theorems.md:6791-6796`; all six lines originate in commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. Stage0 repeats that gloss while leaving exact
definitions, premises, proof, foundation, axioms, and artifacts open. No primary source was
admitted. An optional request for a historical scan timed out and supplied no evidence. A later
zbMATH Open metadata query identified William Burnside's *Theory of Groups of Finite Order*,
Cambridge University Press, 1897, as a matching named primary-book lead; selected normalized
metadata SHA-256 is `12a5a1bfadfccce00e28f3feaa4a3f5171bdcbd6c0ffc5ba8ee5668a09bab9da`.
No book text or theorem/proof locator was admitted. Human status remains H1, and the exact statement
gate remains open.

## Environment

- Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, target
  `x86_64-unknown-linux-gnu`.
- Lake `5.0.0-src+98dc76e`.
- Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; package source status clean.
- `Formalizations/Lean/lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `Formalizations/Lean/lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.
- Pinned `Mathlib/GroupTheory/GroupAction/Quotient.lean` SHA-256:
  `50fc92cfeb4c8df97539ecbe4e6153518bea82afe6da61d531f92a9c0170ebb0`.
- Pinned `Mathlib/GroupTheory/GroupAction/Defs.lean` SHA-256:
  `33de8705170779cce28a6fe4c83323b09b28b4d97e224803fe69ccc7f7f5cb94`.

## Commands and results

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0929` | exit 0; rank 1468, planned, L0/rework_required, no accepted legacy artifacts, theorem_complete false |
| initial `git status --short --untracked-files=all` | exit 0; only the pre-existing automation `.lake` symlink was untracked |
| `git rev-parse HEAD 'HEAD^{tree}'` | exit 0; base revision and tree shown above |
| `git blame -L 6791,6796 -- Docs/researches/math_theorems.md` | exit 0; all six uncited catalog lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| optional Archive.org historical-text request with a 20-second bound | timed out; no bytes or source evidence admitted, and no source claim depends on it |
| zbMATH Open API query for document 2672861 with selected-field normalization | exit 0; identified Burnside's 1897 Cambridge book; selected one-line JSON SHA-256 including final newline `12a5a1bf...b9da`; bibliographic H1 lead only |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | exit 0; Lean and Lake versions recorded above; no update or build was run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | exit 0; pinned revision and tree recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | exit 0 with empty output; pinned package worktree clean |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0929/IntakeProbe.lean)` | exit 0; seven fixed-point/orbit/Burnside interfaces elaborated; three axiom reports were `[propext, Classical.choice, Quot.sound]`; stdout SHA-256 `d4600c9b607f48ce306916f715bd7d59c7022d34ed87642f177880b16a994874` |
| `python3 -m json.tool` on all owned JSON files and `.stage1-worker-selftest.json` | exit 0 for each after finalization |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0929-pycache python3 -m py_compile Stage1_Instances/THM-M-0929/check_intake.py` | exit 0; checker compiled without generated files in the owned path |
| `python3 -B Stage1_Instances/THM-M-0929/check_intake.py --worker-packet .stage1-worker-selftest.json` | exit 0 after finalization; manifest/DAG identity, current pins, null canonical target, H1/M3/R4 boundary, exact artifact inventory, receipt/packet, and six open tasks agree |
| `python3 -B Stage1_Instances/THM-M-0929/check_intake.py` | exit 0; public replay mode passes without the scheduler-only root packet |
| prohibited Lean declaration scan over `Stage1_Instances/THM-M-0929` | exit 1 as expected for no match; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| `git diff --check -- Stage1_Instances/THM-M-0929 .stage1-worker-selftest.json` plus scoped per-new-file no-index checks | exit 0/no diagnostics; all owned files and the worker packet have final newlines, LF endings, and no trailing whitespace |

## Known open gates

An independently accepted immutable primary or authoritative edition, exact theorem and definition
locators, assumptions, proof boundary, attribution history, corrections and errata, and source
review remain open. So do selection of the multiplication, average/division, or structural form;
group/action domains and finiteness; fixed-point and orbit conventions; arithmetic carrier; ordered
binders; additive transport; canonical Lean expression and environment fingerprint; minimal import
certificate; checked transports and all four mutation classes; exhaustive anchor, proof-body,
provenance, dependency, axiom and trust audits; obligation and discovery freezes; typed graphs;
proof and composition; readable reconstruction; hermetic replay; deterministic evidence bundle;
independent verification; and master acceptance.

These failures prevent downstream statement, audit, and theorem completion. They do not invalidate
the self-tested `planned` intake, whose only proposed scheduler state is provisional `[_]` pending
master integration.
