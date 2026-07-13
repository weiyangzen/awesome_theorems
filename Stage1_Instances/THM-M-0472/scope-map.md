# Scope map

## Received claim

The repository names `THM-M-0472` as `欧几里得算法` and gives only the gloss
`求最大公约数的算法`: an algorithm for finding the greatest common divisor. This identifies a
classical algorithm family, not an exact theorem. In particular, it does not say whether the target
is a recursive equation, termination, partial correctness, total correctness, or an executable
program refinement.

## Candidate mathematical boundary

The closest elementary family takes two natural-number inputs and repeatedly replaces a pair by a
remainder pair until one component is zero. The terminal value should be the greatest common
divisor. A total-correctness contract has three logically separate parts:

- remainder descent terminates under a stated measure;
- the returned value divides both original inputs; and
- every common divisor of the inputs divides the returned value.

Pinned Lean's orientation is `Nat.gcd_rec m n : gcd m n = gcd (n % m) m`: the recursion tests the
first argument and replaces `(m,n)` by `(n % m,m)`. The familiar orientation
`gcd(a,b)=gcd(b,a % b)` needs an argument swap or commutativity. This detail must not be erased in
the statement crosswalk.

## Decisions required at statement freeze

1. Preserve and independently review an immutable source passage and decide whether Euclid VII.1,
   VII.2, or a modern combined algorithm specification is authoritative.
2. Freeze natural, nonnegative-integer, signed-integer, or positive-number input domains and the
   output type.
3. Freeze subtraction versus division/remainder presentation, quotient and remainder conventions,
   pair orientation, stopping rule, and termination measure.
4. Decide whether the root is the recurrence identity, an algorithm returning a value with a full
   gcd postcondition, or a refinement between an explicit trace/program and `Nat.gcd`.
5. Resolve `(0,0)`, exactly one zero input, equal inputs, relatively-prime inputs, ordered versus
   unordered inputs, and negative inputs if integers are selected.
6. Supply checked transports for every credited alternate formulation and run all four rev-5.6
   statement mutation classes before inspecting proof closure.

## Related forms, not substitutes

- `Nat.gcd_rec` is the central Euclidean recurrence, but equality preservation alone does not state
  that an independently described algorithm terminates or that its result satisfies the full gcd
  specification.
- `Nat.gcd.induction` exposes well-founded reasoning along remainder descent, but is an induction
  principle rather than the received algorithm theorem.
- `Nat.gcd_dvd_left`, `Nat.gcd_dvd_right`, and `Nat.dvd_gcd` supply the two directions of gcd
  correctness. `Nat.gcd_eq_iff` packages them as an exact universal characterization. These are
  candidate correctness components, not a frozen algorithm root by themselves.
- `Nat.xgcd` and `Nat.gcd_eq_gcd_ab` implement and verify the extended Euclidean algorithm. Bezout
  coefficients belong directly to `THM-M-0473`; they cannot silently replace ordinary gcd
  algorithm correctness here.
- Abstract Euclidean-domain algorithms generalize the natural-number family and introduce
  normalization and unit choices. They are candidates only after a source-faithful transport.

## Explicit exclusions

- A fixed numerical calculation such as `gcd(48,18)=6`.
- Only the statement that a greatest common divisor exists, without algorithm behavior.
- Only the recurrence identity, if the selected source root requires total correctness.
- Only termination, or only the common-divisor half of correctness.
- Bezout's identity, Euclid's lemma, the fundamental theorem of arithmetic, or another neighboring
  theorem used as the root.
- An algorithm over arbitrary Euclidean domains substituted for an elementary integer target.
- A structure, hypothesis, custom axiom, oracle, or unchecked certificate that already contains
  the desired output or correctness facts.
- The catalog's `已验证` label, a theorem name, API output, or successful probe used as proof
  evidence.

No canonical Lean expression or expression fingerprint is frozen by intake. The direct pinned APIs
are candidate anchors for the dependent statement and anchor-audit phases.
