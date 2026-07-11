# THM-M-1072 rev-5.6 intake

This directory is the `planned` intake for the Levy-Khinchin representation of the characteristic
function of a Levy process. The frozen family says that a real-valued Levy process has
characteristic functions with exponential time dependence and a characteristic exponent described
by drift, Gaussian, and jump-measure data.

The repository gloss "characteristic function of a Levy process" and its untrusted "verified"
label do not select a formula or supply proof credit. In particular, the Fourier sign, Gaussian
coefficient, truncation function, drift parameter, Levy-measure condition, and the inclusion of a
converse or uniqueness assertion remain open until one exact source theorem is selected. The
provisional root vector is `[H2, M4, R4]`; no exact Lean target, audit completion, or theorem
completion is claimed.

The scope map separates this process theorem from the adjacent targets about infinitely divisible
laws. The source-statement crosswalk records the evidence boundary, and the task DAG keeps every
dependent phase open. Intake validation and its exact limits are recorded in `validation.md`.
