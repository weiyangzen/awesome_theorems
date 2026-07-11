# THM-M-0396 Statement Freeze

## Canonical target

`Statement.lean` freezes a real, multiplicative Matveev formulation of the
Baker lower-bound theorem. For `n >= 1`, a number field `K`, a real embedding,
positive `alpha i : K`, integer coefficients `b_i`, height parameters `A_i`,
and coefficient majorant `B`, it defines

`Lambda = product_i embedding(alpha_i)^b_i - 1`.

When every `A_i` majorizes both the normalized number-field logarithmic height
`Height.logHeight₁ (alpha i)` and `|log (embedding (alpha i))|`, every `A_i` is
at least `0.16`, `B >= 1` majorizes every `|b_i|`, and `Lambda != 0`, the target
is

`-C < log |Lambda|`,

where `C = 1.4 * 30^(n+3) * n^(9/2) * D^2 * (1 + log D) *
(1 + log(nB)) * product_i A_i` and `D = [K : Q]`.

The chosen real embedding and positivity hypotheses fix the real logarithm
branch. The nonvanishing hypothesis excludes the zero form. Empty products are
excluded by `n >= 1`. The statement makes no effectiveness claim beyond its
displayed explicit inequality and does not include Baker-method applications,
which belong to `THM-M-0397`.

`statement_iff_expanded` checks the complete binder and hypothesis expansion.
`linearFormValue_eq_zero_of_coeff_zero` checks the all-zero-coefficient boundary.
Neither declaration proves the lower-bound theorem.

## Mutation boundary

Removing positivity changes the logarithm domain. Removing the height or
coefficient majorants makes the displayed constant unrelated to the inputs.
Removing `Lambda != 0` asks for `log 0`. Allowing `n = 0` changes the theorem to
the empty product. Changing the number-field domain, binder scope, exponent
domain, or any explicit constant factor is not an equivalent target and
receives no statement credit.

Pinpoint source theorem/page and errata review remains open for the anchor-audit
node. This phase establishes elaboration of the selected exact proposition only:
it does not establish H0, a proof body, audit completion, or theorem completion.
