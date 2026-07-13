# THM-M-1579 rev-5.6 intake

`THM-M-1579` is the discrete-mathematics catalog item `信道容量` (`channel capacity`). The
repository supplies Claude Shannon, the year 1948, the gloss `信道的最大传输速率` (`the maximum
transmission rate of a channel`), and an untrusted `verified` label. It supplies no citation,
channel class, capacity definition, logarithm base or time normalization, ordered binders,
hypotheses, conclusion, or formal artifact.

## Intake result

Shannon's 1948 paper is the primary result-family match, but it contains several materially
different capacity objects. Part I defines noiseless-channel capacity by asymptotic allowed-signal
growth and proves a determinant/root formula for finite-state constraints. Part II defines noisy
discrete capacity as the maximum information rate and later proves an operational limit theorem.
Part IV defines continuous-channel capacity through a normalized asymptotic mutual-information
maximum. These are neither one proposition nor interchangeable definitions.

Selecting a modern finite discrete memoryless channel formula, a capacity-achieving input theorem,
Shannon's operational Theorem 12, or the neighboring noisy-channel coding theorem would invent,
narrow, or substitute missing mathematics. The catalog noun and gloss do not decide whether this
item is a definition, a characterization theorem, or an operational theorem.

## Source and formal boundary

This dossier therefore creates a fail-closed `planned` instance and leaves the canonical
mathematical and Lean targets null. The proposed root vector is `[H5, M4, R4]`: `H5` classifies only
the received catalog wording as not yet one stable truth-valued proposition; it does not dispute
Shannon's published definitions or theorems. `M4` records that no usable exact formal artifact has
been identified for the unselected root, and `R4` records that no source-faithful proof
reconstruction can attach to it yet.

`IntakeProbe.lean` elaborates only adjacent pinned probability-mass, stochastic-kernel,
Kullback-Leibler, elementary entropy, uniquely-decodable-code, and Hamming APIs. A bounded exact
topic search found no channel-capacity or mutual-information theorem declaration in pinned mathlib
or repository-local Lean. One repo-local audit string points to an immutable external
`channel-capacity` project; that string is not a declaration or proof credit, while the referenced
project is an unaudited candidate lead for the downstream anchor audit. This intake search is not a
global absence claim.

`instance.json` is the structured scope authority; `scope-map.md` freezes proposition-changing
choices and exclusions; `source-statement-crosswalk.md` maps the catalog to the inspected source.
All six downstream tasks remain open in `task-dag.json`. No `H0`, `M0`, `R0`, accepted proof state,
audit completion, theorem completion, or master acceptance is claimed.
