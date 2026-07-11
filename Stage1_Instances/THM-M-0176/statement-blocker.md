# Statement gate blocker

Item: `S56-M-0176-STATEMENT`  
Theorem: `THM-M-0176`  
Base revision: `ecf22a6439be62b1cd7ba6d402b68217ef7c119c`  
Verdict: blocked; no exact canonical Lean target is claimed.

## First failed gate

The accepted intake deliberately leaves `canonical_claim` null and records the first blocker as
the primary-source and algebraic/cohomological foundation freeze. The authoritative repository
wording says only "the Riemann-Roch theorem for higher-dimensional algebraic varieties." It does
not select exact source wording or fix the data needed to distinguish materially different formal
statements:

- a smooth projective complex variety, a smooth proper scheme over a field, or another variety
  convention;
- a finite-rank algebraic vector bundle, a locally free coherent sheaf, or a class in algebraic
  K-theory;
- Chow groups/rational equivalence or singular/cohomological characteristic classes, together with
  the coefficient and comparison conventions;
- the definitions and normalizations of the Euler characteristic, Chern character, Todd class,
  tangent bundle, top-degree component, and degree/integration map; and
- connectedness, purity/equidimensionality, dimension-zero, empty-space, and zero-bundle boundary
  policies.

Choosing these in the statement phase would invent mathematics not fixed by the source record.
They cannot be erased as implementation details: they alter the binders, hypotheses, types, and in
some cases the relationship between alternate formulations. Section 5.1 of the rev-5.6 standard
therefore prevents an elaborated target, expression fingerprint, credited transport, and the four
meaningful mutation classes until an accountable source decision freezes them.

The historical discovery module
`Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_125.lean` is not an exact-statement substitute.
Its `SmoothProjectiveVarietyInput` stores `base_isFieldSpectrum`, `projective`, and
`coherentOrVectorBundle` as unconstrained propositions. More decisively,
`HirzebruchRiemannRochPackage` takes the characteristic ring, Chern character, Todd class,
integration map, Euler characteristic, and the desired HRR equality itself as fields.
`StatementShape` then asks for such a package. This is an abstract interface containing the target
formula as supplied data, not a definition of the classical objects or a source-faithful HRR
proposition. Crediting it would broaden/substitute the target and hide the theorem behind a
placeholder interface.

The pinned mathlib source search found no Lean declarations matching Hirzebruch-Riemann-Roch,
Riemann-Roch, Chern character, Todd class, or Chow ring. The historical module does kernel-elaborate
and confirms that generic scheme, smooth/proper morphism, sheaf-cohomology, and homological Euler
characteristic substrates exist. That result is only a substrate/discovery check; it supplies
neither the missing exact source decision nor the absent characteristic-class object model.

No `sorry`, axiom, bodyless declaration, proxy target, proof credit, audit completion, or theorem
completion is introduced. Machine debt remains `M4`. Because the assigned phase did not reach its
completion gate, no `.stage1-worker-selftest.json` is emitted.

## Environment and narrow validation

Commands ran in this worker clone on 2026-07-12 using only the existing pinned `.lake` artifacts.
No update, build, fetch, or clone command was run.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0176` | 0 | rank 125, planned, L0/rework-required, legacy artifacts unaccepted, theorem incomplete |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `cd Formalizations/Lean && lake env lean AwesomeTheorems/Stage1/S1_M_125.lean` | 0 | historical abstract interface and substrate checks elaborated; this is not exact-target evidence |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `rg -n -i 'Hirzebruch\|Riemann.?Roch\|Chern.?Character\|Todd.?Class\|Chow.?Ring' Formalizations/Lean/.lake/packages/mathlib/Mathlib --glob '*.lean'` | 1 | no matching mathlib source declaration or reference; exit 1 means no matches |

The pinned environment identities are: `lean-toolchain` SHA-256
`651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`, Lake manifest SHA-256
`321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`, and historical module
SHA-256 `daff8c3b44437f736322e7f3022493aa7cc372285a2461058567164e12ed1ca7`.

## Retry condition

An accountable reviewer must first pin an immutable primary-source theorem and exact location,
including its wording, definitions, assumptions, coefficient and normalization conventions, and
errata status. The same decision must select the algebraic or cohomological Lean object model and
state every boundary policy above. A later statement worker can then encode that proposition with
concrete APIs, minimize the imports, serialize its elaborated expression, check any alternate-form
transports, and mutation-test the frozen hypotheses, domain, binder scope, and boundary cases.
