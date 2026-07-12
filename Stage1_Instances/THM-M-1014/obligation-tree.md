# THM-M-1014 frozen obligation architecture

## Freeze boundary

Registry version 1 freezes 14 semantic obligations before the proof node may accept closure. Twelve
are machine-required; the source and provenance overlays cannot masquerade as proof premises. The
denominator projection and its digest live in `obligation-registry.json`. A correction, split,
merge, exclusion, eligibility, risk, or weight change requires a new version and append-only delta.

The anchor audit found one unique terminal proof body in pinned mathlib. The direct theorem,
`continuous_map`, the convergence-in-distribution corollary, and the historical repository wrapper
do not receive four copies of coverage. All relevant analytic nodes share the same terminal body ID.

## Typed proof route

```text
M1014-ROOT [open M1]
`-- M1014-T-ASSEMBLE [checked conditional composition]
    `-- M1014-X-PINNED [exact pinned bridge; proof-node acceptance pending]
        |-- M1014-N-WEAK-TOPOLOGY
        |-- M1014-C-COMPOSED-TEST
        |-- M1014-L-MAP-INTEGRAL
        `-- M1014-L-TEST-LIMIT
```

The exact statement, domain, boundary, representation transport, and foundation obligations are
logical refinements of the root. Provenance, evidence, trust, documentation, and workflow edges are
stored in separate graphs. The structural validator checks all edge endpoints, reciprocal
proof/composition edges, acyclicity, required-machine reachability, node schemas, and recipe
coverage.

## Node ledger anchors

### m1014-root

The exact filtered pushforward statement from `Statement.lean`; it remains open at `M1`.

### m1014-s-exact

Owns every universe, ordered binder, instance, premise, and conclusion of the elaborated root.

### m1014-s-domain

Owns `ProbabilityMeasure`, its weak topology, the source measurable-open assumption, the target
Borel assumption, and continuity-derived measurability.

### m1014-s-boundary

Retains arbitrary filters and the constant, identity, Dirac, and degenerate cases supported by the
frozen instances. No sequential or nondegeneracy premise may be introduced.

### m1014-s-transport

Requires a checked direction from the human pushforward formulation to `ProbabilityMeasure.map`
with its explicit almost-everywhere measurability witnesses.

### m1014-s-foundation

Owns transitive imports, kernel trust, classical choice, quotients, extensionality, noncomputability,
and the no-oracle boundary.

### m1014-n-weak-topology

Exposes the bounded-continuous nonnegative integral characterization used by the pinned terminal
body rather than treating weak convergence as an unexplained primitive.

### m1014-c-composed-test

Constructs a valid source test function by composing a target test function with the continuous
map, including the boundedness and measurability side conditions.

### m1014-l-map-integral

Owns the pushforward integral identity on both the approximating measures and the limiting measure.

### m1014-l-test-limit

Applies source weak convergence to the composed test and rewrites with the map-integral identities.

### m1014-x-pinned

The unique bridge is
`ProbabilityMeasure.tendsto_map_of_tendsto_of_continuous` at mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. It is a pinned `M0-P` candidate, but this architecture
node does not accept its proof body for the downstream proof task.

### m1014-t-assemble

`root_of_continuousMappingTerminal` kernel-checks that the exact bridge conclusion yields the exact
public root. Its bridge premise remains explicit.

### m1014-x-source

Billingsley's precise edition/page, assumptions, discontinuity-set specialization, and errata review
remain `H1`; this overlay is not a proof premise.

### m1014-x-provenance

Owns terminal-body identity, aliases, dependency lock, license, transitive declarations, and trust
reports without duplicating semantic credit.

## Status boundary

Every leaf ledger is at most 100 substantive steps, and the major imported theorem remains an
explicit bridge. This phase freezes and self-tests architecture only. It does not accept the bridge
proof body, establish `H0` or `R0`, close the root, complete the audit, or complete the theorem.
