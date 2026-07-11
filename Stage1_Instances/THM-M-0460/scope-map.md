# Scope map

## Provisional included claim

- An arithmetic variety over a number field and an ample line bundle equipped with an admissible
  or semipositive adelic metric, as required by the selected primary theorem.
- A generic sequence of algebraic points whose associated normalized heights tend to the relevant
  minimum.
- At each selected place, the Galois-orbit empirical probability measures converge weakly to the
  canonical probability measure determined by the metrized line bundle.
- Archimedean and non-archimedean cases only to the extent actually asserted by the selected source.

## Decisions required at statement freeze

The statement phase must freeze the primary theorem and its edition; base field; dimension and
geometric hypotheses on the variety; line-bundle positivity and metric regularity; normalized
height and essential-minimum conventions; the exact meaning of generic; the local analytic space;
the canonical measure and its normalization; Galois-orbit multiplicities; place quantification;
and the topology/test-function formulation of weak convergence. It must also settle dimension zero,
empty or eventually repeated sequences, non-generic sequences, and whether equality in a height
inequality is a premise or a consequence.

## Explicit exclusions

- Weyl equidistribution, Chebotarev density, or an abstract probability convergence theorem.
- Equidistribution of torsion points alone as a substitute for the small-point theorem.
- The Bogomolov conjecture or Zhang's small-height inequality without the measure-convergence
  conclusion.
- A structure that assumes the limiting measure or convergence as a field.
- The repository label `已验证` as human-proof or kernel evidence.

No Lean target is frozen at intake. A later target must expose the actual arithmetic variety,
height, analytification, measure, orbit, and weak-convergence interfaces rather than encode the
desired result as an assumption.
