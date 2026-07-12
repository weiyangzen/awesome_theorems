# THM-M-0382 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the repository label "Keel-Tao
endpoint Strichartz estimate". The repository metadata gives Keel and Tao, 1998, and only the gloss
"endpoint Strichartz estimate". It does not state the operator hypotheses, admissible exponent
region, excluded endpoint, time domain, function spaces, constants, or which one of the homogeneous,
dual, and retarded estimates is the target.

The title and date strongly locate the subject near Theorem 1.2 of Keel and Tao's 1998 paper, but
that paper contains an abstract estimate package and applications. Selecting one estimate, or the
whole package, without a pinpoint source transcription would silently change the target. This
intake therefore freezes the ambiguity and the non-substitution boundary, not a canonical theorem.

The root remains `[H1, M4, R4]`. `IntakeProbe.lean` verifies only that the pinned Lean environment
exposes `L^p` seminorm, measurability, continuous-linear-map, and interval-measure ingredients that
a future encoding may use. It is neither the canonical statement nor proof evidence. Exact commands
and results are recorded in `validation.md`.
