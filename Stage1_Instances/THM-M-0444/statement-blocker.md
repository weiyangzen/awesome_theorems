# Statement gate blocker

Item: `S56-M-0444-STATEMENT`  
Theorem: `THM-M-0444`  
Verdict: blocked; no exact canonical Lean target is claimed.

## First failed gate

The repository source record supplies only the label "Kolyvagin Euler system" and the gloss
"construction of an Euler system". It does not pinpoint a primary-source theorem or fix the base
field, elliptic curve or Galois representation, coefficient ring and prime, auxiliary indices,
field tower, cohomology groups, local conditions, Euler factors, Frobenius convention, or the
precise existence and compatibility conclusion. These choices distinguish materially different
constructions. Selecting one without a source pinpoint would invent missing mathematics and would
broaden or substitute the target.

The intake identifies Kolyvagin's 1990 *Euler systems* chapter only as a discovery candidate; no
edition page and theorem label have been accepted. The exact ordered binders, hypotheses,
conclusion, exceptional cases, canonical expression, expression fingerprint, checked transports,
and meaningful removed-hypothesis, changed-domain, changed-scope, and boundary mutations required
by rev-5.6 section 5.1 therefore cannot truthfully be produced. This is the hard statement-identity
blocker already anticipated by the accepted dependency's dossier.

The legacy discovery module
`Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_090.lean` does elaborate in the pinned
environment, but it does not repair the blocker. Its `StatementShape` asserts nonemptiness of a
locally designed `KolyvaginEulerSystemConstructionData` structure whose index type, admissibility
predicate, norm relation, derivative operator, local condition, and Selmer conclusion are abstract
fields. The module itself calls this deliberately weaker than a terminal theorem. Treating that
user-supplied interface as Kolyvagin's construction would be a proxy-statement substitution, so it
receives no exact-statement credit.

No theorem declaration, proxy predicate, `sorry`, axiom, placeholder, broadened target, or
substituted special case was introduced. Machine status remains `M4`, and statement acceptance and
theorem completion are false.

## Environment fingerprint

- Repository base revision: `129c68bce8fd58065c4af147e92a1975267f0279`.
- Validation date: 2026-07-12 (Asia/Shanghai).
- Lean toolchain: `leanprover/lean4:v4.29.0`; Lean `4.29.0`, commit
  `98dc76e3c0a9b856c9b98726b713fb04fab16740`.
- Checked mathlib revision: `8a178386ffc0f5fef0b77738bb5449d50efeea95`.
- `lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- Lake manifest SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.
- Legacy discovery module SHA-256:
  `50c776ffe34f43a11629d861b17bf95368ba96d71072d40e0f34c568e9b75fb2`.

## Validation evidence

Commands ran in this worker clone using only the existing canonical pinned `.lake` artifacts. No
update, build, fetch, or clone command was used.

| Command | Exit | Result |
|---|---:|---|
| `cd Formalizations/Lean && lake env lean AwesomeTheorems/Stage1/S1_M_090.lean` | 0 | Legacy abstract discovery module elaborated; its own documentation says the statement shape is not a terminal Kolyvagin construction theorem |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | Checked mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `rg -n -i 'Kolyvagin\|EulerSystem\|Euler system\|KolyvaginSystem' Formalizations/Lean/.lake/packages/mathlib/Mathlib --glob '*.lean'` | 1 | No matching declaration or source reference in pinned mathlib; exit 1 means no matches |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0444` | 0 | Rank 90, planned, L0/rework-required, legacy artifacts unaccepted, theorem incomplete |

## Retry condition

Provide an immutable primary-source edition and exact theorem/page pinpoint selecting the intended
Kolyvagin construction. The source transcription must fix every arithmetic datum, ordered binder,
hypothesis, indexed class, cohomology target, local condition, norm/corestriction relation, Euler
factor and Frobenius convention, including exceptional cases and errata. The next statement run can
then encode the claim with minimal pinned imports, serialize its elaborated expression, and run the
four required mutation classes.

Until that retry condition is met, the statement phase is not genuinely self-tested to its
completion gate. Consequently no `.stage1-worker-selftest.json` is emitted.
