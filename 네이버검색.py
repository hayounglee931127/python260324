from bs4 import BeautifulSoup
from openpyxl import Workbook


def parse_video_items(html_text):
    soup = BeautifulSoup(html_text, "html.parser")
    items = soup.select("div[data-template-id='videoItem'], div[data-template-type='rraDesk']")
    results = []

    for item in items:
        channel_a = item.select_one("span.sds-comps-profile-info-title-text a") or item.select_one("div.sds-comps-profile-info-title a")
        title_a = item.select_one("a[href*='youtube.com/watch']") or item.select_one("a.TdZKOIuRcDmFG3NkVP7U")
        summary_el = item.select_one("a[class*='cmxnIvIsEuzPw50i3V4d'] span") or item.select_one("a.cmxnIvIsEuzPw50i3V4d span")

        channel_name = channel_a.get_text(strip=True) if channel_a else None
        channel_url = channel_a.get("href") if channel_a and channel_a.has_attr("href") else None

        video_title = None
        video_url = None
        if title_a:
            video_url = title_a.get("href") if title_a.has_attr("href") else None
            video_title = title_a.get_text(strip=True)
            if not video_title:
                txt = title_a.select_one("span")
                video_title = txt.get_text(strip=True) if txt else None

        summary = summary_el.get_text(strip=True) if summary_el else None

        results.append({
            "channel_name": channel_name,
            "channel_url": channel_url,
            "video_title": video_title,
            "video_url": video_url,
            "summary": summary,
        })

    return results


def save_to_excel(results, path="naver_result.xlsx"):
    wb = Workbook()
    ws = wb.active
    ws.title = "NaverResults"

    headers = ["channel_name", "channel_url", "video_title", "video_url", "summary"]
    ws.append(headers)

    for row in results:
        ws.append([row.get(k, "") for k in headers])

    wb.save(path)
    print(f"saved to {path}")


if __name__ == "__main__":
    html_template = """
    <div class="sds-comps-vertical-layout sds-comps-full-layout fKYjNUVVyafU8otgQbWS _svp_item" data-template-id="videoItem" data-template-type="rraDesk" data-template-variant="longform">
      <div class="sds-comps-vertical-layout sds-comps-full-layout pTBMamQNGccaO5bmLJ4l">
        <a nocr="1" href="https://www.youtube.com/watch?v=g0b0YfS8D6E" class="fender-ui_228e3bd1 TdZKOIuRcDmFG3NkVP7U" target="_blank" data-heatmap-target=".glink">
          <span class="sds-comps-text sds-comps-text-ellipsis sds-comps-text-ellipsis-1 sds-comps-text-type-headline1 sds-comps-text-weight-sm">"삼성으론 부족하다"머스크, 반도체 자급자족 '테라팹' 선언｜지금 이 뉴스</span>
        </a>
        <a nocr="1" href="https://www.youtube.com/watch?v=g0b0YfS8D6E" class="fender-ui_228e3bd1 cmxnIvIsEuzPw50i3V4d" target="_blank">
          <span class="sds-comps-text sds-comps-text-ellipsis sds-comps-text-ellipsis-3 sds-comps-text-type-body1 sds-comps-text-weight-sm">일론 머스크 테슬라 CEO가 삼성전자와 TSMC 등 기존 공급망의 한계를 지적하며...</span>
        </a>
      </div>
    </div>
    """

    parsed = parse_video_items(html_template)
    print(parsed)

    save_to_excel(parsed, "naver_result.xlsx")
