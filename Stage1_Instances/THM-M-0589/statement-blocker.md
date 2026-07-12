# Exact-statement gate: blocked

Item: `S56-M-0589-STATEMENT`  
Theorem: `THM-M-0589`  
Base revision: `e562dd8e1c84c4ba651e8fc451dabc0401e3af8f`

## Decision

The exact Lean 4 target cannot be truthfully elaborated from the authoritative repository material.
The record gives only the title "surgery theory", the date "1960s", the attribution "many
mathematicians", and the gloss "classification of manifolds by surgery". These words name a theory
and a family of results, not a unique proposition.

The accepted intake identifies C. T. C. Wall's *Surgery on Compact Manifolds* and William Browder's
*Surgery on Simply-Connected Manifolds* only as discovery candidates. It explicitly records that no
stable copy was inspected theorem by theorem and leaves the edition, theorem/page, definitions,
assumptions, corrections, errata, and independent review open. Therefore neither citation supplies
the exact human claim required before Lean encoding.

The missing choices change the proposition:

- smooth, PL, or topological category and the exact dimension range;
- compactness, connectedness, boundary, orientation, fundamental group, and orientation character;
- ordinary versus simple homotopy equivalence and the structure-set equivalence relation;
- normal-map and normal-invariant conventions;
- the decorated `L`-group, coefficient involution, and obstruction map;
- exact-sequence, obstruction-vanishing, realization, or classification conclusion;
- basepoints, actions, ordered quantifiers, and exceptional or degenerate cases.

Selecting conventional answers, a simply-connected special case, or one familiar surgery exact
sequence would manufacture or substitute a theorem. Encoding the desired classification as an
opaque predicate, field, axiom, or assumption would be a placeholder rather than an exact target.
Both are forbidden. Consequently there is no canonical expression on which minimal imports, an
expression fingerprint, checked alternate transports, or meaningful removed-hypothesis,
changed-domain, changed-binder-scope, and boundary mutations can be established. Machine debt
remains `M4`; no statement acceptance, proof credit, audit completion, or theorem completion is
claimed.

## Lean boundary

The pinned Lean environment is available. A narrow pinned-mathlib source search found no file
containing the theorem-specific phrases `surgery obstruction`, `surgery exact sequence`, or
`degree-one normal map`. Repository search found only the underspecified catalogue record, this
intake dossier, and unrelated legacy mentions that describe surgery infrastructure as absent.
These limited feasibility observations do not select a source claim, replace elaboration, or
perform the separately assigned anchor audit. There is no applicable
`lake env lean <canonical-target>.lean` command because the proposition for that file has not been
identified.

## Validation record

Commands ran from this worker clone on 2026-07-12 (Asia/Shanghai). The canonical `.lake` artifacts
were accessed read-only through the existing symlink; no update, build, clone, fetch, or dependency
mutation was run.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0589` | 0 | rank 629, planned, legacy artifacts unaccepted, theorem incomplete |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `cd Formalizations/Lean && lake --version` | 0 | Lake `5.0.0-src+98dc76e` |
| `cd Formalizations/Lean && sha256sum lean-toolchain lake-manifest.json` | 0 | hashes `651c8a...1d2` and `321626...d81`, recorded in `statement-blocker.json` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| repository `rg` search for the theorem ID, names, gloss, and candidate monograph | 0 | only underspecified metadata, this dossier, and the generated execution entries; no exact proposition or Lean candidate |
| pinned-mathlib `rg` search for the three theorem-specific phrases above | 1 | no matching files (`rg` exit 1 means no match) |

## Retry condition

An accountable reviewer must preserve and inspect an immutable primary-source edition, select one
exact theorem with theorem/page locators, dispose of errata, and independently approve a crosswalk
that freezes every choice above. A later statement worker can then encode that proposition using
real Lean definitions, minimize pinned imports, serialize and hash the elaborated expression, check
alternate transports, and run the four required mutation classes.

This is the first failed gate. The assigned phase is not genuinely self-tested to its completion
gate, so no `.stage1-worker-selftest.json` is emitted.
