# Statement gate blocker

`S56-M-0184-STATEMENT` cannot truthfully pass from the repository's current source material. The
canonical metadata says only "moduli spaces of anti-self-dual connections on four-manifolds."
That phrase does not select one theorem among local smoothness/transversality, expected dimension,
orientation, Uhlenbeck compactification, invariant construction, and Donaldson's intersection-form
results. These alternatives have different domains, hypotheses, and conclusions.

The intake correctly leaves the structure group (`SU(2)`, `SO(3)`, or another compact group),
principal bundle, gauge group, irreducible locus, Sobolev completion, generic-metric assumptions,
characteristic-class conventions, expected-dimension formula, and compactification conclusion
unresolved. Lean elaboration cannot resolve mathematical ambiguity. Choosing values for these
fields would broaden or substitute the requested theorem, which rev-5.6 forbids.

## Legacy probe

The historical `Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_131.lean` file was compiled only as
a discovery probe. Its `StatementShape` declaration quantifies over a structure whose substantive
gauge-theory assumptions and desired conclusions are abstract propositions. Successful elaboration
therefore establishes only that the historical boundary contract is well typed. It does not
identify or elaborate the exact `THM-M-0184` target, and its thirteen imports are not a validated
minimal import set.

## Retry condition

Supply and accept an immutable primary-source pinpoint identifying the intended theorem and page,
with its complete ordered assumptions and conclusion. The statement phase can then encode that
claim, minimize pinned imports, serialize the elaborated expression and environment, add checked
transports, and mutation-test hypothesis removal, domain changes, binder scope, and boundary cases.

Until then the exact-source-identification gate fails, machine debt remains `M3`, and every
downstream phase remains open. No worker self-test manifest is emitted because the assigned phase
is not self-tested successfully.
