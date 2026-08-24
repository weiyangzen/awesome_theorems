# Pollington--de Mathan theorem: distilled proof outline

## H-LAC

Hypotheses: `m : ℕ → ℕ`, every `m n` is positive, and `m` is lacunary.
Inference: unpack lacunarity to fix a ratio `q > 1` that uniformly separates
successive frequencies. Output: the separation estimate needed to choose
independent scales in the interval game. Formal anchor:
`Bugeaud06.pollington_de_mathan` (`hm`, `hlac`). Downstream use: H-WIN.
Exceptional cases: positivity excludes the zero-frequency degeneration; the
first finitely many terms do not affect the strategy. Trust boundary: the
frozen Lean statement supplies these hypotheses.

## H-WIN

Hypotheses: the uniform lacunarity estimate from H-LAC. Inference: play the
Schmidt interval game in blocks whose frequencies are separated by the fixed
ratio. At each block, remove the inverse images of a fixed open arc around
zero; lacunarity bounds how many dangerous components can meet the current
interval, so a legal child interval remains. Output: a Schmidt-winning set of
parameters `ξ` whose residues `ξ * m n` uniformly avoid that arc. Formal
anchor: the proof body represented by `Bugeaud06.pollington_de_mathan`.
Downstream uses: H-NON and H-DIM. Exceptional cases: endpoints of the avoided
arc are included in the dangerous set, so boundary hits cannot invalidate
uniform avoidance. Trust boundary: the Pollington--de Mathan avoidance lemma
and the standard Schmidt-game strategy theorem.

## H-NON

Hypotheses: a parameter `ξ` in the winning set from H-WIN. Inference: its
entire orbit in `AddCircle 1` misses a nonempty open arc; a subset missing such
an arc is not dense. Output: `ξ` belongs to the nondense-orbit set in the
theorem conclusion. Formal anchor: the `Dense (Set.range ...)` subexpression
of `Bugeaud06.pollington_de_mathan`. Downstream use: H-DIM. Exceptional cases:
the range is indexed from zero and uniform avoidance covers every index.
Trust boundary: the definition of topological density.

## H-DIM

Hypotheses: H-WIN gives a winning subset; H-NON embeds it in the nondense-orbit
set. Inference: winning subsets of the real line have Hausdorff dimension one,
and Hausdorff dimension is monotone under inclusion. The containing subset of
`ℝ` has dimension at most one, so the lower and upper bounds agree. Output:
`dimH {ξ : ℝ | ¬ Dense (Set.range fun n => ↑(ξ * m n))} = 1`. Formal
anchor: the complete type of `Bugeaud06.pollington_de_mathan`. Downstream use:
the claim root and Stage6 alias `S6-CLM-00001772`. Exceptional cases: no
measurability assumption is needed for Hausdorff dimension monotonicity.
Trust boundary: the full-dimension theorem for Schmidt-winning sets and the
ambient dimension of `ℝ`.
