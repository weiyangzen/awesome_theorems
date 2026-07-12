# Intake validation

Base revision: `10064cd912bf0d94ab6c8d818dd3a30551a921cd` (tree
`f7483f57d60b00edad176cef2fa658a87622982d`). Validation date: 2026-07-13
(Asia/Shanghai).

This validation covers the planned dossier, source and correction boundary, open task DAG, JSON
and scoped invariants, and a narrow pinned Lean API probe. It does not validate a canonical
Peixoto statement or proof because neither has been frozen. The automation-provided canonical
`.lake` symlink was pre-existing and used read-only; no dependency update, build, clone, fetch, or
other `.lake` mutation was performed. This dirty worker evidence is nonrelease evidence.

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

## Source discovery boundary

Crossref metadata for the 1962 article and 1963 same-title further remark was inspected, together
with Scholarpedia revision 137910. The sources were not added to the repository. The full primary
article and follow-up text were not available through the inspected unauthenticated publisher
interfaces. The modern article supports theorem-family discrimination and identifies material
orientation/regularity boundaries only. Exact primary theorem text, proof and correction mapping,
errata review, catalog root selection, lawful immutable capture, and independent review remain
open, so no `H0` claim is made.

## Commands and results

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; all 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-1367` | exit 0; rank 977, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| `git status --short --untracked-files=all` | preflight exit 0; only the automation-provided untracked `Formalizations/Lean/.lake` symlink existed before this intake |
| `git rev-parse HEAD 'HEAD^{tree}'` | exit 0; recorded base revision and tree above |
| `git blame -L 9964,9969 -- Docs/researches/math_theorems.md` | exit 0; all six uncited catalog lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| Crossref API query for DOI `10.1016/0040-9383(65)90018-2` | exit 0; Peixoto, title, *Topology* 1(2), April 1962, pages 101-120 confirmed; metadata only |
| Crossref API query for DOI `10.1016/0040-9383(63)90032-6` | exit 0; Peixoto, same title, *Topology* 2(1-2), 1963, pages 179-180 confirmed; correction content remains unreviewed |
| bounded Scholarpedia revision 137910 inspection | exit 0; characterization, open-density, orbit-equivalence definition, and orientability/regularity boundary inspected; secondary/source-author discriminator only |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | exit 0; versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | exit 0; pinned revision and tree recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | exit 0; empty output |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1367/IntakeProbe.lean)` | exit 0; twelve adjacent pinned manifold, vector-field, trajectory, flow, orbit, equivalence, and omega-limit APIs elaborated; output SHA-256 `f56fda86120182e3f5de5330cc05f1ddf4e87155cc3350f6b0796d029ea44126`; no target theorem declared |
| exact-topic `rg` search for Peixoto and dynamical structural stability in repo-local and pinned-mathlib `.lean` files | exit 1; expected no match; no exact target declaration found; bounded intake discovery rather than an exhaustive external anchor audit |
| `python3 -m json.tool` on `instance.json`, `task-dag.json`, `intake-receipt.json`, and the root worker packet | exit 0 for each after finalization |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-1367-pycache python3 -m py_compile Stage1_Instances/THM-M-1367/check_intake.py` | exit 0; scoped validator compiled without adding generated files to the owned path |
| `python3 -B Stage1_Instances/THM-M-1367/check_intake.py --worker-packet .stage1-worker-selftest.json` | exit 0; manifest and authoritative-DAG identity, null target, H1/M4/R4 boundary, source pins, exact artifact inventory and hashes, receipt/packet agreement, and six open tasks agree |
| `rg -n --glob '*.lean' '\b(sorry\|admit\|sorryAx)\b\|^[[:space:]]*(axiom\|constant\|opaque\|unsafe)[[:space:]]' Stage1_Instances/THM-M-1367` | exit 1; expected no match for prohibited Lean constructs |
| scoped per-new-file whitespace checks plus `git diff --check` | exit 0; no whitespace errors |

## Known open gates

Canonical root selection; primary theorem and 1963 correction capture; a complete accepted source,
proof and errata crosswalk; independent source review; every surface, boundary, orientation,
regularity, topology, orbit-equivalence, hyperbolicity, recurrence, connection, genericity, and
degenerate-case decision; the canonical Lean expression and fingerprints; checked transports and
statement mutations; exhaustive formal anchor audit; discovery and obligation freezes; typed
graphs; proof and composition; trust and provenance closure; readable reconstruction; hermetic
replay; deterministic release bundle; independent verification; master acceptance; audit
completion; and theorem completion remain open. These failures do not invalidate a truthful
self-tested `planned` intake.
