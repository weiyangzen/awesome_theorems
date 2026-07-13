# THM-M-1597 intake validation

Base revision: `62fad55ced807fdc06921c45d6fcd1f9ad86a1c2` (tree
`9d7c8fe49a4c859d90f3069dc47973ffc5ced768`). Validation date: 2026-07-13
(Asia/Shanghai).

This validation covers the planned dossier, source-statement and non-substitution boundaries, the
six-node open task DAG, structured intake invariants, and a narrow pinned Lean API probe. It does
not validate a canonical RSA proposition or proof because no source-selected root exists. The
automation-provided canonical `.lake` symlink was pre-existing and used read-only; no dependency
update, build, clone, fetch, or other `.lake` mutation was performed. This dirty worker run is
nonrelease evidence.

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
| `python3 scripts/stage1_target.py show THM-M-1597` | exit 0; rank 1217, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| `git status --short --untracked-files=all` | preflight exit 0; only the automation-provided untracked `Formalizations/Lean/.lake` symlink existed before intake |
| `git rev-parse HEAD 'HEAD^{tree}'` | exit 0; base revision and tree recorded above |
| `git blame -L 11763,11768 -- Docs/researches/math_theorems.md` | exit 0; all six uncited catalog lines originate in commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| author-hosted RSA paper retrieval and Crossref query for DOI `10.1145/359340.359342` | exit 0; paper and bibliographic identity inspected for scope discrimination; PDF SHA-256 `f7b1f78d9a7cbeb85e32b8c563a6db60771a5cc4bdc55580645f7cb778a4966b`; external lead only, no H0 admission |
| bounded case-insensitive searches for RSA in tracked Lean, repository files, and pinned mathlib | completed; generic modular arithmetic APIs found, but no exact RSA declaration; intake discovery only |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | exit 0; versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | exit 0; pinned revision and tree recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | exit 0; empty output |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1597/IntakeProbe.lean)` | exit 0; nine modular, totient, and CRT APIs elaborated; stdout SHA-256 `ed1c2dffb8ab7e99b0aaaf366d2984866f58ed95b4a608c7ce4de732edf93da0`; representative axiom reports contain only `propext`, `Classical.choice`, and `Quot.sound`; no target theorem |
| `python3 -m json.tool` on `instance.json`, `task-dag.json`, `intake-receipt.json`, and `.stage1-worker-selftest.json` | exit 0 for each after finalization |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-1597-pycache python3 -m py_compile Stage1_Instances/THM-M-1597/check_intake.py` | exit 0; scoped validator compiled without adding generated files to the owned path |
| `python3 -B Stage1_Instances/THM-M-1597/check_intake.py --worker-packet .stage1-worker-selftest.json` | exit 0 after finalization; manifest/DAG identity, null target, H5/M4/R4 boundary, pins, hashes, receipt/packet, and six open tasks agree |
| `rg -n -e '\bsorry\b' -e '\badmit\b' -e '\bsorryAx\b' -e '\baxiom\b' -e '\bconstant\b' -e '\bopaque\b' -e '\bunsafe\b' Stage1_Instances/THM-M-1597 --glob '*.lean'` | exit 1 as expected; no prohibited declaration in the API-only probe |
| per-untracked-file `git diff --no-index --check /dev/null PATH` plus `git diff --check` | exit 0; no whitespace diagnostics |

## Source and truth boundary

The primary paper's Section VI provides a plausible all-message correctness redirection, but the
catalog does not select it. The paper's wording also needs a truth-critical distinct-primes
condition: without it, its totient product and CRT route fail, and the naive theorem is false. A
coprime-message-only use of Euler's theorem is weaker than the paper's conclusion. These facts were
recorded, not silently repaired into a canonical target.

## Known open gates

The system label must be redirected to an independently reviewed immutable exact proposition. The
result family, source edition and correction record, prime/key/exponent/message/modular model,
encryption/signature distinction, correctness/security/complexity boundary, padding/randomness,
adversary or cost model, ordered binders, exact conclusion, and boundary cases remain open. So do
the canonical Lean expression and environment fingerprints, transports, statement mutations,
exhaustive anchor audit, discovery protocol, obligation registry, typed graphs, proof and
composition, trust/provenance closure, readable reconstruction, hermetic replay, deterministic
bundle, independent verification, master acceptance, audit completion, and theorem completion.
These open gates do not invalidate a truthful self-tested `planned` intake.
