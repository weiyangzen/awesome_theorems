# Statement gate blocker

Item: `S56-M-0714-STATEMENT`

Base revision: `3a479c703900e8096e6b239e7bf5b0da25472b8a`.

## Decision

The rev-5.6 statement phase is blocked and is not self-tested as complete. The repository source
states only that "recursively enumerable sets are Diophantine sets." This identifies the MRDP
theorem family, but it does not select an exact proposition. In particular, it does not define
recursive enumerability, the arity and coding of a set element, the coefficient and solution
domains, the witness-index type, or whether the theorem is uniform in arity. Stage0 explicitly
marks the precise definitions and premises as unfinished.

Those choices are observable in Lean and are not interchangeable by definitional equality. For
example, recursive enumerability can be represented by the domain of a partial-recursive partial
function, by the range of a computable enumeration, or by a coded semidecision predicate. The
input can be a single coded natural or a tuple `Fin n -> Nat`. Diophantine representation can use
natural or integer solutions and one polynomial or a finite system. Freezing any one combination
without an authorized, pinpointed source statement and checked transports would invent missing
mathematics rather than elaborate the exact repository claim.

The pinned APIs do not resolve that ambiguity. `Mathlib.NumberTheory.Dioph` defines `Dioph` for a
set of valuations `Set (alpha -> Nat)` using an existential witness type and an integer-valued
`Poly`, while `Mathlib.Computability.Partrec` defines partial recursiveness. The Dioph module proves
`Dioph.pow_dioph`, but its header calls this only a version of Matiyasevich's theorem and retains
"Finish the solution of Hilbert's tenth problem" as a TODO. It supplies neither a full MRDP
declaration nor a canonical bridge from a selected recursively enumerable predicate to `Dioph`.

This is the first failed gate in section 5.1 of the rev-5.6 blueprint. Without one exact human
statement, there can be no truthful canonical Lean expression, expression fingerprint, credited
encoding transport, or semantic mutation suite. `IntakeProbe.lean` remains an API probe only and
is not promoted to statement evidence.

## Retry condition

An authorized source-selection decision must identify an immutable edition and exact theorem or
page, then freeze:

- the definition of recursively enumerable membership and its Lean encoding;
- the input arity, tuple/coding representation, and whether arity is uniformly quantified;
- the polynomial coefficient domain, solution domain, witness-index type, and one-polynomial
  versus finite-system convention;
- all ordered binders, hypotheses, conclusion, and the treatment of arity zero, empty/full sets,
  and zero witness arity;
- checked transports from the selected source definitions to every credited Lean encoding.

After that decision, this node can elaborate a minimal-import declaration, serialize its expression
and environment, and distinguish removed-hypothesis, changed-domain, changed-binder-scope, and
boundary mutations. The power-is-Diophantine theorem, Hilbert's tenth problem, or an assumed MRDP
premise must not be substituted for the assigned claim.

## Scoped validation on 2026-07-12

No `lake update`, build, fetch, or clone was run. Existing pinned Lake artifacts were used
read-only.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0714` | exit 0; rank 753, lifecycle planned, L0/rework_required, theorem_complete false |
| `rg -n -C 12 'MRDP定理' Docs/researches/math_theorems.md Docs/Stage0_Blueprint.md` | exit 0; the sole claim is the short family-level gloss and Stage0 leaves precise definitions/premises open |
| `(cd Formalizations/Lean && lake env lean --version)` | exit 0; Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | exit 0; pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0714/IntakeProbe.lean)` | exit 0; seven API declarations elaborate, but no exact MRDP proposition is present |
| `git diff --check -- Stage1_Instances/THM-M-0714/statement-blocker.md` | exit 0; no output |

The truthful phase result is `blocked`, with root vector unchanged at `[H3, M4, R4]`. There is no
canonical statement, statement receipt, audit completion, or theorem completion. Because the
assigned phase did not pass, no `.stage1-worker-selftest.json` is emitted.
