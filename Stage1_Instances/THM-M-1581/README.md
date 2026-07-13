# THM-M-1581 rev-5.6 intake

`THM-M-1581` is the discrete-mathematics catalog item `香农无噪声编码定理`
(`Shannon noiseless coding theorem`). The repository supplies Claude Shannon, the year 1948, the
gloss `数据压缩的极限` (`limit of data compression`), and an untrusted `verified` label. It
supplies no citation, source or channel model, entropy definition, code class, loss criterion,
ordered binders, hypotheses, conclusion, or formal artifact.

## Intake result

Shannon's 1948 paper is a strong primary-source lead. Part I, Section 9, Theorem 9 relates the
entropy rate `H` of a source and capacity `C` of a noiseless constrained channel: encoding can
approach average symbol rate `C / H`, and no nonsingular encoding can exceed it. This formulation
uses the paper's surrounding ergodic source, constrained-channel, duration, and transducer model.

That theorem is not the only result now called the noiseless or source coding theorem. Common
forms include a one-symbol prefix or uniquely-decodable expected-length inequality, an asymptotic
block source-coding theorem, and typical-set or almost-lossless fixed-rate variants. They differ in
domains, assumptions, error policy, quantifier order, and conclusion. The catalog gloss selects
none of them, so choosing one now would substitute missing mathematics.

## Source and formal boundary

This dossier creates a fail-closed `planned` instance and leaves the canonical mathematical and
Lean targets null. The provisional root vector is `[H1, M4, R4]`: `H1` records an inspected primary
source family and pinpoint candidate, not an accepted exact source-statement mapping; `M4` records
that no usable exact formal artifact is identified for an unselected root; `R4` records that no
source-faithful readable reconstruction can attach before target selection.

`IntakeProbe.lean` elaborates only adjacent pinned probability-mass, elementary entropy-function,
uniquely-decodable-code, and Kraft-McMillan APIs. A bounded exact-topic search found no source
entropy, expected-code-length source-coding theorem, or Shannon noiseless-coding declaration in
pinned mathlib or repository-local Lean. This is intake discovery, not the downstream anchor audit
and not a global absence claim.

`instance.json` is the structured scope authority; `scope-map.md` freezes proposition-changing
choices and exclusions; `source-statement-crosswalk.md` maps the catalog to the inspected source.
All six downstream tasks remain open in `task-dag.json`. No `H0`, `M0`, `R0`, accepted proof
state, audit completion, theorem completion, or master acceptance is claimed.
