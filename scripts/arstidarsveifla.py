import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Gögn lesin inn
rennsli = pd.read_csv('D_gauges/2_timeseries/daily/ID_86D.csv', sep=';')
vedur = pd.read_csv('A_basins_total_upstrm/2_timeseries/daily/meteorological_data/ID_86.csv', sep=',')

# Dagsetningar 1993-2023
rennsli['dags'] = pd.to_datetime(rennsli[['YYYY','MM','DD']].rename(columns={'YYYY':'year','MM':'month','DD':'day'}))
vedur['dags'] = pd.to_datetime(vedur[['YYYY','MM','DD']].rename(columns={'YYYY':'year','MM':'month','DD':'day'}))

rennsli = rennsli[(rennsli['dags'] >= '1993-10-01') & (rennsli['dags'] <= '2023-09-30')]
vedur = vedur[(vedur['dags'] >= '1993-10-01') & (vedur['dags'] <= '2023-09-30')]

water_year_order = [10, 11, 12, 1, 2, 3, 4, 5, 6, 7, 8, 9]
manudur = ['Okt','Nóv','Des','Jan','Feb','Mar','Apr','Maí','Jún','Júl','Ágú','Sep']

rennsli_man = rennsli.groupby('MM')['qobs'].mean().reindex(water_year_order)
urkoma_man = vedur.groupby('MM')['prec_carra'].mean().reindex(water_year_order)
hiti_man = vedur.groupby('MM')['2m_temp_carra'].mean().reindex(water_year_order)

rennsli_std = rennsli.groupby('MM')['qobs'].std().reindex(water_year_order)
urkoma_std = vedur.groupby('MM')['prec_carra'].std().reindex(water_year_order)
hiti_std = vedur.groupby('MM')['2m_temp_carra'].std().reindex(water_year_order)

x = range(1, 13)

print("=" * 50)
print("NIÐURSTÖÐUR – Árstíðasveifla Tungnaár")
print("=" * 50)

print(f"\nRennsli (m³/s):")
print(f"  Hæsta meðalrennsli:   {rennsli_man.max():.1f} m³/s – {manudur[rennsli_man.values.argmax()]}")
print(f"  Lægsta meðalrennsli:  {rennsli_man.min():.1f} m³/s – {manudur[rennsli_man.values.argmin()]}")
print(f"  Meðalrennsli (30 ár): {rennsli_man.mean():.1f} m³/s")

print(f"\nÚrkoma (mm/dag):")
print(f"  Mest:   {urkoma_man.max():.1f} mm/dag – {manudur[urkoma_man.values.argmax()]}")
print(f"  Minnst: {urkoma_man.min():.1f} mm/dag – {manudur[urkoma_man.values.argmin()]}")

print(f"\nHitastig (°C):")
print(f"  Hæst:  {hiti_man.max():.1f} °C – {manudur[hiti_man.values.argmax()]}")
print(f"  Lægst: {hiti_man.min():.1f} °C – {manudur[hiti_man.values.argmin()]}")
print(f"  Mánuðir yfir 0°C: {(hiti_man > 0).sum()}")

# Myndir teiknaðar
fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 10))
fig.suptitle('Árstíðasveifla – Tungnaá við Maríufoss (1993–2023)', fontsize=14, fontweight='bold')

# Rennsli
ax1.plot(x, rennsli_man.values, color='steelblue', linewidth=2, marker='o')
ax1.fill_between(x, rennsli_man.values - rennsli_std.values,
                    rennsli_man.values + rennsli_std.values,
                    alpha=0.2, color='steelblue')
ax1.set_ylabel('Rennsli (m³/s)')
ax1.set_xticks(list(x))
ax1.set_xticklabels(manudur)
ax1.grid(True, alpha=0.3)
ax1.set_title('Meðalrennsli')

# Úrkoma
ax2.bar(x, urkoma_man.values, color='cornflowerblue', alpha=0.7)
ax2.set_ylabel('Úrkoma (mm/dag)')
ax2.set_xticks(list(x))
ax2.set_xticklabels(manudur)
ax2.grid(True, alpha=0.3)
ax2.set_title('Meðalúrkoma')

# Hitastig
ax3.plot(x, hiti_man.values, color='tomato', linewidth=2, marker='o')
ax3.fill_between(x, hiti_man.values - hiti_std.values,
                    hiti_man.values + hiti_std.values,
                    alpha=0.2, color='tomato')
ax3.axhline(y=0, color='black', linewidth=0.8, linestyle='--')
ax3.set_ylabel('Hitastig (°C)')
ax3.set_xticks(list(x))
ax3.set_xticklabels(manudur)
ax3.grid(True, alpha=0.3)
ax3.set_title('Meðalhitastig')

plt.tight_layout()
plt.savefig('arstidarsveifla.png', dpi=150, bbox_inches='tight')
plt.show()
plt.close()

print("\nMynd vistuð!")