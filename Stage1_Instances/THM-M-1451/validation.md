# THM-M-1451 intake validation

Base revision: `03bed3c211cb739ccd2629908210fda0f9adf6ca` (tree
`a48670276bfe2105ddbfb4057314b21056dae0cb`). Validation date: 2026-07-13
(Asia/Shanghai).

This validation covers the planned dossier, scope/source boundaries, six-node open task DAG,
structured intake invariants, and a narrow pinned Lean API probe. It does not validate a canonical
QR-algorithm proposition or proof because the repository does not select one. The
automation-provided `.lake` symlink was pre-existing and used read-only; no update, build, clone,
fetch, or other `.lake` mutation was performed. This dirty worker run is nonrelease evidence.

## Environment

- Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, target
  `x86_64-unknown-linux-gnu`.
- Lake `5.0.0-src+98dc76e` on Linux `7.0.0-27-generic` x86_64.
- Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; package source status was clean.
- `lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

## Commands and results

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-1451` | exit 0; rank 1128, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| `git status --short --untracked-files=all` | preflight exit 0; only the automation-provided untracked `Formalizations/Lean/.lake` symlink existed before intake |
| `git rev-parse HEAD 'HEAD^{tree}'` | exit 0; base revision and tree recorded above |
| `git blame -L 10595,10600 -- Docs/researches/math_theorems.md` | exit 0; all six uncited target lines originate in commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| SHA-256 over normative, source, toolchain, lock, and candidate-module inputs | exit 0; hashes recorded in `instance.json` and the provisional receipt |
| bounded inspection of Arbenz Chapter 4 | exit 0; printed pages 63-64 contain equation (4.1), Algorithm 4.1, and distinct-modulus conditional convergence description; PDF SHA-256 `9826e5327bafd4d00c42abf5f643c62ec99bed3644d45b853c176234e323eeac`; H1 lead only |
| Crossref queries for Francis Parts 1/2 and Kublanovskaya | exit 0; metadata response digests recorded; primary proposition text not obtained |
| direct Francis Part 1/2 publisher PDF requests | exit 22; HTTP 403, recorded as an inspection boundary rather than bypassed |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | exit 0; versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | exit 0; pinned revision and tree recorded above |
| bounded exact-topic `rg` search over pinned mathlib and repo-local Lean | no exact QR-iteration/algorithm declaration found; the only local match is this probe's disclaimer |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1451/IntakeProbe.lean)` | exit 0; nine adjacent QR-factor, unitary, charpoly, spectrum, and triangular APIs elaborated; representative axiom reports list only `propext`, `Classical.choice`, and `Quot.sound`; complete output SHA-256 `06ee28738236b3f79dbc49d828936301c21f819d075bb6d4b60eebb55e8cbcee` |
| `python3 -m json.tool` on owned JSON files and `.stage1-worker-selftest.json` | exit 0 after finalization |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-1451-pycache python3 -m py_compile Stage1_Instances/THM-M-1451/check_intake.py` | exit 0; validator compiled without generated files in the owned path |
| `python3 -B Stage1_Instances/THM-M-1451/check_intake.py --worker-packet .stage1-worker-selftest.json` | exit 0 after finalization; manifest/DAG identity, planned scope, pins, exact artifact hashes, receipt, packet, and six open tasks agree |
| `rg -n -i --glob '*.lean' 'sorry\|admit\|sorryax\|axiom\|constant\|opaque\|unsafe' Stage1_Instances/THM-M-1451` | exit 1 as expected; no prohibited proof escape in the discovery-only probe |
| scoped `git diff --check` and per-new-file no-index whitespace checks | exit 0; no whitespace diagnostics |

## Known open gates

An immutable pinpoint source and independent review must select the exact algorithm variant,
matrix/scalar domain, QR convention, hypotheses, conclusion, endpoint, convergence topology/rate,
arithmetic model, and boundary cases. The historical primary texts and errata/proof mapping remain
open. So do the canonical Lean expression/environment fingerprint, checked transports and
mutations, exhaustive anchor audit, obligation registry, typed graphs, proof and composition,
trust/provenance closure, readable reconstruction, hermetic replay, deterministic evidence bundle,
independent verification, master acceptance, audit completion, and theorem completion. These open
gates do not invalidate a truthful self-tested `planned` intake.
