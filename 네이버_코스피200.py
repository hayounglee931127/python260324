import requests
from bs4 import BeautifulSoup
import time
import csv

def scrape_kospi200_constituents():
    """코스피200 편입종목 전체 크롤링"""
    
    base_url = "https://finance.naver.com/sise/entryJongmok.naver?type=KPI200"
    
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/124.0.0.0 Safari/537.36"
        )
    }
    
    all_items = []
    
    # 코스피200은 총 200개 종목, 페이지당 10개씩 표시되므로 20페이지
    total_pages = 20
    
    for page in range(1, total_pages + 1):
        url = f"{base_url}&page={page}"
        print(f"페이지 {page}/{total_pages} 크롤링 중...")
        
        try:
            resp = requests.get(url, headers=headers, timeout=10)
            resp.raise_for_status()
            
            soup = BeautifulSoup(resp.text, "html.parser")
            
            # 편입종목 테이블 찾기
            table = soup.select_one("table.type_1")
            if not table:
                print(f"  ⚠ 페이지 {page}: 테이블을 찾을 수 없습니다.")
                continue
            
            rows = table.select("tr")
            
            page_items = []
            for row in rows:
                cols = [td.get_text(strip=True) for td in row.select("td")]
                # 헤더 행 제외 (종목별, 현재가 등이 있는 행)
                if cols and len(cols) >= 7 and "종목별" not in cols[0]:
                    # 종목명, 현재가, 전일비, 등락률, 거래량, 거래대금, 시가총액
                    if len(cols) >= 7:
                        item = {
                            "종목명": cols[0],
                            "현재가": cols[1],
                            "전일비": cols[2],
                            "등락률": cols[3],
                            "거래량": cols[4],
                            "거래대금": cols[5],
                            "시가총액": cols[6]
                        }
                        page_items.append(item)
            
            all_items.extend(page_items)
            print(f"  ✓ {len(page_items)}개 종목 추가 (총 {len(all_items)}개)")
            
            time.sleep(0.5)  # 서버 부하 방지
            
        except Exception as e:
            print(f"  ✗ 오류: {e}")
            break
    
    return all_items

if __name__ == "__main__":
    print("코스피200 편입종목 전체 데이터 크롤링")
    print("=" * 50)
    
    items = scrape_kospi200_constituents()
    
    print(f"\n총 수집된 종목 수: {len(items)}")
    
    print("\n처음 10개 데이터:")
    for i, item in enumerate(items[:10], 1):
        print(f"{i}. {item['종목명']} - {item['현재가']} ({item['등락률']})")
    
    # CSV 저장
    try:
        with open("kospi200_all.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["종목명", "현재가", "전일비", "등락률", "거래량", "거래대금", "시가총액"])
            writer.writeheader()
            writer.writerows(items)
        print(f"\n✓ CSV 파일로 저장되었습니다: kospi200_all.csv")
    except Exception as e:
        print(f"CSV 저장 실패: {e}")
    
    # pandas DataFrame (선택)
    try:
        import pandas as pd
        df = pd.DataFrame(items)
        print(f"DataFrame shape: {df.shape}")
        print("\nDataFrame 미리보기:")
        print(df.head())
    except ImportError:
        print("pandas가 설치되지 않아 DataFrame을 생성할 수 없습니다.")