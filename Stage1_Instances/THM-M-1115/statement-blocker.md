# Exact-statement gate: blocked

Item: `S56-M-1115-STATEMENT`  
Theorem: `THM-M-1115`  
Base revision: `e8462bfe9edb8c428b4a3a6471b14b67541ccfae`

## Decision

The exact Lean 4 target cannot be truthfully elaborated from the repository source record. The
entire mathematical claim is the phrase `给定度序列的随机图` ("a random graph with a prescribed
degree sequence"), accompanied by the name "configuration model", Bollobas, and the year 1980.
This describes a model but supplies no proposition or conclusion. Stage0 independently marks the
precise definitions and prerequisites, proof process, dependencies, axioms, and machine artifact as
`待补充` (to be supplied). The metadata label `已验证` is untrusted under rev-5.6 and cannot choose
the missing theorem.

The intake correctly leaves all proposition-changing choices open. In particular, the source does
not determine:

- whether vertices and half-edges are labelled, and whether the degree data are fixed or form an
  asymptotic family;
- whether the output is a multigraph admitting loops and parallel edges or a simple graph obtained
  by an event or conditioning;
- whether uniformity is on half-edge pairings or on resulting graphs, which are generally weighted
  differently by their numbers of representing pairings;
- whether the intended conclusion is existence of a pairing, preservation of the prescribed
  degrees, a simplicity probability, an enumeration formula, or another asymptotic property;
- which parity, maximum-degree, moment, sparsity, or limiting hypotheses apply, and in what
  quantifier order.

The identified paper, Bollobas, *A Probabilistic Proof of an Asymptotic Formula for the Number of
Labelled Regular Graphs*, European Journal of Combinatorics 1(4) (1980), 311-316, DOI
`10.1016/S0195-6698(80)80030-8`, is only a bibliographic lead. Its title concerns regular graphs,
while the repository wording says a prescribed degree sequence. No immutable primary text,
numbered theorem, page-level statement, surrounding definitions, or errata review is present in the
repository. Replacing the entry by the elementary degree-preservation invariant or by the paper's
regular-graph enumeration result would therefore substitute a convenient theorem rather than
elaborate the exact target.

Consequently there is no canonical proposition for Lean to elaborate. Minimal imports, an
elaborated-expression hash, checked alternate encodings, and meaningful removed-hypothesis,
changed-domain, changed-binder-scope, and boundary mutations all depend on first selecting the
missing mathematical claim. A structure that accepts the intended result as a field would merely
hide that missing claim and is not valid statement evidence.

## Required unblock

An accountable source reviewer must select an immutable primary edition and an exact numbered or
displayed result, audit corrections, and crosswalk every binder, hypothesis, convention, and
conclusion. The selection must explicitly fix the vertex and half-edge labels, pairing sample
space and measure, multigraph/simple-graph convention, degree-sequence regime, parity and regularity
conditions, observable, limiting or finite conclusion, quantifier order, and degenerate cases. A
later statement worker can then encode that claim, minimize its pinned imports, serialize the
elaborated expression and environment, check alternate transports, and run the four required
mutation classes.

## Narrow validation evidence

Commands ran in this worker clone on 2026-07-12. Lean used the existing canonical pinned `.lake`
symlink read-only; no update, build, clone, fetch, or dependency mutation was performed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1115` | 0 | rank 555, planned, `L0/rework_required`, legacy artifacts unaccepted, theorem incomplete |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | 0 | `651c8acc...b1d2` and `321626c8...2d81` |
| `find Stage1_Instances/THM-M-1115 -type f -name '*.lean' -print -quit` | 0 | no Lean source exists in the owned path; no placeholder-bearing declaration was introduced |
| `git diff --check -- Stage1_Instances/THM-M-1115 .stage1-worker-selftest.json` | 0 | no whitespace errors |

First failed gate: exact source-statement identity. Known failures are the canonical Lean target,
minimal-import determination, expression fingerprint, checked transports, and mutation tests. The
assigned phase is therefore not self-tested or complete, and no `.stage1-worker-selftest.json` is
emitted. This artifact claims no accepted receipt, dependent-node credit, or theorem completion.
