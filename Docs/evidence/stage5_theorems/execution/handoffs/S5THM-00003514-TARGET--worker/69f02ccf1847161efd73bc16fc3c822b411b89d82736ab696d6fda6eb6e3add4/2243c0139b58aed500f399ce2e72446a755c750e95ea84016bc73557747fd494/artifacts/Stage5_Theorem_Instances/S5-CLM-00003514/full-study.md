# Full study: finite free convolution Fisher information

## FS-3514-PU01 — frozen identity

Freeze member `ce043ee0710f9124ede295e3fdb19b0dfff6fe5d175dd95062f6ecc1cde033ec`
and source bytes
`99fdffce0be3963d1a2b2f136e123a4aa446ac3d8815c646eae8c18c690c1fe0`.
The hypotheses are the immutable workset identity and source span.  The
inference is exact digest comparison.  The output is one source occurrence and
Stage6 alias.  Its formal anchor is `statement`; downstream nodes are PU02 and
PU06.  Any drift is exceptional and invalidates the package.  Trust stops at
statement authority: the provider's `sorryAx` supplies no proof.

## FS-3514-PU02 — semantic normalization

Normalize `answer(True)` to the proposition `True` and delta-expand `FourProp`
without changing a hypothesis or conclusion.  The hypotheses are the frozen
declaration type and the exact bodies of `finiteAdditiveConvolution`, `Φ`, and
`FourProp`.  The inference is elaboration plus constant census; the output is
the exact root and two transport directions.  Its formal anchor is
`source_to_target`, and PU03/PU06 consume it.  Shadowing, aliases, notation,
coercion or import substitution are exceptional rejection cases.  Worker
digests cross the trust boundary only after independent Master recomputation.

## FS-3514-PU03 — score identification

For distinct real roots, identify the logarithmic-derivative score `sᵢ` as the
sum of reciprocal root gaps; its squared norm is `Φ`.  The hypotheses are
monicity, real-rootedness, exact degree, and the simple-root branch.  The
inference is the logarithmic derivative evaluated at each root.  The output is
the Fisher-information interpretation used by PU04, with formal anchor
`proof_forward`.  Repeated roots are the exceptional top-valued branch handled
in PU05.  The prose is explanatory; kernel closure is the formal trust boundary.

## FS-3514-PU04 — projection inequality

Apply the finite-free-convolution score projection and Jensen contraction to
obtain `Φ(r) ≤ a²Φ(p)+(1-a)²Φ(q)`.  The hypotheses are PU03 and `0 ≤ a ≤ 1`.
The inference is conditional-score compatibility followed by norm contraction.
The output feeds PU05 and is anchored at `proof`.  Degenerate information
values are exceptional and are split before division.  No provider theorem
body crosses this node's trust boundary.

## FS-3514-PU05 — optimization and boundary cases

Choose the minimizing weight, treat zero/top and repeated-root branches, and
invert the nonnegative inequality to get reciprocal superadditivity.  The
hypothesis is PU04's quadratic upper bound.  The inference is scalar
optimization and monotonicity of inversion on extended nonnegative reals.  The
output is exactly the `FourProp` conclusion and feeds PU06; its formal anchor is
`proof_reverse`.  If an information value is `⊤`, its reciprocal is zero; if a
denominator vanishes, the order proof avoids cancellation.  Master mutation
replay is the trust boundary for all exceptional branches.

## FS-3514-PU06 — root reconstruction

Reassemble the six hypotheses, universal quantifiers, and outer `True`
equivalence; preserve source-to-target and target-to-source transport.  The
hypotheses are PU01, PU02, and PU05.  The inference is implication and
quantifier introduction followed by the two equivalence directions.  The
output is the exact-root provisional release candidate, formally anchored at
`audit_root` and consumed by `release-decision`.  Master rejection is the sole
exceptional terminal branch and leaves canonical completion false.  Only the
canonical Master may cross the acceptance trust boundary.
