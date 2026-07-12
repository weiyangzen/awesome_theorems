# THM-M-1550 rev-5.6 intake

This directory is the rev-5.6 `planned` instance for the Lax-pair target. Historical Lean and
blueprint material is discovery input only and supplies no accepted proof credit.

## Scope map

| Surface | In scope | Boundary at intake |
|---|---|---|
| Human source claim | A Lax evolution `dL/dt = [P,L]` preserves the spectral invariants of `L` | The repository's phrase "representation of integrable systems" is too broad to assert that every integrable system admits a Lax pair |
| Canonical mathematical root | finite-dimensional complex matrices on a stated time domain; a Lax equation plus sufficient evolution hypotheses implies isospectrality | Exact binders, regularity, and the minimal evolution assumptions remain for the statement phase |
| Object model | `Matrix n n Complex`, commutator, derivative on a real time domain, algebra spectrum | Unbounded operators, PDE domains, inverse scattering, and a definition/classification of all integrable systems are excluded |
| Conservation output | equality of spectra at any two times; characteristic polynomial and trace-power conservation are candidate refinements | No completeness or functional independence of conserved quantities is claimed |
| Historical local Lean | `Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_209.lean` | Candidate APIs and proofs must be re-elaborated and audited under rev-5.6 before credit |
| Foundations | Lean 4 kernel and pinned mathlib with an explicit classical/choice policy | Exact toolchain, import closure, axioms, and TCB fingerprint remain open |

The source label `已验证` is untrusted metadata. The intake does not broaden the source into a
universal existence theorem for Lax representations. The provisional statement instead isolates
the standard spectral-conservation implication that the cited primary paper actually supports.

## Statement phase

`Statement.lean` now freezes that conditional target with explicit universes, finite complex
matrices, the real time domain, the Lax-equation premise, the conjugating-evolution premise, and
the algebra-spectrum conclusion. `statement.json` and `statement-validation.md` record its
expression fingerprint, pinned environment, checked direct expansion, mutations, and boundary
policy. This elaboration is statement evidence only; it is not a proof of the target.

## Intake verdict

Lifecycle is `planned`; provisional root vector is `[H1, M3, R3]`. The first failed theorem gate is
the exact-statement gate: no normalized Lean expression hash, environment fingerprint, checked
transport, or mutation evidence has been accepted. The theorem is not complete.

## Obligation-tree phase

`obligation-registry.json` and `typed-graphs.json` freeze ten canonical obligations and seven
separate reciprocal graph types. `ObligationTree.lean` checks only conditional child-to-root
composition; it assumes the spectrum-under-conjugation leaf and therefore gives no theorem proof
credit. The frozen root cut, all debt boundaries, and exact validation results are recorded in
`obligation-tree.md` and `obligation-tree-validation.md`.

Validation commands and their exact outcomes are recorded in `validation.md`.
