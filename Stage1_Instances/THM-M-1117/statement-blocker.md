# Exact-statement gate: blocked

Item: `S56-M-1117-STATEMENT`  
Theorem: `THM-M-1117`  
Base revision: `646931af665a6683a1fa53db71b5416bee63abff`

## Decision

The exact Lean 4 target cannot be truthfully elaborated from the repository's source record. The
record gives only the title "small-world networks", Watts/Strogatz, 1998, and the phrase
"small-world phenomenon". It provides no numbered theorem, page, exact proposition, or immutable
source edition. The intake identifies the 1998 *Nature* article only as a bibliographic discovery
lead and explicitly records that no analytic result has been selected or independently reviewed.

The phrase does not determine a proposition. In particular, the following unresolved choices
change the mathematics rather than merely its Lean encoding:

- the finite vertex set, initial ring degree, and admissible relation between graph size and degree;
- the rewiring probability space, edge processing order, and handling of loops, duplicate edges,
  dependencies, degree changes, and connectivity;
- whether path length means diameter, an average over ordered or unordered pairs, or an average
  conditional on connectivity, and how unreachable pairs are treated;
- whether clustering is a mean local coefficient or a global transitivity ratio, including the
  convention at vertices of degree below two;
- the comparison baseline, quantitative inequalities, parameter regime, and whether the conclusion
  is deterministic, in expectation, with high probability, asymptotic, or a reported simulation.

The publisher abstract and figures described in the intake are evidence about a model and observed
phenomenon, not a uniquely identified analytic theorem. Choosing a familiar modern theorem about a
Watts--Strogatz variant, proving existence of some graph with high clustering and small diameter,
or replacing the model by an Erdos--Renyi or Newman--Watts graph would substitute a different
claim. Defining a `SmallWorld` structure whose fields contain the desired conclusion would merely
assume the result and is also forbidden.

Consequently the phase fails at exact human-claim identity, before ordered binders, hypotheses,
minimal imports, an elaborated kernel expression, an expression fingerprint, checked transports,
or the four required mutation classes can be established. `IntakeProbe.lean` remains only a pinned
graph-API availability check; it is not a canonical statement. No Lean source was added because
there is no honest expression for `lake env lean` to elaborate.

## Required unblock

An accountable source reviewer must preserve an immutable primary-source edition, identify an
exact numbered or displayed analytic result (rather than a plot, simulation, or empirical
observation), check errata, and freeze the graph construction, observables, normalizations,
quantifier order, probability/asymptotic semantics, inequalities, and every degenerate convention
listed above. A later statement worker can then encode that exact claim, minimize pinned imports,
serialize and hash the elaborated expression, compile checked transports, and mutation-test a
removed hypothesis, changed domain, changed binder scope, and boundary case.

## Narrow validation evidence

Commands ran in this worker clone on 2026-07-12. The canonical `.lake` symlink and pinned packages
were read only; no update, build, clone, fetch, or dependency mutation was performed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1117` | 0 | Rank 557, planned, legacy artifacts unaccepted, theorem incomplete |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `cd Formalizations/Lean && lake --version` | 0 | Lake `5.0.0-src+98dc76e` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | 0 | SHA-256 `651c8acc...b1d2` and `321626c8...2d81` |
| repository search for `THM-M-1117`, the Chinese title, Watts/Strogatz, and the small-world phrase | 0 | Found only the underspecified metadata, Stage0 projection, generated rev-5.6 scheduling rows, and this target's intake dossier; no exact proposition or accepted formal artifact |
| pinned-mathlib source search for small-world, Watts--Strogatz, characteristic path length, and rewiring terminology | 1 | No theorem-specific match; exit 1 denotes no match and is not proof of nonexistence |

First failed gate: exact source-statement identity. Known failures are the canonical target,
minimal-import determination, expression fingerprint, checked transports, and mutation tests. The
assigned phase is not self-tested to completion, so no `.stage1-worker-selftest.json` is emitted.
No statement acceptance, proof credit, audit completion, or theorem completion is claimed.
