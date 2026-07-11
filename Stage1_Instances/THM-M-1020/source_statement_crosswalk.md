# Source-statement crosswalk

| Claim component | Repository source | Exact content available | Intake assessment |
|---|---|---|---|
| Name | `Docs/researches/math_theorems.md`, entry “Parseval恒等式” | Name only | Parseval has several inequivalent Fourier/integration formulations |
| Claimed statement | Same entry; projected into `Docs/Stage0_Blueprint.md` | `特征函数的积分恒等式` | Insufficient to determine a proposition |
| Attribution/date | Same entry | Marc-Antoine Parseval; 1799 | Historical metadata does not identify a probability characteristic-function theorem or a primary source |
| Domain | Probability theory / foundations metadata | Classification only | Does not decide functions versus measures, real line versus higher dimension, or required densities |
| Verification status | Same entry | `已验证` | Untrusted source label under rev-5.6; no proof or source receipt accompanies it |
| Lean target | Target manifest lane `hard_mathlib_anchor_and_wrapper` | No module or declaration | Anchor discovery must follow, not precede, exact statement selection |

## Unresolved source fork

The phrase can plausibly refer to a Plancherel theorem applied to characteristic functions, an
identity relating two probability densities through their characteristic functions, or another
Fourier inner-product formula. These differ in hypotheses and constants. In particular, a general
characteristic function is bounded but need not be integrable or square-integrable. Consequently,
none of these candidates is promoted to the canonical statement.

The statement phase requires a primary mathematical source with an edition or immutable file,
page/theorem location, displayed formula, Fourier-transform convention, domains, assumptions, and
errata check. It must then map each premise and conclusion to ordered Lean binders. Until that
exists, `H0` is impossible and machine closure is ineligible for credit.

No external URL or theorem name is presented as evidence, and no machine-checked result is claimed.
