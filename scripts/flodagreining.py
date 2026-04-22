import pandas as pd
import matplotlib.pyplot as plt
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

rennsli['vatnsar'] = rennsli['dags'].apply(
    lambda x: x.year if x.month >= 10 else x.year - 1
)

idx = rennsli.groupby('vatnsar')['qobs'].idxmax()
annual_peaks = rennsli.loc[idx].reset_index(drop=True)
Q_peaks = np.sort(annual_peaks['qobs'].values)  
n = len(Q_peaks)


i = np.arange(1, n + 1)
P_gringorten = (i - 0.44) / (n + 0.12)
T_return = 1 / (1 - P_gringorten)  

print(f"Fjöldi annual peaks: {n}")
print(f"Minnsta flóð: {Q_peaks[0]:.1f} m³/s")
print(f"Stærsta flóð: {Q_peaks[-1]:.1f} m³/s")

# Gumbel
def gumbel_fit(Q):
    mu = np.mean(Q)
    sigma = np.std(Q, ddof=1)
    beta = sigma * np.sqrt(6) / np.pi
    u = mu - 0.5772 * beta
    return u, beta

def gumbel_quantile(T, u, beta):
    return u - beta * np.log(-np.log(1 - 1/T))

u, beta = gumbel_fit(Q_peaks)

# Log Normal 3 (LN3) 
ln3_params = stats.lognorm.fit(Q_peaks, floc=0)

# Log Pearson 3 (LP3)
lp3_params = stats.pearson3.fit(np.log(Q_peaks))

# Endurkomutímar til að teikna
T_plot = np.linspace(1.01, 200, 1000)
P_plot = 1 - 1/T_plot

Q_gumbel = gumbel_quantile(T_plot, u, beta)

Q_ln3 = stats.lognorm.ppf(P_plot, *ln3_params)

Q_lp3 = np.exp(stats.pearson3.ppf(P_plot, *lp3_params))

T_vals = [10, 50, 100]

print("\n" + "="*50)
print("NIÐURSTÖÐUR – Flóðagreining Tungnaár")
print("="*50)

for T in T_vals:
    q_gum = gumbel_quantile(T, u, beta)
    q_ln3 = stats.lognorm.ppf(1 - 1/T, *ln3_params)
    q_lp3 = np.exp(stats.pearson3.ppf(1 - 1/T, *lp3_params))
    print(f"\nQ{T} (T = {T} ár):")
    print(f"  Gumbel:      {q_gum:.1f} m³/s")
    print(f"  Log Normal3: {q_ln3:.1f} m³/s")
    print(f"  Log Pearson3:{q_lp3:.1f} m³/s")

n_boot = 1000
Q100_boot = []

for _ in range(n_boot):
    sample = np.random.choice(Q_peaks, size=n, replace=True)
    u_b, beta_b = gumbel_fit(sample)
    Q100_boot.append(gumbel_quantile(100, u_b, beta_b))

CI_low  = np.percentile(Q100_boot, 5)
CI_high = np.percentile(Q100_boot, 95)

print(f"\n90% Confidence Interval fyrir Q100 (Gumbel):")
print(f"  Neðri mörk: {CI_low:.1f} m³/s")
print(f"  Efri mörk:  {CI_high:.1f} m³/s")

fig, ax = plt.subplots(figsize=(12, 7))

# Gringorten punktar
ax.scatter(T_return, Q_peaks, color='black', zorder=5, 
           label='Annual peaks (Gringorten)', s=40)

# Dreifingarlínur
ax.plot(T_plot, Q_gumbel, 'r-',  linewidth=2, label='Gumbel')
ax.plot(T_plot, Q_ln3,    'b-',  linewidth=2, label='Log Normal 3')
ax.plot(T_plot, Q_lp3,    'g-',  linewidth=2, label='Log Pearson 3')

# CI skuggi
Q100_gumbel = gumbel_quantile(100, u, beta)
ax.annotate('', xy=(100, CI_high), xytext=(100, CI_low),
            arrowprops=dict(arrowstyle='<->', color='red', lw=2))
ax.text(105, CI_low - 20,
        f'90% CI\n[{CI_low:.0f}, {CI_high:.0f}]', 
        color='red', fontsize=9, va='top')

# Q10, Q50, Q100 línur
for T in T_vals:
    q = gumbel_quantile(T, u, beta)
    ax.axvline(x=T, color='gray', linestyle=':', linewidth=1)
    ax.text(T+1, ax.get_ylim()[0] if ax.get_ylim()[0] > 0 else 100, 
            f'T={T}', fontsize=8, color='gray')

ax.set_xscale('log')
ax.set_xlabel('Endurkomutími (ár) – lógaritmískur skali')
ax.set_ylabel('Rennsli (m³/s)')
ax.set_title('Flóðagreining – Tungnaá við Maríufoss (1993–2023)')
ax.legend()
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('flodagreining.png', dpi=150, bbox_inches='tight')
plt.show()
plt.close()
print("\nMynd vistuð!")