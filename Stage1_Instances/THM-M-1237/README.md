# THM-M-1237 rev-5.6 intake

This directory is the rev-5.6 `planned` instance for the Sobolev embedding theorem. Historical
Stage1 prose and `S1_M_175.lean` are discovery inputs only and provide no accepted proof credit.

## Scope map

| Surface | In scope | Boundary at intake |
|---|---|---|
| Exact root | Morrey-Sobolev embedding `W^{1,p}(Omega) -> C^{0,1-n/p}(closure Omega)` for `p > n` on a bounded Lipschitz/extension domain | The domain convention, representative relation, norm, and exact constant must be frozen in the statement phase |
| Local analytic core | Euclidean compact-support inequality and the exponent gap `p > n` | Existing mathlib imports and declarations are candidates, not credited closure |
| Sobolev object model | `W^{1,p}`, weak derivative, almost-everywhere equivalence, continuous representative | The historical local structures encode several facts as `Prop` fields and are not an exact formal root |
| Domain bridge | extension operator from `Omega` to Euclidean space, restriction, boundary representative | Extension hypotheses and boundary conventions remain open |
| Conclusion | a Holder-continuous representative with exponent `1 - n/p` and a quantitative estimate | Plain continuity is a consequence, not a substitute for the frozen root |
| Foundations | Lean 4 kernel, pinned mathlib, classical/choice/quotient policy | Exact toolchain, transitive imports, axioms, and TCB remain open |

The intended root deliberately excludes critical and subcritical cases (`p <= n`), unbounded or
arbitrary measurable domains without an extension hypothesis, and vector-valued generalizations.
Those variants require separate theorem statements and cannot be used to broaden this target.

## Intake verdict

Lifecycle is `planned`; provisional root vector is `[H1, M3, R3]`. The source statement is
mathematically standard, but a versioned primary-source scan, exact assumption/errata crosswalk,
and independent review remain open. The statement phase now supplies a self-tested exact Lean
target, environment and file fingerprints, checked transport, and structural mutation record in
`Statement.lean` and `statement.json`. Master acceptance and every downstream gate remain open;
this does not claim a proof or theorem completion.

## Validation

The intake commands remain in `validation.md`; `statement-validation.md` records the narrow Lean
elaboration and statement-node checks.
