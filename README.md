# Vatnafræðileg greining – Tungnaá við Maríufoss
**UMV201G – Vatnafræði | Lokaverkefni – Vor 2026**  
Háskóli Íslands, Umhverfis- og byggingarverkfræðideild

**Höfundar:** Adam David Wheeler & Júlíus Guðjónsson  
**Kennarar:** Hörður Helgason & Tarek Selim

---

## Um verkefnið

Þetta repo inniheldur allan kóða sem notaðir voru í lokaverkefninu í vatnafræði.
Verkefnið fjallar um vatnafræðilega greiningu á Tungnaá við Maríufoss
(ID 86 í LamaH-Ice gagnasafninu) á tímabilinu 1993–2023.

Greiningin nær yfir:
- Árstíðasveiflu rennslis, úrkomu og hitastigs.
- Grunnvatnsmat með Lyne-Hollick og Eckhardt aðferðum
- Recession greiningu
- Grunnlíkingu vatnafræðinnar (P = Q + ET + ΔS)
- Langæislínu rennslis
- Flóðagreiningu (Gumbel, Log Normal 3, Log Pearson 3)
- Leitnigreiningu (Theil-Sen + Modified Mann-Kendall)
- Greiningu á rennslisatburði (10. apríl 2023)

---

## Gögn

Hrá gögn eru **ekki** geymd í þessu repo. Öll gögn koma úr **LamaH-Ice** gagnasafninu:

> Helgason, H. B. & Nijssen, B. (2024). LamaH-Ice: LArge-SaMple DAta for Hydrology  
> and Environmental Sciences for Iceland. *Earth System Science Data*, 16, 2741–2771.  
> https://doi.org/10.5194/ESSD-16-2741-2024

**Niðurhal gagna:** https://www.hydroshare.org/resource/86117a5f36cc4b7c90a5d54e18161c91/

Gögn sem notuð eru fyrir mælistöð ID 86 (Maríufoss):

| Skrá | Lýsing |
|------|---------|
| `ID_86D.csv` | Daglegar rennslismælingar (m³/s), 1993–2023 |
| `ID_86.csv` | Veðurfræðileg gögn (úrkoma, hitastig, ET o.fl.) úr CARRA endurgreiningu |
| `Catchment_attributes.csv` | Eiginleikar vatnasviðs |
| `Gauge_attributes.csv` | Upplýsingar um mælistöð |

---

## Uppsetning og keyrsla

### Kröfur

```bash
Python >= 3.9
pandas
numpy
matplotlib
scipy
pymannkendall
```

Setja upp með:

```bash
pip install pandas numpy matplotlib scipy pymannkendall
```

---

## Skráaruppbygging

```
repo/
├── data/                          
├── scripts/
│   ├── arstidarsveifla.py        
│   ├── grunnvatn.py               
│   ├── recession.py              
│   ├── grunnliking.py             
│   ├── langislina.py              
│   ├── flodasveifla.py            
│   ├── flodagreining.py           
│   ├── leitnigreining.py          
│   └── flodaatburdur.py           
├── figures/
│   ├── arstidarsveifla.png        
│   ├── grunnvatn.png              
│   ├── grunnvatn_samanburdur.png  
│   ├── recession.png              
│   ├── grunnliking_manadarlegt.png 
│   ├── langaislina.png            
│   ├── flodasveifla.png           
│   ├── flodagreining.png          
│   ├── leitnigreining.png         
│   ├── leitnigreining_vetur.png   
│   ├── leitnigreining_sumar.png   
│   └── flodatburður.png          
└── README.md
```

---

## Keyrsla

Keyrðu hvern kóða fyrir sig úr scripts möppu repo-sins:

```bash
python scripts/arstidarsveifla.py
python scripts/grunnvatn.py
python scripts/recession.py
python scripts/grunnliking.py
python scripts/langislina.py
python scripts/flodasveifla.py
python scripts/flodagreining.py
python scripts/leitnigreining.py
python scripts/flodaatburdur.py
```

Myndir eru vistaðar sjálfkrafa í `figures/` möppuna.

---

## Tengsl skráa við myndir í skýrslunni

| Mynd í skýrslu | PNG skrá | Skript |
|----------------|----------|--------|
| Mynd 4.1 – Árstíðasveifla | `arstidarsveifla.png` | `arstidarsveifla.py` |
| Mynd 4.2 – Grunnvatnsgreining (Lyne-Hollick) | `grunnvatn.png` | `grunnvatn.py` |
| Mynd 4.3 – Samanburður baseflow aðferða | `grunnvatn_samanburdur.png` | `grunnvatn.py` |
| Mynd 4.4 – Recession-greining | `recession.png` | `recession.py` |
| Mynd 4.5 – Mánaðarleg grunnlíking | `grunnliking_manadarlegt.png` | `grunnliking.py` |
| Mynd 4.6 – Langæislína rennslis | `langaislina.png` | `langislina.py` |
| Mynd 4.7 – Flóðasveifla (annual peaks) | `flodasveifla.png` | `flodasveifla.py` |
| Mynd 4.8 – Flóðagreining (dreifingar) | `flodagreining.png` | `flodagreining.py` |
| Mynd 4.9 – Leitnigreining (ársgrundvöllur) | `leitnigreining.png` | `leitnigreining.py` |
| Mynd 4.10a – Leitnigreining vetur | `leitnigreining_vetur.png` | `leitnigreining.py` |
| Mynd 4.10b – Leitnigreining sumar | `leitnigreining_sumar.png` | `leitnigreining.py` |
| Mynd 4.11 – Rennslisatburður 10. apríl 2023 | `flodatburður.png` | `flodaatburdur.py` |

