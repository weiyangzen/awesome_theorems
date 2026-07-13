# Intake validation

Base revision: `e179b2be594419aa5fb33c3862f73491fdaf113e` (tree
`8c1da8dad4712804811f550b583129e7b73effdc`). Validation date: 2026-07-13
(Asia/Shanghai).

This validation covers only the planned dossier, source and non-substitution boundaries, open task
DAG, structured intake invariants, and a narrow pinned Lean interface probe. It does not validate a
canonical Weierstrass proposition or proof because the repository source has not fixed one. The
automation-provided `.lake` symlink was pre-existing and used read-only. No dependency update,
build, clone, fetch, or other `.lake` mutation was performed. Dirty worker evidence is nonrelease.

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

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; all 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean targets passed |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0265` | exit 0; rank 1273, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| `git status --short --untracked-files=all` | preflight exit 0; only the automation-provided untracked `Formalizations/Lean/.lake` symlink existed before intake |
| `git rev-parse HEAD 'HEAD^{tree}'` | exit 0; base revision and tree recorded above |
| `git blame -L 1908,1913 -- Docs/researches/math_theorems.md` | exit 0; all six uncited catalog lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `curl -L --max-time 30 -sS 'https://api.crossref.org/works/10.1017/cbo9781139567886.002' -o /tmp/weier-crossref.json` | exit 0; authoritative Cambridge edition metadata lead retrieved; 1,881 bytes; SHA-256 `fe4fc307bfb6cc1959ca1cf5523034818843759aba077fe097490351c4bee44b`; no chapter text or H0 evidence |
| `rg -n -i 'Weierstrass\|polynomialFunctions_closure_eq_top\|exists_polynomial_near' Formalizations/Lean/.lake/packages/mathlib/Mathlib/Topology/ContinuousMap/Weierstrass.lean Formalizations/Lean/.lake/packages/mathlib/Mathlib/Topology/ContinuousMap/StoneWeierstrass.lean Formalizations/Lean/.lake/packages/mathlib/Mathlib/Analysis/SpecialFunctions/Bernstein.lean Formalizations/Lean --glob '*.lean' --glob '!.lake/**' Stage1_Instances/THM-M-0265` | exit 0; five direct real-interval interfaces and Bernstein substrate located; broader Stone-Weierstrass candidate not selected |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | exit 0; versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | exit 0; pinned revision/tree recorded above; empty package-status output |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0265/IntakeProbe.lean)` | exit 0; six exact-topic interfaces elaborated; three representative declarations reported `[propext, Classical.choice, Quot.sound]`; stdout SHA-256 `fd940c948628daa7b3c22b08f373a65aa8a84ee90bfa9c8f66c889a3d7c8f250` |
| `python3 -m json.tool Stage1_Instances/THM-M-0265/instance.json` (repeated with `task-dag.json`, `intake-receipt.json`, and `.stage1-worker-selftest.json`) | exit 0 for each after finalization; all JSON parsed |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0265-pycache python3 -m py_compile Stage1_Instances/THM-M-0265/check_intake.py` | exit 0; checker compiled without generated files in the owned path |
| `python3 -B Stage1_Instances/THM-M-0265/check_intake.py --worker-packet .stage1-worker-selftest.json` | exit 0 after finalization; manifest/DAG identity, source and dependency pins, H1/M3/R4 boundary, null target, artifact inventory, receipt/packet agreement, probe output, and six open tasks agreed |
| `rg -n --glob '*.lean' '(^\|[^[:alnum:]_])(sorry\|admit\|sorryAx)([^[:alnum:]_]\|$)\|^[[:space:]]*(axiom\|constant\|opaque\|unsafe)[[:space:]]' Stage1_Instances/THM-M-0265` | exit 1 as expected; no prohibited declaration; `#print axioms` is diagnostic only |
| `git diff --check -- Stage1_Instances/THM-M-0265 .stage1-worker-selftest.json`, plus `git diff --no-index --check /dev/null PATH` for every new file | tracked check exit 0; each new-file check had expected difference exit 1 with empty diagnostics |

## Known open gates

An immutable primary or authoritative edition, pinpoint exact proposition, incorporated definitions,
premise/conclusion/proof crosswalk, translation, corrections or errata, and independent review
remain open. So do domain and scalar selection, the function carrier, uniform topology, polynomial
encoding, quantifiers, conclusion form, boundary cases, canonical Lean expression and environment
fingerprints, checked transports, statement mutations, exhaustive anchor and provenance audit,
discovery and obligation freezes, typed graphs, proof and composition, trust closure, readable
reconstruction, hermetic replay, deterministic bundle, independent verification, master acceptance,
audit completion, and theorem completion. These open gates do not invalidate a truthful self-tested
`planned` intake.
