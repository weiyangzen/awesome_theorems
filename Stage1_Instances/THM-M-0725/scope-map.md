# Scope map

## Included topic boundary

- Complexity classes defined from exponential time bounds on a source-specified machine model.
- A source-specified hierarchy relation, such as strict containment between time classes or levels
  obtained using oracle access or alternation.
- Concrete encodings of languages/decision problems, input size, runtime, and acceptance.
- Every constructibility, growth, reduction, uniformity, and closure hypothesis in the selected
  source proposition.

## Ambiguities to resolve at statement freeze

The repository record does not decide among these materially different readings:

1. **Deterministic hierarchy:** an instance of a deterministic time-hierarchy theorem, for example
   a strict inclusion between two classes whose time bounds are exponential but sufficiently
   separated.
2. **Nondeterministic hierarchy:** a corresponding nondeterministic separation, with different
   theorem hypotheses and proof infrastructure.
3. **Exponential hierarchy:** levels defined by bounded alternation or by oracle access to preceding
   levels, together with an equality, inclusion, union, or collapse statement.
4. **Class definition or characterization:** a fact about `EXPTIME`, `NEXPTIME`, completeness, or a
   union of bounded-time classes rather than a hierarchy theorem.

The statement phase must inspect an immutable source and freeze exactly one proposition. It must
fix ordered binders, the machine and cost models, encoding and input-length conventions, the exact
growth family (including floors/ceilings), time constructibility, reduction notion, oracle and
alternation semantics, and all small-input boundary cases.

## Explicit exclusions

- The polynomial hierarchy, arithmetic hierarchy, or space hierarchy as substitutes.
- `P != EXPTIME`, `EXPTIME != NEXPTIME`, or another familiar separation absent a source crosswalk.
- A mere definition of `EXPTIME` or of hierarchy levels when the selected source claim is strictness.
- An arbitrary-time machine record whose desired hierarchy property is assumed as structure data.
- A convenient theorem about `Nat.pow`, asymptotics, or computability in place of a complexity result.
- The repository label `已验证` as evidence of a human or machine proof.

No canonical Lean target is frozen at intake because the source record does not identify one.
