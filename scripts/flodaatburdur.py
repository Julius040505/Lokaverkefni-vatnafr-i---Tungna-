import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np

rennsli = pd.read_csv(
    r'C:\Users\adamw\OneDrive\Desktop\lamah_ice\D_gauges\2_timeseries\daily\ID_86D.csv',
    sep=';')

vedur = pd.read_csv(
    r'C:\Users\adamw\OneDrive\Desktop\lamah_ice\A_basins_total_upstrm\2_timeseries\daily\meteorological_data\ID_86.csv',
    sep=',')

rennsli['dags'] = pd.to_datetime(rennsli[['YYYY','MM','DD']].rename(columns={'YYYY':'year','MM':'month','DD':'day'}))
vedur['dags']   = pd.to_datetime(vedur[['YYYY','MM','DD']].rename(columns={'YYYY':'year','MM':'month','DD':'day'}))

rennsli = rennsli[(rennsli['dags'] >= '1993-10-01') & (rennsli['dags'] <= '2023-09-30')].copy().reset_index(drop=True)
vedur   = vedur[(vedur['dags'] >= '1993-10-01') & (vedur['dags'] <= '2023-09-30')].copy().reset_index(drop=True)

rennsli['qobs'] = rennsli['qobs'].where(rennsli['qobs'] >= 0, np.nan).interpolate()
rennsli['vatnsar'] = rennsli['dags'].apply(lambda x: x.year if x.month >= 10 else x.year - 1)

idx = rennsli.groupby('vatnsar')['qobs'].idxmax()
annual_peaks = rennsli.loc[idx].reset_index(drop=True)
top5 = annual_peaks.nlargest(5, 'qobs').copy()
top5['dags_str'] = top5['dags'].dt.strftime('%d.%m.%Y')

print("5 hæstu flóðin:")
print(top5[['dags_str', 'vatnsar', 'qobs']].to_string())

topp_dagur   = top5.iloc[0]['dags']
topp_rennsli = top5.iloc[0]['qobs']
print(f"\nValinn atburður: {topp_dagur.strftime('%d.%m.%Y')}")
print(f"Hámarksrennsli: {topp_rennsli:.1f} m³/s")

start = topp_dagur - pd.Timedelta(days=10)
end   = topp_dagur + pd.Timedelta(days=10)

Q_atb = rennsli[(rennsli['dags'] >= start) & (rennsli['dags'] <= end)].copy()
V_atb = vedur[(vedur['dags'] >= start) & (vedur['dags'] <= end)].copy()

fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 10), sharex=True)
fig.suptitle(f'Greining á rennslisatburði – Tungnaá við Maríufoss\n'
             f'{start.strftime("%d.%m.%Y")} til {end.strftime("%d.%m.%Y")}',
             fontsize=13, fontweight='bold')

upphaf             = pd.Timestamp('2023-03-31')
time_to_peak_start = pd.Timestamp('2023-04-07')
qmax               = pd.Timestamp('2023-04-10')
lok_urkoma         = pd.Timestamp('2023-04-10')
recession_end      = pd.Timestamp('2023-04-17')

ax1.plot(Q_atb['dags'], Q_atb['qobs'], 'b-', linewidth=2, label='Rennsli (Q)')
ax1.axvline(x=upphaf,             color='green',  linestyle='--', linewidth=1.5, label='Upphaf atburðar')
ax1.axvline(x=time_to_peak_start, color='purple', linestyle='--', linewidth=1.5, label='Upphaf 2. hækkunar')
ax1.axvline(x=qmax,               color='red',    linestyle='--', linewidth=1.5, label=f'Qmax = {topp_rennsli:.0f} m³/s')
ax1.axvline(x=recession_end,      color='orange', linestyle='--', linewidth=1.5, label='Lok recession')

ax1.annotate('', xy=(qmax, 480), xytext=(time_to_peak_start, 480),
             arrowprops=dict(arrowstyle='<->', color='purple', lw=2))
ax1.text(pd.Timestamp('2023-04-08'), 490, 'Time-to-peak\n3 dagar', ha='center', fontsize=8, color='purple')

ax1.annotate('', xy=(recession_end, 200), xytext=(qmax, 200),
             arrowprops=dict(arrowstyle='<->', color='orange', lw=2))
ax1.text(pd.Timestamp('2023-04-13'), 210, 'Recession time\n7 dagar', ha='center', fontsize=8, color='orange')

ax1.set_ylabel('Rennsli (m³/s)'); ax1.set_title('Rennsli (Q)')
ax1.legend(loc='upper left', fontsize=8); ax1.grid(True, alpha=0.3)

ax2.bar(V_atb['dags'], V_atb['prec_carra'], color='steelblue', alpha=0.7, label='Úrkoma (P)')
ax2.axvline(x=lok_urkoma, color='red', linestyle='--', linewidth=1.5, label='Lok úrkomu')
ax2.set_ylabel('Úrkoma (mm/dag)'); ax2.set_title('Úrkoma (P)')
ax2.legend(loc='upper right', fontsize=8); ax2.grid(True, alpha=0.3)

ax3.plot(V_atb['dags'], V_atb['2m_temp_carra'], 'r-', linewidth=2, label='Hitastig (T)')
ax3.axhline(y=0, color='black', linestyle='--', linewidth=0.8)
ax3.set_ylabel('Hitastig (°C)'); ax3.set_xlabel('Dagsetning'); ax3.set_title('Hitastig (T)')
ax3.legend(loc='upper right', fontsize=8); ax3.grid(True, alpha=0.3)

for ax in [ax1, ax2, ax3]:
    ax.xaxis.set_major_locator(mdates.DayLocator(interval=1))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%d.%m'))
plt.setp(ax3.xaxis.get_majorticklabels(), rotation=45, ha='right')

plt.tight_layout()
plt.savefig('flodatburður.png', dpi=150, bbox_inches='tight')
plt.show(); plt.close()
print("Mynd vistuð!")