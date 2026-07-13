# Intake validation

Base revision: `fb0baac89ea0633612be3b47448464b4b8e4bef7`; base tree:
`018557070da18ea1733a82de81a238750c59aa84`.

This validation covers target membership, the planned dossier and open task DAG, catalog and
primary-source discrimination, JSON and scoped invariants, a narrow pinned Lean API probe,
prohibited-construct hygiene, and whitespace. It does not validate a canonical Kneser statement or
proof because the exact source root and Lean encoding belong to the downstream statement phase.

The initial worktree contained only the automation-provided untracked
`Formalizations/Lean/.lake` symlink to canonical pinned artifacts. It was used read-only. No
`lake update`, `lake build`, dependency clone or fetch, network-triggering Lake operation, or other
`.lake` mutation was performed. The owned intake files and root worker packet make the final tree
dirty and nonrelease.

## Source discovery boundary

The GDZ scans of Kneser's 1953 density paper and volume-61 finite-subset paper were inspected, as
were the bibliographic and opening-statement boundary of the 1956 locally compact paper. The first
matches the catalog year; the other two match its abelian-group gloss more closely. The source
hashes and pinpoint findings are in `instance.json` and `source-statement-crosswalk.md`.

These primary records establish that complete published Kneser proofs exist, supporting provisional
`H1`. They do not select the catalog root or close `H0`: complete statement/definition/premise/proof
mapping, translation, corrections and errata, lawful durable source admission, and independent
review remain open.

Pinned mathlib supplies adjacent sumset and stabilizer interfaces. A bounded exact `Kneser` search
found only a Freiman-Kneser TODO/reference. The probe validates interface availability only,
supporting an `M4` substrate boundary rather than an exact statement or proof claim.

## Environment fingerprint

- Platform: Linux 7.0.0-27-generic, x86_64.
- Lean: 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`.
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
| `python3 Docs/tools/check_stage1_standard.py` | 0 | all 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0938` | 0 | rank 1477; planned; no legacy slot; legacy artifacts unaccepted; theorem_complete false |
| initial `git status --short --untracked-files=all` | 0 | only `?? Formalizations/Lean/.lake`; preserved read-only |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base revision and tree shown above |
| `git blame -L 6854,6859 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| GDZ/DOI source requests, PDF inspection, and `sha256sum` | 0 | three proposition-changing primary families and the recorded locators/digests were discriminated; no canonical selection or H0 claim |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | 0 | Lean and Lake versions agree with the fingerprint; no update or build was run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned mathlib revision/tree above; package worktree clean |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0938/IntakeProbe.lean)` | 0 | nine adjacent pinned sumset/stabilizer APIs elaborated; output SHA-256 `97d06690d2cf4d4b43266ca1f6dd79efea0c78ec1a725e605e62ef3cc34f5f7b` |
| exact `Kneser` search over pinned mathlib Lean | 0 | one TODO/reference line only; output SHA-256 `0dd08c2d254f6ea23a862907b0be96eca61f029d3437969bfb2a072ea0820305` |
| `python3 -m json.tool` on all structured owned artifacts and `.stage1-worker-selftest.json` | 0 | all structured artifacts are valid JSON after finalization |
| Python compile of `Stage1_Instances/THM-M-0938/check_intake.py` | 0 | scoped validator parses without writing bytecode into the owned path |
| `python3 -B Stage1_Instances/THM-M-0938/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | target identity, planned H1/M4/R4 boundary, source hashes, exact inventory, worker packet, and six open tasks agree |
| prohibited Lean proof-escape scan over the intake probe | 1 (expected no match) | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| scoped byte checks plus `git diff --check` | 0 aggregate | final newlines present; no invalid bytes, trailing whitespace, or diff diagnostics |

## Known downstream failures

- The catalog's 1953 date and abelian-group gloss do not select among the integer-density,
  finite-cardinality, and locally compact/Haar-measure source roots.
- No exact ambient group, subset model, invariant, stabilizer semantics, hypotheses, conclusion,
  binder order, alternate encoding, or degenerate-case disposition is frozen.
- No exact Lean target, minimal imports, expression/environment fingerprints, checked transports,
  or required removed-hypothesis/domain/binder/boundary mutations exist.
- Exhaustive anchor audit, discovery and obligation freezes, typed graphs, proof integration,
  composition, provenance and trust closure, readable reconstruction, hermetic replay,
  deterministic bundle, independent release verification, and master acceptance remain open.

These failures prevent statement, audit-completion, and theorem-completion claims. They do not
invalidate a truthful, self-tested `planned` intake whose purpose is to freeze scope and open the
downstream DAG. Only the integration lane may accept the provisional worker receipt.
