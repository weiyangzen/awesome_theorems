# Exact-statement gate: blocked

Item: `S56-M-1114-STATEMENT`  
Theorem: `THM-M-1114`  
Base revision: `cd7d0c47c19a08d85f4314833fd1e5a339230a3c`

## Decision

The exact Lean 4 target cannot be truthfully elaborated from the authoritative repository record.
That record contains only the title "giant component", the attribution Erdos/Renyi, the year 1960,
and the phrase "the appearance of a giant component in a random graph". It gives no numbered
theorem, source page, graph law, parameter regime, probability mode, quantifier order, or component
size conclusion. The accepted intake therefore freezes a theorem family and explicitly leaves the
canonical proposition open.

The historical candidate, Erdos and Renyi, *On the evolution of random graphs* (1960), does not by
itself select a result. A retrieval attempt against the Stanford-hosted scan produced a malformed
PDF: `pdfinfo` reported only five pages and `pdftotext` reported a broken page tree. It therefore
cannot support a complete, page-pinned transcription of the cited 45-page article. Selecting a
familiar modern formulation would additionally replace the paper's uniform random-graph process
with a binomial `G(n,p)` model unless that transport were first justified.

The unresolved choices change the proposition rather than merely its Lean encoding:

- the uniform `G(n,m)` process versus binomial `G(n,p)`, and the exact parameter scaling;
- supercritical existence alone versus uniqueness, asymptotic density, and bounds on all other
  components;
- inclusion of a subcritical contrast or the critical case;
- convergence in probability, probability tending to one, or an explicit error estimate;
- the order of fixed parameters, epsilon bounds, asymptotic limits, and component witnesses;
- rounding conventions, ties for largest components, and the density equation and its selected
  root.

Encoding any one of these variants would broaden, weaken, or substitute the unspecified source
claim. Encoding the desired conclusion as an assumption or opaque predicate would be a forbidden
placeholder. Consequently there is no canonical expression on which minimal imports, an
elaborated-expression hash, checked transports, or meaningful mutation tests can be established.
Machine state remains `M4`; statement acceptance and theorem completion are false.

## Lean boundary

The pinned environment is usable. Pinned mathlib contains
`Mathlib.Probability.Combinatorics.BinomialRandomGraph.Defs`, which defines `G(V,p)`, but its own
combinatorics README describes binomial random graphs as "just the definition". A source search
found no giant-component or largest-component theorem. This establishes only that some eventual
model vocabulary is available; it neither identifies the historical claim nor supplies its
asymptotic conclusion. Running `lake env lean` on a manufactured target would therefore be fake
elaboration evidence, so no target file was created.

## Validation record

Commands ran from this worker clone on 2026-07-12 (Asia/Shanghai). The existing canonical `.lake`
artifacts were read only; no update, build, dependency clone, or fetch command was run.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1114` | 0 | rank 554, planned, legacy artifacts unaccepted, theorem incomplete |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `cd Formalizations/Lean && lake --version` | 0 | Lake `5.0.0-src+98dc76e` |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | 0 | `651c8acc...b1d2` and `321626c8...2d81` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| pinned-mathlib `rg` search for Erdos/Renyi, random graph, giant component, largest component, and `G(n,m/p)` | 0 | found the binomial random-graph definition and unrelated Erdos results; no giant-component theorem |
| retrieval and inspection of the Stanford-hosted 1960-paper candidate | 0 transport; unusable content | SHA-256 `1ad77dbc...76f`; malformed five-page PDF/page tree, not a complete inspectable edition |

## Retry condition

An accountable source reviewer must preserve an immutable complete primary edition, record its
content hash, select and transcribe the exact numbered theorem with page and definition locators,
audit errata, and freeze every model, regime, asymptotic, quantifier, uniqueness, size, and boundary
choice above. If a modern `G(n,p)` restatement is selected, its equivalence to the chosen historical
claim must be justified rather than assumed. A later statement run can then implement the real Lean
substrate, minimize pinned imports, serialize and hash the elaborated expression, check transports,
and run the required mutation classes.

This is the first failed gate. The assigned phase is not genuinely self-tested to completion, so
no `.stage1-worker-selftest.json` is emitted and no downstream-node or theorem-completion credit is
claimed.
