# Transmon Energy Spectrum Study

This project numerically investigates the energy spectrum, transition
frequencies, charge dispersion, and anharmonicity of a transmon qubit.

## Physical model

The transmon Hamiltonian is

$$
\hat{H}
=
4E_C(\hat{n}-n_g)^2
-
E_J\cos\hat{\phi}.
$$

In the charge basis, the Hamiltonian matrix is

$$
H_{n'n}
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

## Parameters

| Parameter | Value |
|---|---:|
| Charging energy $E_C/h$ | 0.3 GHz |
| Josephson energy $E_J/h$ | 15.0 GHz |
| Default ratio $E_J/E_C$ | 50 |
| Offset-charge range $n_g$ | -1 to 1 |
| Charge cutoff | 15 |
| Number of energy levels | 5 |

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

Increasing $E_J/E_C$ strongly suppresses the charge dispersion of
$f_{01}$.

### 4. Anharmonicity

![Anharmonicity](figures/04_anharmonicity_vs_ej_ec.png)

At large $E_J/E_C$, the anharmonicity approaches

$$
\alpha \approx -E_C.
$$

### 5. Numerical and approximate transition frequency

![Transition-frequency comparison](figures/05_f01_vs_ej_ec.png)

The numerical result is compared with the large-$E_J/E_C$
approximation

$$
f_{01}
\approx
\sqrt{8E_JE_C}-E_C.
$$

### 6. Relative anharmonicity

![Relative anharmonicity](figures/06_relative_anharmonicity_vs_ej_ec.png)

Although charge dispersion is suppressed as $E_J/E_C$ increases, the
relative anharmonicity decreases.

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
python 1. Transmon Energy Spectrum.py
```
