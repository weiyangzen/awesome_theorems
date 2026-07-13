# THM-M-0955 intake validation

Base revision: `a3b18eec39bf04be025b1641cae02f4d44fdf11a` (tree
`fdfff18dea4c6798c5b322b6088dfe556109c134`). Validation date: 2026-07-13
(Asia/Shanghai).

This validation covers target membership, the planned dossier and six-node open task DAG,
repository and primary-bibliographic provenance, source and non-substitution boundaries, structured
intake invariants, and a narrow pinned Lean API probe. It does not validate a canonical
Bose-Chowla proposition or proof because the source statement is not frozen.

The initial worktree contained only the automation-provided untracked `Formalizations/Lean/.lake`
symlink to canonical pinned artifacts. It was used read-only. No `lake update`, `lake build`,
dependency clone or fetch, or other `.lake` mutation was performed. The owned intake artifacts and
root worker packet make this a dirty, nonrelease run.

## Source discovery boundary

The Springer publisher record and Crossref metadata identify R. C. Bose and S. Chowla,
*Theorems in the additive theory of numbers*, Commentarii Mathematici Helvetici 37 (1962),
141-147, DOI `10.1007/BF02566968`. The publisher records receipt on 28 March 1962 and publication
in December 1962. Its summary says that the paper extends earlier results on difference sets and
`B_2` sequences. The publisher HTML SHA-256 was
`75b5e6fbd35a72c2b67f381d8b61ef8f391540508bb4d676a9118f96d10b0034`, and the Crossref JSON
SHA-256 was `0d1de1cf7f6066174b4c1c5b5b3a8452cb58585b9d48eca20be7c2702a1608ed`.

The accessible article page was a subscription preview. Its advertised PDF URL returned an access
page rather than PDF bytes, so no theorem formula or proof was extracted. Exact `B_2`/`B_h`
selection, definitions, hypotheses, construction, theorem/page locator, proof boundary,
corrections, errata, and independent review remain open. The publisher's 1962 date conflicts with
the catalog's unexplained 1960 date. These facts support `H1`, not `H0`.

## Environment

- Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, target
  `x86_64-unknown-linux-gnu`.
- Lake `5.0.0-src+98dc76e`.
- Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; package worktree clean.
- `Formalizations/Lean/lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `Formalizations/Lean/lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

## Commands and results

All repository commands ran at the repository root unless a different working directory is shown.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | standard structure passed for 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | 0 | target set, ranks, digest, and uniform baseline passed |
| `python3 scripts/stage1_target.py show THM-M-0955` | 0 | rank 1489, planned, L0/rework_required, theorem incomplete |
| initial `git status --short --untracked-files=all` | 0 | only the pre-existing `.lake` symlink; preserved read-only |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base revision and tree shown above |
| `git blame -L 6973,6978 -- Docs/researches/math_theorems.md` | 0 | all six catalog lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| publisher/Crossref metadata retrieval and SHA-256 capture for DOI `10.1007/BF02566968` | 0 | matching authors/title/journal/pages and 1962 date located; the publisher summary identifies the B2 family; full theorem unavailable |
| direct publisher PDF request and file-type check | retrieval boundary | returned access HTML, not a PDF; no primary theorem text claimed |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | 0 | versions agree with the environment fingerprint; no update/build run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned revision/tree above; package clean |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0955/IntakeProbe.lean)` | 0 | six adjacent Freiman, energy, finite-field, and cyclic-group signatures elaborated; output SHA-256 `42fa9e5d42318c702ec5c11eb0aea0bcb387392eb8a34ca41ebac0078a5e5196` |
| bounded exact-topic `rg` over pinned mathlib and repository Lean sources (`\bSidon\b|\bBose[- ]?Chowla\b|\bBhSet\b|\bB_h\b`) | 1 (expected no match) | no occurrence of those precise terms |
| `python3 -B Stage1_Instances/THM-M-0955/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | identity, planned H1/M4/R4 boundary, null target, pins, inventory, worker packet, and six open tasks agree |
| JSON parsing, Python AST/bytecode-free parsing, prohibited-construct scan, and new-file whitespace checks | 0 | structured artifacts and checker passed; no prohibited Lean escape or whitespace diagnostic |
| `git diff --check -- Stage1_Instances/THM-M-0955 .stage1-worker-selftest.json` | 0 | no tracked-diff whitespace diagnostics; no-index checks cover untracked files |

## Known downstream failures

- Master acceptance of `S56-M-0955-INTAKE` is pending.
- No admitted full primary text, exact numbered `B_2` or `B_h` theorem, definitions, premise and
  conclusion map, proof passage, correction audit, date reconciliation, or independent review is
  complete.
- No canonical Lean target, minimal imports, expression/environment fingerprint, checked alternate
  encoding, or removed-hypothesis/domain/binder/boundary mutation is frozen.
- No exhaustive anchor audit, discovery protocol, obligation registry, typed graphs, proof,
  composition, readable reconstruction, trust closure, hermetic replay, deterministic bundle,
  independent release verification, audit completion, or theorem completion exists.

These failures block dependent statement and theorem-completion claims. They do not invalidate a
truthful `planned` intake whose purpose is to freeze ambiguity and leave the downstream DAG open.
Only the integration lane may accept the provisional receipt.
