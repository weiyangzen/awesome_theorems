# THM-M-0487 intake validation (historical phase record)

Base revision: `997541734bb32f987fb15f163335a82512992120` (tree
`2c866b9d840d48c48ac839740c62d3b9440be0e5`). Validation date: 2026-07-13
(Asia/Shanghai).

This section records the earlier intake validation. It covers the planned dossier, source and non-substitution boundaries, six-node open
task DAG, structured intake invariants, and a narrow pinned Lean API/boundary probe. It does not
validate a canonical weak-Goldbach Lean expression or any unbounded proof. The
automation-provided canonical `.lake` symlink existed before this intake and was used read-only;
no dependency update, build, clone, fetch, or other `.lake` mutation was performed. This dirty
worker run is nonrelease evidence.

## Environment

- Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, target
  `x86_64-unknown-linux-gnu`.
- Lake `5.0.0-src+98dc76e` on Linux `7.0.0-27-generic` x86_64.
- Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; package source status was clean before and after
  the probe.
- `lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.
- Helfgott arXiv:1312.7748v2 source archive SHA-256:
  `f2be46b7480bae643083e211dc19b539018950384dc59c1c5faa6e263fd2b366`.

## Commands and results

All commands ran from the repository root unless the command shows another working directory.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and execution skill passed |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0487` | exit 0; rank 1366, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| `git status --short --untracked-files=all` (preflight) | exit 0; only the automation-provided untracked `Formalizations/Lean/.lake` symlink existed before intake |
| `git rev-parse HEAD 'HEAD^{tree}'` | exit 0; base revision and tree match this record |
| `git blame -L 3574,3579 -- Docs/researches/math_theorems.md` | exit 0; all six uncited catalog fields originate at commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `curl -L --fail --silent --show-error https://arxiv.org/src/1312.7748v2` to `/tmp`, followed by `sha256sum`, `tar`, and bounded source inspection | exit 0; exact source archive, Main Theorem, and final analytic/computational composition hashes recorded; temporary files removed |
| bounded exact-topic search over repo-local Lean and pinned mathlib | completed; no Goldbach or sum-of-three-primes terminal theorem found; this is intake discovery, not a global absence proof |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | exit 0; versions recorded above; no update or build was run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | exit 0; manifest-pinned mathlib revision and tree recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | exit 0 before and after the probe; empty output |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0487/IntakeProbe.lean)` | exit 0; six pinned APIs plus strict `n = 7`, oddness, and repeated/even-prime boundary examples elaborated; prime-two/three axiom reports printed; no target theorem |
| `python3 -m json.tool` on `instance.json`, `task-dag.json`, `intake-receipt.json`, and `.stage1-worker-selftest.json` | exit 0 for each finalized JSON artifact |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0487-pycache python3 -m py_compile Stage1_Instances/THM-M-0487/check_intake.py` | exit 0; validator compiled without generated files in the owned path |
| `python3 -B Stage1_Instances/THM-M-0487/check_intake.py --worker-packet .stage1-worker-selftest.json` | exit 0 at intake finalization; authority identity, pins, source hashes, frozen human claim, then-null Lean target, H1/M4/R3 intake boundary, exact inventory, receipt/packet, and six open tasks agreed |
| `rg -n -e '\bsorry\b' -e '\badmit\b' -e '\bsorryAx\b' -e '\baxiom\b' -e '\bconstant\b' -e '\bopaque\b' -e '\bunsafe\b' Stage1_Instances/THM-M-0487 --glob '*.lean'` | exit 1 as expected; no prohibited declaration or proof escape in the discovery-only probe |
| `git diff --check`, plus `git diff --no-index --check /dev/null <file>` for every untracked changed file | exit 0 for whitespace diagnostics; every changed file passed |

The probe's printed axiom reports say `Nat.prime_two` and `Nat.prime_three` depend on `propext`,
`Classical.choice`, and `Quot.sound` in the pinned environment. This reports only the inspected
boundary ingredients; it is not a trust report for a target proof, because no target proof exists.

## Known open gates

The following list is the intake-time boundary. The statement-phase addendum below supersedes its
claims that the expression, imports, binders, transports, and mutations are still open.

Immutable source admission, full major-arc/minor-arc/computational dependency mapping, exact
assumption and errata audit, computation artifacts and trust review, independent source review,
integer-to-natural transport, exact ordered binders and boundary conventions, canonical Lean
target and minimal imports, expression/environment fingerprints, checked alternate transports,
and all four statement mutation classes remain open. So do the exhaustive anchor audit,
discovery protocol, obligation registry, typed graphs, proof, composition and trust closure,
readable reconstruction, hermetic replay, deterministic bundle, independent verification, master
acceptance, audit completion, and theorem completion. These failures do not invalidate a truthful
self-tested `planned` intake.

## Statement-phase addendum

`statement-validation.md` records the later scoped statement run against base
`561d83df037004ceb2259292d7c63be930b40391`. That run freezes and fingerprints the canonical
natural target with the two necessary narrow imports, integer-domain and equality-orientation transports, four mutation
classes, and the 5/7/8 boundaries. It supersedes this intake record only for statement status; all
proof, source-review, audit, validation, release, and master-acceptance gates remain open.
