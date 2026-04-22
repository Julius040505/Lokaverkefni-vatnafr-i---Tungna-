import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

rennsli = pd.read_csv(
    r'C:\Users\adamw\OneDrive\Desktop\lamah_ice\D_gauges\2_timeseries\daily\ID_86D.csv',
    sep=';')
vedur = pd.read_csv(
    r'C:\Users\adamw\OneDrive\Desktop\lamah_ice\A_basins_total_upstrm\2_timeseries\daily\meteorological_data\ID_86.csv',
    sep=',')

rennsli['dags'] = pd.to_datetime(rennsli[['YYYY','MM','DD']].rename(columns={'YYYY':'year','MM':'month','DD':'day'}))
vedur['dags']   = pd.to_datetime(vedur[['YYYY','MM','DD']].rename(columns={'YYYY':'year','MM':'month','DD':'day'}))

rennsli = rennsli[(rennsli['dags'] >= '1993-10-01') & (rennsli['dags'] <= '2023-09-30')].copy()
vedur   = vedur[(vedur['dags'] >= '1993-10-01') & (vedur['dags'] <= '2023-09-30')].copy()

rennsli['qobs'] = rennsli['qobs'].where(rennsli['qobs'] >= 0, np.nan).interpolate()

A_m2 = 1141.1 * 1e6
rennsli['Q_mm'] = rennsli['qobs'] * 86400 / A_m2 * 1000

water_order  = [10, 11, 12, 1, 2, 3, 4, 5, 6, 7, 8, 9]
manudur_nofn = ['Okt','Nóv','Des','Jan','Feb','Mar','Apr','Maí','Jún','Júl','Ágú','Sep']
dagar        = [31, 30, 31, 31, 28, 31, 30, 31, 30, 31, 31, 30]

Q_man  = rennsli.groupby('MM')['Q_mm'].mean().reindex(water_order)
P_man  = vedur.groupby('MM')['prec_carra'].mean().reindex(water_order)
ET_man = vedur.groupby('MM')['total_et_carra'].mean().reindex(water_order)

Q_rod  = [Q_man[m]  * d for m, d in zip(water_order, dagar)]
P_rod  = [P_man[m]  * d for m, d in zip(water_order, dagar)]
ET_rod = [ET_man[m] * d for m, d in zip(water_order, dagar)]
dS_rod = [P_rod[i] - Q_rod[i] - ET_rod[i] for i in range(12)]

print("=" * 75)
print("MÁNAÐARLEG GRUNNLÍKING – Tungnaá við Maríufoss (1993–2023) [mm/mánuð]")
print("=" * 75)
print(f"{'Mánuður':<8} {'P':>8} {'Q':>8} {'ET':>8} {'ΔS':>8}")
print("-" * 75)
for i, m in enumerate(manudur_nofn):
    print(f"{m:<8} {P_rod[i]:>8.1f} {Q_rod[i]:>8.1f} {ET_rod[i]:>8.1f} {dS_rod[i]:>8.1f}")
print("-" * 75)
print(f"{'Ársumma':<8} {sum(P_rod):>8.1f} {sum(Q_rod):>8.1f} {sum(ET_rod):>8.1f} {sum(dS_rod):>8.1f}")

x = np.arange(12)
width = 0.2

fig, ax = plt.subplots(figsize=(13, 6))
fig.suptitle('Mánaðarleg grunnlíking – Tungnaá við Maríufoss (1993–2023)', fontsize=13, fontweight='bold')

ax.bar(x - 1.5*width, P_rod,  width, label='P – Úrkoma',    color='steelblue', alpha=0.8)
ax.bar(x - 0.5*width, Q_rod,  width, label='Q – Rennsli',   color='orange',    alpha=0.8)
ax.bar(x + 0.5*width, ET_rod, width, label='ET – Uppgufun', color='green',     alpha=0.8)
ax.bar(x + 1.5*width, dS_rod, width, label='ΔS – Geymsla',  color='gray',      alpha=0.8)

ax.axhline(y=0, color='black', linewidth=0.8)
ax.set_xticks(x); ax.set_xticklabels(manudur_nofn)
ax.set_ylabel('mm/mánuð')
ax.set_title('P, Q, ET og ΔS eftir mánuðum')
ax.legend(); ax.grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.savefig('grunnliking_manadarlegt.png', dpi=150, bbox_inches='tight')
plt.show(); plt.close()
print("Mynd vistuð!")