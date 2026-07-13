# THM-M-0243 intake validation

Base revision: `c6fd6dad8fcfe5fd464416cd452f50286b546978` (tree
`5a80b61d8fa09336779f8d1453dcfe4299c9472f`). Validation date: 2026-07-13
(Asia/Shanghai).

This validation covers the planned theorem dossier, scope map, source-statement crosswalk, open
task DAG, structured intake invariants, and pinned Lean candidate probe. It does not validate a
canonical Bohr-Mollerup proposition or proof: primary-source admission, exact root selection, and
source-to-Lean transport remain open. The automation-provided `Formalizations/Lean/.lake` symlink
was pre-existing and used read-only. No `lake update`, `lake build`, dependency clone/fetch, or
other `.lake` mutation was performed. This dirty worker evidence is nonrelease.

## Environment

- Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, target
  `x86_64-unknown-linux-gnu`.
- Lake `5.0.0-src+98dc76e`.
- Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; package source status was clean before and after
  the probe.
- `lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

## Commands and results

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and execution skill presence passed |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0243` | exit 0; rank 1253, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| `git status --short --untracked-files=all` (preflight) | exit 0; only the automation-provided untracked `Formalizations/Lean/.lake` symlink existed before intake |
| `git rev-parse HEAD 'HEAD^{tree}'` | exit 0; base revision and tree match this record |
| `git blame -L 1752,1757 -- Docs/researches/math_theorems.md` | exit 0; all six uncited catalog fields originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| bounded inspection of NIST DLMF section 5.5(iv) | exit 0; modern positivity, recurrence, normalization, log-convexity, and positive-domain equality components crosswalked; secondary live reference only, not H0 |
| bounded `rg` search in repo-local Lean and pinned mathlib | exit 0; exact-topic pinned module and declaration located; no repo-local target artifact or source-identical transport credited; intake discovery only |
| `(cd Formalizations/Lean && lake env lean --version)` | exit 0; Lean version, commit, and target recorded above |
| `(cd Formalizations/Lean && lake --version)` | exit 0; Lake version recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | exit 0; pinned revision and tree recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | exit 0 before and after validation; empty output |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0243/IntakeProbe.lean)` | exit 0; six exact-topic Gamma APIs elaborated and two candidate axiom reports printed; complete output SHA-256 `8d122b58946005336d4654abfad6b935c7b927d87f48a047e69de744ebbeb7e2` |
| `python3 -m json.tool` on `instance.json`, `task-dag.json`, `intake-receipt.json`, and `.stage1-worker-selftest.json` | exit 0 after finalization |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0243-pycache python3 -m py_compile Stage1_Instances/THM-M-0243/check_intake.py` | exit 0; scoped validator compiled without generated files in the owned path |
| `python3 -B Stage1_Instances/THM-M-0243/check_intake.py --worker-packet .stage1-worker-selftest.json` | exit 0 after finalization; authority/DAG identity, source and dependency hashes, null target, H1/M3/R4 boundary, exact artifact inventory, receipt/packet, validation actions, and six open tasks agree |
| token-anchored prohibited-declaration scan over the owned Lean probe | exit 1 as expected; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration token; diagnostic `#print axioms` is intentionally permitted |
| scoped new-file whitespace checks and `git diff --check` | exit 0; no whitespace errors |

The probe reports `[propext, Classical.choice, Quot.sound]` for both
`Real.convexOn_log_Gamma` and `Real.eq_Gamma_of_log_convex`. Those reports describe discovered
candidate interfaces only. They do not select or accept a foundation profile or prove the target.

## Known open gates

An immutable primary source and approved exact statement, definition, premise, proof-boundary,
correction/errata, and independent-review map remain open. So do uniqueness-implication versus
two-sided root selection, total versus subtype carrier, log-convexity transport, exact Lean target
and minimal imports, expression and environment fingerprints, statement mutations, exhaustive
anchor and terminal-body provenance audit, discovery protocol, obligation registry, typed graphs,
proof and composition, trust closure, readable reconstruction, hermetic replay, deterministic
bundle, independent verification, master acceptance, audit completion, and theorem completion.
These failures do not invalidate a truthful self-tested `planned` intake.
