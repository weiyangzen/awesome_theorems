# Source-statement crosswalk

| Claim component | Source anchor available at intake | Selected target component | Assessment |
|---|---|---|---|
| Theorem identity | `Docs/researches/math_theorems.md`, entry "Rankine-Hugoniot条件" | Rankine-Hugoniot condition | Repository identity only; no equation or hypotheses |
| Informal content | Same entry: `激波的跳跃条件` (shock jump condition) | Vanishing weak defect across a shock interface | Compatible but underdetermined |
| Attribution/date | Same entry: Rankine/Hugoniot, 1870 | Historical theorem family | Untrusted metadata pending primary-source audit |
| Formal status | Same entry: `已验证` | No Lean declaration selected | Metadata label gives no machine credit |
| Scalar law | Not specified by repository source | `u_t + (f(u))_x = 0`, real scalar states | Explicit intake specialization requiring review |
| Jump equation | Not written in repository source | `s(uR-uL)=f(uR)-f(uL)` | Standard candidate formulation, not yet source-certified or Lean-elaborated |
| Weak-solution equivalence | Not written in repository source | Zero distributional interface defect iff jump equation | Necessary to make the target a theorem rather than a bare equation; source audit open |

Stage0 repeats the same terse content in `Docs/Stage0_Blueprint.md` and adds no mathematical
hypotheses. Consequently this intake is `H3`: a theorem family is identifiable, but no pinpoint
primary edition, theorem/page locator, assumption mapping, errata check, archive hash, or independent
review exists. The scalar target is chosen conservatively for execution and is not represented as a
translation already guaranteed by the metadata.

The source-audit phase must locate immutable primary or authoritative mathematical sources for the
weak jump calculation, distinguish Rankine's and Hugoniot's historical formulations from the modern
conservation-law statement, record editions/pages and corrections, and review the mapping of every
hypothesis and both implications. Until then, no `H0` or historical-fidelity claim is made.
