# Scope map

## Preserved theorem family

The repository fixes the title `单值性定理` and the gloss "analytic continuation of holomorphic
functions along paths." This identifies the classical monodromy-theorem family, but not a
proposition. Intake preserves two source-supported candidate branches without selecting either:

- **homotopy invariance:** analytic continuations of one initial element along paths with the same
  endpoints agree when the paths are homotopic relative to their endpoints;
- **simply-connected single-valuedness:** if an initial element admits continuation along every
  path in a simply-connected domain, the resulting branch is single-valued.

The second is commonly derived from the first after path connectedness and the required
continuation and uniqueness infrastructure. That relationship is not yet a checked transport for
this target.

## Proposition-changing decisions

Statement work must select and crosswalk all of the following from an immutable source:

1. A domain in `Complex`, `Complex^n`, a Riemann surface, Riemann domain, or analytic manifold,
   together with openness, nonemptiness, connectedness, local path connectedness, and simple
   connectedness assumptions.
2. The codomain and the model of a holomorphic/analytic element or germ, including its starting
   point, neighborhood, representative equivalence, and identity/uniqueness principle.
3. What it means to continue along a path: finite chains of elements, germs over each point, a
   sheaf-etale lift, or an equivalent construction, plus existence and uniqueness requirements.
4. Whether paths are arbitrary continuous paths, piecewise smooth paths, or another class; their
   parametrization, endpoints, and whether homotopies are relative to endpoints.
5. Whether continuation is assumed along two paths, every member of one homotopy, every path from
   a basepoint, or every path in the whole domain.
6. Whether the conclusion is equality of terminal germs/elements, path independence, existence of
   a global single-valued analytic function, or a uniqueness statement, with ordered binders and
   all coercions fixed.

## Boundary and degenerate cases

No case is excluded at intake. A source-selected statement must resolve empty or disconnected
domains, endpoints outside the starting component, constant paths and homotopies, identical paths,
loops, a singleton or empty lift family, failure of continuation along some path, non-separated
germ spaces, zero or constant analytic elements, and domains that are connected but not simply
connected. These cases can change whether the hypotheses are satisfiable or the conclusion follows.

The dossier excludes a uniqueness-of-analytic-continuation theorem on one connected open set, an
identity theorem, a path-lifting theorem by itself, a covering-space monodromy action, and analytic
continuation of a particular special function. Those are related inputs or different targets, not
silent replacements for the catalog record.

## Lean boundary

Pinned mathlib's `IsLocalHomeomorph.monodromy_theorem` uses a topological base `X`, a total space
`E`, a projection `p : E -> X`, `IsLocalHomeomorph p`, `IsSeparatedMap p`, two paths, an
endpoint-relative homotopy, a family of continuous lifts with common start, and concludes equality
of lift endpoints. Its docstring describes how an etale space of analytic germs could instantiate
the abstract theorem. The current intake has not selected or constructed that analytic etale
space, related it to the source's continuation notion, or derived the simply-connected branch.
The pinned candidate is therefore recorded for downstream exact anchor audit without machine
status credit.
