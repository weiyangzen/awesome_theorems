# Lean 4 anchor audit

Item: `S56-M-0005-ANCHOR_AUDIT`  
Base revision: `b5772eecbf53803a9883e5b3d896542717fddec9`  
Audit date: 2026-07-12

## Verdict

The pinned mathlib revision contains required support infrastructure but no Kunneth or
Eilenberg-Zilber theorem. One relevant external Lean 4 project was located at an immutable commit:
`facebookresearch/atlas-lean@34ffed396f376454c1a9b297f3fd74c5c801fb50`. It uses the same Lean
and mathlib pins and contains close topological and algebraic declarations, but every root-critical
body is closed with `sorry`. It is therefore an anchor-only discovery with no machine-proof credit.

The structured candidate inventory, exact revisions, file hashes, scope mismatches, and terminal
body trace are in `anchor_candidates.json`. No dependency was cloned, fetched, or added.

## Pinned mathlib audit

Audited revision: `8a178386ffc0f5fef0b77738bb5449d50efeea95`, commit date
2026-03-30, Lean `v4.29.0`. A full source-tree search of `Mathlib/` and `Archive/` found no spelling
of Kunneth/Kuenneth and no Eilenberg-Zilber or Alexander-Whitney declaration. Searches relating
homology, tensor, `Tor`, and `ShortExact` found no theorem joining those surfaces.

The kernel-visible support anchors are:

| Module | Declaration | Role | Root closure |
|---|---|---|---|
| `Mathlib.AlgebraicTopology.SingularHomology.Basic` | `singularChainComplexFunctor`, `singularHomologyFunctor` | singular chain/homology definitions | no product comparison |
| `Mathlib.CategoryTheory.Monoidal.Tor` | `Tor`, `isZero_Tor_succ_of_projective` | derived tensor and projective vanishing | no Kunneth exact sequence |
| `Mathlib.Algebra.Homology.ShortComplex.ShortExact` | `ShortExact`, `ShortExact.map`, `ShortExact.splittingOfProjective` | exact-sequence vocabulary | no Kunneth maps or exactness |

`Tor.lean` explicitly says that it has "almost nothing to say" about `Tor`; even symmetry between
the two derived-variable definitions remains future work. `AnchorAuditProbe.lean` checks these
support declarations against the pinned kernel environment and prints their axiom profiles.

## External candidate audit

Sourcegraph public Lean-code discovery found Kunneth-family results only in
`facebookresearch/atlas-lean`. The audited commit is immutable, uses
`leanprover/lean4:v4.29.0`, pins the same mathlib commit, and is MIT licensed.

The closest declarations are in `Atlas/AlgebraicTopologyI/code/Section25.lean`:
`algebraic_kunneth`, `algebraic_kunneth_natural`, `KunnethTopological.kunnethShortExact_exact`,
`KunnethTopological.kunnethShortExact_naturality`, and `KunnethTopological.kunneth_topological`.
The product bridge appears in `code/EilenbergZilber.lean` as
`eilenbergZilber_homotopyEquiv`, `eilenbergZilber_natural`, and
`eilenbergZilberHomologyIso`.

These are not proof candidates. The two audited files contain respectively 11 and 4 `sorry`
occurrences. The apparently completed `kunneth_topological` term calls exactness and splitting
theorems whose bodies are `by sorry`. The Kunneth maps, their zero composite, naturality, singular
chain freeness/instances, and Eilenberg-Zilber equivalence/naturality are also placeholders. Thus
the terminal proof-body provenance crosses `sorryAx`; compiling that project would not establish
the rev-5.6 trust gate.

It also does not exactly inhabit the frozen target: its topological API is universe-zero and
pointwise; its naturality theorem fixes only the middle component of an existential short-complex
morphism, not the tensor/Tor component equations required by `NaturalKunnethSequence`; and its
typeclass surface omits the target's explicit `IsDomain` parameter. A checked transport would still
be required even after all upstream placeholders were removed.

## Commands and results

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets with ranks 1 through 1546 passed. |
| `python3 scripts/stage1_target.py show THM-M-0005` | 0 | Rank 100, planned hard-mathlib lane, theorem incomplete. |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | Exact pinned revision `8a178386...a95`. |
| `rg` spelling and semantic searches over pinned `Mathlib/` and `Archive/` | 0/1 | No exact/bridge theorem; only the support anchors listed above. Exit 1 denotes no matches for exact spellings. |
| four Sourcegraph streaming searches for Kunneth/Kuenneth/EilenbergZilber/AlexanderWhitney | 0 | Relevant indexed Lean hits confined to `facebookresearch/atlas-lean`; Kuenneth had zero hits. |
| GitHub repository search for five Kunneth/Eilenberg-Zilber Lean phrases | 0 | Zero repository-name/description matches; this is supplementary discovery only. |
| GitHub contents API at commit `34ffed39...fb50`, SHA-256, and `rg -n '\b(sorry\|admit)\b'` | 0 | Immutable files hashed; 11 placeholders in `Section25.lean`, 4 in `EilenbergZilber.lean`. |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0005/AnchorAuditProbe.lean` | 0 | All seven support declarations checked; printed profiles use only `propext`, `Classical.choice`, and `Quot.sound`. |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0005/KunnethStatement.lean` | 0 | Frozen target still elaborates; four pre-existing unused-parameter warnings only. |
| `python3 -m json.tool Stage1_Instances/THM-M-0005/anchor_candidates.json` | 0 | Structured inventory parsed. |
| `git diff --check -- Stage1_Instances/THM-M-0005 .stage1-worker-selftest.json` | 0 | No whitespace errors. |

The grep.app endpoint returned HTTP 429 and authenticated GitHub code search was unavailable; these
are recorded discovery limitations, not silently treated as negative results. No `lake update`,
build, dependency clone/fetch, or `.lake` mutation was performed.

## Status boundary

Worker verdict: the node-specific anchor inventory is self-tested and provisional, subject to
master acceptance. The root remains `[H1, M3, R3]`. The next proof architecture must treat the
algebraic Kunneth theorem, chain-level product comparison, exactness, tensor/Tor component maps,
and two-variable naturality as open root-critical obligations. The theorem is not complete.
