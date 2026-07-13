# Intake validation

Base revision: `9c75282d42a7ef447d885d1d56997a79418bcd8a` (tree
`cc5285432a02107fadffb68c698690d1b98ac5f2`). Validation date: 2026-07-13
(Asia/Shanghai).

This validation covers the planned dossier, source-statement and non-substitution boundaries,
six-node open task DAG, structured intake invariants, and a narrow pinned Lean interface probe. It
does not validate a canonical Bennett proposition or proof because neither is source-frozen. The
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
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0980` | exit 0; rank 1514, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| `git status --short` | preflight exit 0; only the automation-provided untracked `Formalizations/Lean/.lake` symlink existed before this intake |
| `git blame -L 7155,7160 -- Docs/researches/math_theorems.md` and duplicate lines 7280-7285 | exit 0; both six-field uncited records originate in commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| Crossref work lookup for DOI `10.1080/01621459.1962.10482149` | exit 0; matching title, George Bennett, March 1962, JASA 57(297), pages 33-45; observed response SHA-256 `7844ac367c35e91002d155f862c084cdb08c89c20dde4275d9d17899c4d7f071` |
| Semantic Scholar DOI lookup | exit 0; same title, author, year, and DOI; open-access PDF URL empty and abstract unavailable |
| publisher and JSTOR source-text requests | access blocked; no article text, pinpoint theorem, or proof was represented as inspected |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | exit 0; versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | exit 0; pinned revision and tree recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | exit 0; empty output |
| exact-topic `rg` search in repo-local Lean and pinned mathlib | bounded search found only this probe's disclaimer and a legacy Bernstein record listing Bennett as absent; output SHA-256 `1884d6895b0f58e39d8ee46c65fa0048423fc01a7aebd53f2e1a5df12dfcb732` |
| `(cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0980/IntakeProbe.lean)` | exit 0; six interfaces elaborated and four axiom reports printed; stdout SHA-256 `b61ecb4ca6a9cd0732ab4d7f70202d9673ab7f1ae06a4f6e54873d69b7c370b2`; empty stderr |
| `python3 -m json.tool` on all structured owned JSON and the root worker packet | exit 0 for each after finalization |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0980-pycache python3 -m py_compile Stage1_Instances/THM-M-0980/check_intake.py` | exit 0; scoped validator compiled without generated files in the owned path |
| `python3 -B Stage1_Instances/THM-M-0980/check_intake.py --worker-packet .stage1-worker-selftest.json` | exit 0; manifest and authoritative-DAG identity, null target, H1/M4/R4 boundary, source and dependency pins, exact artifacts, provisional receipt, worker packet, and six open tasks agree |
| prohibited Lean construct scan over `IntakeProbe.lean` | exit 1 as expected; no match for `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` |
| scoped per-new-file whitespace checks plus `git diff --check` | exit 0; no whitespace errors |

## Known open gates

An accepted immutable source edition and exact proposition, pinpoint theorem and incorporated
definitions, probability and index domains, independence and centering hypotheses, boundedness and
variance conventions, exact Bennett rate and constants, tail event and codomain, boundary cases,
proof-boundary and errata audit, category/duplicate-record resolution, and independent source review
remain open. So do the canonical Lean expression and environment fingerprints, minimal imports,
checked transports, statement mutations, exhaustive anchor and provenance audit, discovery and
obligation freezes, typed graphs, proof and composition, readable reconstruction, hermetic replay,
deterministic evidence bundle, independent verification, master acceptance, audit completion, and
theorem completion. These open gates do not invalidate a truthful self-tested `planned` intake.
