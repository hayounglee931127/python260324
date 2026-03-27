import pandas as pd
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

file_path = Path('c:/work/kosisSample.xlsx')
print('exists:', file_path.exists())

xls = pd.ExcelFile(file_path)
print('sheets:', xls.sheet_names)

df = pd.read_excel(file_path, sheet_name=0)
print('shape:', df.shape)
print(df.head(5))
print('columns:', df.columns.tolist())

# 클린 작업
cols = [str(c).strip().replace('\n',' ') for c in df.columns]
df.columns = cols
print('clean columns:',df.columns.tolist())

year = None; br=None; tfr=None
for c in df.columns:
    v=c.lower()
    if year is None and ('년' in v or 'year' in v): year=c
    if br is None and ('출생아' in v or 'birth' in v): br=c
    if tfr is None and ('출산율' in v or 'tfr' in v or 'fertility' in v): tfr=c
print('detected', year, br, tfr)

if year: df[year] = pd.to_numeric(df[year], errors='coerce')
if br: df[br] = pd.to_numeric(df[br], errors='coerce')
if tfr: df[tfr] = pd.to_numeric(df[tfr], errors='coerce')

sel = [c for c in [year, br, tfr] if c]
print('null counts:\n', df[sel].isna().sum())

if year and br:
    df = df.dropna(subset=[year, br])
    df = df[(df[year]>0) & (df[year]<2100)]
    df = df.sort_values(year)
    print('cleaned shape', df.shape)
    print(df[[year, br] + ([tfr] if tfr else [])].head())

    plt.figure(figsize=(10,6))
    plt.plot(df[year], df[br], marker='o', linestyle='-')
    plt.title('대한민국 연도별 출생아 수')
    plt.xlabel('년도')
    plt.ylabel('출생아 수')
    plt.grid(True, linestyle='--', alpha=0.5)
    out = Path('c:/work/kosis_births_by_year.png')
    plt.tight_layout(); plt.savefig(out, dpi=150)
    print('saved plot', out)

    df.to_csv(Path('c:/work/kosisSample_cleaned.csv'), index=False, encoding='utf-8-sig')
    print('saved csv', 'kosisSample_cleaned.csv')

    print('birth describe:')
    print(df[br].describe())
    if tfr:
        print('tfr describe:')
        print(df[tfr].describe())
    print('min birth', df.loc[df[br].idxmin(), [year,br]].to_dict())
    print('max birth', df.loc[df[br].idxmax(), [year,br]].to_dict())
else:
    print('필수 컬럼 누락')
