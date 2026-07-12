# Statement gate blocker

Item: `S56-M-0521-STATEMENT`  
Theorem: `THM-M-0521`  
Verdict: blocked; no exact canonical Lean target is claimed.

## First failed gate

The accepted intake records only the repository label "Kolyvagin's theorem" and the gloss "BSD
for elliptic curves of rank 0 or 1". That text does not identify a primary-source theorem or fix
whether rank is analytic or algebraic, whether the rank-zero and rank-one cases are separate, the
base field and curve class, modularity and conductor assumptions, Heegner hypotheses, or which BSD
conclusion is meant. Rank equality, finiteness of the Tate-Shafarevich group, prime-primary order
statements, and the full leading-coefficient formula are materially different propositions.

The nearby repository target `THM-M-0522` separately names a Kolyvagin-Gross-Zagier theorem, so it
cannot be used to infer this target's identity. The intake lists Kolyvagin's finiteness paper and
his *Euler systems* chapter only as discovery candidates; it accepts no immutable edition,
theorem/page pinpoint, assumption crosswalk, errata review, or independent source review. Choosing
a familiar modern corollary would therefore invent missing mathematics and could broaden or
substitute the requested theorem.

Consequently the ordered binders, hypotheses, conclusion, boundary cases, canonical expression,
expression fingerprint, checked alternate transports, and the four meaningful mutation classes
required by rev-5.6 section 5.1 cannot be produced truthfully. No theorem declaration, proxy
predicate, axiom, placeholder, broadened target, or substituted special case was introduced.
Machine status remains `M4`; statement acceptance and theorem completion are false.

## Lean API boundary

The smallest pinned probe, `IntakeProbe.lean`, elaborates with three imports and confirms only
partial vocabulary: Weierstrass elliptic curves and projective points, generic complex L-series
derivatives, and the Dedekind-domain Selmer group. The generic `LSeries` is not an elliptic curve's
Hasse-Weil L-function, and `IsDedekindDomain.selmerGroup` is not the Galois-cohomological Selmer
group needed by Kolyvagin's argument. A bounded source search found no `Kolyvagin` occurrence in
the pinned mathlib tree. These checks do not define or prove the target.

## Environment fingerprint

- Repository base revision: `e3d0fd205c9c81486cb86f68cdc66d4d4e5bb264`.
- Validation date: 2026-07-12 (Asia/Shanghai).
- Lean toolchain: `leanprover/lean4:v4.29.0`; Lean `4.29.0`, commit
  `98dc76e3c0a9b856c9b98726b713fb04fab16740`.
- Checked mathlib revision: `8a178386ffc0f5fef0b77738bb5449d50efeea95`.
- `lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- Lake manifest SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.
- Intake probe SHA-256:
  `a00c88b24128515c82af4b9d75102a1efcf2a9e708d970a06238a3b02bf8cf0e`.
- The worker used the pre-existing canonical `.lake` symlink read-only; it ran no update, build,
  fetch, or clone command.

## Validation evidence

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0521` | 0 | Rank 893, planned, L0/rework-required, legacy artifacts unaccepted, theorem incomplete |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0521/IntakeProbe.lean` | 0 | All six partial API checks elaborated against the pinned environment |
| `git -C /home/sansha-2/external/awesome_theorems/Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | Checked mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `rg -n -i 'Kolyvagin' /home/sansha-2/external/awesome_theorems/Formalizations/Lean/.lake/packages/mathlib/Mathlib --glob '*.lean'` | 1 | No occurrence in pinned mathlib; exit 1 means no matches |

## Retry condition

Provide an immutable primary-source edition and an exact theorem/page pinpoint selecting the
intended Kolyvagin result, plus an independent review of its transcription. The accepted source
crosswalk must fix the rank notion and direction, curve and field hypotheses, all modularity,
conductor, Heegner and nonvanishing conditions, the exact Mordell-Weil and Tate-Shafarevich
conclusions, and exceptional cases or errata. A later statement run can then encode that claim,
minimize pinned imports, serialize its elaborated expression, and execute removed-hypothesis,
changed-domain, changed-scope, and boundary mutations.

Until that condition is met, the statement phase is not genuinely self-tested to its completion
gate. Therefore no `.stage1-worker-selftest.json` is emitted.
