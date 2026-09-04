# Transmon Energy Spectrum Study

This project numerically investigates the energy spectrum, transition frequencies, charge dispersion, and anharmonicity of a transmon qubit using Python and `scqubits`.

The main objective is to study how the ratio $E_J/E_C$ affects the transmon's sensitivity to offset-charge noise and its anharmonicity.

---

## Physical Model

The transmon Hamiltonian is

$$\hat{H}=4E_C(\hat{n}-n_g)^2-E_J\cos(\hat{\phi}).$$

The parameters and operators are:

- $E_C$: charging energy
- $E_J$: Josephson energy
- $n_g$: offset charge
- $\hat{n}$: Cooper-pair number operator
- $\hat{\phi}$: superconducting phase operator

The phase and Cooper-pair number operators are conjugate variables satisfying

$$
[\hat{\phi},\hat{n}]=i.
$$

---

## Hamiltonian in the Charge Basis

The transmon Hamiltonian is represented using charge states

$$
\{\lvert n\rangle\}.
$$

In this basis, the matrix elements are

$$
\langle n' \vert \hat{H} \vert n\rangle
=
4E_C(n-n_g)^2\delta_{n'n}
-
\frac{E_J}{2}
\left(
\delta_{n',n+1}
+
\delta_{n',n-1}
\right).
$$

The first term is diagonal and represents the charging energy:

$$
\langle n' \vert \hat{H}_{C} \vert n\rangle
=
4E_C(n-n_g)^2\delta_{n'n}.
$$

The Josephson term couples neighboring charge states:

$$
\langle n' \vert \hat{H}_{J} \vert n\rangle
=
-\frac{E_J}{2}
\left(
\delta_{n',n+1}
+
\delta_{n',n-1}
\right).
$$

Therefore, the Josephson coupling connects

$$
\lvert n\rangle
\longleftrightarrow
\lvert n+1\rangle.
$$

---

## Transition Frequencies

After diagonalizing the Hamiltonian, the eigenenergies are denoted by

$$
E_0,\ E_1,\ E_2,\ldots
$$

The first two transition frequencies are

$$
f_{01}
=
\frac{E_1-E_0}{h},
$$

and

$$
f_{12}
=
\frac{E_2-E_1}{h}.
$$

The anharmonicity is defined as

$$
\alpha
=
f_{12}-f_{01}.
$$

For a transmon, the anharmonicity is negative because the energy-level spacing decreases for higher excited states.

---

## Large-Ratio Approximation

In the transmon regime, where

$$
\frac{E_J}{E_C}\gg 1,
$$

the lowest transition frequency is approximately

$$
f_{01}
\approx
\frac{\sqrt{8E_JE_C}-E_C}{h}.
$$

The anharmonicity is approximately

$$
\alpha
\approx
-\frac{E_C}{h}.
$$

In `scqubits`, $E_C$ and $E_J$ are entered directly in frequency units such as GHz. Under this convention, the corresponding expressions become

$$
f_{01}
\approx
\sqrt{8E_JE_C}-E_C,
$$

and

$$
\alpha
\approx
-E_C.
$$

---

## Parameters

| Parameter | Code variable | Value |
|---|---|---:|
| Charging energy | `EC` | 0.3 GHz |
| Josephson energy | `EJ` | 15.0 GHz |
| Default energy ratio | `EJ / EC` | 50 |
| Offset-charge range | `ng_values` | -1 to 1 |
| Charge-basis cutoff | `N_cut` | 15 |
| Number of energy levels | `num_levels` | 5 |

The ratio $E_J/E_C$ is also scanned over a wider range to study the transition from the charge-sensitive regime to the transmon regime.

---

## Numerical Procedure

The calculation follows these steps:

1. Construct a transmon object using `scqubits`.
2. Sweep the offset charge $n_g$.
3. Diagonalize the Hamiltonian at every parameter value.
4. Store the eigenenergies in an energy table.
5. Calculate $f_{01}$, $f_{12}$, and $\alpha$.
6. Calculate the charge dispersion.
7. Repeat the calculation for different values of $E_J/E_C$.
8. Compare the numerical results with analytical approximations.

---

## Results

### 1. Energy Spectrum versus Offset Charge

![Energy spectrum versus offset charge](figures/01_energy_spectrum_vs_ng.png)

This figure shows the lowest transmon energy levels as functions of the offset charge $n_g$.

In the transmon regime, the energy bands become nearly flat. This means that the energy levels are less sensitive to fluctuations in the offset charge.

---

### 2. Transition Frequencies versus Offset Charge

![Transition frequencies versus offset charge](figures/02_transition_frequencies_vs_ng.png)

The transition frequencies are calculated from the energy differences:

$$
f_{01}(n_g)
=
E_1(n_g)-E_0(n_g),
$$

and

$$
f_{12}(n_g)
=
E_2(n_g)-E_1(n_g).
$$

Because the program uses GHz as its energy unit, these energy differences are reported directly in GHz.

The difference between $f_{01}$ and $f_{12}$ demonstrates that the transmon has an anharmonic energy spectrum.

---

### 3. Charge Dispersion versus Energy Ratio

![Charge dispersion versus EJ over EC](figures/03_charge_dispersion_vs_ej_ec.png)

The charge dispersion of the $0\rightarrow1$ transition is defined as

$$
\epsilon_{01}
=
\max_{n_g}
\left[
f_{01}(n_g)
\right]
-
\min_{n_g}
\left[
f_{01}(n_g)
\right].
$$

In NumPy, this quantity is calculated using the peak-to-peak function:

```python
charge_dispersion_01 = np.ptp(f01_vs_ng)
```

As $E_J/E_C$ increases, the charge dispersion decreases exponentially.

Therefore, operating in the large-$E_J/E_C$ regime strongly suppresses the transmon's sensitivity to charge noise.

---

### 4. Anharmonicity versus Energy Ratio

![Anharmonicity versus EJ over EC](figures/04_anharmonicity_vs_ej_ec.png)

The anharmonicity is

$$
\alpha
=
f_{12}-f_{01}.
$$

In the large-$E_J/E_C$ regime,

$$
\alpha
\approx
-E_C.
$$

For the parameters used in this project,

$$
E_C=0.3\ \mathrm{GHz},
$$

so the expected anharmonicity is approximately

$$
\alpha
\approx
-0.3\ \mathrm{GHz}.
$$

The negative sign indicates that the $1\rightarrow2$ transition frequency is lower than the $0\rightarrow1$ transition frequency.

---

### 5. Numerical and Approximate Transition Frequencies

![Numerical and approximate transition frequencies](figures/05_f01_vs_ej_ec.png)

The numerical transition frequency is calculated by diagonalizing the full transmon Hamiltonian:

$$
f_{01}^{\mathrm{num}}
=
E_1-E_0.
$$

The analytical approximation is

$$
f_{01}^{\mathrm{approx}}
=
\sqrt{8E_JE_C}-E_C.
$$

The approximation becomes more accurate as $E_J/E_C$ increases because the system moves deeper into the transmon regime.

---

### 6. Relative Anharmonicity versus Energy Ratio

![Relative anharmonicity versus EJ over EC](figures/06_relative_anharmonicity_vs_ej_ec.png)

The relative anharmonicity is defined as

$$
\alpha_{\mathrm{rel}}
=
\frac{\lvert\alpha\rvert}{f_{01}}.
$$

The absolute anharmonicity remains approximately determined by $E_C$, while $f_{01}$ increases with $E_J/E_C$.

As a result, the relative anharmonicity decreases as $E_J/E_C$ increases.

A smaller relative anharmonicity makes it more difficult to selectively drive the $0\rightarrow1$ transition without also exciting higher energy levels.

---

## Physical Interpretation

Increasing $E_J/E_C$ produces two important effects.

### Advantage: Reduced Charge-Noise Sensitivity

The dependence of the transition frequency on $n_g$ becomes exponentially smaller:

$$
\epsilon_{01}
\longrightarrow
0.
$$

This makes the transmon more robust against fluctuations in the offset charge.

### Tradeoff: Reduced Relative Anharmonicity

The relative anharmonicity decreases:

$$
\frac{\lvert\alpha\rvert}{f_{01}}
\longrightarrow
\text{smaller value}.
$$

This reduces the frequency separation between neighboring transitions relative to the qubit frequency and makes leakage control more challenging during fast gate operations.

---

## Main Conclusion

Increasing $E_J/E_C$ exponentially suppresses charge dispersion and reduces the transmon's sensitivity to charge noise.

However, increasing $E_J/E_C$ also reduces the relative anharmonicity

$$
\frac{\lvert\alpha\rvert}{f_{01}},
$$

which makes leakage into higher energy levels more difficult to control during fast gate operations.

The choice of $E_J/E_C$ is therefore a compromise between:

- resistance to charge noise;
- sufficient anharmonicity;
- transition selectivity;
- fast and accurate qubit control.

---

## Repository Structure

```text
Transmon-Energy-Spectrum-Study/
├── 1. Transmon Energy Spectrum.py
├── requirements.txt
├── README.md
└── figures/
    ├── 01_energy_spectrum_vs_ng.png
    ├── 02_transition_frequencies_vs_ng.png
    ├── 03_charge_dispersion_vs_ej_ec.png
    ├── 04_anharmonicity_vs_ej_ec.png
    ├── 05_f01_vs_ej_ec.png
    └── 06_relative_anharmonicity_vs_ej_ec.png
```

---

## Installation

Install the required Python packages with

```bash
pip install -r requirements.txt
```

The main dependencies are:

- NumPy
- Matplotlib
- scqubits

---

## Usage

Run the simulation with

```bash
python "1. Transmon Energy Spectrum.py"
```

The program calculates the transmon spectrum and saves the six result figures in the `figures` folder.

---
