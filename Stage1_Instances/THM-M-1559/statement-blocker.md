# Exact-statement gate: blocked

Item: `S56-M-1559-STATEMENT`  
Theorem: `THM-M-1559`  
Verdict: blocked; no exact canonical Lean target is claimed.

## First failed gate

The repository source record gives only the title "Riemann-Hilbert problem" and the gloss
"an analytic problem for integrable systems." It supplies no primary-source edition, theorem/page
pinpoint, or exact proposition. The intake identifies the historical monodromy-realization family,
but correctly leaves unresolved choices that change the truth value:

- a logarithmic connection on some holomorphic vector bundle versus a Fuchsian system on the
  trivial bundle;
- arbitrary versus irreducible monodromy, and whether the datum is a representation or conjugacy
  classes;
- the rank, finite singular set, treatment of infinity, gauge/conjugacy equivalence, and permission
  for apparent singularities;
- a restricted positive theorem versus a counterexample to unrestricted realization.

In particular, asserting unrestricted realization by a Fuchsian system on the trivial bundle would
ignore the counterexample boundary already recorded at intake. Selecting an irreducible case, a
nontrivial-bundle theorem, an operator jump-factorization problem, or a negated existence statement
without a pinpoint source would instead narrow or substitute the catalogue claim. Sections 5 and
5.1 of the rev-5.6 standard make this ambiguity a hard blocker: ordered binders, hypotheses,
conclusion, an elaborated expression hash, checked transports, and meaningful statement mutations
cannot be manufactured before the mathematical variant is fixed.

The legacy discovery module
`Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_178.lean` does not repair this failure. It chooses
an operator-valued contour jump problem rather than the intake's historical monodromy-realization
family. Its essential contour-boundary, invertibility, compatibility, trace, jump, normalization,
and uniqueness conditions are stored as abstract proposition fields paired with witnesses. Thus it
can package user-supplied assumptions without defining the classical regular-singular connection
or proving monodromy realization. Although the module elaborates, it receives no exact-statement or
proof credit under the uniform L0 rework rule.

No theorem declaration, proxy target, `sorry`, axiom, placeholder predicate, broadened statement,
or substituted special case was introduced. Machine status remains `M4`; statement acceptance,
audit completion, and theorem completion are false.

## Checked Lean boundary

`StatementProbe.lean` uses the two minimal independent pinned imports needed to elaborate a useful
substrate boundary. It checks:

- `OnePoint ℂ` as a carrier for the complex projective line;
- the fundamental group of the subtype obtained by deleting a chosen singular set; and
- homomorphisms from that group to `Matrix.GeneralLinearGroup (Fin rank) ℂ` as monodromy data.

This probe does not provide a holomorphic vector bundle, logarithmic/meromorphic connection,
regular-singularity predicate, monodromy functor for such a connection, Fuchsian system, or a
realization relation. It is negative boundary evidence only, not the canonical target.

## Retry condition

An accountable source review must first select an immutable primary edition and exact
theorem/counterexample location, transcribe the claim, and freeze every variant choice above. The
formal environment must then supply concrete encodings for the selected differential system or
connection, regular singularities, its monodromy, and the relevant equivalence. A later statement
run can then elaborate that exact proposition with minimal imports, serialize its expression and
environment fingerprint, and execute removed-hypothesis, changed-domain, binder-scope, and boundary
mutations.

Because this statement phase is blocked rather than complete, no
`.stage1-worker-selftest.json` is emitted.

## Environment and validation evidence

- Repository base revision: `6280a5556a0879b07f75e8bfd9359fa6cc60101b`.
- Validation date: 2026-07-12 (Asia/Shanghai).
- Lean toolchain: `leanprover/lean4:v4.29.0`; Lean `4.29.0`, commit
  `98dc76e3c0a9b856c9b98726b713fb04fab16740`.
- Checked mathlib revision: `8a178386ffc0f5fef0b77738bb5449d50efeea95`.
- SHA-256 values: `lean-toolchain`
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`;
  `lake-manifest.json`
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`;
  legacy discovery module
  `feab847fa74e339b230193feb8f1753619f22e0a7b4cacc175ef788a472701a2`;
  `StatementProbe.lean`
  `28530b2303671d1c523cdce2699fd0218e4cdbde4b5e2b907727b0bc68de4b1a`.

All commands ran in this worker clone against the already materialized canonical `.lake` link. No
dependency update, build, clone, or fetch was performed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1559` | 0 | Rank 178, planned, L0/rework-required, legacy artifacts unaccepted, theorem incomplete |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1559/StatementProbe.lean` | 0 | Punctured-sphere and finite-dimensional complex monodromy substrate elaborated; no canonical target was asserted |
| `cd Formalizations/Lean && lake env lean AwesomeTheorems/Stage1/S1_M_178.lean` | 0 | Legacy operator jump-interface module elaborated; its printed declarations confirm an abstract nonterminal boundary |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0 at commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `rg -n -i 'Riemann.Hilbert\|Riemann-Hilbert\|Fuchsian system\|regular singular connection\|logarithmic connection\|monodromy realization' Formalizations/Lean/.lake/packages/mathlib/Mathlib --glob '*.lean'` | 1 | No matching terminal API or theorem in pinned mathlib; exit 1 means no matches |
