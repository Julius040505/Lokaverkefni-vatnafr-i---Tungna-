import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
from scipy import stats

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

Q = rennsli['qobs'].values
min_length = 10

recession_periods = []
i = 1
while i < len(Q) - min_length:
    if Q[i] < Q[i-1]:
        start = i - 1
        j = i
        while j < len(Q) and Q[j] < Q[j-1]:
            j += 1
        end = j - 1
        if end - start >= min_length:
            recession_periods.append((start, end))
        i = j
    else:
        i += 1

k_values = []
valid_periods = []

for start, end in recession_periods:
    Q_period = Q[start:end+1]
    t = np.arange(len(Q_period))
    lnQ = np.log(Q_period)
    slope, intercept, r, p, se = stats.linregress(t, lnQ)
    
    if slope < 0 and r**2 > 0.85:
        k = -1 / slope
        k_values.append(k)
        valid_periods.append((start, end, slope, intercept, r**2))

best = max(valid_periods, key=lambda x: x[4])
start, end, slope, intercept, r2 = best
Q_period = Q[start:end+1]
dags_period = rennsli['dags'].values[start:end+1]
t = np.arange(len(Q_period))
Q_fitted = np.exp(intercept + slope * t)
lnQ = np.log(Q_period)
k_best = -1/slope
Q0 = np.exp(intercept)

print(f"Fjöldi lækkunartímabila: {len(recession_periods)}")
print(f"Fjöldi gildra k-gilda: {len(k_values)}")
print()
print(f"Hallatala (slope) = {slope:.4f}")
print()
print(f"Recession constant:")
print(f"   k = -1 / slope")
print(f"   k = -1 / ({slope:.4f})")
print(f"   k = {k_best:.1f} dagar")
print()
print(f"Túlkun:")
print(f"   Rennsli lækkar í e⁻¹ ≈ 37% af upphafsgildi á {k_best:.0f} dögum.")
print()
print(f"   Meðal k (öll tímabil) = {np.mean(k_values):.1f} dagar")
print(f"   Staðalfrávik k        = {np.std(k_values):.1f} dagar")
print(f"   Min k = {np.min(k_values):.1f}, Max k = {np.max(k_values):.1f} dagar")

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
fig.suptitle('Recession Analysis – Tungnaá við Maríufoss', 
             fontsize=14, fontweight='bold')

# Mynd 1 Rennsli yfir tíma
ax1.plot(dags_period, Q_period, 'bo-', markersize=4, label='Mælt rennsli')
ax1.plot(dags_period, Q_fitted, 'r--', linewidth=2, 
         label=f'Fitted: Q = {Q0:.0f}·e^(-t/{k_best:.1f})')
ax1.set_ylabel('Rennsli (m³/s)')
ax1.set_title('Lækkunartímabil')
ax1.legend()
ax1.grid(True, alpha=0.3)
ax1.xaxis.set_major_locator(mdates.DayLocator(interval=2))
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%d.%m.%Y'))
plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45, ha='right')

# Mynd 2 ln(Q) vs t
ax2.plot(t, lnQ, 'bo', markersize=6, label='ln(Q) mælt')
ax2.plot(t, intercept + slope*t, 'r-', linewidth=2, 
         label='Línuleg aðhvarfsgreining')
textstr = f'ln(Q) = {intercept:.2f} + ({slope:.4f})·t\nR² = {r2:.3f}'
ax2.text(0.05, 0.05, textstr, transform=ax2.transAxes, fontsize=10,
         verticalalignment='bottom',
         bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))
ax2.set_xlabel('Tími t (dagar frá upphafi)')
ax2.set_ylabel('ln(Q)')
ax2.set_title('ln(Q) sem fall af t')
ax2.legend()
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('recession.png', dpi=150, bbox_inches='tight')
plt.show()
plt.close()
print("Mynd vistuð!")