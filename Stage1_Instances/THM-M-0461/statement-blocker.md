# Statement gate blocker

Item: `S56-M-0461-STATEMENT`  
Theorem: `THM-M-0461`  
Verdict: blocked; no exact canonical Lean 4 target is claimed.

## First failed gate

The repository source supplies only the generic title "Equidistribution theorem", the attribution
"many mathematicians", the period "20th century", and the gloss "equidistribution of special
points". It does not define "special point" or identify a primary theorem. In particular, it does
not fix an ambient variety or dynamical system, a sequence or net of points or Galois orbits, a
height or ordering parameter, a limiting measure, a topology or mode of convergence, or the
geometric and arithmetic hypotheses.

At least three materially different roots remain compatible with that wording: equidistribution
of Galois orbits of small or special points on an abelian variety, arithmetic-dynamical
equidistribution of small or preperiodic points, and a classical analytic or ergodic uniform
distribution theorem. These roots have different domains, binders, assumptions, measures, and
conclusions. The adjacent source entry for Zhang's distribution theorem separately says
"equidistribution of small-height points", so it does not disambiguate this target and cannot be
silently substituted for it.

A repository-wide source search found only the same metadata wording and generated projections.
The pinned mathlib source search found no declaration matching equidistribution of special, small,
or Galois-orbit points. Absence of a search match is not itself proof that no formalization exists,
but it provides no exact target capable of repairing the missing source specification.

Consequently there is no truthful proposition to elaborate. The required ordered binders,
hypotheses, conclusion, domains and universes, boundary cases, minimal import, checked alternate
transports, normalized expression hash, and meaningful statement mutations cannot be frozen.
Under rev-5.6 section 5, statement ambiguity and a missing expression fingerprint are hard
tree-construction blockers. The instance remains at `M4`. No `sorry`, axiom, placeholder, opaque
proxy predicate, broadened theorem, or substitute target was introduced.

## Environment fingerprint

- Repository base revision: `3988dde7b18619a1cac9d1022256785302545497`.
- Validation date: 2026-07-12 (Asia/Shanghai).
- Lean toolchain: `leanprover/lean4:v4.29.0`; Lean `4.29.0`, commit
  `98dc76e3c0a9b856c9b98726b713fb04fab16740`.
- Lake: `5.0.0-src+98dc76e`.
- Checked mathlib revision: `8a178386ffc0f5fef0b77738bb5449d50efeea95`.
- `lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

## Validation evidence

Commands ran from this worker clone, except commands explicitly changing into
`Formalizations/Lean`. The existing `.lake` symlink points to the canonical pinned artifacts and
was read only. No update, build, fetch, or clone command was used.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0461` | 0 | Rank 309, lifecycle `planned`, legacy artifacts unaccepted, theorem incomplete |
| `rg -n -i 'THM-M-0461\|等分布定理\|特殊点的等分布\|equidistribution of special points\|special points.*equidistribut\|equidistribut.*special points' Docs Formalizations/Lean/AwesomeTheorems --glob '*.md' --glob '*.json' --glob '*.lean'` | 0 | Found only source metadata, generated projections, and this target's workflow/dossier records; no exact proposition |
| `rg -n -i 'equidistribut.*(special\|small\|galois)\|(?:special\|small\|galois).*equidistribut\|Szpiro\|Ullmo\|Zhang.*equidistribut\|Bilu.*equidistribut\|Yuan.*equidistribut' Formalizations/Lean/.lake/packages/mathlib/Mathlib --glob '*.lean'` | 1 | No matching pinned mathlib source declaration |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `cd Formalizations/Lean && lake --version` | 0 | Lake `5.0.0-src+98dc76e` |
| `cd Formalizations/Lean && sha256sum lean-toolchain lake-manifest.json` | 0 | Produced the two hashes recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | Checked mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` |

There is no applicable `lake env lean <target>.lean` command: neither the source nor the intake
identifies an exact expression. Elaborating a fabricated generic convergence statement or a chosen
equidistribution theorem would validate a substitution, not the assigned statement.

## Retry condition

Resume only after an immutable primary source or authoritative scope amendment identifies one
precise theorem and supplies its edition or immutable revision, theorem/page, definitions,
assumptions, errata disposition, ambient objects, special-point predicate, limiting process,
measure, and convergence mode. A later statement run can then construct the source-to-Lean
crosswalk, elaborate the exact target with minimal pinned imports, fingerprint it, check alternate
encodings, and mutation-test hypotheses, domains, binder scope, and boundary cases.

Until then, statement acceptance and theorem completion are false. Because this assigned phase is
not genuinely self-tested to its completion gate, no `.stage1-worker-selftest.json` is emitted.
