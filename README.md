# Transmon Energy Spectrum Study

This project numerically investigates the energy spectrum, transition
frequencies, charge dispersion, and anharmonicity of a transmon qubit.

## Physical model

The transmon qubit is described by the Hamiltonian

$$
\hat{H}=4E_C(\hat{n}-n_g)^2-E_J\cos(\hat{\phi}),
$$

where:

- \(E_C\) is the charging energy.
- \(E_J\) is the Josephson energy.
- \(\hat{n}\) is the Cooper-pair number operator.
- \(n_g\) is the offset charge.
- \(\hat{\phi}\) is the superconducting phase operator.

The conjugate operators satisfy

$$
[\hat{\phi},\hat{n}]=i.
$$

In the charge basis \(\{|n\rangle\}\), the Hamiltonian matrix elements are

$$
\langle n'|\hat{H}|n\rangle
=
4E_C(n-n_g)^2\delta_{n'n}
-\frac{E_J}{2}
\left(
\delta_{n',n+1}+\delta_{n',n-1}
\right).
$$

The diagonal term represents the charging energy, while the off-diagonal
terms describe Josephson tunneling between neighboring charge states.

In the large-\(E_J/E_C\) transmon regime, the lowest transition frequency is approximately

$$
f_{01}\approx\frac{\sqrt{8E_JE_C}-E_C}{h},
$$

and the anharmonicity is approximately

$$
\alpha=f_{12}-f_{01}\approx-\frac{E_C}{h}.
$$

In the numerical program, `scqubits` uses \(E_C/h\) and \(E_J/h\) in GHz.
Therefore, the corresponding frequency-unit expressions become

$$
f_{01}\approx\sqrt{8E_JE_C}-E_C,
\qquad
\alpha\approx-E_C,
$$

when \(E_C\) and \(E_J\) are entered directly in GHz.

## Parameters

| Parameter | Symbol | Value |
|---|---|---:|
| Charging energy | EC/h | 0.3 GHz |
| Josephson energy | EJ/h | 15.0 GHz |
| Energy ratio | EJ/EC | 50 |
| Offset-charge range | ng | −1 to 1 |
| Charge-basis cutoff | ncut | 15 |
| Calculated energy levels | — | 5 |

## Results

### 1. Energy spectrum versus offset charge

![Energy spectrum](figures/01_energy_spectrum_vs_ng.png)

The low-energy spectrum becomes nearly insensitive to offset charge in
the transmon regime.

### 2. Transition frequencies

![Transition frequencies](figures/02_transition_frequencies_vs_ng.png)

The different transition frequencies demonstrate the anharmonic energy
structure of the transmon.

### 3. Charge dispersion

![Charge dispersion](figures/03_charge_dispersion_vs_ej_ec.png)

The charge dispersion of the \(0\rightarrow1\) transition is defined as

$$
\epsilon_{01}
=
\max_{n_g}\left[f_{01}(n_g)\right]
-
\min_{n_g}\left[f_{01}(n_g)\right].
$$

Increasing \(E_J/E_C\) exponentially suppresses \(\epsilon_{01}\), making
the transmon less sensitive to offset-charge fluctuations.

### 4. Anharmonicity

![Anharmonicity](figures/04_anharmonicity_vs_ej_ec.png)

The anharmonicity is defined as

$$
\alpha=f_{12}-f_{01}.
$$

In the transmon regime,

$$
\alpha\approx-\frac{E_C}{h}.
$$

The negative anharmonicity means that the \(1\rightarrow2\) transition
frequency is lower than the \(0\rightarrow1\) transition frequency.

### 6. Relative anharmonicity

![Relative anharmonicity](figures/06_relative_anharmonicity_vs_ej_ec.png)

The relative anharmonicity is

$$
\alpha_{\mathrm{rel}}
=
\frac{|\alpha|}{f_{01}}.
$$

Although increasing \(E_J/E_C\) suppresses charge dispersion, it also
reduces the relative anharmonicity.

## Main Conclusion

Increasing $E_J/E_C$ exponentially suppresses charge dispersion and reduces the transmon's sensitivity to charge noise. However, increasing $E_J/E_C$ also reduces the relative anharmonicity $|\alpha|/f_{01}$, making leakage into higher energy levels more difficult to control during fast gate operations.

## Installation

Install the required Python packages:

```bash
pip install -r requirements.txt
```

## Usage

Run the simulation with:

```bash
python "1. Transmon Energy Spectrum.py"
```
