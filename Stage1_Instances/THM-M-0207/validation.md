# Intake validation

Base revision: `72e9e8092182121a6794921f61fcc9cae22f726d` (tree
`0d6c1fdf06d1573c256af331c6b198e5a787af43`). Validation date: 2026-07-13
(Asia/Shanghai).

This validation covers target membership, the planned dossier, source and non-substitution
boundaries, the open task DAG, scoped intake invariants, and a narrow pinned Lean discovery probe.
It does not validate a canonical Napoleon proposition or a proof because neither is frozen. The
automation-provided canonical `.lake` symlink was pre-existing and used read-only. No dependency
update, build, clone, fetch, or other `.lake` mutation was performed. This dirty worker run is
nonrelease evidence.

## Environment

- Linux `x86_64`; worker timezone `Asia/Shanghai`.
- Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, target
  `x86_64-unknown-linux-gnu`.
- Lake `5.0.0-src+98dc76e`.
- Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; package source status was clean.
- `Formalizations/Lean/lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `Formalizations/Lean/lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

## Commands and results

All repository commands ran at the repository root unless a different working directory is shown.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; all 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and execution-skill presence passed |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0207` | exit 0; rank 1538, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| `git status --short --untracked-files=all` before editing | exit 0; only the pre-existing automation-provided `Formalizations/Lean/.lake` symlink |
| `git rev-parse HEAD 'HEAD^{tree}'` | exit 0; base revision and tree recorded above |
| `git blame -L 1492,1497 -- Docs/researches/math_theorems.md` | exit 0; all six uncited catalog fields originate at commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| repository and Stage0 source inspection | exit 0; no primary citation, theorem/page, exact domain, orientation, construction, center definition, proof, errata, reviewer, or formal artifact was supplied |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | exit 0; versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | exit 0; pinned revision/tree recorded above and package status empty |
| bounded exact-topic `rg` search in repository-local Lean and pinned mathlib | no Napoleon or outward-equilateral-triangle construction found; generic equilateral and centroid infrastructure located; intake discovery only, not an exhaustive anchor audit |
| `(cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0207/IntakeProbe.lean)` | exit 0; eight adjacent interfaces elaborated; three support lemmas reported `[propext, Classical.choice, Quot.sound]`; stdout SHA-256 `6809bfc4d703ae1d14369f617c6b533e4ae446dbca2e1454ef2b784a50ef39f5`; no target declaration or proof body credited |
| `python3 -m json.tool` on all structured owned JSON and `.stage1-worker-selftest.json` | exit 0 after finalization |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0207-pycache python3 -m py_compile Stage1_Instances/THM-M-0207/check_intake.py` | exit 0; checker compiled without generated files in the owned path |
| `python3 -B Stage1_Instances/THM-M-0207/check_intake.py --worker-packet .stage1-worker-selftest.json` | exit 0; authority identity, source and scope boundary, null target, H1/M4/R4 classification, pins, artifact hashes, receipt, packet, and six open tasks agree |
| prohibited Lean construct scan over `IntakeProbe.lean` | exit 1 as expected; no match for `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declarations |
| scoped `git diff --check` and byte-level checks for every owned file | exit 0; no whitespace, carriage-return, NUL, or final-newline error |

## Known open gates

An accepted immutable source edition, exact theorem locator, complete definition/assumption/proof/
translation/errata mapping, independent source review, Euclidean domain, dimension, ordered input,
nondegeneracy, outward orientation, attached-triangle construction, center convention, exact output
predicate, and degenerate cases remain open. So do the canonical Lean expression and environment
fingerprints, minimal imports, checked transports, statement mutations, exhaustive anchor audit,
discovery and obligation freezes, typed graphs, proof, composition, provenance and trust closure,
readable reconstruction, hermetic replay, deterministic bundle, independent verification, master
acceptance, audit completion, and theorem completion. These open gates do not invalidate a truthful,
self-tested `planned` intake.
