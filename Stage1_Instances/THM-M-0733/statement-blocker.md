# Exact-statement gate: blocked

Item: `S56-M-0733-STATEMENT`  
Theorem: `THM-M-0733`  
Worker base revision: `91055abb3f5bee7f79323bc9cbefa7f2a8145f1f`

## Gate decision

The exact Lean 4 target cannot be truthfully elaborated from the repository source record. The
record gives the topic label `自然证明` (Natural Proofs), the attribution Razborov/Rudich (1994),
and only the gloss `证明复杂性下界的障碍` (an obstacle to proving complexity lower bounds). The
separate computer-science catalogue similarly says only that natural-proof methods face a
fundamental barrier. Stage0 explicitly leaves the exact definitions, premises, computation model,
resource measure, adversary model, and security parameter open.

These words do not select one proposition from the Natural Proofs framework. In particular, they
do not fix:

- the Boolean-function ensemble, truth-table encoding, circuit basis, circuit family, or size
  bound;
- the exact largeness density and its asymptotic quantifiers;
- the constructivity algorithm, input representation, uniformity convention, and running-time
  bound;
- the usefulness condition, including eventual versus infinitely-often quantification;
- the pseudorandom-function or related cryptographic premise, hardness parameters, advantage, and
  security quantifiers;
- the conditional barrier conclusion, small input lengths, zero/vacuous bounds, or other boundary
  conventions.

Different choices change the domains, ordered binders, hypotheses, and conclusion. Replacing the
gloss with an unconditional assertion that every circuit lower-bound proof is impossible would be
false. Choosing a particular conference, journal, survey, or standard corollary formulation without
an immutable pinpoint source and approved crosswalk would instead substitute mathematics not
present in the target record.

Consequently there is no canonical human claim to map to a Lean `Prop`, no meaningful minimal
import claim, no normalized expression to fingerprint, and no sound removed-hypothesis,
changed-domain, binder-scope, or boundary-case mutation suite. This is the first failed gate under
section 5.1 of the rev-5.6 blueprint, before proof evidence may be inspected. No target declaration,
`sorry`, `admit`, `axiom`, assumed barrier, weakened finite instance, or broadened theorem was added.

## Pinned validation record

Validation ran on `2026-07-12` (`Asia/Shanghai`) inside the worker clone. The existing canonical
`.lake` link and artifacts were used read-only; no update, build, fetch, or clone was run.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 1546 uniform-L0 Lean 4 targets, and the execution skill validated |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0733` | 0 | rank 770, planned, legacy artifacts unaccepted, `theorem_complete: false` |
| repository `rg` search for `THM-M-0733`, the Chinese/English labels, authors, and both glosses | 0 | found only the underspecified catalogue records and open Stage0 fields; no source-frozen proposition |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `(cd Formalizations/Lean && lake --version)` | 0 | Lake `5.0.0-src+98dc76e` |
| `(cd Formalizations/Lean && sha256sum lean-toolchain lake-manifest.json)` | 0 | hashes `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2` and `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | mathlib `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| pinned-mathlib `rg` search for Natural Proofs, Razborov/Rudich, pseudorandom functions, circuit lower bounds, and Boolean circuits | 0 | only an unrelated prose occurrence of "natural proof" was found; no theorem-specific API or formal target |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0733/IntakeProbe.lean)` | 0 | candidate finite-function/cardinality/polytime-machine APIs elaborated; this is an intake-only vocabulary probe, not a canonical target |
| `rg -n '\\b(sorry|admit)\\b|^[[:space:]]*axiom\\b' Stage1_Instances/THM-M-0733 -g '*.lean'` | 1 | expected no-match exit; no prohibited placeholder or axiom occurs in the target's Lean source |

The successful API probe distinguishes an available pinned Lean environment from the missing
mathematical statement. It receives no statement or proof credit.

## Retry condition and status boundary

An accountable source review must preserve and hash an immutable primary-source edition, select an
exact theorem/page or passage, incorporate the referenced definitions, resolve errata and version
differences, and freeze every parameter and quantifier listed above. It must crosswalk that exact
claim to this repository target and independently approve the selection. A later statement worker
can then implement the same claim, minimize pinned imports, serialize and hash its elaborated
expression, check credited alternate encodings, and execute all four required mutation classes.

The statement item remains `[ ]`, blocked at `M4`; the root remains `[H5, M4, R4]`, with
`audit_complete: false` and `theorem_complete: false`. The assigned phase did not pass its
completion gate, so no `.stage1-worker-selftest.json` is emitted.
