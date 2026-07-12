# Exact-statement gate: blocked

Item: `S56-M-0601-STATEMENT`  
Theorem: `THM-M-0601`  
Base revision: `162f31e26f99fc08e308d576b8fb1b6f18a338c6`

## Decision

The exact Lean 4 target cannot be truthfully elaborated from the authoritative repository record.
The only repository statement is `流形的柄分解` (handle decomposition of manifolds). The intake
records Milnor's *Morse Theory*, Matsumoto's *An Introduction to Morse Theory*, and Kosinski's
*Differential Manifolds* as discovery candidates, but no immutable edition, numbered theorem,
page, exact wording, assumptions, definitions, or errata review has been selected. The intake
explicitly reserves these decisions for this phase rather than claiming that one candidate is the
source of the canonical proposition.

The short wording does not determine a unique theorem. In particular, it leaves open:

- whether the object is closed, has boundary, is a compact cobordism relative to an incoming
  boundary, or is noncompact with a locally finite decomposition;
- the dimension, connectedness, countability, compactness, smoothness, collar, and corner
  hypotheses and their quantifier order;
- the initial stage, permitted handle indices, finiteness and ordering of attachments, and the
  precise attaching-embedding and smoothing data;
- whether reconstruction means diffeomorphism, diffeomorphism relative to boundary, or another
  equivalence of filtered manifolds;
- the treatment of the empty manifold, dimension zero, empty boundary, and disconnected cases.

These choices change the domains, binders, hypotheses, and conclusion. Selecting conventional
answers would manufacture one member of a family of handle-decomposition theorems. Defining an
opaque `HandleDecomposition` predicate, assuming attachment or reconstruction fields, stating only
the existence of a Morse function, or replacing diffeomorphic reconstruction by a CW or homotopy
equivalence would be a placeholder or substituted theorem. None was introduced.

Consequently there is no canonical expression on which minimal imports, normalized-expression
hashing, alternate-form transports, or meaningful removed-hypothesis, changed-domain,
changed-binder-scope, and boundary mutations can be performed. The first failed gate is canonical
statement identification, before Lean elaboration. Machine debt remains `M4`; statement
acceptance, audit completion, and theorem completion are all false.

## Pinned Lean boundary

The pinned environment is available, and the intake smoke module still elaborates base manifold
vocabulary. At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, a bounded source
search found no differential-topological handle decomposition, handle attachment, cobordism, or
Morse-theory API. The only `Morse function` hits concern Galois groups of polynomials and are
unrelated. This is feasibility evidence only, not the later anchor audit and not a substitute for
the missing source statement.

There is no applicable `lake env lean <canonical-target>.lean` command because the proposition for
such a file has not been identified. Running the existing `IntakeCheck.lean` establishes only that
`IsManifold` and `ContMDiff` elaborate; it supplies no handle-decomposition statement evidence.

## Validation record

Commands ran inside this worker clone on 2026-07-12 (Asia/Shanghai). The canonical `.lake`
directory was used through the clone's existing symlink and was not modified. No update, build,
clone, fetch, or dependency mutation command was run.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0601` | 0 | rank 639, planned, legacy artifacts unaccepted, theorem incomplete |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `cd Formalizations/Lean && lake --version` | 0 | Lake `5.0.0-src+98dc76e` |
| `cd Formalizations/Lean && sha256sum lean-toolchain lake-manifest.json` | 0 | hashes `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2` and `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| repository `rg` search for the theorem ID, Chinese and English names, candidate authors, and handle-decomposition wording | 0 | only underspecified catalogue metadata and the intake dossier; no exact proposition or historical Lean target |
| pinned-mathlib `rg` search for handle decomposition, handlebody, handle attachment, Morse function/theory, and cobordism | 0 | only unrelated polynomial Morse-function hits; no differential-topological target API |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0601/IntakeCheck.lean` | 0 | printed the pinned types of `IsManifold` and `ContMDiff`; intake smoke check only |

## Retry condition

An accountable source review must preserve an immutable primary-source edition, identify the exact
numbered theorem and page, transcribe its definitions and assumptions, dispose of errata, and
independently approve a row-by-row crosswalk. It must freeze all object, boundary, attachment,
reconstruction, and degenerate-case choices listed above. A later statement run can then implement
the required concrete Lean substrate, elaborate the exact ordered signature with minimized pinned
imports, serialize and hash the expression and environment, check any alternate transports, and
run all four mutation classes.

This records the failed gate without claiming the assigned node. The phase is not genuinely
self-tested to completion, so no `.stage1-worker-selftest.json` is emitted.
