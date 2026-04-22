import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import theilslopes
import pymannkendall as mk

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

annual_q = rennsli.groupby('vatnsar')['qobs'].mean()

slope_a, intercept_a, _, _ = theilslopes(annual_q.values, annual_q.index)

result_a = mk.hamed_rao_modification_test(annual_q.values)

print("=" * 50)
print("LEITNIGREINING – Ársgrunnur")
print("=" * 50)
print(f"Theil-Sen slope: {slope_a:.4f} m³/s/ár")
print(f"Modified Mann-Kendall:")
print(f"  Trend:     {result_a.trend}")
print(f"  p-gildi:   {result_a.p:.4f}")
print(f"  Tau:       {result_a.Tau:.4f}")
print(f"  Marktækt (p<0.05): {'Já' if result_a.p < 0.05 else 'Nei'}")

fig, ax = plt.subplots(figsize=(12, 6))
fig.suptitle('Leitnigreining – Tungnaá við Maríufoss (1993–2023)',
             fontsize=14, fontweight='bold')

trend_a = intercept_a + slope_a * annual_q.index

ax.plot(annual_q.index, annual_q.values, 'bo-', 
        markersize=5, linewidth=1, label='Árlegt meðalrennsli')
ax.plot(annual_q.index, trend_a, 'r-', 
        linewidth=2, label=f'Theil-Sen leitnilína\n(slope = {slope_a:.3f} m³/s/ár)')

marktaekt = 'Já' if result_a.p < 0.05 else 'Nei'
textstr = (f"Modified Mann-Kendall próf:\n"
           f"  Trend: {result_a.trend}\n"
           f"  p-gildi: {result_a.p:.4f}\n"
           f"  Marktækt: {marktaekt}")
ax.text(0.02, 0.98, textstr, transform=ax.transAxes, fontsize=9,
        verticalalignment='top',
        bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))

ax.set_xlabel('Vatnsár')
ax.set_ylabel('Rennsli (m³/s)')
ax.set_title('Árlegt meðalrennsli')
ax.legend(loc='upper right')
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('leitnigreining.png', dpi=150, bbox_inches='tight')
plt.show()
print("Mynd vistuð!")

vetur_df = rennsli[rennsli['dags'].dt.month.isin([12, 1, 2])]
vetur_q = vetur_df.groupby('vatnsar')['qobs'].mean()

slope_v, intercept_v, _, _ = theilslopes(vetur_q.values, vetur_q.index)

result_v = mk.hamed_rao_modification_test(vetur_q.values)

print("\n" + "=" * 50)
print("LEITNIGREINING – Vetur (Des, Jan, Feb)")
print("=" * 50)
print(f"Theil-Sen slope: {slope_v:.4f} m³/s/ár")
print(f"Modified Mann-Kendall:")
print(f"  Trend:     {result_v.trend}")
print(f"  p-gildi:   {result_v.p:.4f}")
print(f"  Tau:       {result_v.Tau:.4f}")
print(f"  Marktækt (p<0.05): {'Já' if result_v.p < 0.05 else 'Nei'}")

fig, ax = plt.subplots(figsize=(12, 6))
fig.suptitle('Leitnigreining – Vetur (Des, Jan, Feb)\nTungnaá við Maríufoss (1993–2023)',
             fontsize=14, fontweight='bold')

trend_v = intercept_v + slope_v * vetur_q.index

ax.plot(vetur_q.index, vetur_q.values, 'bo-',
        markersize=5, linewidth=1, label='Vetrar meðalrennsli')
ax.plot(vetur_q.index, trend_v, 'r-',
        linewidth=2, label=f'Theil-Sen leitnilína\n(slope = {slope_v:.3f} m³/s/ár)')

marktaekt_v = 'Já' if result_v.p < 0.05 else 'Nei'
textstr_v = (f"Modified Mann-Kendall próf:\n"
             f"  Trend: {result_v.trend}\n"
             f"  p-gildi: {result_v.p:.4f}\n"
             f"  Marktækt: {marktaekt_v}")
ax.text(0.02, 0.98, textstr_v, transform=ax.transAxes, fontsize=9,
        verticalalignment='top',
        bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))

ax.set_xlabel('Vatnsár')
ax.set_ylabel('Rennsli (m³/s)')
ax.set_title('Vetrar meðalrennsli')
ax.legend(loc='upper right')
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('leitnigreining_vetur.png', dpi=150, bbox_inches='tight')
plt.show()
print("Vetur mynd vistuð!")

sumar_df = rennsli[rennsli['dags'].dt.month.isin([6, 7, 8])]
sumar_q = sumar_df.groupby('vatnsar')['qobs'].mean()

slope_s, intercept_s, _, _ = theilslopes(sumar_q.values, sumar_q.index)

result_s = mk.hamed_rao_modification_test(sumar_q.values)

print("\n" + "=" * 50)
print("LEITNIGREINING – Sumar (Jún, Júl, Ágú)")
print("=" * 50)
print(f"Theil-Sen slope: {slope_s:.4f} m³/s/ár")
print(f"Modified Mann-Kendall:")
print(f"  Trend:     {result_s.trend}")
print(f"  p-gildi:   {result_s.p:.4f}")
print(f"  Tau:       {result_s.Tau:.4f}")
print(f"  Marktækt (p<0.05): {'Já' if result_s.p < 0.05 else 'Nei'}")

fig, ax = plt.subplots(figsize=(12, 6))
fig.suptitle('Leitnigreining – Sumar (Jún, Júl, Ágú)\nTungnaá við Maríufoss (1993–2023)',
             fontsize=14, fontweight='bold')

trend_s = intercept_s + slope_s * sumar_q.index

ax.plot(sumar_q.index, sumar_q.values, 'bo-',
        markersize=5, linewidth=1, label='Sumar meðalrennsli')
ax.plot(sumar_q.index, trend_s, 'r-',
        linewidth=2, label=f'Theil-Sen leitnilína\n(slope = {slope_s:.3f} m³/s/ár)')

marktaekt_s = 'Já' if result_s.p < 0.05 else 'Nei'
textstr_s = (f"Modified Mann-Kendall próf:\n"
             f"  Trend: {result_s.trend}\n"
             f"  p-gildi: {result_s.p:.4f}\n"
             f"  Marktækt: {marktaekt_s}")
ax.text(0.02, 0.98, textstr_s, transform=ax.transAxes, fontsize=9,
        verticalalignment='top',
        bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))

ax.set_xlabel('Vatnsár')
ax.set_ylabel('Rennsli (m³/s)')
ax.set_title('Sumar meðalrennsli')
ax.legend(loc='upper right')
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('leitnigreining_sumar.png', dpi=150, bbox_inches='tight')
plt.show()
plt.close()
print("Sumar mynd vistuð!")