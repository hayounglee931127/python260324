import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# 한글 폰트 설정
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['axes.unicode_minus'] = False

# 타이타닉 데이터셋 로드
print("=== 타이타닉 데이터셋 로드 ===")
titanic_df = pd.read_csv('https://raw.githubusercontent.com/pandas-dev/pandas/master/doc/data/titanic.csv')

print(f"원본 데이터 크기: {titanic_df.shape}")
print("\n원본 데이터 샘플:")
print(titanic_df.head())
print("\n데이터 타입:")
print(titanic_df.dtypes)
print("\n결측치 확인:")
print(titanic_df.isnull().sum())

# ===== 데이터 클랜징 =====
print("\n\n=== 데이터 클랜징 시작 ===")

# 1. 분석에 필요한 열 선택 (PassengerId, Survived, Sex, Age 등)
required_columns = ['PassengerId', 'Survived', 'Sex', 'Age', 'Pclass', 'Fare']
titanic_df = titanic_df[required_columns].copy()

# 2. 결측치 처리
# Age 컬럼의 결측치를 중앙값으로 채우기
age_median = titanic_df['Age'].median()
titanic_df = titanic_df.fillna({'Age': age_median})

# Fare 컬럼의 결측치를 평균값으로 채우기
fare_mean = titanic_df['Fare'].mean()
titanic_df = titanic_df.fillna({'Fare': fare_mean})

# 3. Survived와 Sex가 null인 행 제거
titanic_df = titanic_df.dropna(subset=['Survived', 'Sex'])

# 4. Survived를 정수형으로 변환
titanic_df['Survived'] = titanic_df['Survived'].astype(int)

# 5. Sex 컬럼을 영문으로 변환 (male/female)
titanic_df['Sex'] = titanic_df['Sex'].str.lower()

print(f"클랜징 후 데이터 크기: {titanic_df.shape}")
print("\n클랜징 후 결측치 확인:")
print(titanic_df.isnull().sum())
print("\n클랜징 후 데이터 샘플:")
print(titanic_df.head())

# ===== 생존율 계산 =====
print("\n\n=== 성별 생존율 계산 ===")

# 성별로 그룹화하여 생존율 계산
survival_by_gender = titanic_df.groupby('Sex')['Survived'].agg(['sum', 'count', 'mean'])
survival_by_gender.columns = ['생존자수', '총인원', '생존율']
survival_by_gender['생존율'] = survival_by_gender['생존율'] * 100

print(survival_by_gender)

# 더 자세한 통계
print("\n\n=== 성별 생존 통계 ===")
for sex in titanic_df['Sex'].unique():
    sex_data = titanic_df[titanic_df['Sex'] == sex]
    survived = sex_data[sex_data['Survived'] == 1].shape[0]
    total = sex_data.shape[0]
    survival_rate = (survived / total) * 100
    
    print(f"\n{sex.capitalize()}:")
    print(f"  - 총 인원: {total}")
    print(f"  - 생존자: {survived}")
    print(f"  - 사망자: {total - survived}")
    print(f"  - 생존율: {survival_rate:.2f}%")
    print(f"  - 평균 나이: {sex_data['Age'].mean():.2f}")

# ===== 그래프 표현 =====
print("\n\n=== 그래프 생성 ===")

# 그래프 크기 설정
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('Titanic - Gender Survival Analysis', fontsize=16, fontweight='bold')

# 1. 성별 생존율 (막대 그래프)
ax1 = axes[0, 0]
gender_survival = titanic_df.groupby('Sex')['Survived'].mean() * 100
colors = ['#FF6B9D', '#4A90E2']
bars1 = ax1.bar(gender_survival.index, gender_survival.values, color=colors, alpha=0.7, edgecolor='black')
ax1.set_ylabel('Survival Rate (%)', fontsize=11)
ax1.set_title('Survival Rate by Gender', fontsize=12, fontweight='bold')
ax1.set_ylim(0, 100)
# 막대 위에 수치 표시
for bar in bars1:
    height = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width()/2., height,
            f'{height:.1f}%', ha='center', va='bottom', fontweight='bold')

# 2. 성별 생존자 수 (스택 막대 그래프)
ax2 = axes[0, 1]
survival_counts = pd.crosstab(titanic_df['Sex'], titanic_df['Survived'])
survival_counts.plot(kind='bar', ax=ax2, color=['#E74C3C', '#27AE60'], alpha=0.7, edgecolor='black')
ax2.set_xlabel('')
ax2.set_ylabel('Count', fontsize=11)
ax2.set_title('Survival Count by Gender', fontsize=12, fontweight='bold')
ax2.set_xticklabels(ax2.get_xticklabels(), rotation=0)
ax2.legend(['Did not survive', 'Survived'], loc='upper right')

# 3. 성별 파이차트 (생존율)
ax3 = axes[1, 0]
male_survival = titanic_df[titanic_df['Sex'] == 'male']['Survived'].mean() * 100
female_survival = titanic_df[titanic_df['Sex'] == 'female']['Survived'].mean() * 100

male_data = [male_survival, 100 - male_survival]
female_data = [female_survival, 100 - female_survival]

x_pos = np.arange(2)
width = 0.35

bars_male = ax3.bar(x_pos - width/2, male_data, width, label='Male', color='#4A90E2', alpha=0.7, edgecolor='black')
bars_female = ax3.bar(x_pos + width/2, female_data, width, label='Female', color='#FF6B9D', alpha=0.7, edgecolor='black')

ax3.set_ylabel('Percentage (%)', fontsize=11)
ax3.set_title('Survival Rate Comparison', fontsize=12, fontweight='bold')
ax3.set_xticks(x_pos)
ax3.set_xticklabels(['Survived', 'Did not survive'])
ax3.legend()
ax3.set_ylim(0, 100)

# 4. 성별, 선실 등급별 생존율
ax4 = axes[1, 1]
survival_by_gender_class = titanic_df.groupby(['Sex', 'Pclass'])['Survived'].mean() * 100
survival_pivot = survival_by_gender_class.unstack()

survival_pivot.plot(kind='bar', ax=ax4, color=['#3498DB', '#E74C3C', '#F39C12'], 
                    alpha=0.7, edgecolor='black')
ax4.set_xlabel('')
ax4.set_ylabel('Survival Rate (%)', fontsize=11)
ax4.set_title('Survival Rate by Gender and Class', fontsize=12, fontweight='bold')
ax4.set_xticklabels(ax4.get_xticklabels(), rotation=0)
ax4.legend(['Class 1', 'Class 2', 'Class 3'], title='Passenger Class', loc='upper right')
ax4.set_ylim(0, 100)

plt.tight_layout()
plt.savefig('titanic_survival_analysis.png', dpi=300, bbox_inches='tight')
print("✓ 그래프가 'titanic_survival_analysis.png'로 저장되었습니다.")

plt.show()

print("\n=== 분석 완료 ===")
