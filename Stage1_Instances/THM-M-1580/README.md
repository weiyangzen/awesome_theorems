# THM-M-1580 rev-5.6 intake

`THM-M-1580` is the discrete-mathematics catalog item `香农噪声信道编码定理`
(`Shannon noisy-channel coding theorem`). The repository supplies Claude Shannon, the year 1948,
the gloss `信道编码的存在性` (`existence of channel coding`), and an untrusted `verified` label.
It supplies no citation, channel model, source model, capacity definition, code or decoder, error
criterion, ordered binders, hypotheses, conclusion, or formal artifact.

## Intake result

Shannon's 1948 paper is a strong primary-source lead. Its Section 13, Theorem 11 states a
source-channel theorem for a discrete source of entropy rate `H` and a discrete noisy channel of
capacity `C`: below capacity, suitable coding makes error frequency or equivocation arbitrarily
small, while above capacity it gives an equivocation bound and converse. The same section's
Theorem 12 instead characterizes capacity by the asymptotic logarithm of the largest reliably
distinguishable signal set.

Those formulations do not uniquely repair the catalog gloss. Theorem 11 depends on the paper's
ergodic finite-state source/channel framework and combines achievability with above-capacity
claims. A modern finite-alphabet memoryless-channel theorem instead quantifies over block codes,
uses a strict rate below mutual-information capacity, and must choose average or maximal block
error. The printed `H <= C` clause also needs source review because its displayed random-coding
argument later uses a strict rate inequality. Selecting any one of these roots now would invent or
substitute missing mathematics.

## Source and formal boundary

This dossier therefore creates a fail-closed `planned` instance and leaves the canonical
mathematical and Lean targets null. The provisional root vector is `[H5, M4, R4]`: `H5` classifies
the received catalog wording as not yet one stable proposition; it does not dispute Shannon's
published results. `M4` records that no usable exact formal artifact has been identified for that
unselected root, and `R4` records that no source-faithful readable proof can attach to it yet.

`IntakeProbe.lean` elaborates only adjacent pinned probability-mass, stochastic-kernel,
Kullback-Leibler, elementary entropy, uniquely-decodable-code, and Hamming APIs. A bounded exact
topic search found no channel-capacity or noisy-channel coding theorem declaration in pinned
mathlib or repository-local Lean. This is intake discovery, not the downstream anchor audit and
not a global absence claim.

`instance.json` is the structured scope authority; `scope-map.md` freezes proposition-changing
choices and exclusions; `source-statement-crosswalk.md` maps the catalog to the inspected source.
All six downstream tasks remain open in `task-dag.json`. No `H0`, `M0`, `R0`, accepted proof
state, audit completion, theorem completion, or master acceptance is claimed.
