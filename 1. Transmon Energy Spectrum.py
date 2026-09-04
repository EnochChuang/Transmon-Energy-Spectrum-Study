import numpy as np
import matplotlib.pyplot as plt
import scqubits as scq
from pathlib import Path

figure_dir = Path(__file__).resolve().parent / "figures"
figure_dir.mkdir(exist_ok=True)

print("Figures saved to:", figure_dir)

# unit of EJ/h, EC/h = GHz
EC = 0.3
EJ = 15.0
N_cut = 15
num_levels = 5
ng_values = np.linspace(-1.0, 1.0, 201)
ratio_list = np.array([10, 20, 30, 50, 80, 100], dtype=float)
n_values = np.arange(-N_cut, N_cut + 1)
# dim = len(n_values) # dim 等於 n_values 裡面元素的數量

def transmon_hamiltonian(EC, EJ, ng):
    H_charge = np.diag(
        4 * EC * (n_values - ng)**2
    )
    H_josephson = np.zeros((len(n_values), len(n_values)))
    for i in range(len(n_values) - 1):
        H_josephson[i, i + 1] = -EJ / 2
        H_josephson[i + 1, i] = -EJ / 2

    H = H_charge + H_josephson
    return H

# Part 1: Transmon properties at the default working point
transmon = scq.Transmon(EC=EC, EJ=EJ, ng=0.0, ncut=N_cut, truncated_dim=num_levels )
evals = transmon.eigenvals(evals_count=num_levels)
evals = evals - evals[0]

H_manual = transmon_hamiltonian(
    EC=EC,
    EJ=EJ,
    ng=0.0
)

evals_manual = np.linalg.eigvalsh(H_manual)
evals_manual = evals_manual[:num_levels]
evals_manual = evals_manual - evals_manual[0]

print(
    "Manual Hamiltonian energies [GHz] =",
    np.round(evals_manual, 6)
)
print(
    "scqubits energies [GHz] =",
    np.round(evals, 6)
)
print(
    "Maximum difference [GHz] =",
    np.max(np.abs(evals_manual - evals))
)

f01 = evals[1]-evals[0]
f12 = evals[2]-evals[1]
alpha = f12 - f01
formatted_evals = [f"{energy:.2f}" for energy in evals]
print("relative energies [GHz] =", formatted_evals)
print(f"f01 = {f01:.2f} GHz")
print(f"f12 = {f12:.2f} GHz")
print(f"anharmonicity alpha = {alpha:.2f} GHz")

# Part 2: Energy spectrum versus ng
fig1, ax1 = transmon.plot_evals_vs_paramvals(param_name="ng", param_vals=ng_values, evals_count=num_levels, subtract_ground=True)
ax1.set_xlabel(
    r"Offset charge $n_g$",
    fontsize=12,
    color="black",
    fontfamily="Arial"
)
ax1.set_ylabel(
    r"Transition Energy [GHz]",
    fontsize=12,
    color="black",
    fontfamily="Arial"
)
ax1.set_title(r"Transmon Spectrum vs. Offset Charge", fontsize=16)
fig1.tight_layout()
fig1.savefig(
    figure_dir / "01_energy_spectrum_vs_ng.png",
    dpi=300,
    bbox_inches="tight"
)

# Part 3: Transition frequencies versus ng
spec = transmon.get_spectrum_vs_paramvals(param_name="ng", param_vals=ng_values, evals_count=num_levels, subtract_ground=False)
energy_table = np.asarray(spec.energy_table)
print("energy_table shape =", energy_table.shape)

f01_vs_ng = energy_table[:, 1] - energy_table[:, 0]
f12_vs_ng = energy_table[:, 2] - energy_table[:, 1]
f23_vs_ng = energy_table[:, 3] - energy_table[:, 2]
fig2, ax2 = plt.subplots(figsize=(8, 5))
ax2.plot(
    ng_values,
    f01_vs_ng,
    label=r"$f_{01}=E_1-E_0$"
)
ax2.plot(
    ng_values,
    f12_vs_ng,
    label=r"$f_{12}=E_2-E_1$"
)
ax2.plot(
    ng_values,
    f23_vs_ng,
    label=r"$f_{23}=E_3-E_2$"
)
ax2.set_xlabel(r"Offset charge $n_g$")
ax2.set_ylabel("Transition frequency [GHz]")
ax2.set_title("Transmon Transition Frequencies vs. Offset Charge")
ax2.legend()
ax2.grid(True)
fig2.tight_layout()
fig2.savefig(
    figure_dir / "02_transition_frequencies_vs_ng.png",
    dpi=300,
    bbox_inches="tight"
)

charge_dispersion_01 = np.ptp(f01_vs_ng)
print(f"f01 charge dispersion = {charge_dispersion_01:.6e} GHz")

# Part 4: EJ/EC sweep
dispersion_01 = []
alpha_list = []
f01_list = []
relative_alpha_list = []
for ratio in ratio_list:
    transmon.EJ = ratio*EC
    spec = transmon.get_spectrum_vs_paramvals(param_name="ng", param_vals=ng_values, evals_count=num_levels, subtract_ground=False)
    energy_table = np.asarray(spec.energy_table)
    f01_vs_ng = energy_table[:, 1]-energy_table[:, 0]
    dispersion_01.append(np.ptp(f01_vs_ng)) # ptp = peak-to-peak
    transmon.ng = 0.0
    evals = transmon.eigenvals(evals_count=num_levels)
    f01 = evals[1]-evals[0]
    f12 = evals[2]-evals[1]
    alpha_list.append(f12 - f01)
    f01_list.append(f01)
    relative_alpha_list.append(abs(f12 - f01) / f01)

for ratio, alpha in zip(ratio_list, alpha_list):
    print(
        f"EJ/EC = {ratio:.0f}, "
        f"anharmonicity = {alpha:.6e} GHz"
    )

# Part 5: Analytical approximation
ratio_list_th = np.linspace(5, 100, 500)
EJ_list_th = ratio_list_th * EC
f01_approx = (np.sqrt(8 * EJ_list_th * EC) - EC)

# Part 6: Plotting the results
fig3, ax3 = plt.subplots(figsize=(8, 5))
fig4, ax4 = plt.subplots(figsize=(8, 5))
fig5, ax5 = plt.subplots(figsize=(8, 5))
ax3.semilogy(ratio_list, dispersion_01, "o-", color="#1B9431")
ax3.set_xlabel(r"$E_J/E_C$")
ax3.set_ylabel(r"$f_{01}$ charge dispersion [GHz]")
ax3.set_title(r"Charge Dispersion vs. $E_J/E_C$")
ax3.grid(True, which = "both")
fig3.savefig(
    figure_dir / "03_charge_dispersion_vs_ej_ec.png",
    dpi=300,
    bbox_inches="tight"
)

ax4.plot(ratio_list, alpha_list, "o-", color="#000099", label="Numerical solution")
ax4.set_xlabel(r"$E_J/E_C$")
ax4.set_ylabel(r"$\alpha$ [GHz]")
ax4.set_title(r"Anharmonicity vs. $E_J/E_C$")
ax4.axhline(
    -EC,
    color="black",
    linestyle="--",
    label=r"$\alpha\approx-E_C$"
    )
ax4.legend()
ax4.grid(True, which = "both")
fig4.savefig(
    figure_dir / "04_anharmonicity_vs_ej_ec.png",
    dpi=300,
    bbox_inches="tight"
)

ax5.plot(ratio_list_th, f01_approx, '-', color = "#28C8C8", label = "approximation formula")
ax5.plot(ratio_list, f01_list, 'o', color = "#28C8C8", label = "numerical solution")
ax5.grid(True, which="both")
ax5.set_xlabel(r"$E_J/E_C$")
ax5.set_ylabel(r"$f_{01}$ [GHz]")
ax5.set_title(r"Numerical and Approximate $f_{01}$ vs. $E_J/E_C$")
ax5.legend()
fig5.savefig(
    figure_dir / "05_f01_vs_ej_ec.png",
    dpi=300,
    bbox_inches="tight"
)

fig6, ax6 = plt.subplots(figsize=(8, 5))
ax6.plot(
    ratio_list,
    relative_alpha_list,
    "o-", color="#FF6310"
)
ax6.set_xlabel(r"$E_J/E_C$")
ax6.set_ylabel(r"Relative anharmonicity $|\alpha|/f_{01}$")
ax6.set_title(r"Relative Anharmonicity vs. $E_J/E_C$")
ax6.grid(True)
fig6.savefig(
    figure_dir / "06_relative_anharmonicity_vs_ej_ec.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()