# Intake validation

Base revision: `59c86ca38b16fe4d3901ba66530aae4df0e881b0` (tree
`2b8fc12c558d4fe807d7b4ac4b2c9a127002338e`). Validation date: 2026-07-13
(Asia/Shanghai).

This validation covers the planned dossier, the source-statement mismatch and non-substitution
boundary, open task DAG, JSON and scoped invariants, and a narrow pinned Lean API probe. It does not
validate a canonical Artin-theorem proposition or proof because neither has been frozen. The
automation-provided canonical `.lake` symlink was pre-existing and used read-only; no dependency
update, build, clone, fetch, or other `.lake` mutation was performed. This dirty worker run is
nonrelease evidence.

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

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; all 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0075` | exit 0; rank 1103, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| `git status --short --untracked-files=all` | preflight exit 0; only the automation-provided untracked `Formalizations/Lean/.lake` symlink existed before this intake |
| `git blame -L 554,559 -- Docs/researches/math_theorems.md` | exit 0; all six uncited catalog lines originate in commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| bounded inspection of Serre, *Linear Representations of Finite Groups*, Chapter 9 | exit 0; Theorem 17 and its cyclic-subgroup corollary on printed page 70 located in the university-mirrored scan; digest `099bb953993bce35bcbdccd989140248e4db8dd066744a62830b7fe940627516`; theorem is rational spanning, not linear independence; H1 source lead only |
| Crossref inspection for `10.1007/BF02941010` | exit 0; Artin's 1931 article metadata and pages 292-306 identified; no exact original theorem passage available or credited |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | exit 0; versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | exit 0; pinned revision and tree recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | exit 0; empty output |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | exit 0; hashes recorded above |
| bounded exact-topic `rg` search in pinned mathlib and repo-local Lean | exit 0; no Artin-induction or induced-character-independence terminal found; only the THM-M-0429 legacy audit task contains the phrase "induced character" |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0075/IntakeProbe.lean)` | exit 0; eight adjacent character, induced-representation, adjunction, and Dedekind-independence APIs elaborated; stdout SHA-256 `d34978c563908658aa27c9ab78bc83a477c2361d4245d55cbce6aa9f5ba1d2f0`; no target theorem declared |
| `python3 -m json.tool` on `instance.json`, `task-dag.json`, `intake-receipt.json`, and the root worker packet | exit 0 for each after finalization |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0075-pycache python3 -m py_compile Stage1_Instances/THM-M-0075/check_intake.py` | exit 0; scoped validator compiled without generated files in the owned path |
| `python3 -B Stage1_Instances/THM-M-0075/check_intake.py --worker-packet .stage1-worker-selftest.json` | exit 0; manifest and authoritative-DAG identity, null target, H1/M4/R4 boundary, source mismatch and pins, exact artifact hashes, receipt and worker packet, and six open tasks agree |
| prohibited Lean construct scan over `IntakeProbe.lean` | exit 1 as expected; no match for `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` |
| scoped per-new-file whitespace checks plus `git diff --check` | exit 0; no whitespace errors |

## Known open gates

An accountable correction or identification of the catalog claim, an accepted immutable source
edition and exact proposition, group/subgroup/character/induction/coefficient/conclusion and
boundary conventions, pinpoint historical-source mapping, errata audit, and independent source
review remain open. So do the canonical Lean expression and environment fingerprints, checked
transports, statement mutations, exhaustive formal anchor audit, discovery protocol, obligation
registry, typed graphs, proof and composition, trust and provenance closure, readable
reconstruction, hermetic replay, deterministic bundle, independent verification, master
acceptance, audit completion, and theorem completion. These open gates do not invalidate a
truthful self-tested `planned` intake.
