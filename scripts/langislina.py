import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

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

Q_sorted = np.sort(Q)[::-1]

n = len(Q_sorted)
exceedance = np.arange(1, n + 1) / n * 100 

Q5  = np.percentile(Q, 95)
Q50 = np.percentile(Q, 50)  
Q95 = np.percentile(Q, 5)   

print("=" * 40)
print("LANGÆISLÍNA RENNSLIS – TUNGNAÁ")
print("=" * 40)
print(f"Q5  (hárennsli):  {Q5:.1f} m³/s")
print(f"Q50 (miðgildi):   {Q50:.1f} m³/s")
print(f"Q95 (lágrennsli): {Q95:.1f} m³/s")
print(f"Q5/Q95 hlutfall:  {Q5/Q95:.1f}")

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
fig.suptitle('Langæislína rennslis – Tungnaá við Maríufoss (1993–2023)', 
             fontsize=14, fontweight='bold')

ax1.plot(exceedance, Q_sorted, color='steelblue', linewidth=2)
ax1.axvline(x=5,  color='red',    linestyle='--', linewidth=1.5, label=f'Q5  = {Q5:.1f} m³/s')
ax1.axvline(x=50, color='green',  linestyle='--', linewidth=1.5, label=f'Q50 = {Q50:.1f} m³/s')
ax1.axvline(x=95, color='orange', linestyle='--', linewidth=1.5, label=f'Q95 = {Q95:.1f} m³/s')
ax1.axhline(y=Q5,  color='red',    linestyle=':', linewidth=1)
ax1.axhline(y=Q50, color='green',  linestyle=':', linewidth=1)
ax1.axhline(y=Q95, color='orange', linestyle=':', linewidth=1)
ax1.set_xlabel('Líkindi þess að rennsli sé náð eða farið yfir (%)')
ax1.set_ylabel('Rennsli (m³/s)')
ax1.set_title('Venjulegur skali')
ax1.legend()
ax1.grid(True, alpha=0.3)

ax2.semilogy(exceedance, Q_sorted, color='steelblue', linewidth=2)
ax2.axvline(x=5,  color='red',    linestyle='--', linewidth=1.5, label=f'Q5  = {Q5:.1f} m³/s')
ax2.axvline(x=50, color='green',  linestyle='--', linewidth=1.5, label=f'Q50 = {Q50:.1f} m³/s')
ax2.axvline(x=95, color='orange', linestyle='--', linewidth=1.5, label=f'Q95 = {Q95:.1f} m³/s')
ax2.axhline(y=Q5,  color='red',    linestyle=':', linewidth=1)
ax2.axhline(y=Q50, color='green',  linestyle=':', linewidth=1)
ax2.axhline(y=Q95, color='orange', linestyle=':', linewidth=1)
ax2.set_xlabel('Líkindi þess að rennsli sé náð eða farið yfir (%)')
ax2.set_ylabel('Rennsli (m³/s) – lógaritmískur skali')
ax2.set_title('Lógaritmískur skali')
ax2.legend()
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('langaislina.png', dpi=150, bbox_inches='tight')
plt.show()
plt.close()
print("Mynd vistuð!")