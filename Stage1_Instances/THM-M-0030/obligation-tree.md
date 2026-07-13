# THM-M-0030 frozen obligation tree

This is the public architecture surface for `S56-M-0030-OBLIGATION_TREE`. The registry contains
28 semantic obligations. The accepted root remains `[H1, M3, R3]`; every node below is a frozen
proof interface, visible source-body decomposition, or governance boundary rather than accepted
proof state.

## Tree

```text
M0030-ROOT exact proper-ideal Krull intersection theorem
`-- M0030-X-MATHLIB-BODY exact pinned terminal declaration
    `-- M0030-N-FINITE-MODULE finite-module intersection theorem
        |-- M0030-N-LOCAL-CONTAINMENT proper local ideal lies in the Jacobson radical
        |   |-- M0030-L-PROPER-MAXIMAL
        |   `-- M0030-L-MAXIMAL-JACOBSON
        `-- M0030-N-JACOBSON general Jacobson-intersection theorem
            |-- M0030-L-JACOBSON-UNIT checked sign adapter
            |   `-- M0030-X-JACOBSON-UNIT-SOURCE pinned source-shaped unit theorem
            `-- M0030-N-FIXEDPOINT-IFF characterize the power intersection by r*x=x
                `-- M0030-T-FIXEDPOINT-COMPOSE combine both iff directions
                    |-- M0030-B-FIXEDPOINT-FORWARD
                    |   |-- M0030-C-INFIMUM-SUBMODULE
                    |   |-- M0030-C-STABLE-INTERSECTION
                    |   |   `-- M0030-C-INFIMUM-SUBMODULE (shared)
                    |   `-- M0030-L-FG-NAKAYAMA
                    |       `-- M0030-T-STABILITY-EVALUATE
                    |           |-- M0030-C-INFIMUM-SUBMODULE (shared)
                    |           |-- M0030-C-STABLE-INTERSECTION (shared)
                    |           `-- M0030-L-STABILIZATION-INDEX
                    |               `-- M0030-C-STABLE-INTERSECTION (shared)
                    `-- M0030-B-FIXEDPOINT-BACKWARD
                        `-- M0030-L-POWER-INDUCTION
```

The statement/foundation obligations `M0030-S-*` refine the root without duplicating proof credit.
The `M0030-X-SOURCE`, `M0030-X-PROVENANCE`, `M0030-X-TRUST`, `M0030-X-READABLE`, and
`M0030-X-WORKFLOW` nodes are typed support boundaries and never proof premises.

## Node ledgers

### m0030-root

- Claim: the exact `KrullIntersectionTarget` from `Statement.lean`.
- Inputs: `M0030-X-MATHLIB-BODY`, exact canonical binder context.
- Route: checked binder-order adapter `root_of_exactMathlibAnchor`.
- Boundary: the anchor is still an explicit premise and is not installed or accepted here.

### m0030-s-interface

- Claim: preserve `CommRing`, Noetherian, local, ideal, properness, and natural-power scope exactly.
- Inputs: the statement fingerprint and four mutation classes.
- Route: re-elaborate `KrullIntersectionTarget` without added hypotheses.
- Boundary: scope evidence cannot close a proof.

### m0030-s-membership-transport

- Claim: ideal equality is equivalent to the elementwise every-power formulation.
- Inputs: the canonical root and `MembershipTarget`.
- Route: `krullIntersectionTarget_iff_membershipTarget` uses ideal extensionality and `mem_iInf`.
- Boundary: a checked transport is not a second semantic theorem or proof body.

### m0030-s-proper-boundary

- Claim: `I = top` is a counter-boundary and `I = bottom` stays in scope.
- Inputs: local-ring nontriviality and ideal lattice operations.
- Route: use the checked `topIdeal_is_counterboundary` and `bottomIdeal_is_in_scope` witnesses.
- Boundary: boundary witnesses do not prove the arbitrary proper-ideal root.

### m0030-s-foundation

- Claim: every terminal body and composition obeys the selected foundation, computation, and TCB policy.
- Inputs: machine-derived axiom and transitive dependency reports.
- Route: later trust validation must reconcile `propext`, `Classical.choice`, and `Quot.sound`.
- Boundary: complete transitive trust and independent replay remain open.

### m0030-x-mathlib-body

- Claim: pinned `Ideal.iInf_pow_eq_bot_of_isLocalRing` has the exact conclusion.
- Inputs: `M0030-N-FINITE-MODULE` in its visible source body.
- Route: specialize the finite-module theorem to the regular module and convert submodules to ideals.
- Boundary: this is one pinned terminal body, deduplicated from audit and future proof wrappers.

### m0030-n-finite-module

- Claim: `iInf (I^n smul top) = bottom` for every finite module over the local ring.
- Inputs: `M0030-N-JACOBSON` and `M0030-N-LOCAL-CONTAINMENT`.
- Route: use `le_maximalIdeal` and `maximalIdeal_le_jacobson`, checked conditionally by
  `finiteModuleIntersection_of_jacobson`.
- Boundary: both the general Jacobson theorem and local containment remain explicit premises.

### m0030-n-local-containment

- Claim: every proper ideal of a local ring lies below the Jacobson radical of bottom.
- Inputs: `M0030-L-PROPER-MAXIMAL` and `M0030-L-MAXIMAL-JACOBSON`.
- Route: checked composition `localProperIdealJacobson_of_bounds`.
- Boundary: each imported containment has its own proof-body identity and provenance boundary.

### m0030-l-proper-maximal

- Claim: a proper ideal lies below the unique maximal ideal.
- Inputs: local-ring structure and properness.
- Route: pinned `IsLocalRing.le_maximalIdeal`.
- Boundary: it does not establish Jacobson containment by itself.

### m0030-l-maximal-jacobson

- Claim: the unique maximal ideal lies below the Jacobson radical of bottom.
- Inputs: local-ring structure.
- Route: pinned `IsLocalRing.maximalIdeal_le_jacobson`.
- Boundary: it must be composed with proper-to-maximal containment.

### m0030-n-jacobson

- Claim: `I <= jacobson bottom` forces the finite-module intersection to be bottom.
- Inputs: `M0030-N-FIXEDPOINT-IFF` and `M0030-L-JACOBSON-UNIT`.
- Route: take an element in the intersection, obtain a fixed-point coefficient, and cancel `1-r`.
- Boundary: both material child facts remain explicit conditional premises.

### m0030-l-jacobson-unit

- Claim: `r` in the Jacobson radical makes `1-r` a unit.
- Inputs: `M0030-X-JACOBSON-UNIT-SOURCE`.
- Route: checked `jacobsonUnit_of_source` supplies the sign/negation adapter.
- Boundary: the source theorem has a distinct content-addressed body.

### m0030-x-jacobson-unit-source

- Claim: `s-1` in the Jacobson radical makes `s` a unit.
- Inputs: exact commutative-ring and membership context.
- Route: pinned `Ideal.isUnit_of_sub_one_mem_jacobson_bot`.
- Boundary: it is source-shaped; the `1-r` form is a checked child-to-parent transport.

### m0030-n-fixedpoint-iff

- Claim: `x` lies in every `I^n`-multiple iff some `r` in `I` fixes `x`.
- Inputs: `M0030-T-FIXEDPOINT-COMPOSE`.
- Route: pinned `Ideal.mem_iInf_smul_pow_eq_bot_iff`.
- Boundary: this is the distinct pinned declaration/body boundary; it delegates its visible
  internal two-branch composition to `M0030-T-FIXEDPOINT-COMPOSE` rather than duplicating that
  internal proof obligation.

### m0030-t-fixedpoint-compose

- Claim: combine the forward and backward implications into the exact fixed-point iff.
- Inputs: `M0030-B-FIXEDPOINT-FORWARD` and `M0030-B-FIXEDPOINT-BACKWARD`.
- Route: construct the two implications without omitting either branch.
- Boundary: no local composition declaration for the visible internal body is claimed yet.

### m0030-c-infimum-submodule

- Claim: define `N = iInf (I^n smul top)` and expose `N <= I^k smul top` for every `k`.
- Inputs: the complete lattice of submodules.
- Route: `iInf_le` plus the pinned stable/trivial filtration definitions.
- Boundary: defining `N` and its containment interfaces does not prove it is bottom.

### m0030-c-stable-intersection

- Claim: the intersection submodule satisfies the stability relation needed for Nakayama.
- Inputs: `M0030-C-INFIMUM-SUBMODULE` and the stable power filtration.
- Route: intersect the stable filtration with the trivial filtration at `N` and retain its `Stable` witness.
- Boundary: this node does not itself assert `N <= I smul N`.

### m0030-l-stabilization-index

- Claim: choose an index where the stable filtration equality holds.
- Inputs: the `Stable` witness.
- Route: unpack the eventual-stability witness and specialize it at its chosen index.
- Boundary: evaluating the filtration terms as `N` is a separate composition.

### m0030-t-stability-evaluate

- Claim: evaluate both stabilized terms as `N` and derive `N <= I smul N`.
- Inputs: the infimum submodule, stable-intersection witness, and chosen index.
- Route: use the pinned `hN` identities on both sides of the specialized stability equality.
- Boundary: this exact output, rather than generic stability, is the Nakayama premise.

### m0030-l-fg-nakayama

- Claim: finite generation and `N <= I smul N` provide one coefficient in `I` fixing all of `N`.
- Inputs: `M0030-T-STABILITY-EVALUATE` and Noetherian finite generation.
- Route: `Submodule.exists_mem_and_smul_eq_self_of_fg_of_le_smul`.
- Boundary: the Nakayama determinant-trick body is not duplicated as a second root proof.

### m0030-b-fixedpoint-forward

- Claim: every element in the power intersection admits a fixed-point coefficient in `I`.
- Inputs: `M0030-C-INFIMUM-SUBMODULE`, `M0030-C-STABLE-INTERSECTION`, and
  `M0030-L-FG-NAKAYAMA`.
- Route: regard the element as a member of the finitely generated stable intersection and apply the
  uniform Nakayama witness.
- Boundary: source-level decomposition only; accepted node evidence remains empty.

### m0030-b-fixedpoint-backward

- Claim: a coefficient `r in I` fixing `x` places `x` in every power multiple.
- Inputs: `M0030-L-POWER-INDUCTION`.
- Route: convert membership in every power to membership in the infimum.
- Boundary: the induction must cover all natural indices, including zero.

### m0030-l-power-induction

- Claim: `r*x=x` and `r in I` imply `x in I^n smul top` for all `n`.
- Inputs: the fixed-point equation and ideal membership.
- Route: the zero case is top; the successor case rewrites powers and applies
  `Submodule.smul_mem_smul`.
- Boundary: it proves only the backward fixed-point direction.

### m0030-x-source

- Claim: map every material premise and transition to reviewed primary sources.
- Inputs: historical Krull source and modern Stacks leads.
- Route: edition/theorem/page, assumption, definition, proof-node, and errata crosswalk.
- Boundary: this is H evidence only; the current historical mapping remains H1.

### m0030-x-provenance

- Claim: identify the actual terminal body and complete declaration origins.
- Inputs: pinned mathlib revision, blob, imports, aliases, and licenses.
- Route: transitive declaration closure with wrapper/body deduplication.
- Boundary: the current anchor audit is bounded, not release-grade provenance closure.

### m0030-x-trust

- Claim: bind kernel, compiled artifacts, executables, axioms, supply chain, and replay policy.
- Inputs: complete TCB inventory and clean offline validation.
- Route: release validation under the selected foundation profile.
- Boundary: unknown transitive trust fails closed.

### m0030-x-readable

- Claim: give an independently reviewed reader route through every root-relevant node.
- Inputs: exact node fingerprints, source maps, and formal anchors.
- Route: short outline plus substantive node ledgers with at most 100 steps per leaf.
- Boundary: this architecture surface remains R3 and is not an R0 review.

### m0030-x-workflow

- Claim: accept only dependency-legal proof, validation, and release receipts.
- Inputs: typed task DAG, freshness, invalidation, revocation, and independent attestations.
- Route: master reconciliation after all prerequisite receipts pass.
- Boundary: worker self-test proposes `[_]` for this phase only; no accepted state is written.

## Status boundary

The registry denominator is frozen independently of closure status. The conditional Lean harness
checks seven compositions and reports only `propext`, `Classical.choice`, and `Quot.sound`; it uses no
placeholder or undeclared premise. Accepted obligations and receipt IDs remain empty. H0, E1/M0
acceptance, R0, complete trust/provenance, proof integration, validation, release, `AUDIT-Z`, and
theorem completion remain open.
