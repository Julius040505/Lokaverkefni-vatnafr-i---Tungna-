import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.dates as mdates

rennsli = pd.read_csv(
    r'C:\Users\adamw\OneDrive\Desktop\lamah_ice\D_gauges\2_timeseries\daily\ID_86D.csv', 
    sep=';'
)

rennsli['dags'] = pd.to_datetime(rennsli[['YYYY','MM','DD']].rename(
    columns={'YYYY':'year','MM':'month','DD':'day'}))

rennsli = rennsli[(rennsli['dags'] >= '1993-10-01') & 
                  (rennsli['dags'] <= '2023-09-30')].copy().reset_index(drop=True)

rennsli['qobs'] = rennsli['qobs'].where(rennsli['qobs'] >= 0, np.nan)
rennsli['qobs'] = rennsli['qobs'].interpolate(method='linear')

rennsli['vatnsar'] = rennsli['dags'].apply(
    lambda x: x.year if x.month >= 10 else x.year - 1
)

idx = rennsli.groupby('vatnsar')['qobs'].idxmax()
annual_peaks = rennsli.loc[idx].reset_index(drop=True)
annual_peaks['dags_str'] = annual_peaks['dags'].dt.strftime('%d.%m.%Y')

print("Annual peaks:")
print(annual_peaks[['dags_str', 'vatnsar', 'qobs']].to_string())

# Mánuður hvers flóðs
annual_peaks['manudur'] = annual_peaks['dags'].dt.month

# Fjöldi flóða í hverjum mánuði
manudur_fjoldi = annual_peaks['manudur'].value_counts().sort_index()

manudur_nofn = {
    10: 'Okt', 11: 'Nóv', 12: 'Des',
    1: 'Jan', 2: 'Feb', 3: 'Mar',
    4: 'Apr', 5: 'Maí', 6: 'Jún',
    7: 'Júl', 8: 'Ágú', 9: 'Sep'
}

# Röðum eftir vatnsári (Okt → Sep)
rod = [10, 11, 12, 1, 2, 3, 4, 5, 6, 7, 8, 9]
x_nofn = [manudur_nofn[m] for m in rod]
x_gildi = [manudur_fjoldi.get(m, 0) for m in rod]

print("\nFlóð eftir mánuðum:")
for nafn, gildi in zip(x_nofn, x_gildi):
    print(f"  {nafn}: {gildi}")

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
fig.suptitle('Flóðasveifla – Tungnaá við Maríufoss (1993–2023)', 
             fontsize=14, fontweight='bold')

bars = ax1.bar(x_nofn, x_gildi, color='steelblue', alpha=0.8, edgecolor='black')
for bar, val in zip(bars, x_gildi):
    if val > 0:
        ax1.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 0.1,
                str(int(val)), ha='center', va='bottom', fontweight='bold')
ax1.set_ylabel('Fjöldi annual peaks')
ax1.set_xlabel('Mánuður')
ax1.set_title('Í hvaða mánuði koma stærstu flóðin?')
ax1.grid(True, alpha=0.3, axis='y')

ax2.plot(annual_peaks['dags'], annual_peaks['qobs'], 
         'bo-', markersize=5, linewidth=1, label='Annual peak')
ax2.set_ylabel('Rennsli (m³/s)')
ax2.set_xlabel('Ár')
ax2.set_title('Annual peak flows yfir tíma')
ax2.grid(True, alpha=0.3)
ax2.legend()
ax2.xaxis.set_major_locator(mdates.YearLocator(2))
ax2.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))

plt.tight_layout()
plt.savefig('flodasveifla.png', dpi=150, bbox_inches='tight')
plt.show()
plt.close()
print("Mynd vistuð!")