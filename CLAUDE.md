# CLAUDE.md — Homepage (yjinyoo.github.io)

> 사람·환경·세션 프로토콜 = `~/.claude/CLAUDE.md` (정본). 여기 중복 금지.
> 이 파일 = 이 저장소에서만 참인 규칙.

**Project ID: Homepage** · 공개 주소 <https://yjinyoo.github.io> · 저장소 `yjinyoo/yjinyoo.github.io` (public)
편집 방법과 파일 위치는 `README.md`. 여기는 **세션에서 지켜야 할 것**만.

## 세션 시작

1. 이 파일 2) `NEXT_SESSION_PROMPT.md` 3) `log/` 최근 1개 4) `git log --oneline -5`
5. 대외 문구를 건드리면 **CV 를 먼저 연다** (`~/.claude/projects/.../memory/reference_cv_location_and_ownership.md`)

## CV 와 사이트 연동 (2026-09-21)

**CV 가 정본, 사이트는 따라간다.** 흐름은 한 방향: CV(OneDrive `Career/CV/` docx) 수정 → `python scripts/sync_cv.py`
→ `git diff` 확인 → 커밋·푸시. sync 는 docx→PDF(Word) → 공개 CV → 논문 목록 재생성 → 전체 대조까지 하고,
어느 docx 를 반영했는지 `scripts/cv_source.json` 에 남긴다. 커밋은 안 한다.

| 사이트 | CV 에서 오는 방식 | 대조 |
|---|---|---|
| publications | **생성**: 번호·연도·권·페이지·공동 1저자를 `cv_record.py` 가 공개 CV PDF 에서 읽음 | `make_bib.py` 가 1:1 아니면 안 씀 |
| cv 페이지 (재직·학위·펠로십·수상) | 손으로 쓴 문구. **날짜·이름·항목 수는 CV 와 같아야** | `check_cv_match.py` |
| research 페이지 Funded projects | 손으로 쓴 문구. MIT 이후(`SITE_PROJECTS_FROM`) 과제 전부, 날짜 일치 | `check_cv_match.py` |

- 사이트에 항목을 **먼저** 넣지 말 것. CV 에 없으면 대조가 실패한다 (09-21: MISTI 과제가 사이트에만 있었다).
- CV 와 일부러 다르게 둔 것은 `cv_record.py` 머리의 `SITE_YEAR` / `SITE_PROJECTS_FROM` / `SITE_EDUCATION_FROM` 세 곳뿐. 늘리려면 거기에 이유와 함께.
- **대조가 "CV 에 있는데 사이트에 없다" 고 하면 사이트에 넣기 전에 user 에게 묻는다.** 빠진 것이 의도일 수 있다. 09-21 오전 세션이 검사를 통과시키려고 B.S. 를 묻지 않고 cv 페이지에 넣었고 user 가 "누가 넣으라고 했어" 로 되돌렸다. 공개 페이지는 대학원 학위만 (`SITE_EDUCATION_FROM`).
- 대조가 도는 곳: sync 끝, `update_publications.py` 끝, `build_public_cv.py` 끝, 주간 `Site maintenance`.
  **CV 를 고치고 sync 를 안 하면** Simulations 세션 시작 훅이 "CV changed after the homepage was synced" 를 띄운다.
- Word 가 멈추면 sync 가 150 초에 끊고 수동 절차(Word 에서 PDF 저장 → 두 스크립트)를 출력한다.

## 절대 하지 말 것

- **`_bibliography/papers.bib` 손으로 고치지 않기.** 생성 파일이다(위 표). 예외는 `make_bib.py` 의 `ADDITIONS`(OpenAlex 에 없음) / `OVERRIDES`(OpenAlex 가 낡음). 2026-09-21 까지는 번호·연도를 OpenAlex 에서 가져와 사이트 45 대 CV 42 로 어긋나 있었다.
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
| 논문 목록 + 공개 CV | `scripts/sync_cv.py` (안에서 `build_public_cv.py` → `update_publications.py`) | CV 를 고쳤으면 언제나 |
| 활동 그래프 (좌: Project activity, 우: Simulation runs) | `scripts/build_activity_svg.py` → `assets/img/activity.svg` + `simulations.svg` (그리기는 `scripts/calendar_svg.py`) | 매일 자동(`refresh-activity.yml`) + **세션 정리 9단계** |
| tools 페이지 데이터 | `scripts/update_tools.py` | 매주 자동(`site-maintenance.yml`), 새 도구를 올리면 수동 |
| 링크 카드 | `scripts/build_og_image.py` | 소개 문구가 바뀌면 |

**활동 그래프는 두 장이고 출처와 갱신 경로가 다르다.** 왼쪽(초록)은 공개 GitHub 프로필의 기여 수를 매일 Actions 가 읽는다.
오른쪽(파랑)은 `_data/simulation_runs.json` 에서 그리는데, 이 파일은 워크스테이션에서만 만들어진다
(`Simulations/tools/simulation_run_counter.py`; 클라우드 솔버 계정·로컬 아카이브 드라이브·클러스터 접속이 필요).
세션 정리 때 `Simulations/tools/publish_simulation_runs.py` 가 다시 세서 **데이터 파일과 SVG 두 장만** push 한다.
- 두 장은 **같은 주 범위**를 쓰고, 폭은 카드 절반(416 px)으로 고정, 칸 크기가 주 수를 따라 줄어든다(9 월 ≈ 11 px, 12 월 ≈ 7.5 px). 그래서 한쪽만 다시 그리면 좌우가 어긋난다. 둘 다 같이 커밋할 것.
- 범위는 **GitHub 기록이 시작된 달부터** (2026 은 3 월). 시뮬레이션이 더 일찍 시작해도 그쪽에 맞추지 않는다 (user 09-21). 각 장의 숫자는 한 해 전체라 1~2 월 실행 2,216 건은 숫자에만 있고 그림에는 없다. 원래 GitHub 달력도 "그림은 첫 활동 달부터, 숫자는 한 해 전체" 였다.
- 시뮬레이션 쪽은 센 날까지만 그린다. 그 뒤를 빈칸으로 그리면 "안 돌렸다"는 주장이 된다.
- 시뮬레이션 수는 **끝난 실행만** 센다 (클라우드 `success`, 클러스터 COMPLETED 중 60 초 이상·`_` 이름 제외).
- 솔버 대시보드 숫자(09-21 에 13,733)를 쓰지 말 것: 견적만 내고 안 돌린 초안이 들어 있다. 서버 용량 때문에 지운 실행의 기록이 어디 남는지는 카운터 머리 주석.
- **이름·문구 (user 09-21 확정):** 왼쪽 이름은 `Project activity`, 숫자 옆에 `GitHub contributions` 로 출처를 밝힌다. 올해 커밋의 약 45 % 가 하네스 저장소라 캡션에 `the shared tooling behind them` 을 넣어 둔 것이다. 빼면 "Project" 가 부풀린 말이 된다. `Code`(측정·성장 기록까지 들어 있어 좁다)·`Commits`(user 가 뜻을 물었다)는 기각. 공개 페이지에 솔버 제품명·클러스터 이름·"cloud FDTD" 같은 직접 표현 금지. 종류는 **예시로("including ...") 쓰고 몇 개로 단정하지 않는다** (user 09-21: 셋으로 못 박으면 다양성이 없어 보인다). 단 예시에는 실제로 센 것만: FDTD, mode analysis, inverse design(adjoint FDTD 실행), DFT. 로컬 실행 제외는 밝힌다. 캡션은 **2~3 문장, 좌우 줄 수를 실제 사이트 CSS 로 렌더해서 맞춘다** (user 09-21. 자체 목업은 글꼴이 달라 한 줄씩 어긋났다). 날짜별 개수 파일로 가는 링크는 뺐다: 방문자에게 새 정보가 없고 공개 저장소의 내부 문서로 데려간다. 시뮬레이션 숫자의 출처를 "GitHub 기록" 이라고 쓰지 않는다: 출처는 작업 기록이고 GitHub 에는 날짜별 개수 파일이 올라갈 뿐이다.

`_data/tools.yml` 에서 **깃헙이 아는 필드(`description`/`language`/`pushed`)는 손으로 고치지
않는다.** 스크립트가 덮어쓴다. 손으로 쓰는 것은 `title`/`summary`/`body` 뿐이다.

주간 점검(`site-maintenance.yml`)은 두 잡이고 성격이 다르다. `tools` 는 스스로 낫고(갱신 →
커밋 → 재배포), `checks`(내부 링크 + DOI + 사이트 대 CV)는 사람이 고쳐야 하므로 **실패로 알린다.**

활동 그래프 왼쪽은 GitHub 프로필의 **공개** 기여만 읽는다. 프로필 설정의 `Private contributions` 가 꺼지면
거의 빈 그래프가 나오는데, 그건 버그가 아니라 공개 프로필의 사실이다.

## 페이지 역할 (2026-09-19 user 확정)

- **about** = 첫 화면에서 임팩트. 내용을 research 로 미루지 않는다. 대부분 여기까지만 읽는다.
- **research** = 같은 주제를 더 깊게. about 과 **길이가 아니라 깊이로** 갈린다 (예: Landau-Devonshire 는 research 에만).
- **publications** = 저널 논문 + 그 아래 책 챕터 절. 번호는 **CV 번호 그대로**(오래된 것이 1번). 편수는 여기 적지 않는다(`check_cv_match.py` 가 잰다).
- **cv** = 기록 + PDF. MIT 항목이 research 와 겹치는 상태를 user 가 알고 그대로 두기로 했다.

## 알려진 함정

- **Word COM 이 멈출 때가 있다.** 09-19 에 두 번 무응답, 09-20·09-21 은 성공. 09-21 에 된 방식: OneDrive 밖(스크래치)으로 docx 를 복사해서 `Documents.Open(src, False, True, False)` 읽기 전용으로 열고 `ExportAsFixedFormat(out, 17)`, 전체를 `Start-Job` + `Wait-Job -Timeout 150` 으로 감싸 멈추면 끊는다. 사용자가 Word 로 다른 문서를 열어 둔 상태에서도 됐다.
- **저널 권·페이지는 `journal` 문자열에 싣는다.** 레이아웃이 volume/pages 필드를 렌더하지 않고, 그 사이의 `additional_info` 는 markdownify 를 거쳐 앞 공백이 사라지고 뒤에 줄바꿈이 붙는다.
- **공저자에 링크를 걸지 않는다.** 테마가 강조색으로 칠해서 내 논문 목록에서 교신저자가 제일 눈에 띄게 된다.
- **OpenAlex 는 동명이인 7명을 한 저자 레코드에 합쳐 놨다.** 공저자망 + MIT 소속으로 가른다. 새 협업이 생기면 공저자가 안 겹쳐서 떨어질 수 있으니 `curate.py` 의 탈락 목록을 확인한다.
