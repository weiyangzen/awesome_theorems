# Source-statement crosswalk

## Repository sources inspected

`Docs/researches/math_theorems.md:10327-10332` records the title `Axiom A系统`, Stephen Smale,
1967, the complete gloss `双曲系统的公理` ("axioms for hyperbolic systems"), importance "high",
and status `已验证`. It contains no bibliography, definition, quantifiers, hypotheses, conclusion,
or proof. The record first entered the repository in commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`; that commit is repository provenance, not a primary
mathematical source.

`Docs/Stage0_Blueprint.md:38429-38454` repeats the same gloss while expressly leaving the precise
definitions and premises, proof process, dependency graph, equivalent formulations, axioms,
machine-checked state, and artifact links open. The rev-5.6 manifest retains `已验证` only in the
field `source_status_untrusted`. None of these records identifies an exact proposition.

## Primary definition source

Stephen Smale, "Differentiable dynamical systems", *Bulletin of the American Mathematical
Society* **73** (1967), no. 6, 747-817, DOI `10.1090/S0002-9904-1967-11798-1`, is the pinpoint
primary source. In section 1.6, item (6.1), printed page 777, after fixing `f : M -> M` as a
diffeomorphism of a compact manifold, Smale says that `f` satisfies Axiom A when `(a)` its
nonwandering set is hyperbolic and `(b)` its periodic points are dense in that set. Section 1.1 on
page 749 also gives the standing conventions that manifolds are connected and manifolds/maps are
differentiable of class `C^r`, `1 <= r <= infinity`, unless stated otherwise; boundarylessness is
not silently added here.

Stable records inspected: DOI resolver
`https://doi.org/10.1090/S0002-9904-1967-11798-1`, AMS article landing page
`https://pubs.ams.org/journals/bull/1967-73-06/S0002-9904-1967-11798-1`, and AMS PDF
`https://www.ams.org/bull/1967-73-06/S0002-9904-1967-11798-1/S0002-9904-1967-11798-1.pdf`.

The dependencies are also pinpointed in the same article: periodic points are defined in section
1.1 on page 747 using a positive iterate; wandering/nonwandering points and the closed invariant set
are defined on page 749; a hyperbolic set is defined on page 776 using a continuous invariant
Whitney splitting into stable and unstable tangent directions; and contracting/expanding bundle
maps and metric independence are treated on pages 758-759. The inspected PDF has SHA-256
`759e0601e50ceebc812c4a4c67e5b9ed59534848c6d342a2e2cf56871db19551`. The PDF is not copied
into this dossier. An independent source-fidelity/errata review remains open, so this locator does
not establish `H0`.

## Phrase crosswalk

| Repository phrase | Possible mathematical component | Prospective Lean surface | Intake status |
|---|---|---|---|
| `Axiom A系统` | the class of diffeomorphisms satisfying Smale's Axiom A | a new source-matched predicate on a bundled diffeomorphism | named definition family only |
| "hyperbolic" | invariant stable/unstable tangent splitting with uniform exponential estimates | manifolds, tangent maps, vector subbundles, norms, iterates, invariance, and estimates | exact encoding and constants absent |
| "system" | in item (6.1), a diffeomorphism of a connected compact `C^r` manifold under the standing conventions | exact manifold model, `C^r` level, bundled diffeomorphism, and iterates | primary definition boundary identified; boundary convention/formal encoding open |
| nonwandering set | points whose every neighborhood returns under a positive iterate | topology, iterates, neighborhood quantifiers, and a source-frozen predicate | not mentioned or defined in the record |
| periodic points | positive-period points dense in the relevant invariant set | `Function.periodicPts` and `Dense` after exact subspace/coercion decisions | likely component, not a supplied conclusion |
| Smale item (6.1), p. 777 | conjunction that defines Axiom A | a source-matched predicate, not a theorem proof | pinpoint definition identified; independent review open |
| `已验证` | untrusted inventory label | no proposition or proof object | explicitly rejected as evidence |

## Human-source boundary

The provisional human status is `H5` for the received catalog target: the primary source confirms
that it is a named axiom/definition, not a stable theorem proposition. This is not a claim that the
definition is mathematically invalid or that theorems about Axiom A systems are open. It means
ordinary theorem-proof execution must first be redirected to an approved exact proposition, as
required by the rev-5.6 `H5` rule.

Before source acceptance, an accountable reviewer must independently verify the recorded edition
and hash, map every standing convention and dependent definition, check corrections and errata, and
approve either a definition-only target decision or an exact redirected theorem. The review must
also explain why that result belongs to `THM-M-1413` rather than `THM-M-1412`, `THM-M-1414`, or
`THM-M-1415`. Even this pinpoint citation cannot turn a definition into a proved proposition.

## Lean discovery boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, a bounded search of
`Mathlib/Dynamics` and `Mathlib/Geometry/Manifold` found no declaration named for Axiom A,
nonwandering sets, or differentiable hyperbolicity. Pinned mathlib does expose generic
`Diffeomorph`, `tangentMap`, `omegaLimit`, `Function.periodicPts`, and `Dense` interfaces;
`IntakeProbe.lean` checks those names only. This bounded observation is not a full immutable anchor
audit, an external-project absence claim, an Axiom A encoding, or proof evidence.
