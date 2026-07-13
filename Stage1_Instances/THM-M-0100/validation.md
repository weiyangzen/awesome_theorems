# Intake validation

Base revision: `771d5d4800fbd95eaaa343e9bc55ebfdde20b364` (tree
`a98ba0c37e56a7c04256f7d7df305c88e5cbe76e`). Validation date: 2026-07-13
(Asia/Shanghai).

This validation covers the planned dossier, property-versus-theorem and non-substitution
boundaries, six-node open task DAG, structured intake invariants, and a narrow pinned Lean API
probe. It does not validate a canonical Kazhdan Property (T) proposition or proof because neither
has been frozen. The automation-provided canonical `.lake` symlink was pre-existing and used
read-only; no dependency update, build, clone, fetch, or other `.lake` mutation was performed. This
dirty worker run is nonrelease evidence.

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

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets, and skill presence passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0100` | 0 | rank 1116, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| `git status --short --untracked-files=all` | 0 | preflight contained only the pre-existing automation-provided `Formalizations/Lean/.lake` symlink |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base revision and tree recorded above |
| `git blame -L 733,738 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog fields originate in commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| author-hosted Bekka-de la Harpe-Valette PDF inspection | 0 | Definition 1.1.3, Proposition 1.2.1, Theorem 1.2.5, and Theorem 1.3.1 inspected; distinct source surfaces recorded; the catalog property label remains H5 pending approved theorem redirection |
| Crossref DOI metadata and Springer endpoint inspection | 0 | original 1967 bibliography confirmed; publisher PDF endpoint returned HTML access content rather than the article, so original theorem text was not inspected |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | 0 | versions recorded above; no update or build run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | 0 | pinned revision and tree recorded above; package status clean |
| bounded `rg` search for Kazhdan Property (T), almost invariant, invariant vector, and unitary representation in repo-local Lean and pinned mathlib | 0/1 | no exact Property (T) target found; Kazhdan matches concerned Kazhdan-Lusztig and generic representation APIs; intake discovery only |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0100/IntakeProbe.lean)` | 0 | four adjacent pinned APIs elaborated; no target declaration or proof body |
| `python3 -m json.tool` on the three owned JSON files and root worker packet | 0 | structured artifacts are valid JSON after finalization |
| `python3 -c` with `ast.parse` on `check_intake.py` | 0 | validator parsed without writing generated files into the owned path |
| `python3 -B Stage1_Instances/THM-M-0100/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | target/DAG identity, source and dependency hashes, H5/M4/R4 null target, inventory, packet, and six open tasks agree |
| `python3 -B Stage1_Instances/THM-M-0100/check_intake.py` | 0 | public replay mode passes without the scheduler-only packet |
| prohibited Lean construct scan over the owned path | 1, expected | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| per-new-file `git diff --no-index --check /dev/null` plus scoped `git diff --check` | 0 aggregate | no whitespace diagnostics |

## Known open gates

Canonical selection among the compact-Kazhdan-set definition, the almost-invariant-vector
characterization, Fell-topology isolation, compact generation, higher-rank or lattice examples,
and Property (FH) equivalence remains open. So do the original proposition, a complete source
definition/assumption/conclusion/proof-node map, correction and translation audit, repository source
admission, independent review, all group/topology/representation/Hilbert-space/quantifier/boundary
conventions, canonical Lean target and minimal imports, expression/environment fingerprints,
checked transports, statement mutations, exhaustive anchor audit, discovery protocol, obligation
registry, typed graphs, proof and composition, trust and provenance closure, readable
reconstruction, hermetic replay, deterministic bundle, independent verification, master acceptance,
audit completion, and theorem completion.

## Status boundary

This is provisional worker self-test evidence for `S56-M-0100-INTAKE` only. It supports a planned
dossier, not an accepted node receipt. No canonical statement, H0 source closure, proof, audit
completion, theorem completion, or master acceptance is claimed.
