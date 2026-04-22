import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.dates as mdates

# ================================
# 1. LESA INN OG HREINSA GÖGN
# ================================
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

def ladson_filter(Q, alpha=0.98):
    """Lyne-Hollick baseflow filter – 3 passes"""
    Q = np.array(Q, dtype=float)
    n = len(Q)
    
    Qf = np.zeros(n)
    Qf[0] = Q[0] / 2
    for i in range(1, n):
        Qf[i] = alpha * Qf[i-1] + ((1 + alpha) / 2) * (Q[i] - Q[i-1])
        Qf[i] = max(Qf[i], 0)
    Qb = np.clip(Q - Qf, 0, Q)

    Qf2 = np.zeros(n)
    Qf2[-1] = Qb[-1] / 2
    for i in range(n-2, -1, -1):
        Qf2[i] = alpha * Qf2[i+1] + ((1 + alpha) / 2) * (Qb[i] - Qb[i+1])
        Qf2[i] = max(Qf2[i], 0)
    Qb2 = np.clip(Qb - Qf2, 0, Qb)

    Qf3 = np.zeros(n)
    Qf3[0] = Qb2[0] / 2
    for i in range(1, n):
        Qf3[i] = alpha * Qf3[i-1] + ((1 + alpha) / 2) * (Qb2[i] - Qb2[i-1])
        Qf3[i] = max(Qf3[i], 0)
    Qb3 = np.clip(Qb2 - Qf3, 0, Qb2)
    
    return Qb3, np.maximum(Q - Qb3, 0)

def eckhardt_filter(Q, alpha=0.98, BFImax=0.50):
    """Eckhardt baseflow filter"""
    Q = np.array(Q, dtype=float)
    n = len(Q)
    Qb = np.zeros(n)
    Qb[0] = Q[0] * BFImax
    for i in range(1, n):
        Qb[i] = ((1 - BFImax) * alpha * Qb[i-1] + (1 - alpha) * BFImax * Q[i]) / (1 - alpha * BFImax)
        Qb[i] = min(max(Qb[i], 0), Q[i])
    return Qb, Q - Qb

Q = rennsli['qobs'].values

Qb_lad, Qf_lad = ladson_filter(Q)
rennsli['Qb'] = Qb_lad
rennsli['Qf'] = Qf_lad

Qb_eck, Qf_eck = eckhardt_filter(Q)
rennsli['Qb_eck'] = Qb_eck
rennsli['Qf_eck'] = Qf_eck

BFI_ladson = Qb_lad.mean() / Q.mean()
BFI_eck    = Qb_eck.mean() / Q.mean()

bfi_ar = rennsli.groupby('vatnsar').apply(
    lambda x: x['Qb'].sum() / x['qobs'].sum()
).reset_index()
bfi_ar.columns = ['vatnsár', 'BFI']

print("=" * 45)
print("NIÐURSTÖÐUR – Grunnvatnsgreining")
print("=" * 45)
print(f"BFI Lyne-Hollick (α=0.98):   {BFI_ladson:.2f}")
print(f"BFI Eckhardt (BFImax=0.50):  {BFI_eck:.2f}")
print(f"Meðal BFI (Lyne-Hollick):    {bfi_ar['BFI'].mean():.3f}")

ar = rennsli[rennsli['vatnsar'] == 2009]

fig2, (ax3, ax4) = plt.subplots(2, 1, figsize=(12, 10))
fig2.suptitle('Grunnvatnsgreining – Tungnaá við Maríufoss', fontsize=14, fontweight='bold')

ax3.fill_between(ar['dags'], ar['Qb'], alpha=0.7, color='steelblue', label='Grunnrennsli (Qb)')
ax3.fill_between(ar['dags'], ar['Qb'], ar['qobs'], alpha=0.7, color='orange', label='Yfirborðsrennsli (Qf)')
ax3.plot(ar['dags'], ar['qobs'], color='black', linewidth=0.8, label='Heildarrennsli (Q)')
ax3.set_ylabel('Rennsli (m³/s)')
ax3.set_title('Baseflow separation – Vatnsárið 2010 (Lyne-Hollick)')
ax3.legend()
ax3.grid(True, alpha=0.3)
ax3.xaxis.set_major_locator(mdates.MonthLocator())
ax3.xaxis.set_major_formatter(mdates.DateFormatter('%d.%m.%y'))
plt.setp(ax3.xaxis.get_majorticklabels(), rotation=45, ha='right')

ax4.bar(bfi_ar['vatnsár'], bfi_ar['BFI'], color='steelblue', alpha=0.7)
ax4.axhline(y=bfi_ar['BFI'].mean(), color='red', linestyle='--',
            linewidth=2, label=f"Meðal BFI = {bfi_ar['BFI'].mean():.2f}")
ax4.set_ylabel('BFI')
ax4.set_xlabel('Vatnsár')
ax4.set_title('Baseflow Index (BFI) eftir vatnsárum')
ax4.legend()
ax4.grid(True, alpha=0.3)
ax4.set_ylim(0, 1)

plt.tight_layout()
plt.savefig('grunnvatn.png', dpi=150, bbox_inches='tight')
plt.show()

fig1, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))
fig1.suptitle('Samanburður baseflow separation aðferða – Vatnsárið 2010', 
             fontsize=13, fontweight='bold')

ax1.fill_between(ar['dags'], ar['Qb'], alpha=0.7, color='steelblue', label='Grunnrennsli (Qb)')
ax1.fill_between(ar['dags'], ar['Qb'], ar['qobs'], alpha=0.7, color='orange', label='Yfirborðsrennsli (Qf)')
ax1.plot(ar['dags'], ar['qobs'], color='black', linewidth=0.5)
ax1.set_ylabel('Rennsli (m³/s)')
ax1.set_title(f'Lyne-Hollick (α=0.98) – BFI = {BFI_ladson:.2f}')
ax1.legend(loc='upper right')
ax1.set_ylim(0, 300)
ax1.grid(True, alpha=0.3)
ax1.xaxis.set_major_locator(mdates.MonthLocator())
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%d.%m.%y'))

ax2.fill_between(ar['dags'], ar['Qb_eck'], alpha=0.7, color='steelblue', label='Grunnrennsli (Qb)')
ax2.fill_between(ar['dags'], ar['Qb_eck'], ar['qobs'], alpha=0.7, color='orange', label='Yfirborðsrennsli (Qf)')
ax2.plot(ar['dags'], ar['qobs'], color='black', linewidth=0.5)
ax2.set_ylabel('Rennsli (m³/s)')
ax2.set_title(f'Eckhardt (BFImax=0.50) – BFI = {BFI_eck:.2f}')
ax2.legend(loc='upper right')
ax2.set_ylim(0, 300)
ax2.grid(True, alpha=0.3)
ax2.xaxis.set_major_locator(mdates.MonthLocator())
ax2.xaxis.set_major_formatter(mdates.DateFormatter('%d.%m.%y'))
plt.setp(ax2.xaxis.get_majorticklabels(), rotation=45, ha='right')

plt.tight_layout()
plt.savefig('grunnvatn_samanburdur.png', dpi=150, bbox_inches='tight')
plt.show()
plt.close()
print("Myndir vistaðar!")