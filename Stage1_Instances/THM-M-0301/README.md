# THM-M-0301 rev-5.6 intake

`THM-M-0301` is the catalog item "BMO space duality theorem." The repository gives only the
gloss "BMO is the dual of H^1," attributes it to Charles Fefferman in 1971, and carries an
untrusted `已验证` (`verified`) label. This dossier records a fail-closed `planned` intake from the
uniform `L0 / rework_required` baseline.

## Intake result

Fefferman's two-page 1971 announcement was inspected. Its Theorem 1 states the classical
real-variable result on `R^n`: BMO, defined by bounded average oscillation over cubes and modulo
constants, is the dual of the Hardy space `H^1(R^n)`, with the integral pairing initially stated
on a dense subspace of smooth rapidly decreasing `H^1` functions. The adjacent text defines
`H^1` as the `L^1` functions whose Riesz transforms are all in `L^1`.

That identifies the intended theorem family and source statement, but it does not yet fix every
choice needed for a canonical Lean proposition: dimension and scalar conventions, Riesz-transform
normalization, the precise `H^1` norm/model, the BMO quotient norm, almost-everywhere representatives,
the extension of the pairing, and the strength of the norm comparison remain open. The announcement
also points to an in-preparation work for detailed proofs; no complete primary proof, errata record,
or independent source review is accepted here.

## Boundaries

The repository separately catalogs the same mathematical result as `THM-M-0363`. That dossier is
read-only discovery input; the two theorem IDs share no status, receipt, proof credit, or target
ownership. A master-level duplicate decision remains necessary before either identity can be used
as the other's canonical authority.

`IntakeProbe.lean` checks only adjacent pinned measure-theory, Schwartz-space, integration, and
continuous-linear-map interfaces. A bounded local search found no concrete BMO, real Hardy-space,
or analytic Riesz-transform API in pinned mathlib. No target theorem or proof body is declared.

The provisional root vector is `[H1, M4, R4]`: a primary announcement and its statement boundary
have been inspected, but complete proof-source fidelity and review remain open; no usable exact
formal target or proof is credited; and no source-faithful readable proof reconstruction has been
accepted. All six downstream tasks remain open. Neither audit completion nor theorem completion is
claimed.
