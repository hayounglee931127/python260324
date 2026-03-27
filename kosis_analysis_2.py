import pandas as pd
from pathlib import Path

file_path = Path('c:/work/kosisSample.xlsx')

# 원래 구조는 indicator가 행이고 연도가 열인 형태임
raw = pd.read_excel(file_path, sheet_name=0)
raw.columns = [str(c).strip().replace('\n',' ') for c in raw.columns]
print('원본 크기', raw.shape)
print(raw.head())

# 첫 컬럼: 항목명
first_col = raw.columns[0]
# numeric year columns
year_cols = [c for c in raw.columns if c != first_col]

# 출생아수, 합계출산율만 분리
birth_rows = raw[raw[first_col].str.contains('출생아수|출생아 수|Birth', na=False)]
tfr_rows = raw[raw[first_col].str.contains('합계출산율|총출산율|Total fertility rate|TFR', na=False)]
print('birth_rows', birth_rows.shape, 'tfr_rows', tfr_rows.shape)

# 사실 1개씩만 있어야 함
if birth_rows.shape[0] >=1:
    br = birth_rows.iloc[0].drop(first_col)
    br.index = pd.to_numeric(br.index, errors='coerce')
    br = pd.to_numeric(br.values, errors='coerce')
    df_birth = pd.DataFrame({'year': pd.to_numeric(year_cols, errors='coerce'), 'births': br})
else:
    df_birth = pd.DataFrame()

if tfr_rows.shape[0] >=1:
    tfr = tfr_rows.iloc[0].drop(first_col)
    df_tfr = pd.DataFrame({'year': pd.to_numeric(year_cols, errors='coerce'), 'tfr': pd.to_numeric(tfr.values, errors='coerce')})
else:
    df_tfr = pd.DataFrame()

print(df_birth.head())
print(df_tfr.head())

if not df_birth.empty:
    df_birth = df_birth.dropna(subset=['year','births']).sort_values('year')
    df_birth['year'] = df_birth['year'].astype(int)
    df_birth.to_csv('c:/work/kosis_births_long.csv', index=False, encoding='utf-8-sig')

if not df_tfr.empty:
    df_tfr = df_tfr.dropna(subset=['year','tfr']).sort_values('year')
    df_tfr['year'] = df_tfr['year'].astype(int)
    df_tfr.to_csv('c:/work/kosis_tfr_long.csv', index=False, encoding='utf-8-sig')

# 기본분석
if not df_birth.empty:
    print('출생아 min, max\n', df_birth.loc[df_birth.births.idxmin()], df_birth.loc[df_birth.births.idxmax()])
    print(df_birth.describe())

if not df_tfr.empty:
    print('tfr min, max\n', df_tfr.loc[df_tfr.tfr.idxmin()], df_tfr.loc[df_tfr.tfr.idxmax()])
    print(df_tfr.describe())

import matplotlib
matplotlib.use('Agg')
# 한글 깨짐 방지를 위해 Windows 기본 한글폰트(Malgun Gothic) 설정
import matplotlib.font_manager as fm
font_path = 'C:/Windows/Fonts/malgun.ttf'
if Path(font_path).exists():
    font_prop = fm.FontProperties(fname=font_path)
    plt_rc = {
        'font.family': font_prop.get_name(),
        'axes.unicode_minus': False,
    }
    matplotlib.rcParams.update(plt_rc)
else:
    # 대체 폰트가 없으면 한글 문제가 나올 수 있음
    matplotlib.rcParams['axes.unicode_minus'] = False

import matplotlib.pyplot as plt

if not df_birth.empty:
    plt.figure(figsize=(10,6))
    plt.plot(df_birth.year, df_birth.births, marker='o')
    plt.title('대한민국 연도별 출생아 수')
    plt.xlabel('년도')
    plt.ylabel('출생아 수')
    plt.grid(True)
    plt.tight_layout()
    p = Path('c:/work/kosis_births_by_year.png')
    plt.savefig(p, dpi=150)
    print('saved', p)

if not df_tfr.empty:
    plt.figure(figsize=(10,6))
    plt.plot(df_tfr.year, df_tfr.tfr, marker='o', color='orange')
    plt.title('대한민국 연도별 합계출산율')
    plt.xlabel('년도')
    plt.ylabel('합계출산율')
    plt.grid(True)
    plt.tight_layout()
    p2 = Path('c:/work/kosis_tfr_by_year.png')
    plt.savefig(p2, dpi=150)
    print('saved', p2)
