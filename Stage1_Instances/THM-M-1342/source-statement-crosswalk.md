# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md:9789-9794` supplies exactly the title
`李雅普诺夫稳定性理论`, attribution to Aleksandr Lyapunov, the year 1892, the gloss
`平衡点的稳定性`, importance "high," and status `已验证`. Git history attributes all six
uncited lines to repository commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The entry has no
equation, dynamical model, definition, binder, hypothesis, conclusion, bibliography, edition,
theorem/page locator, proof boundary, correction record, or formal artifact.

`Docs/Stage0_Blueprint.md:36507-36532` repeats the gloss while explicitly leaving the exact
definitions and premises, proof process, dependencies, equivalent formulations, axioms, machine
status, and artifact links open. The rev-5.6 manifest preserves `已验证` only as
`source_status_untrusted` and resets the target to `L0 / rework_required`.

The adjacent physics record `Docs/researches/physics_theorems.md:6801-6807` says to use a Lyapunov
function to judge equilibrium stability. It has no exact proposition or source locator and belongs
to distinct target `THM-P-0796`; it is corroborating topic metadata, not the authoritative source
or a substitute for `THM-M-1342`.

## Component crosswalk

| Repository element | Possible mathematical component | Prospective Lean surface | Intake assessment |
|---|---|---|---|
| "stability theory" | definitions plus theorems about persistence, attraction, rates, and instability | predicates over flows or quantified integral curves | subject-family label, not one proposition |
| "equilibrium" | fixed point of a vector field or flow, constant solution, equilibrium trajectory, or invariant set | `Function.IsFixedPt`, an equation such as `f x0 = 0`, or a checked constant-curve bridge | object and dynamics absent |
| "stability" | Lyapunov, uniform, asymptotic, exponential, local, global, orbital, or another notion | neighborhoods/balls and quantified forward solutions; possibly `Filter.Tendsto` for attraction | conclusion and quantifier order absent |
| Aleksandr Lyapunov / 1892 | historical attribution | provenance metadata only | not an edition, theorem/page locator, or reviewed source |
| `已验证` | untrusted catalog status | no Lean declaration or proof object | explicitly rejected as evidence |

## Inspected discovery source

Gerald Teschl, *Ordinary Differential Equations and Dynamical Systems*, Graduate Studies in
Mathematics 140, AMS, 2012, Section 6.5, pages 198-199, was inspected as an authoritative modern
source lead. On page 198 it gives three separate fixed-point notions: Lyapunov stability by nested
neighborhoods and forward trajectories, asymptotic stability by adding local convergence, and
exponential stability by a local exponential estimate. It also states that convergence condition
(6.26) does not automatically imply stability.

The author-hosted preliminary PDF retrieved during intake had SHA-256
`362433156525216abf596c17ce843204510e96d57afa4284a37c7aa5a9ffc36e`; the official errata PDF had
SHA-256 `3eacbac5b8fc762c5d3f21183cba3ae638b9ac5fbe703cc52cf2857b9605996e`. The catalog does not cite
this book, and the cited passage supplies definitions rather than selecting a theorem for the
catalog target. The source is therefore used only to demonstrate the material ambiguity; no
canonical root or H0 evidence is credited.

## Proposition boundaries

A fixed-point stability definition is not the same proposition as a direct-method criterion,
linearization theorem, spectral characterization, converse theorem, invariance principle, or
instability result. Lyapunov, asymptotic, and exponential stability also have different logical
strengths. The statement changes further with autonomous versus nonautonomous dynamics, one flow
versus all possibly nonunique solutions, local versus global existence, point versus set stability,
and metric versus general topological encodings. The repository chooses none of these.

The neighboring math targets are material boundaries: `THM-M-1343` covers the direct method,
`THM-M-1344` covers the indirect method, and `THM-M-1355` separately covers stability of linear
systems. This intake borrows no source or proof credit from them.

## Source and Lean gate

The supplied wording is not one stable proposition. Before statement execution, an accountable
reviewer must redirect the theory label to a corrected exact claim, preserve an immutable source
edition, record a stable definition/theorem/section/page locator, transcribe all ordered binders,
hypotheses, and the complete conclusion, audit referenced definitions and errata, reconcile the
three neighbor targets, and obtain independent source review. Only then may the statement phase
freeze minimal imports, an elaborated Lean expression and environment fingerprint, checked
alternate transports, and statement mutations.

The provisional human-source status is `H5`. This does not assert that Lyapunov stability theory is
false or mathematically open. It records that a subject label and noun phrase cannot be proved as a
Lean proposition without a source-governed correction. `M4` records no usable exact formal artifact
for that unidentified root, and `R4` records that no source-faithful proof reconstruction can attach
before root selection.

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the bounded intake probe
elaborates adjacent solution, fixed-point, neighborhood, ball, and convergence APIs. A bounded
local search found no obvious named target theorem under the searched terms. These facts are
feasibility inputs only, not the later exhaustive anchor audit, an external absence claim, or proof.
