# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:4720-4725` records only the title, Schauder attribution, 1930 date,
the gloss "fixed point of a compact map on a Banach space," importance, and an untrusted `verified`
status. `Docs/Stage0_Blueprint.md:17422-17445` repeats the gloss while leaving the definitions,
premises, formal system, proof, dependencies, equivalents, axioms, machine status, and artifacts
open. Neither record is an exact theorem statement.

## Primary source lead

J. Schauder, "Der Fixpunktsatz in Funktionalraeumen," *Studia Mathematica* **2**(1) (1930),
171-180, DOI `10.4064/sm-2-1-171-180`, was inspected through the publisher scan. The relevant text
is `Satz II` on printed page 175: in a `B`-space, let `H` be convex and closed; let the continuous
functional operation `F` map `H` into itself; if `F(H)` is compact, then a fixed point exists. The
paper's surrounding definitions and printed page 175 connect `B`-spaces with the real normed
complete spaces considered by Banach.

The scan and Crossref metadata are external discovery inputs. They have not been lawfully preserved
inside an accepted source bundle, and no independent reviewer has approved the exact incorporated
definitions, nonemptiness convention, translation, proof boundary, corrections, or errata. This is
`H1`, not `H0`.

## Component crosswalk

| Input wording | Candidate mathematical component | Planned Lean component | Intake status |
|---|---|---|---|
| `B`-space / Banach space | real complete normed linear space | `NormedAddCommGroup E`, `NormedSpace Real E`, `CompleteSpace E` | family identified; exact binders open |
| convex and closed `H` | invariant domain, not assumed compact | `Convex Real H`, `IsClosed H` | source lead inspected |
| `F` maps `H` into itself | self-map of the selected domain | `Set.MapsTo F H H` or subtype map | encoding open |
| continuous `F` | continuity of the self-map | `ContinuousOn F H` or subtype continuity | global/domain scope open |
| `F(H)` compact | compact particular range | `IsCompact (F '' H)` | candidate only; relative/modern variants excluded pending review |
| fixed point exists | some in-domain point satisfies `F x = x` | `Exists fun x => x in H and Function.IsFixedPt F x` | conclusion family identified |
| no printed nonempty premise | possible source convention or implicit consequence | `H.Nonempty` if approved | materially unresolved |
| `verified` | inherited catalog classification | no formal component | explicitly untrusted |

## Duplicate and neighbor boundary

| Target | Repository wording | Relationship and boundary |
|---|---|---|
| `THM-M-0318` | fixed-point theorem on a Banach space | same title/author/year in functional analysis; its dossier selects the compact-domain form and transfers no state or evidence |
| `THM-M-0636` / `THM-M-0640` | Brouwer compact-convex / closed-ball families | finite-dimensional or differently scoped premises, not substitutes |
| `THM-M-0638` | Tychonoff locally convex fixed-point theorem | broader ambient family, separately owned |
| `THM-M-0639` | Kakutani set-valued fixed-point theorem | changes a function to a correspondence, not a substitute |
| `THM-M-1444` | Banach fixed-point theorem | contraction and uniqueness family, not Schauder's compactness theorem |

## Acceptance boundary

Before `H0`, an independent reviewer must approve a preserved immutable edition, exact theorem and
page, every incorporated definition and premise, conclusion, translation, proof boundary, and
errata disposition. Before statement acceptance, integration must decide the relationship with
`THM-M-0318` and freeze one exact claim, binder order, boundary policy, Lean encoding, checked
transports, expression hash, and environment fingerprint.
