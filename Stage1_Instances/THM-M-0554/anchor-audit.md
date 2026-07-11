# THM-M-0554 Lean 4 anchor audit

## Scope and immutable revisions

This audit compares the frozen `Stage1.THM_M_0554.Statement` with repo-local,
pinned mathlib, and bounded public Lean 4 discovery surfaces. The local
toolchain is `leanprover/lean4:v4.29.0`; mathlib was inspected at the locked
commit `8a178386ffc0f5fef0b77738bb5449d50efeea95`. The legacy artifact was
inspected at its containing commit
`16d227cffb7cb7d9e8392b6c0ff8211e498e1330`. No dependency was fetched,
updated, installed, or modified.

## Candidate inventory

| Candidate | Checked role | Exact-root verdict |
|---|---|---|
| `Mathlib.Algebra.Homology.SpectralSequence.Basic`: `SpectralSequence`, `E₂CohomologicalSpectralSequence`, `pageFunctor` | Generic pages, homology transitions, and cohomological bidegree convention | Substrate only. It neither constructs a spectral sequence from CW skeleta nor identifies its `E₂` page or abutment. |
| `Mathlib.Topology.CWComplex.Classical.{Basic,Finite}`: `CWComplex`, `RelCWComplex.skeleton`, `skeleton_mono`, `RelCWComplex.Finite` | Genuine CW, skeletal-filtration, and finiteness APIs | Substrate only. No checked connection to generalized cohomology, an exact couple, cellular cohomology, or convergence exists. |
| `Mathlib.AlgebraicTopology.SingularHomology`: `singularChainComplexFunctor`, `singularHomologyFunctor`, homotopy invariance | Ordinary homology infrastructure | Nearby non-target. It is covariant homology and supplies neither a generalized cohomology theory nor the AHSS. |
| repo-local `S1_M_106.lean` | Generic wrappers, local proposition-valued interfaces, and explicit debt gates | Discovery only. It has no terminal AHSS proof body and supplies no inhabitant of the frozen proposition. |

`AnchorAudit.lean` checks the named pinned declarations and prints their actual
types. A recursive source search found no mathlib declaration named for
Atiyah-Hirzebruch or AHSS and no generalized-cohomology/exact-couple theorem
composing the three substrate areas. None of these rows receives root proof
credit, so there is no terminal proof-body or axiom provenance to promote.

## External discovery

On 2026-07-12, GitHub REST repository searches for `Atiyah-Hirzebruch spectral
sequence Lean`, `AHSS Lean theorem prover`, `generalized cohomology Lean4`, and
`spectral sequence CW complex Lean` each returned `total_count: 0` with
`incomplete_results: false`. grep.app requests for four corresponding source
terms all returned HTTP 429. The latter is an access limitation, not negative
evidence. Repository metadata search is also not exhaustive code search.

No credible external candidate was discovered, hence there is no external
revision, module, declaration, toolchain, license, proof body, or dependency
closure to claim or import. Future discoveries must be audited at immutable
commits before receiving any machine credit.

## Classification

The bounded anchor-audit phase is complete pending master acceptance. The
exact root remains `M4` with `formalization_debt`: the locked environment has
useful but disconnected substrate and no exact or stronger terminal proof
candidate. Human-source status is not upgraded by this phase. The dossier
remains `planned`; full audit and theorem completion are both false.

## Validation receipt

Base revision: `9c8fbcb508ef94b14b4cc94df3d576550867591d`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets accepted. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets in ranks 1 through 1546. |
| `python3 scripts/stage1_target.py show THM-M-0554` | 0 | Rank 106, planned, L0/rework-required, theorem incomplete. |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | Returned locked commit `8a178386ffc0f5fef0b77738bb5449d50efeea95`. |
| `rg -n -i 'Atiyah\|Hirzebruch\|AHSS\|generalized (co)?homology\|cohomology theor\|CW complex\|cellular cohomology\|exact couple' Formalizations/Lean/.lake/packages/mathlib/Mathlib --glob '*.lean'` | 0 | CW and unrelated text/substrate matches; no terminal AHSS candidate. |
| `lake env lean ../../Stage1_Instances/THM-M-0554/AnchorAudit.lean` from `Formalizations/Lean` | 0 | Principal mathlib substrate declarations elaborated and their types printed. |
| `lake env lean ../../Stage1_Instances/THM-M-0554/Statement.lean` from `Formalizations/Lean` | 0 | Frozen target still elaborated. |
| `python3 -m json.tool Stage1_Instances/THM-M-0554/anchor-audit.json` | 0 | Structured audit parses. |
| `rg -n '^\s*(sorry\|admit\|axiom)(\s\|$)' Stage1_Instances/THM-M-0554` | 1 | Expected no-match status: no prohibited Lean declaration token. |
| `git diff --check -- Stage1_Instances/THM-M-0554 .stage1-worker-selftest.json` | 0 | No whitespace errors. |

Status boundary: this is scoped candidate-inventory evidence only. It is not
an AHSS proof, human-source acceptance, obligation-tree completion, audit
completion, or theorem completion.
