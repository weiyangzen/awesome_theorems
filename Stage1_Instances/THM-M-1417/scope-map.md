# Scope map

## Preserved source scope

The repository fixes only a Chinese label meaning "SRB measure," the attribution
"Sinai/Ruelle/Bowen," the year 1976, and a gloss meaning "physical measure(s) of dissipative
systems." It supplies no primary source, definition, premise, or conclusion. Intake therefore
preserves an SRB measure subject-area boundary only.

## Proposition-changing decisions

An approved source correction must freeze all of the following:

- discrete time (a self-map or diffeomorphism) versus continuous time (a flow), including
  invertibility and the time domain;
- the phase space, universes, topology, measurable structure, compactness, boundary, dimension,
  smooth-manifold model, metric, and regularity class;
- a whole phase space, compact invariant set, attractor, or basin, and the exact invariant,
  Anosov, Axiom A, uniform, nonuniform, or partial-hyperbolicity assumptions;
- transitivity or irreducibility assumptions and whether more than one SRB or physical measure is
  allowed;
- the ambient Riemannian/Lebesgue reference volume and the support and normalization of the
  requested invariant Borel measure;
- the definition: absolute continuity of conditional measures on unstable leaves, a positive- or
  full-volume physical basin described by empirical measures or observables, an entropy formula,
  an equilibrium-state condition, a zero-noise limit, or checked equivalences among them;
- existence, uniqueness, characterization, ergodicity, entropy, statistical stability, or another
  exact truth-valued conclusion; and
- all ordered binders, hypotheses, null-set conventions, exceptional cases, and boundary behavior.

These choices yield inequivalent propositions outside carefully stated hypotheses. They are a
resolution checklist, not a canonical claim.

## Candidate family not credited

A secondary survey summarizes a familiar candidate for a `C^2` diffeomorphism with an irreducible
Axiom A attractor: existence and uniqueness of an invariant Borel probability measure, with
several equivalent unstable-conditional, entropy, physical-basin, and zero-noise
characterizations. The catalog does not cite that survey, select its assumptions, or say that this
combined theorem is the intended root. The separate 1976 Ruelle bibliographic candidate does not,
from its title alone, supply the complete combined statement either. No part of this family is
selected or credited at intake.

## Explicit exclusions

The target must not be silently replaced with the surrounding catalog items for hyperbolic
dynamical systems (`THM-M-1411`), Anosov diffeomorphisms (`THM-M-1412`), Axiom A systems
(`THM-M-1413`), spectral decomposition (`THM-M-1414`), Markov partitions (`THM-M-1415`), or
Bowen-Margulis measures (`THM-M-1416`). Lyapunov exponents (`THM-M-1418`), Oseledets' theorem
(`THM-M-1419`), Pesin theory (`THM-M-1420`), and Pesin's entropy formula (`THM-M-1421`) are also
separate roots, even when a chosen SRB theorem would depend on them.

Generic measure-preserving, invariant-measure, ergodicity, Birkhoff-average, or recurrence facts
are only possible ingredients. A finite example, an arbitrary probability measure relabeled as an
SRB measure, or a record assuming the desired measure/basin/conditional properties is not the
catalog target. A paper title, survey statement, or the catalog's untrusted status label cannot
close the source or proof gate.

## Formal boundary

No canonical Lean expression is frozen. Pinned mathlib provides Birkhoff averages,
measure-preserving maps, ergodicity, measure and almost-everywhere infrastructure, and smooth
manifold derivatives. A bounded exact-topic search found no SRB, Sinai-Ruelle-Bowen, or physical-
measure declaration. `IntakeProbe.lean` checks adjacent substrate only. These discovery facts are
not an anchor audit, exact statement, definition of an SRB measure, or machine-proof evidence.
