# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md` identifies the item as "随机图相变",
attributes it to Erdos and Renyi in 1960, and describes it only as "the phase
transition phenomenon in random graphs". `Docs/Stage0_Blueprint.md` repeats
that metadata. Neither file fixes a model, asymptotic regime, quantifiers, or
conclusion. Their `已验证` label is explicitly untrusted under rev-5.6.

## Primary-source candidate

Paul Erdos and Alfred Renyi, "On the evolution of random graphs",
*Publications of the Mathematical Institute of the Hungarian Academy of
Sciences* **5** (1960), 17-61, is the historical primary-source candidate.
The paper studies the component evolution of a random graph as its number of
edges grows and is the source to inspect for the intended threshold claim.

This bibliographic identification is discovery evidence, not `H0`. The exact
theorem number/page, original `G(n,m)` hypotheses, translation to `G(n,p)`,
edition scan, and errata have not yet been independently checked. The common
modern `p = c/n` formulation therefore remains a proposed normalization, not
a source-certified quotation.

## Crosswalk

| Repository phrase | Intended mathematical component | Required Lean component | Intake status |
|---|---|---|---|
| "random graph" | Erdos-Renyi graph on `n` labelled vertices | finite vertex type, simple graph, Bernoulli-edge probability law | model family included; exact source model open |
| "phase transition" | qualitative change at average degree one | asymptotic theorem split at `c < 1` and `c > 1` | included; exact bounds open |
| subcritical regime | no linear component; largest component logarithmic in standard forms | maximum component cardinality and probability limit | included; constants and probability mode open |
| supercritical regime | one linear giant; other components logarithmic in standard forms | unique-giant predicate, component-size bounds, probability limit | included; giant fraction equation open |
| year 1960 | historical evolution theorem | immutable source locator and assumption map | paper identified; theorem/page review open |

## Statement-fidelity blockers

1. Inspect a stable scan of the 1960 paper and record the exact theorem/page,
   notation, hypotheses, and all conclusions selected for the canonical root.
2. Decide whether the root follows the paper's uniform `G(n,m)` process or a
   modern `G(n,p)` transport; any transport must later be mathematically and
   kernel checked rather than asserted.
3. Fix all asymptotic quantifiers, constants, rounding conventions, and the
   probability mode, including what "small" means on each side.
4. Check corrections or errata and obtain independent source review before
   any `H0` claim.
5. Audit pinned mathlib and external Lean 4 projects only after the exact
   statement is frozen; no machine candidate is credited by this intake.
