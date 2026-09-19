# NEXT SESSION — Homepage

사이트는 공개돼 있고 동작한다: <https://yjinyoo.github.io>
**먼저 `CLAUDE.md` 를 읽을 것.** 하지 말아야 할 것과 배포 확인 방법이 거기 있다.

## 상태 (2026-09-19)

| 페이지 | 상태 |
|---|---|
| about | 소개, 하는 일 3줄, 설계 루프, 활동 그래프, 연락처 |
| research | 소자 프로젝트 3건, 과제 4건(AFRL/NSF/MISTI/NRF) |
| publications | 45편, 번호·권·페이지, 공동 1저자 14편 |
| cv | 재직 3건, 학위 2건(석사부터), 수상 7건, PDF |

내부 링크 깨진 것 없음. DOI 45개 확인됨. 매일 활동 그래프 자동 갱신.

## 바로 다음 두 가지

1. **tools 페이지를 만든다.** nav 순서는 about → research → publications → **tools** → cv
   (user 가 `software` 대신 `tools` 로 확정). 각 항목은 무엇을 하는가 / 왜 만들었는가(숫자가
   있으면 그 숫자) / 저장소 링크 세 줄. 지금 올라간 셋:
   - <https://github.com/yjinyoo/beol-eo-prescreen> 전압 분배·경사 전극 쐐기장·1차 섭동
   - <https://github.com/yjinyoo/refcheck> 참고문헌 3색인 대조
   - <https://github.com/yjinyoo/harness-budget> 컨텍스트 예산·메모리 무결성·죽은 경로·recall@K
2. **about 설계 루프 문단 끝에 한 절만 붙인다.** user 확정 문구:
   `The loop is scripted end to end and run by coding agents.`
   **주장은 쓰지 않는다.** AI 역량은 tools 페이지가 증거로 보여주는 구성이고,
   about 에서 대놓고 말하지 않기로 했다. `AI-driven` 류 수식어 금지.

## 열린 것

1. **Search Console 은 2026-09-19 에 소유권 인증까지 끝났다** (HTML 파일 방식).
   남은 것: sitemap 제출과 홈 주소 색인 요청을 user 가 눌렀는지 미확인.
   `site:yjinyoo.github.io` 로 색인 여부부터 보고 판단할 것.
2. **아직 user 손으로만 되는 것:** GitHub 프로필 Website 칸, Google Scholar Homepage 칸,
   LinkedIn Contact info Website 칸. 랩 멤버 페이지(`jeehwanlab.mit.edu`) 링크가 MIT 도메인이라
   효과가 가장 크지만 관리자에게 요청해야 한다.
3. **CV 원본이 아직 틀렸다.** `Curriculum Vitae_YJYOO_081926.docx` 의 GIST 포닥 종료일이
   Feb. 2022 인데 실제는 Feb. 2023. `scripts/build_public_cv.py` 의 `CORRECTIONS` 가 매 빌드마다
   고쳐서 내보내는 중. 원본을 고치면 그 항목을 지울 것.
4. **검색 노출 확인.** 새 주소라 색인에 며칠~몇 주 걸린다. 다음 세션에서
   `site:yjinyoo.github.io` 로 색인 여부를 먼저 보고, 안 잡혔으면 1번이 됐는지 묻는다.
5. **특허 10건·국제학회 15건.** CV 에 있고 사이트에는 없다. 특허만 넣는 쪽을 권했고 답 미정.
6. **cv 페이지 MIT 항목이 research 와 중복.** user 가 알고 그대로 두기로 했다. 먼저 꺼내지 말 것.

## 하지 말 것

- `_bibliography/papers.bib` 손으로 고치기 (생성 파일)
- CV PDF 를 원본 그대로 올리기 (전화번호)
- 공개 페이지에 `co-advised by Kim and Englund` 쓰기
- about 을 줄여서 research 로 내용 옮기기 (user 가 명시적으로 반대)
- 미공개 프로젝트의 구조·수치·파트너 적기

## 다음에 논문이 나오면

```bash
python scripts/update_publications.py     # 재수집 → 동명이인 분리 → bib → DOI 검증
```

공동 1저자면 `scripts/make_bib.py` 의 `CO_FIRST` 에 DOI 를 추가한다. 서지 DB 에는 그 정보가
없어서 자동으로는 절대 안 들어온다. CV 가 정본이다.

## 공개 저장소 후속

- **내부본에 이관할 버그 3건** (공개본에서 고쳤고 내부본은 아직 옛 상태):
  `tools/refcheck_crossref.py` 의 저널명 정규식과 `guess_title`, `tools/link_lint.py` 의
  하드코딩된 폴더명. **실제 교정지로 공개본을 한 번 돌려 본 뒤** 이관할 것. 내부본은
  Science 양식에서 검증된 상태라 무턱대고 덮으면 그 경로가 깨질 수 있다.
- **다음 공개 후보:** `device_assert.py`(661줄, 프로젝트 기대값 제거 필요),
  `fab_check.py`(308줄, 엔진만 내고 `fab_constraints.md` 29항목은 예시로 대체).
- **올리지 않기로 한 것:** `leak_check.py`(패턴이 곧 협업자·프로젝트 목록),
  카이랄 두 건(원고 미발표).
