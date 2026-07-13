# THM-M-0816 exact-statement gate: blocked

Item: `S56-M-0816-STATEMENT`  
Base revision: `3ef3a6bf4f2f9b86930beb27693f7429fea3e63a` (tree
`c9eba4c65f6e228f9cefc8bdf62136b7fb69426a`)

## Decision

The exact Lean 4 target cannot be truthfully elaborated from the authoritative repository record.
The catalog gives only Turan's name, Pal Turan, the year 1941, and the gloss "the maximum number of
edges in a graph containing no complete subgraph." It does not identify the order of the forbidden
complete graph or select one of the materially different statements commonly called Turan's
theorem.

The intake correctly preserves this ambiguity. Its canonical mathematical statement and Lean
module, expression, expression hash, and target-environment fingerprint are null. In particular,
the source record does not decide among:

- the sharp edge inequality for an `(r + 1)`-clique-free graph;
- the quotient/remainder formula for the extremal edge count;
- the equality or uniqueness characterization by a balanced complete `r`-partite graph; or
- an extremal-number formulation for a forbidden complete graph.

It also does not freeze finite-graph representation, the `K_(r+1)` indexing convention, a graph on
exactly `n` vertices versus an arbitrary finite vertex type, the use of an abstract Turan-graph
edge count versus explicit natural-number arithmetic, or the `r = 0`, `n = 0`, `n < r`, and `n = r`
boundaries. Those choices alter domains, binders, hypotheses, conclusions, and degenerate cases.
Choosing the familiar pinned mathlib edge bound or uniqueness theorem would therefore invent or
substitute missing mathematics rather than elaborate the exact received target.

The official REAL-J archive authenticates volume 48 (1941) and the article title *Egy grafelmeleti
szelsoertek feladatrol*. The incorporated evidence is archive metadata only. The article's exact
proposition, definitions, proof boundary, assumptions, corrections, errata, and an independent
source review remain absent. The statement gate fails before minimal canonical imports, an
elaborated expression fingerprint, checked transports, or meaningful removed-hypothesis,
changed-domain, changed-binder-scope, and boundary mutations can be established. Those mutations
are undefined, not passed.

The node remains `[ ]`, the lifecycle remains `planned`, and the root vector remains
`[H1, M3, R4]`. No `Statement.lean`, canonical declaration, proof body, axiom, placeholder,
weakened special case, or broadened theorem was added.

The prerequisite `S56-M-0816-INTAKE` is provisional `[_]`, with an unaccepted worker receipt and no
accepted receipt ID. Dependency acceptance is therefore also pending, although the absent exact
source statement is independently decisive.

## Pinned Lean boundary

The existing discovery-only `IntakeProbe.lean` was re-elaborated with its sole direct import,
`Mathlib.Combinatorics.SimpleGraph.Extremal.Turan`. It checked all eight pinned candidate
interfaces. Most directly relevant are:

```lean
SimpleGraph.CliqueFree.card_edgeFinset_le
  (cf : G.CliqueFree (r + 1)) :
  let n := Fintype.card V
  G.edgeFinset.card <=
    (n ^ 2 - (n % r) ^ 2) * (r - 1) / (2 * r) + (n % r).choose 2

SimpleGraph.isTuranMaximal_iff_nonempty_iso_turanGraph (hr : 0 < r) :
  G.IsTuranMaximal r <->
    Nonempty (G ≃g SimpleGraph.turanGraph (Fintype.card V) r)
```

The edge-bound declaration deliberately has no positivity hypothesis and handles `r = 0`; the
uniqueness declaration requires `0 < r`. Adding positivity to the former or removing it from the
latter would change the candidate. Their common feature module and successful elaboration are
`M3` discovery evidence only. They are not a canonical statement, a minimal-import certification
for an absent target, an anchor audit, or proof credit.

The pinned environment is Lean 4.29.0 at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` (tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`). The automation-provided canonical `.lake` symlink
was used read-only. No update, build, dependency clone or fetch, or other `.lake` mutation ran.

## Validation record

Commands ran on 2026-07-13 in this isolated worker clone.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0816` | 0 | rank 1375; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| pre-edit `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided untracked `.lake` symlink existed; base revision and tree are recorded above |
| `git blame -L 5998,6003 -- Docs/researches/math_theorems.md` | 0 | all six sparse catalog lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `python3 -B Stage1_Instances/THM-M-0816/check_intake.py` | 1 | historical intake replay rejects its frozen repository base after master integration; the intake evidence was recorded rather than rewritten |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions recorded above |
| mathlib `git rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned revision and tree recorded above; package worktree clean |
| `cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0816/IntakeProbe.lean` | 0 | all eight Turan candidate interfaces elaborated; stdout SHA-256 `b6669e90bde77db74c966c7a136e88907e6a7c62d8a37fb41e4b008f850ca653` |
| prohibited-construct scan over owned Lean files | 1, expected no match | no `sorry`, `admit`, `sorryAx`, axiom, constant, opaque, or unsafe declaration |

## Retry condition

Accountable reviewers must preserve an immutable primary or approved authoritative source, select
and independently approve one exact proposition, and map every incorporated definition, ordered
binder, hypothesis, conclusion, proof boundary, correction, erratum, and boundary case. They must
settle the forbidden-clique order, graph model, inequality/value/equality/uniqueness root,
arithmetic presentation, positivity convention, and all degenerate cases listed above.

A fresh statement worker can then encode exactly that reviewed claim, minimize its pinned imports,
serialize and hash the elaborated expression and environment, compile every credited transport,
and run all four required mutation classes.

This blocker is the assigned phase's truthful result, not completion of this node or any downstream
node. `audit_complete: false` and `theorem_complete: false`; no debt-vector change is proposed.
Because the exact-statement deliverable did not pass, no `.stage1-worker-selftest.json`, worker
`[_]`, statement receipt, proof credit, or master acceptance is claimed.
