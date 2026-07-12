# Scope map

## Topic boundary

The source record points only to an operator estimate in an Lp setting. A valid later statement
must identify all of the following from one immutable source:

- the concrete operator or operator family and how it is initially defined;
- source and target measure spaces and scalar/value spaces;
- the exact exponent range, including endpoint exclusions or weak-type endpoints;
- analytic hypotheses on kernels, measures, geometry, regularity, or cancellation;
- whether the conclusion is an eLpNorm inequality, strong/weak type estimate, or a bounded extension
  between quotient Lp spaces, including the dependence of its constant.

## Material ambiguities

"Lp boundedness" can describe mutually non-equivalent theorems. Examples include boundedness of
Calderon-Zygmund singular integrals for `1 < p < infinity`, weak `(1,1)` and strong `(p,p)` bounds
for a maximal operator, Plancherel's `L2` result for a Fourier transform, interpolation consequences,
or the tautological boundedness of an object already supplied as a continuous linear map. These
choices have different domains, hypotheses, conclusions, endpoint behavior, and proof trees.

The statement phase must also settle sigma-finiteness or doubling assumptions, real versus complex
values, almost-everywhere quotienting, measurability, dense-domain extension, and whether the
constant is existential, explicit, or uniform over an operator class.

## Explicit exclusions

- Choosing any named operator merely because it is standard in harmonic analysis.
- Treating all operators, or "various operators", as one quantified family without a source-defined
  class and uniform hypotheses.
- Assuming `T : Lp ->L Lp` and presenting its built-in continuity as the intended theorem.
- Replacing strong type with weak type, an endpoint estimate, a special exponent, or a finite-space
  analogue.
- Using the neighboring maximal-function or Coifman-McIntosh-Meyer inventory entries as the target.
- Treating the repository label `已验证` as evidence of a source proof or kernel closure.

No canonical claim or Lean target is frozen at intake because the record is not a proposition.
