# Scope map

## Included claim family

- A centered, real-valued Gaussian process `(X_t)_(t in T)`.
- The canonical increment pseudometric `d(s,t) = sqrt(E[(X_s - X_t)^2])` on its index set.
- A universal-constant lower bound for `E[sup_(t in T) X_t]` in terms of
  `epsilon * sqrt(log N(T,d,epsilon))`, either at every positive scale or optimized over scales.
- The measurability, separability, boundedness, and finiteness assumptions actually required by the
  selected primary statement.

This is a claim-family freeze, not an exact statement freeze. The source inventory says only
"lower bound for Gaussian processes", so details not fixed there remain visibly open.

## Statement-phase decisions

The selected source must determine whether `N` is a covering number, packing number, or maximum
separated-set cardinality; open versus closed balls; the scale factor hidden by conversion between
those conventions; and the value and quantification of the universal constant. It must also settle
whether the conclusion uses `E sup X_t`, `E sup |X_t|`, or expected increment diameter; whether `T`
is finite before a limiting argument; and the exact separability/measurability and integrability
conditions for an infinite index set.

The formal statement must specify treatment of the empty and singleton index sets, zero increment
variance, infinite entropy, extended-real versus real expectations, pseudometric quotienting, and
scales for which the entropy is `0`, `1`, finite, or infinite. Binder order, universes, and all
side conditions must follow the inspected source rather than a convenient library API.

## Explicit exclusions

- Dudley's metric-entropy upper bound, Borell-TIS concentration, Slepian comparison, or a generic
  Gaussian tail estimate as a substitute for the lower bound.
- A finite-dimensional standard-normal maximum lemma presented as the full process theorem without
  the separated-set comparison and limiting/measurability bridge required by the selected scope.
- Assuming the desired entropy lower bound as a hypothesis or a field of an abstract structure.
- Replacing the canonical increment pseudometric by an unrelated metric without a checked
  domination or transport theorem.
- Treating the metadata label `已验证` or a bibliographic citation as Lean proof evidence.
