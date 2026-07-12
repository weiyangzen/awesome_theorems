# Intake validation

Base revision: `8c50139eafcb1c2e29e7ca69379648590820bf53`; base tree:
`84cd63b08ff977c1b895e0299927df8b6d6bc8ae`.

This validation covers target membership, the planned dossier and open task DAG, repository-source
provenance, source-family discrimination, JSON and scoped invariants, a narrow pinned Lean substrate
probe, a bounded repo-local and mathlib search, prohibited-construct hygiene, and whitespace. It
does not validate a canonical theorem statement or proof because the catalog supplies no stable
truth-valued proposition.

The preflight worktree contained only the automation-provided untracked
`Formalizations/Lean/.lake` symlink to canonical pinned artifacts. It was used read-only. No
`lake update`, `lake build`, dependency clone or fetch, network-triggering Lake operation, or other
`.lake` mutation was performed. The owned intake files and root worker packet make the final tree
dirty and nonrelease.

## Source discovery boundary

The author-hosted preliminary edition of Gerald Teschl's *Ordinary Differential Equations and
Dynamical Systems* was inspected as a temporary worker input at Section 6.5, printed pages 199-200.
Equation (6.32) is the scalar transcritical example `x' = mu*x - x^2`; Problem 6.17 asks the reader
to prove its claims. The passage's phrase "two stable fixed points" conflicts with the derivatives
at the two equilibria and the adjacent derivative criterion, while no matching official erratum was
found. The PDF SHA-256 is
`362433156525216abf596c17ce843204510e96d57afa4284a37c7aa5a9ffc36e`; the 6,874-byte extract has
SHA-256 `72cf623f3faffe4eb6df0d1ad7ca173bb3c5157e03bd4cb07840ee2f08911e9f`; the inspected official
errata has SHA-256 `3eacbac5b8fc762c5d3f21183cba3ae638b9ac5fbe703cc52cf2857b9605996e`.
No source file was added to the repository, and no immutable source admission, corrected
proposition, complete premise/proof/errata mapping, or independent H0 review is claimed.

## Environment fingerprint

- Platform: Linux x86_64.
- Lean: `4.29.0`, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`.
- Lake: `5.0.0-src+98dc76e`.
- Pinned mathlib: `8a178386ffc0f5fef0b77738bb5449d50efeea95`; tree
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; package worktree clean.
- `Formalizations/Lean/lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `Formalizations/Lean/lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

## Commands and results

All repository commands ran at the repository root on 2026-07-13 Asia/Shanghai unless a different
`cwd` is shown.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-1361` | 0 | rank 971; planned; no legacy slot; legacy artifacts unaccepted; theorem_complete false |
| initial `git status --short --untracked-files=all` | 0 | only `?? Formalizations/Lean/.lake`; preserved read-only |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base revision and tree shown above |
| `git blame -L 9922,9927 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `git rev-parse bcf3f9fa79ab8c2b6610c9875668c2589b35b74f:Docs/researches/math_theorems.md` | 0 | source-record blob `5c1de0c2bda67f7257142dd99b0dd91d69e0a3bf` |
| `curl -L --fail --silent --show-error https://www.mat.univie.ac.at/~gerald/ftp/book-ode/ode.pdf -o /tmp/thm-m-1361-teschl-ode.pdf` | 0 | temporary source-family discovery input only; observed PDF digest recorded above |
| `pdftotext -f 210 -l 211 -layout /tmp/thm-m-1361-teschl-ode.pdf /tmp/thm-m-1361-teschl-pages.txt` | 0 | extracted 6,874 bytes with the digest recorded above |
| analogous download and text search of the official errata PDF | 0 | no match for bifurcation, transcritical, printed pages 199-200, or equations 6.31-6.33; discovery observation only |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | 0 | Lean and Lake versions agree with the fingerprint; no update or build was run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned mathlib revision/tree above; package worktree clean |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1361/IntakeProbe.lean)` | 0 | six adjacent implicit-function, integral-curve, flow, fixed-point, derivative, and smoothness APIs elaborated; complete output SHA-256 `c47c71c8c2c48e05a0b435ca8c7077f2ade6a5b856340cbd52cdddaf1473a9bd` |
| `rg -n -i --glob '*.lean' 'bifurcat\|transcritical' Formalizations/Lean/.lake/packages/mathlib/Mathlib Formalizations/Lean/AwesomeTheorems` | 1 (expected no match) | no exact-topic occurrence; intake discovery only, not an exhaustive anchor audit or global absence claim |
| `python3 -m json.tool` on all structured owned artifacts and `.stage1-worker-selftest.json` | 0 | all structured artifacts are valid JSON after finalization |
| Python `ast.parse` on `Stage1_Instances/THM-M-1361/check_intake.py` | 0 | scoped validator parses without writing bytecode |
| `python3 -B Stage1_Instances/THM-M-1361/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | target identity, planned H5/M4/R4 boundary, null formal target, source issue, exact inventory, worker packet, source hashes, and six open tasks agree |
| `python3 -B Stage1_Instances/THM-M-1361/check_intake.py` | 0 | public replay mode passes without the scheduler-only packet |
| prohibited Lean proof-escape scan over the owned path | 1 (expected no match) | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration in the API-only probe |
| per-file `git diff --no-index --check /dev/null` for every owned file and the worker packet | 0 aggregate | no whitespace diagnostics; no-index exit 1 for each new file is only the expected new-file difference |
| `git diff --check -- Stage1_Instances/THM-M-1361 .stage1-worker-selftest.json` | 0 | tracked-diff command emitted no diagnostics; untracked-file coverage comes from the preceding no-index checks |

## Known downstream failures

- The title and gloss do not select one stable proposition. No repository-selected primary source,
  exact theorem, incorporated definitions, assumptions, proof boundary, correction decision, or
  independent source review exists.
- The inspected source is not catalog provenance, supplies a prototypical example rather than a
  general theorem, delegates proof to a problem, and contains an unresolved apparent stability typo.
- The dynamics model, state and parameter spaces, equilibrium branches, regularity, stability
  predicate, locality, genericity, nondegeneracy, coordinate conventions, quantifier order, exact
  conclusion, and boundary cases remain open.
- No canonical Lean expression, exact imports, expression/environment fingerprint, checked
  alternate encoding, or statement mutation is frozen.
- Formal anchor audit, discovery and obligation freezes, typed graphs, proof, composition, trust
  closure, readable reconstruction, hermetic replay, deterministic bundle, independent release
  verification, and master acceptance remain open.

These failures prevent statement, audit-completion, and theorem-completion claims. They do not
invalidate a truthful, self-tested `planned` intake whose purpose is to freeze the ambiguity and
open the downstream DAG. Only the integration lane may accept the provisional worker receipt.
