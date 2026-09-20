# CLAUDE.md — Homepage (yjinyoo.github.io)

> 사람·환경·세션 프로토콜 = `~/.claude/CLAUDE.md` (정본). 여기 중복 금지.
> 이 파일 = 이 저장소에서만 참인 규칙.

**Project ID: Homepage** · 공개 주소 <https://yjinyoo.github.io> · 저장소 `yjinyoo/yjinyoo.github.io` (public)
편집 방법과 파일 위치는 `README.md`. 여기는 **세션에서 지켜야 할 것**만.

## 세션 시작

1. 이 파일 2) `NEXT_SESSION_PROMPT.md` 3) `log/` 최근 1개 4) `git log --oneline -5`
5. 대외 문구를 건드리면 **CV 를 먼저 연다** (`~/.claude/projects/.../memory/reference_cv_location_and_ownership.md`)

## 절대 하지 말 것

- **`_bibliography/papers.bib` 손으로 고치지 않기.** 생성 파일이다. `scripts/update_publications.py` 로 다시 만들고, 예외는 스크립트 안의 `CO_FIRST` / `ADDITIONS` / `OVERRIDES` / `YEAR_OVERRIDE` 에 넣는다. 손으로 고치면 다음 갱신에 사라진다.
- **CV PDF 를 원본 그대로 올리지 않기.** 전화번호가 들어 있다. `scripts/build_public_cv.py` 가 지우고, 저장한 파일을 다시 읽어 남아 있으면 출력을 삭제하고 실패한다.
- **`co-advised by Kim and Englund` 를 공개 페이지에 쓰지 않기.** CV 에는 그렇게 적혀 있으나 공개물에서는 Kim 이 먼저·단독, Englund 는 범위를 한정해서 (`on the CMOS integrated photonics work`). 근거 = memory `user_joint_kim_englund_appointment`.
- **미공개 프로젝트의 소자 구조·수치·파트너를 적지 않기.** NDA 건, 투고 중 원고, 프로그램 상세가 섞여 있다. 안전선은 이미 공개된 GitHub 프로필 수준.
- **`google2cef4b219e13a627.html` 를 지우지 않기.** 쓰레기 파일처럼 보이지만 Google Search Console
  소유권 인증 파일이다. 지우면 인증이 풀리고 색인 상태 보고가 끊긴다. 테마가 `google_site_verification`
  설정 키를 렌더하지 않아서 메타 태그 방식이 안 되고, 이 파일 방식으로 인증돼 있다 (2026-09-19).
- **공식 과제 제목을 줄이지 않기.** 2026-09-19 에 MISTI 제목을 줄였다가 하필 `advanced quantum photonic integrated circuits` 를 잘랐다. 정본은 최종 보고서.

## 배포와 확인

푸시하면 `Deploy site` 워크플로가 빌드해서 `gh-pages` 브랜치에 올린다. Pages 소스는 그 브랜치다(`main` 아님).

```bash
SHA=$(git rev-parse HEAD)
until [ "$(gh run list --workflow='Deploy site' --limit 8 --json headSha,status \
  --jq "[.[] | select(.headSha==\"$SHA\")][0].status")" = "completed" ]; do sleep 15; done
gh run list --workflow='Deploy site' --limit 8 --json headSha,conclusion \
  --jq "[.[] | select(.headSha==\"$SHA\")][0]"
```

- **커밋 해시로 골라서 기다릴 것.** `--limit 1` 은 푸시 직후 직전 run 을 돌려줘서, 남의 빌드를 내 빌드로 착각한다.
- **`gh run watch` 의 종료 코드를 믿지 말 것.** 실패한 run 에도 0 을 준다. `conclusion` 을 읽는다.
- 배포 후 `python scripts/check_links.py` (내부 링크 전수), 논문을 건드렸으면 `python scripts/check_dois.py`.
- 화면이 안 바뀌어 보이면 캐시다. `?cb=$(date +%s)` 를 붙여 받아 보고 판단한다.

## 테마 CSS 를 이길 때

테마는 gem 안에 있어 고칠 수 없다. `_includes/site_styles.liquid` 가 각 페이지에서 덧씌운다.
**`!important` 만으로는 못 이긴다.** 테마도 `!important` 를 쓰는 자리가 있고, 그러면 명시도로 결판난다.
번호 뱃지가 두 번이나 흰색으로 남은 원인이 이것이다(테마 `.publications ol.bibliography li .abbr abbr` 가
글자색을 카드 배경색으로 박아 둔다). 실제 규칙을 먼저 읽고 선택자를 맞춘다:

```bash
curl -s https://yjinyoo.github.io/assets/css/main.css | grep -oE "<선택자 조각>[^{]*\{[^}]*\}"
```

## 생성물 네 가지

| 무엇 | 스크립트 | 언제 |
|---|---|---|
| 논문 목록 | `scripts/update_publications.py` | 새 논문이 나오면 |
| 활동 그래프 | `scripts/build_activity_svg.py` | 매일 자동(`refresh-activity.yml`), 수동 실행도 가능 |
| tools 페이지 데이터 | `scripts/update_tools.py` | 매주 자동(`site-maintenance.yml`), 새 도구를 올리면 수동 |
| CV PDF · 링크 카드 | `scripts/build_public_cv.py`, `scripts/build_og_image.py` | CV 나 소개 문구가 바뀌면 |

`_data/tools.yml` 에서 **깃헙이 아는 필드(`description`/`language`/`pushed`)는 손으로 고치지
않는다.** 스크립트가 덮어쓴다. 손으로 쓰는 것은 `title`/`summary`/`body` 뿐이다.

주간 점검(`site-maintenance.yml`)은 두 잡이고 성격이 다르다. `tools` 는 스스로 낫고(갱신 →
커밋 → 재배포), `checks`(내부 링크 + DOI)는 사람이 고쳐야 하므로 **실패로 알린다.**

활동 그래프는 GitHub 프로필의 **공개** 기여만 읽는다. 프로필 설정의 `Private contributions` 가 꺼지면
거의 빈 그래프가 나오는데, 그건 버그가 아니라 공개 프로필의 사실이다.

## 페이지 역할 (2026-09-19 user 확정)

- **about** = 첫 화면에서 임팩트. 내용을 research 로 미루지 않는다. 대부분 여기까지만 읽는다.
- **research** = 같은 주제를 더 깊게. about 과 **길이가 아니라 깊이로** 갈린다 (예: Landau-Devonshire 는 research 에만).
- **publications** = 45편, 번호는 오래된 것이 1번.
- **cv** = 기록 + PDF. MIT 항목이 research 와 겹치는 상태를 user 가 알고 그대로 두기로 했다.

## 알려진 함정

- **Word COM 이 멈춘다.** docx→PDF 를 두 번 시도해 둘 다 문서 여는 데서 무응답. PyMuPDF 로 기존 PDF 를 직접 다룬다.
- **저널 권·페이지는 `journal` 문자열에 싣는다.** 레이아웃이 volume/pages 필드를 렌더하지 않고, 그 사이의 `additional_info` 는 markdownify 를 거쳐 앞 공백이 사라지고 뒤에 줄바꿈이 붙는다.
- **공저자에 링크를 걸지 않는다.** 테마가 강조색으로 칠해서 내 논문 목록에서 교신저자가 제일 눈에 띄게 된다.
- **OpenAlex 는 동명이인 7명을 한 저자 레코드에 합쳐 놨다.** 공저자망 + MIT 소속으로 가른다. 새 협업이 생기면 공저자가 안 겹쳐서 떨어질 수 있으니 `curate.py` 의 탈락 목록을 확인한다.
