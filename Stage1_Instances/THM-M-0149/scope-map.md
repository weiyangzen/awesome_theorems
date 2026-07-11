# Scope map

## Provisional included claim

- A fixed natural dimension `d` and a fixed positive real discrepancy threshold `epsilon`.
- Normal projective varieties, or pairs `(X, B)` if the selected source theorem is the pair version.
- The epsilon-log-canonical singularity condition and the source's positivity condition on the
  anti-log-canonical divisor, such as Fano or nef and big.
- Boundedness in the algebro-geometric sense: membership in fibers of a finite-type family, with
  the exact base field and family/equivalence convention taken from the source.

## Decisions required at statement freeze

The statement phase must inspect and select an exact primary theorem, then freeze: the base field
and characteristic; whether the objects are varieties or log pairs; normality and projectivity;
dimension convention; the range of `epsilon`; coefficient restrictions on `B`; epsilon-lc versus
klt hypotheses; Fano versus weak Fano/log Fano positivity; Q-Cartier assumptions; and the precise
definition of bounded family. It must also settle dimension zero, empty families, reducibility,
geometric versus arithmetic base change, and whether the conclusion bounds varieties alone or
pairs including their boundaries.

## Explicit exclusions

- Boundedness with dimension or `epsilon` allowed to vary.
- Birational boundedness, bounded complements, effective birationality, or a volume bound alone as
  a substitute for boundedness of the asserted objects.
- Smooth Fano boundedness as a substitute for the singular epsilon-lc theorem.
- The Borisov-Alexeev-Borisov conjecture name or the repository label `已验证` as proof evidence.
- An abstract structure that takes the desired finite-type family or boundedness proposition as a
  field.

No Lean target is frozen at intake. A later expression must expose concrete varieties/pairs,
singularity discrepancies, divisor positivity, and the bounded-family conclusion, or record exact
missing APIs rather than weakening the theorem.
