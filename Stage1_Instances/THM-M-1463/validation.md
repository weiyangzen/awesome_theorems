# THM-M-1463 intake validation

Base revision: `2d82479e32843fd52283dcd9bb305954729c1199` (tree
`30134b43ab41e973d2558be90371bf18d6edb259`). Validation date: 2026-07-13
(Asia/Shanghai).

This validation covers target-set consistency, the planned dossier, source-statement and
non-substitution boundaries, the six-node open task DAG, structured intake invariants, and a narrow
pinned Lean API probe. It does not validate a canonical Petrov-Galerkin proposition or proof: the
catalog supplies a method-family gloss rather than a source-selected truth-valued statement. The
automation-provided canonical `.lake` symlink was pre-existing and used read-only. No dependency
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
| `python3 scripts/stage1_target.py show THM-M-1463` | exit 0; rank 1140, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| `git status --short --untracked-files=all` (preflight) | exit 0; only the automation-provided untracked `Formalizations/Lean/.lake` symlink existed before intake |
| `git rev-parse HEAD 'HEAD^{tree}'` | exit 0; base revision and tree match this record |
| `git blame -L 10679,10684 -- Docs/researches/math_theorems.md` | exit 0; all six uncited catalog fields originate at commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| Crossref lookup for DOI `10.1007/BF01436561` | exit 0; publisher metadata located Babuška's 1973 article, response size 9,398 bytes and SHA-256 `f6c73f1bbe6095ac594c7185186b1bd087d452f683ef60349b4f4ce6d9e4c8cf`; article body not inspected |
| bounded exact-topic search in repo-local sources and pinned mathlib | repo search exit 0 only for the catalog record, Stage0 projection, and an explicit exclusion in the distinct Lax-Milgram dossier; pinned-mathlib search expected no-match exit 1; no source-identical terminal declaration located; intake discovery only |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | exit 0; versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | exit 0; pinned revision and tree recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | exit 0; empty output |
| `(cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-1463/IntakeProbe.lean)` | exit 0; ten adjacent bilinear-map, subspace, projection, coercivity, and Lax-Milgram APIs elaborated; stdout SHA-256 `fca28174be61b20686a7db6249af514c234e66c209a8d2d81eab76db0f7919a3`; representative axiom reports contain only `propext`, `Classical.choice`, and `Quot.sound`; no target theorem |
| `python3 -m json.tool` on `instance.json`, `task-dag.json`, `intake-receipt.json`, and the root worker packet | exit 0 after finalization |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-1463-pycache python3 -m py_compile Stage1_Instances/THM-M-1463/check_intake.py` | exit 0; scoped validator compiled without adding generated files to the owned path |
| `python3 -B Stage1_Instances/THM-M-1463/check_intake.py --worker-packet .stage1-worker-selftest.json` | exit 0 after finalization; manifest/DAG identity, null target, H5/M4/R4 boundary, pins, exact inventory, receipt/packet, and six open tasks agree |
| `rg -n -e '\bsorry\b' -e '\badmit\b' -e '\bsorryAx\b' -e '\baxiom\b' -e '\bconstant\b' -e '\bopaque\b' -e '\bunsafe\b' Stage1_Instances/THM-M-1463 --glob '*.lean'` | exit 1 as expected; no prohibited declaration in the API-only probe |
| scoped new-file no-index whitespace checks plus `git diff --check` | exit 0; no whitespace diagnostics |

## Known open gates

The method label must be redirected to an independently reviewed, immutable, exact proposition.
The scalar field, trial and test spaces, continuous and discrete variational problems, form and
argument convention, right-hand side, inf-sup and adjoint conditions, norms, constants,
approximation family, conclusion, neighbor boundaries, and degenerate cases remain open. So do the
canonical Lean expression and environment fingerprint, checked transports, statement mutations,
exhaustive formal anchor audit, discovery protocol, obligation registry, typed graphs, proof and
composition, trust and provenance closure, readable reconstruction, hermetic replay, deterministic
bundle, independent verification, master acceptance, audit completion, and theorem completion.

These open gates do not invalidate a truthful, self-tested `planned` intake. Only the integration
lane can accept the provisional node receipt.
