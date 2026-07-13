# THM-M-0861 statement validation

Item: `S56-M-0861-STATEMENT`

Base revision: `db4b8793e70ce8af74c9c9490acfa50aa3684d5e` (tree
`6434a20532ae7c523ad293e67a6228ab384bfb8a`). Validation date: 2026-07-13
(`Asia/Shanghai`).

## Frozen target

`Stage1Instances.THM_M_0861.KonigEdgeColoringTarget` quantifies a mathlib `Graph` over arbitrary
vertex and edge universes, with finite actual vertex and edge sets. This preserves the historical
multigraph domain even when those finite sets are embedded in infinite ambient carriers. Separate
edge identities retain parallel edges. A `Bool` side assignment must take different values at the
two ends of every actual link, which excludes loops without imposing connectedness or nonemptiness.

Degree is the finite cardinality of the incidence set, so parallel edges are counted separately.
Maximum degree is the finite supremum over the actual vertex set. A proper coloring maps actual
edge identities to `Fin k` and separates every distinct pair incident at a common vertex.
`HasChromaticIndex G Delta` combines colorability with `Delta` colors and the lower bound that every
proper palette has at least `Delta` colors. This is exactly the catalog equality, while
`ExpandedTarget` exposes the 1916 Satz C upper-bound conjunct and the elementary lower-bound
conjunct. Their iff is kernel-checked by
`konigEdgeColoringTarget_iff_expandedTarget`.

The empty and zero-degree convention is explicit: an edgeless graph has the unique empty coloring
into `Fin 0` and chromatic index zero. Empty graphs, isolated vertices, disconnected graphs,
nonregular graphs, and parallel bundles are retained. No simple-graph, line-graph, regularity,
connectedness, nonemptiness, or stored-coloring substitution is used.

## Lean boundary

The deletion-minimal direct imports are:

- `Mathlib.Combinatorics.Graph.Basic`
- `Mathlib.Data.Set.Card`

Deleting either import makes the exact module fail. The fully explicit canonical expression has
SHA-256 `4e7919ed3b44379a42d69ef88cfb5e512248eccfe755392723cb6769c4f8e197`.
The statement file has SHA-256
`a6ce9ee3edd720d38fa9306324e38b48d5f0430a8b9513b9207e7808ea1b380d`, and the direct Lean output
has SHA-256 `6b80a3cfac8567914519f94b1cf01c86a011335f754040101bf75a8cad0d26d6`.

Four separately elaborated mutations remove bipartiteness, restrict the domain to finite ambient
carrier types, move one bipartition outside the graph binder, or exclude the valid maximum-degree
zero boundary. Lean rejects definitional equality with each mutation, and the Python checker
confirms four distinct explicit-expression fingerprints. These are structural identity tests, not
claims that every changed proposition is false.

## Commands and results

All commands ran inside this worker clone. Lean reused the automation-provided canonical pinned
`.lake` symlink read-only. No dependency update, build, clone, fetch, or `.lake` mutation was run.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and exactly 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0861` | 0 | rank 1415, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, x86_64 Linux |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0861/Statement.lean` | 0 | exact root, checked expansion, four expected equality rejections, loop and empty boundary lemmas, axiom reports, and explicit expression elaborated |
| `cd Formalizations/Lean && python3 -B ../../Stage1_Instances/THM-M-0861/check_statement.py` | 0 | expression/source/output/pin checks passed; both import deletions failed; all four mutation hashes differ |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | 0 | mathlib `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree `bdc39a3123201dae413a9d9be56ec242c19e5c2b` |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | 0 | empty output; pinned package stayed clean |
| scoped JSON, Python, prohibited-construct, and whitespace checks | 0 overall | artifacts parse and compile; prohibited scan returns the expected no-match result; no whitespace diagnostics |

`IsBipartite.noLoops`, `edgeColorable_zero_of_edgeSet_eq_empty`, and
`hasChromaticIndex_zero_of_edgeSet_eq_empty` report no axioms. The definitional iff reports only
`propext`, `Classical.choice`, and `Quot.sound`. No canonical theorem proof is declared and no
`sorry`, `admit`, `sorryAx`, custom axiom, constant, opaque, or unsafe declaration appears.

## Status boundary

This is provisional worker-self-tested statement evidence. The intake dependency itself remains
provisional and master acceptance must be dependency ordered. Independent source acceptance,
anchor and terminal-body audit, obligation freeze, proof, composition, readable reconstruction,
hermetic replay, independent verification, release, and master acceptance remain open. Root debt
moves only from `[H1,M4,R4]` to provisional `[H1,M3,R4]`; no audit or theorem completion is claimed.
