"""레벨 목표 점수 보정용 자동 플레이 시뮬레이션.

index.html의 족보 점수(HANDS), 날개 보너스/해금(WINGS), 이동 횟수(levelMoves)를 바꾸면
여기 상수도 같이 바꾼 뒤 실행해서 TARGETS를 다시 정한다.
실행: python tools/simulate.py  (레벨별 탐욕 플레이 점수의 30/50/70% 분위 출력)
탐욕 AI는 사람보다 약간 약하므로 목표는 대략 p30~p50 근처로 잡는다.
"""
import random
from collections import Counter

BASE = dict(pair=10, twopair=20, trips=30, straight=40, flush=45, full=60, quads=100, sf=150)
BONUS = {'W': 1, 'E': 1, 'N': 4, 'S': 9}
UNLOCK = {'W': 1, 'E': 1, 'N': 5, 'S': 10}

def pts(r): return 11 if r == 14 else (10 if r >= 11 else r)

def ev(cards):
    rs = [c[0] for c in cards]; ss = [c[1] for c in cards]
    cnt = Counter(rs); u = sorted(cnt)
    fl = len(set(ss)) == 1
    st = len(u) == 5 and (u[4] - u[0] == 4 or u == [2, 3, 4, 5, 14])
    allp = sum(pts(r) for r in rs)
    v = sorted(cnt.values(), reverse=True)
    rw = lambda n: [k for k in cnt if cnt[k] == n]
    if st and fl: return BASE['sf'] + allp
    if v[0] == 4: return BASE['quads'] + 4 * pts(rw(4)[0])
    if v[0] == 3 and v[1] == 2: return BASE['full'] + allp
    if fl: return BASE['flush'] + allp
    if st: return BASE['straight'] + allp
    if v[0] == 3: return BASE['trips'] + 3 * pts(rw(3)[0])
    if v[0] == 2 and v[1] == 2: return BASE['twopair'] + sum(2 * pts(k) for k in rw(2))
    if v[0] == 2: return BASE['pair'] + 2 * pts(rw(2)[0])
    return 0

def total(board, hubs):
    s = 0; n = 0
    for w, cs in board.items():
        x = ev(cs + [hubs[w]])
        if x: s += x * BONUS[w]; n += 1
    return s * max(n, 1)

def wings(L): return [w for w in 'WENS' if L >= UNLOCK[w]]
def moves(L): return min(12, 6 + (L - 1) // 3)

def play(L):
    deck = [(r, s) for r in range(2, 15) for s in range(4)]; random.shuffle(deck)
    ws = wings(L)
    board = {w: [deck.pop() for _ in range(4)] for w in ws}
    hubs = {w: deck.pop() for w in ws}
    pocket = []
    m = moves(L)
    while m > 0:
        cur = total(board, hubs)
        best = (cur, None)
        slots = [(w, i) for w in ws for i in range(4)]
        for a in range(len(slots)):
            for b in range(a + 1, len(slots)):
                (w1, i1), (w2, i2) = slots[a], slots[b]
                if w1 == w2: continue
                board[w1][i1], board[w2][i2] = board[w2][i2], board[w1][i1]
                t = total(board, hubs)
                board[w1][i1], board[w2][i2] = board[w2][i2], board[w1][i1]
                if t > best[0]: best = (t, ('s', slots[a], slots[b]))
        for pi, pc in enumerate(pocket):
            for (w, i) in slots:
                old = board[w][i]; board[w][i] = pc
                t = total(board, hubs); board[w][i] = old
                if t > best[0]: best = (t, ('p', pi, (w, i)))
        m -= 1
        if best[1]:
            if best[1][0] == 's':
                (w1, i1), (w2, i2) = best[1][1], best[1][2]
                board[w1][i1], board[w2][i2] = board[w2][i2], board[w1][i1]
            else:
                pi, (w, i) = best[1][1], best[1][2]
                pocket[pi], board[w][i] = board[w][i], pocket[pi]
            continue
        c = deck.pop()
        bp = (cur, None)
        for (w, i) in slots:
            old = board[w][i]; board[w][i] = c
            t = total(board, hubs); board[w][i] = old
            if t > bp[0]: bp = (t, (w, i))
        if bp[1]:
            w, i = bp[1]; old = board[w][i]; board[w][i] = c
            if len(pocket) < 2: pocket.append(old)
        elif len(pocket) < 2:
            pocket.append(c)
    return total(board, hubs)

random.seed(2)
for L in range(1, 16):
    xs = sorted(play(L) for _ in range(400))
    q = lambda p: xs[int(p * len(xs))]
    print(L, moves(L), 'p30', q(.3), 'p50', q(.5), 'p70', q(.7))
