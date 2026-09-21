# NEXT SESSION — Homepage

사이트는 공개돼 있고 동작한다: <https://yjinyoo.github.io>
**먼저 `CLAUDE.md` 를 읽을 것.** 하지 말아야 할 것과 배포 확인 방법이 거기 있다.

## 상태 (2026-09-19)

| 페이지 | 상태 |
|---|---|
| about | 소개, 하는 일 3줄, 설계 루프, 활동 그래프, 연락처. 루프 문단 끝에서 tools 로 링크 |
| research | 소자 프로젝트 3건, 과제(MIT 이후, CV 와 대조됨) |
| publications | 저널 논문 + 책 챕터 절. **번호·연도·권·페이지·공동 1저자를 CV 에서 읽는다** (09-21 부터). 설명 문구 없음 |
| tools | 공개 저장소 7건. `_data/tools.yml` 에서 렌더 |
| cv | 재직·학위(09-21 B.S. 추가)·**Fellowships / Awards 분리**, PDF. 날짜·항목은 CV 와 대조됨 |

내부 링크 깨진 것 없음. 편수와 DOI 수는 여기 적지 않는다: `check_cv_match.py` 와 `check_dois.py` 가 잰다.

## 스스로 도는 것 (건드릴 필요 없음)

| 언제 | 무엇 | 파일 |
|---|---|---|
| 매일 | 활동 그래프 갱신, 바뀌면 재배포 | `.github/workflows/refresh-activity.yml` |
| 매주 월 | tools 데이터를 깃헙에서 갱신, 바뀌면 커밋 + 재배포 | `.github/workflows/site-maintenance.yml` |
| 매주 월 | 내부 링크 + DOI + 논문 목록 대 CV. **고칠 사람이 필요하므로 실패로 알린다** | 같은 파일 |
| 상시 | 방문 집계 (국가·페이지·유입 경로) | Cloudflare Web Analytics, 09-20 켬 |

주간 점검이 빨간색이면 그게 이 프로젝트의 다음 할 일이다. 먼저 어느 잡이 떨어졌는지 본다:
`tools` 잡은 스스로 낫게 돼 있어서 거기서 떨어졌다면 깃헙 API 나 권한 문제고, `checks` 잡이
떨어졌으면 링크나 DOI 가 실제로 깨졌거나, CV 와 논문 목록 중 한쪽만 다시 만든 것이다.

## 새 도구를 공개했을 때

1. `_data/tools.yml` 에 블록 하나 추가 (`repo` / `title` / `summary` / `body`)
2. `python scripts/update_tools.py` — 깃헙이 아는 필드는 스크립트가 채운다. **손으로 적지 말 것**
3. 푸시하고 배포 확인

`summary` 는 목록에 한 줄로 뜨는 절. `body` 는 두 문단: 무엇을 하는가, 그리고 **어떤 실패를
잡는가.** 두 번째가 이 페이지의 값이다.

## CV 를 고쳤으면 (새 논문·과제·수상·직위, 오타 하나라도)

**CV 가 먼저, 사이트는 따라간다.** 규칙 전체는 `CLAUDE.md` "CV 와 사이트 연동".

1. CV 원본(OneDrive `Career/CV/` docx)을 고친다. 논문이면 `Co-first author` 표시까지
2. `python scripts/sync_cv.py` — PDF 내보내기 → 공개 CV → 논문 목록 재생성 → 사이트 전체 대조
3. 대조가 실패하면 그 줄이 할 일이다. 과제·수상·직위가 새로 생겼으면 cv/research 페이지에 문구를 쓴다
   (날짜·이름은 CV 그대로). 다시 `python scripts/check_cv_match.py`
4. `git diff` 보고 커밋·푸시, 배포 확인

온라인 선공개라 권·페이지가 없으면 CV 에 `(2026)` 만 적어도 된다. 권·페이지가 나오면 CV 만 고치고 sync.
CV 를 고치고 sync 를 잊으면 Simulations 세션 시작 훅이 알린다.

## 글을 쓸 때 (2026-09-19 user 교정 셋)

1. **공개물에 특정 언어를 박지 말 것.** 문구만이 아니라 코드도. 토크나이저에 한글 음절 범위가
   박혀 있었는데, **빠진 문자는 토큰이 아예 안 만들어져서 결과에 "없음"으로도 안 나타난다.**
   구조만 남기고 언어는 쓰는 사람이 얹게 한다.
2. **읽는 사람을 안내하는 문장을 쓰지 말 것.** "이 줄은 두 번 읽을 만하다", "이건 따로 한 줄
   받을 만하다" 류. 다음 문장이 스스로 할 일을 가로챈다. 비공개 코드가 있다는 사실도 말하지 않는다.
3. **설명 없는 전문 용어 금지.** `recall@K` 를 그대로 썼다가 user 가 무슨 뜻이냐고 물었다.
   물어봤다는 게 답이다.

## 열린 것

1. **CV 원본과 공개본이 이제 같다 (09-20 해결).** docx 의 GIST 포닥 종료일을 고쳤고,
   Word COM 이 이번에는 변환에 성공해 `Curriculum Vitae_YJYOO_Sep_2026.pdf` 를 새로 뽑았다.
   `build_public_cv.py` 의 `DEFAULT_SRC` 가 그 파일을 가리키고 `CORRECTIONS` 는 **비었다.**
   다시 채우지 말 것: 보정이 필요하면 원본이 틀린 것이고 고칠 곳은 원본이다.
   ⚠ 사이트 cv 페이지에서 뺀 항목이 원본에 남아 있으면 또 갈라진다. 대외 문구를 고치면
   원본도 같이 본다.
2. **아직 user 손으로만 되는 것:** GitHub 프로필 Website 칸, Google Scholar Homepage 칸,
   LinkedIn Contact info. 랩 멤버 페이지(`jeehwanlab.mit.edu`) 링크가 MIT 도메인이라 효과가
   가장 크지만 관리자에게 요청해야 한다.
   **이 셋이 방문 집계보다 먼저다.** 분석을 켜 뒀어도 유입이 없으면 볼 것이 없고,
   셋을 걸어야 Cloudflare 에서 유입 경로가 갈려 나온다.
3. **검색 노출.** 소유권 인증과 사이트맵 제출은 끝났다. `site:yjinyoo.github.io` 로 색인 여부부터
   보고 판단할 것.
4. **특허 10건·국제학회 15건.** CV 에 있고 사이트에는 없다. 특허만 넣는 쪽을 권했고 답 미정.
5. **cv 페이지 MIT 항목이 research 와 중복.** user 가 알고 그대로 두기로 했다. 먼저 꺼내지 말 것.

## 공개 저장소

지금 일곱: `beol-eo-prescreen`, `refcheck`, `harness-budget`, `fab-check`, `device-assert`,
`resonance-extract`, `mpi-env-check`.

**후보를 목록에서 고르지 말고 폴더를 훑을 것.** 09-20 에 `resonance-extract` 가 빠져 있었는데,
인계의 후보 목록 두 개만 보고 그게 전부라고 여긴 탓이었다. `tools/` 를 직접 훑으니 둘이 더 나왔다.
남은 후보는 `gds_lint`(BLOCK 3건이 얕다: 파운드리 NDA 언급 한 줄, 내부 경로 한 줄).

**올리지 않기로 한 것.** 그림 도구 일곱 개(user 지시, `house_check` 계열 포함),
본딩 사진 → GDS 건은 **코드에서 치수를 다 빼도 작업 방식 자체가 남고 그게 미발표 프로젝트의
방법이라** 보류했다. 일반화한 판본이 `~/bondmap/bondmap.py` 에 로컬로만 있다.

**Origin MCP 는 우리 것이 아니다.** `youngminsw/Origin-Pro-MCP` (MIT, 별 39개, PyPI 등재)의
클론이고 141 커밋 중 124개가 원작자 것이다. **우리 17 커밋이 upstream 에 안 올라가 있다**
(batch 도구, 하우스 스타일, 전수 리뷰에서 나온 수정 13건). 새 저장소가 아니라 **upstream PR**
이 답이고, 한 덩어리로 낼지 쪼갤지는 따로 앉아서 볼 일이다. 홈페이지에 적기에도 그쪽이 세다.

## 내부본 이관 5건 (Simulations 세션에서)

정본 = `Simulations/harness/known_issues.md` 의 2026-09-19 절 + 그 이전 기록.

- **조건 없이 바로:** 층 두께가 샘플 간격만큼 짧게 나오는 버그(`tools/device_assert.py`),
  누출 검사기 오탐 둘(`tools/leak_check.py`)
- **조건 있음:** 참고문헌 도구 셋. 인계에 "실제 교정지로 공개본을 먼저 돌려 볼 것"이라고 돼
  있는데, 그 조건의 **의도**는 "Science 양식에서 검증된 경로를 깨지 말 것"이다. 교정지 한 건은
  어차피 한 양식이라 의도를 반만 만족시킨다. **제목을 인쇄하는 양식과 안 하는 양식으로 참고문헌을
  열 개쯤 만들어 양쪽 버전에 돌리는 쪽**이 싸고 덮는 범위가 넓다.
