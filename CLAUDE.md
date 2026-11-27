# 숲속 포커 친구들 — 작업 안내

동물 테마 포커 카드 퍼즐 웹게임. 게임 목표, 규칙, 하지 않을 것은 [docs/intent/card-puzzle.md](docs/intent/card-puzzle.md)에 정리돼 있으니 작업 전에 먼저 읽는다.

## 사용자
- 한국어로 대화한다.
- 개발자가 아니고 터미널을 쓰지 않는다. 명령어를 직접 실행하라고 하지 말고, 결과는 쉬운 말로 설명한다.
- 주로 아이폰에서 플레이하고, 클라우드(claude.ai/code)에서 개발을 진행한다.

## 구조
- `index.html` — 게임 전체(HTML + CSS + JS 한 파일). 외부 라이브러리·빌드 없음.
  - `<script>` 앞부분 "게임 규칙 (순수 로직)" 구역: 족보 판정(`evalHand`), 점수(`scoreRun`), 레벨 수치(`TARGETS`, `levelMoves`, `WINGS`, `HANDS`), 힌트(`bestAction`).
  - 그 아래: 저장(localStorage 키 `forest-poker-pals-v2`), 화면(`render`), 입력 처리(`handle`), 모달·튜토리얼.
- `tools/simulate.py` — 레벨 목표 점수 보정용 시뮬레이션. 점수·보너스·이동 규칙을 바꾸면 이 파일 상수도 맞춰 바꾸고 다시 돌려서 `TARGETS`를 정한다.
- `docs/intent/` — 의도 문서.

## 규칙
- 원작(paganuko.com의 Willie Wheeler)의 이름·캐릭터·그림·화면 구성을 따라 하지 않는다. 게임 방식만 같은 장르로 유지한다.
- 저장 데이터 형식을 호환되지 않게 바꾸면 `SAVE_KEY`의 버전 숫자를 올린다.
- 375px 폭(아이폰)에서 가로 스크롤 없이 보드와 하단 버튼이 한 화면에 들어가야 한다.
- 규칙이나 수치를 바꾸면 튜토리얼(`TUTORIAL`)과 규칙 창(`showRules`) 설명도 같이 고친다. 규칙이 바뀌면 의도 문서도 갱신한다.

## 배포
- GitHub Pages가 `main` 브랜치 루트를 배포한다: https://tito-tito.github.io/forest-poker-pals/
- `main`에 반영되면 1~2분 뒤 게임 주소에 나타난다. 브랜치에서 작업했다면 PR을 만들고, 사용자가 원하면 `main`에 합친다.
