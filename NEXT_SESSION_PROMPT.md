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

## 열린 것

1. **user 손으로만 되는 것** (여러 번 안내했고 완료 여부 미확인):
   GitHub 프로필 Website 칸, Google Scholar Homepage 칸, LinkedIn Contact info Website 칸,
   Google Search Console 등록 + sitemap 제출. 랩 멤버 페이지(`jeehwanlab.mit.edu`) 링크가
   MIT 도메인이라 효과가 가장 크지만 관리자에게 요청해야 한다.
2. **검색 노출 확인.** 새 주소라 색인에 며칠~몇 주 걸린다. 다음 세션에서
   `site:yjinyoo.github.io` 로 색인 여부를 먼저 보고, 안 잡혔으면 1번이 됐는지 묻는다.
3. **특허 10건·국제학회 15건.** CV 에 있고 사이트에는 없다. 특허만 넣는 쪽을 권했고 답 미정.
4. **cv 페이지 MIT 항목이 research 와 중복.** user 가 알고 그대로 두기로 했다. 먼저 꺼내지 말 것.

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
