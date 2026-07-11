# Statement gate blocker

Item: `S56-M-0434-STATEMENT`  
Theorem: `THM-M-0434`  
Verdict: blocked; no exact canonical Lean target is claimed.

## First failed gate

The intake selects the Lie-algebra Fundamental Lemma proved in Ngo's 2010 paper, but its source
crosswalk does not yet pin and transcribe a particular theorem statement together with every
referenced definition, normalization, characteristic restriction, and transfer result. The catalog
phrase `基本引理的证明` does not itself determine the endoscopic datum, group versus Lie-algebra
form, matching relation, transfer-factor normalization, Haar measures, unit functions, or residual
characteristic regime. Inventing any of those choices would broaden or substitute the source claim.

Even after those source choices are fixed, the pinned Lean environment does not contain the
required endoscopy and reductive-group-over-local-field object model. In particular, the scoped
mathlib search found no Langlands-Shelstad Fundamental Lemma declaration or definitions for its
endoscopic data, matching regular semisimple classes, transfer factors, hyperspecial/parahoric
models, or orbital integrals. The two search hits are unrelated uses of "fundamental lemma" in
homotopical algebra and the Selberg sieve.

The historical discovery module
`Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_083.lean` elaborates, but it explicitly supplies
the missing mathematical objects through structures with unconstrained `Prop` fields and arbitrary
functions. Its `OrbitalIntegralComparison` takes the stable orbital integral, ordinary orbital
integral, transfer factor, and matching map as data. Its `StatementShape` then asks for their
pointwise equality, while `statementShape_of_orbital_integral_identity` assumes exactly that
equality. Thus the module is an honest interface boundary, not a source-faithful encoding of Ngo's
theorem, and cannot receive exact-statement credit.

Under rev-5.6 sections 2 and 5, source identity and an exact elaborated expression are mandatory.
The ordered binders, exact normalized expression, expression hash, checked transports, and
meaningful hypothesis/domain mutations therefore cannot truthfully be produced. The machine state
remains `M4`; no `sorry`, axiom, proxy theorem, or substituted result was added.

## Environment fingerprint

- Repository base revision: `d597fdb5ebb83567497a9aedd50af4142cf18c58`.
- Validation date: 2026-07-12 (Asia/Shanghai).
- Lean toolchain: `leanprover/lean4:v4.29.0`; Lean `4.29.0`, commit
  `98dc76e3c0a9b856c9b98726b713fb04fab16740`.
- Checked mathlib revision: `8a178386ffc0f5fef0b77738bb5449d50efeea95`.
- `lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- Lake manifest SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.
- Historical discovery module SHA-256:
  `d105f07451150a7e396e969ff063967e166b898b007f45990b6b9f20bd5913b8`.

## Validation evidence

Commands ran from this worker clone using only the existing canonical pinned `.lake` artifacts.
No update, build, fetch, or clone command was used.

| Command | Exit | Result |
|---|---:|---|
| `cd Formalizations/Lean && lake env lean AwesomeTheorems/Stage1/S1_M_083.lean` | 0 | Historical interface/discovery module elaborated; it contains no exact terminal target |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | Checked mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `rg -n -i 'FundamentalLemma\|fundamental lemma\|endoscop\|orbital.?integral\|transfer.?factor\|hyperspecial\|parahoric\|stable.?conjug' Formalizations/Lean/.lake/packages/mathlib/Mathlib --glob '*.lean'` | 0 | Only two unrelated textual hits: homotopical algebra and the Selberg sieve; no required declaration or object model found |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0434` | 0 | Rank 83, planned, L0/rework-required, legacy artifacts unaccepted, theorem incomplete |

## Retry condition

Provide an immutable copy and digest of the primary source with a precise theorem/page anchor and a
verbatim statement/definition crosswalk fixing the characteristic regime and all normalizations.
Then provide or implement pinned Lean definitions for reductive groups and Lie algebras over local
fields, endoscopic data, matching regular semisimple classes, stable and ordinary orbital integrals,
transfer factors, Haar normalizations, and hyperspecial unit functions. A later statement run can
then elaborate the source-faithful proposition, fingerprint it, and mutation-test its hypotheses.

Until that retry condition is met, statement acceptance and theorem completion are false. Because
the assigned phase is not self-tested to its completion gate, no `.stage1-worker-selftest.json` is
emitted.
