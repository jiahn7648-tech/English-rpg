import streamlit as st
import random
import time

# ─────────────────────────────────────────────────────────
#  페이지 설정
# ─────────────────────────────────────────────────────────
st.set_page_config(
    page_title="단어 용사 어드벤처",
    page_icon="⚔️",
    layout="centered",
)

# ─────────────────────────────────────────────────────────
#  CSS
# ─────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;700;900&family=Noto+Sans+KR:wght@300;400;500;700&display=swap');

/* ── 루트 변수 */
:root {
    --bg-deep:     #06050f;
    --bg-card:     #0d0b1e;
    --bg-card2:    #120f28;
    --border:      #2a2060;
    --border-glow: #6644cc;
    --accent:      #a78bfa;
    --accent2:     #e94560;
    --gold:        #f0c060;
    --text:        #ddd8f0;
    --text-muted:  #7870a0;
    --green:       #34d399;
    --red:         #f87171;
    --blue:        #60a5fa;
}

html, body, [class*="css"] {
    font-family: 'Noto Sans KR', sans-serif;
    background: var(--bg-deep) !important;
    color: var(--text);
}

/* 별 배경 */
body::before {
    content: '';
    position: fixed;
    inset: 0;
    background:
        radial-gradient(ellipse at 20% 20%, rgba(100,60,200,0.18) 0%, transparent 50%),
        radial-gradient(ellipse at 80% 80%, rgba(233,69,96,0.12) 0%, transparent 50%),
        radial-gradient(ellipse at 50% 50%, rgba(6,5,15,0) 0%, #06050f 100%);
    pointer-events: none;
    z-index: 0;
}

/* 떠다니는 파티클 */
@keyframes float1 { 0%,100%{transform:translateY(0) translateX(0);opacity:.6} 50%{transform:translateY(-30px) translateX(15px);opacity:1} }
@keyframes float2 { 0%,100%{transform:translateY(0) translateX(0);opacity:.4} 50%{transform:translateY(20px) translateX(-20px);opacity:.8} }
@keyframes float3 { 0%,100%{transform:translateY(0);opacity:.3} 50%{transform:translateY(-20px);opacity:.7} }

.stApp { background: transparent !important; }
section.main > div { padding-top: 1rem; }

/* ── 메인 타이틀 */
.title-wrap {
    text-align: center;
    padding: 2rem 0 1rem;
    position: relative;
}
.title-main {
    font-family: 'Cinzel', serif;
    font-size: clamp(1.8rem, 5vw, 3rem);
    font-weight: 900;
    background: linear-gradient(135deg, #f0c060, #a78bfa, #e94560);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    letter-spacing: 0.05em;
    text-shadow: none;
    margin: 0;
    line-height: 1.2;
}
.title-sub {
    font-size: 13px;
    color: var(--text-muted);
    letter-spacing: 0.2em;
    text-transform: uppercase;
    margin-top: 6px;
}
.title-divider {
    width: 120px;
    height: 2px;
    background: linear-gradient(90deg, transparent, var(--accent), transparent);
    margin: 12px auto;
}

/* ── 카드 */
.game-card {
    background: linear-gradient(135deg, var(--bg-card) 0%, var(--bg-card2) 100%);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 1.5rem 2rem;
    margin-bottom: 1rem;
    position: relative;
    overflow: hidden;
}
.game-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--accent), transparent);
}
.game-card h2 {
    font-family: 'Cinzel', serif;
    color: var(--gold);
    margin-top: 0;
    font-size: 1.3rem;
}
.game-card p { color: var(--text); margin: 6px 0; }

/* ── 장소 헤더 */
.location-header {
    background: linear-gradient(135deg, rgba(20,15,50,0.9), rgba(30,20,60,0.9));
    border: 1px solid var(--border-glow);
    border-radius: 12px;
    padding: 1rem 1.5rem;
    margin-bottom: 1.2rem;
    text-align: center;
    position: relative;
    box-shadow: 0 0 30px rgba(102,68,204,0.2);
}
.location-header .loc-emoji { font-size: 2.5rem; display: block; margin-bottom: 4px; }
.location-header .loc-name {
    font-family: 'Cinzel', serif;
    font-size: 1.1rem;
    color: var(--gold);
    letter-spacing: 0.1em;
}
.location-header .loc-desc { font-size: 13px; color: var(--text-muted); margin-top: 4px; }

/* ── 말풍선 */
.bubble-wrap { display: flex; gap: 12px; margin: 10px 0; align-items: flex-start; }
.bubble-avatar {
    width: 44px; height: 44px;
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.3rem;
    flex-shrink: 0;
    border: 2px solid var(--border-glow);
    background: var(--bg-card2);
}
.bubble-content { flex: 1; }
.bubble-name { font-size: 11px; color: var(--text-muted); margin-bottom: 4px; font-weight: 500; }
.bubble-text {
    background: var(--bg-card2);
    border: 1px solid var(--border);
    border-radius: 4px 14px 14px 14px;
    padding: 10px 14px;
    font-size: 14px;
    color: var(--text);
    line-height: 1.7;
    position: relative;
}
.bubble-text.villain {
    border-color: rgba(233,69,96,0.5);
    background: rgba(233,69,96,0.05);
}
.bubble-text.system {
    border-color: rgba(240,192,96,0.4);
    background: rgba(240,192,96,0.04);
    color: var(--gold);
    border-radius: 14px;
    text-align: center;
    font-style: italic;
}
.bubble-wrap.right { flex-direction: row-reverse; }
.bubble-wrap.right .bubble-text {
    border-radius: 14px 4px 14px 14px;
}

/* ── HP 바 */
.hp-section { margin: 8px 0 16px; }
.hp-row { display:flex; align-items:center; gap:10px; margin:6px 0; }
.hp-icon { font-size:1.1rem; }
.hp-info { flex:1; }
.hp-label-row { display:flex; justify-content:space-between; font-size:12px; margin-bottom:4px; }
.hp-name { color: var(--text); font-weight:500; }
.hp-num { color: var(--text-muted); font-family: monospace; }
.hp-bar-bg { background:#1a1535; border-radius:8px; height:14px; overflow:hidden; border:1px solid var(--border); }
.hp-fill-player  { background: linear-gradient(90deg,#3b82f6,#34d399); height:100%; border-radius:8px; transition:width .5s cubic-bezier(.4,0,.2,1); }
.hp-fill-villain { background: linear-gradient(90deg,#e94560,#f59e0b); height:100%; border-radius:8px; transition:width .5s cubic-bezier(.4,0,.2,1); }

/* ── 배지 */
.badge {
    display: inline-block;
    padding: 3px 11px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 500;
    margin: 2px 3px 2px 0;
}
.badge-item   { background:rgba(167,139,250,0.12); color:#a78bfa; border:1px solid rgba(167,139,250,0.4); }
.badge-word   { background:rgba(244,114,182,0.12); color:#f472b6; border:1px solid rgba(244,114,182,0.4); }
.badge-gold   { background:rgba(240,192,96,0.12);  color:#f0c060; border:1px solid rgba(240,192,96,0.4); }
.badge-green  { background:rgba(52,211,153,0.12);  color:#34d399; border:1px solid rgba(52,211,153,0.4); }

/* ── 전투 로그 */
.log-box {
    background: rgba(6,5,15,0.8);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 1rem 1.2rem;
    max-height: 220px;
    overflow-y: auto;
    font-size: 13px;
    line-height: 2;
    color: var(--text-muted);
    scrollbar-width: thin;
    scrollbar-color: var(--border) transparent;
}
.log-box p { margin: 0; }
.log-atk  { color: var(--blue); }
.log-dmg  { color: var(--red); }
.log-heal { color: var(--green); }
.log-item { color: var(--accent); }
.log-sys  { color: var(--gold); }
.log-win  { color: var(--green); font-weight:700; font-size:15px; }
.log-lose { color: var(--red);   font-weight:700; font-size:15px; }

/* ── 단어장 테이블 */
.word-table { width:100%; border-collapse:collapse; font-size:13px; }
.word-table th { background: rgba(102,68,204,0.2); color:var(--accent); padding:8px 12px; text-align:left; border-bottom:1px solid var(--border); font-weight:500; }
.word-table td { padding:8px 12px; border-bottom:1px solid rgba(42,32,96,0.5); color:var(--text); }
.word-table tr:hover td { background:rgba(102,68,204,0.06); }
.word-table .eng { color:#f472b6; font-weight:500; }
.word-table .kor { color:var(--text-muted); }

/* ── 경고 박스 */
.warn-box {
    background: rgba(248,113,113,0.08);
    border: 1px solid rgba(248,113,113,0.3);
    border-radius: 8px;
    padding: 0.7rem 1rem;
    color: #fca5a5;
    font-size: 13px;
    margin-bottom: 0.8rem;
}
.info-box {
    background: rgba(167,139,250,0.08);
    border: 1px solid rgba(167,139,250,0.3);
    border-radius: 8px;
    padding: 0.7rem 1rem;
    color: var(--accent);
    font-size: 13px;
    margin-bottom: 0.8rem;
}

/* ── 섹션 타이틀 */
.sec-title {
    font-size: 15px;
    font-weight: 700;
    color: var(--accent);
    margin: 1.5rem 0 0.6rem;
    display: flex;
    align-items: center;
    gap: 8px;
}
.sec-title::after {
    content:'';
    flex:1;
    height:1px;
    background: linear-gradient(90deg, var(--border), transparent);
}

/* ── 진행 바 오버라이드 */
div.stProgress > div > div > div {
    background: linear-gradient(90deg, var(--accent), var(--accent2)) !important;
}

/* ── 버튼 */
div.stButton > button {
    border-radius: 10px !important;
    font-family: 'Noto Sans KR', sans-serif !important;
    font-weight: 500 !important;
    background: rgba(30,25,60,0.8) !important;
    border: 1px solid var(--border) !important;
    color: var(--text) !important;
    transition: all .2s !important;
}
div.stButton > button:hover {
    border-color: var(--accent) !important;
    color: var(--accent) !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 4px 20px rgba(167,139,250,0.2) !important;
}
div.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, rgba(102,68,204,0.6), rgba(167,139,250,0.3)) !important;
    border-color: var(--accent) !important;
    color: #fff !important;
}
div.stButton > button[kind="primary"]:hover {
    box-shadow: 0 4px 25px rgba(167,139,250,0.4) !important;
}

/* ── 텍스트 인풋 */
div.stTextInput > div > div > input {
    background: var(--bg-card2) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    color: var(--text) !important;
    font-family: 'Noto Sans KR', sans-serif !important;
}
div.stTextInput > div > div > input:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 1px var(--accent) !important;
}
div.stTextInput > label { color: var(--text-muted) !important; font-size: 13px !important; }

/* ── divider */
hr { border-color: var(--border) !important; opacity:0.5; }

/* ── form */
div[data-testid="stForm"] {
    background: rgba(13,11,30,0.4);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1.2rem;
}

/* ── 엔딩 배너 */
.ending-win {
    background: linear-gradient(135deg, rgba(52,211,153,0.1), rgba(96,165,250,0.1));
    border: 1px solid rgba(52,211,153,0.4);
    border-radius: 16px;
    padding: 2rem;
    text-align: center;
}
.ending-lose {
    background: linear-gradient(135deg, rgba(248,113,113,0.1), rgba(30,10,20,0.3));
    border: 1px solid rgba(248,113,113,0.4);
    border-radius: 16px;
    padding: 2rem;
    text-align: center;
}
.ending-text { font-size: 15px; line-height: 2.2; color: var(--text); margin: 0; }

/* ── 이펙트 뱃지 */
.effect-tag {
    display: inline-block;
    background: rgba(167,139,250,0.15);
    border: 1px solid rgba(167,139,250,0.3);
    border-radius: 6px;
    padding: 4px 10px;
    font-size: 12px;
    color: var(--accent);
    margin: 2px;
}

/* ── 텍스트에어리어 (없으면 스크롤 생략) */
div.stTextArea > div > div > textarea {
    background: var(--bg-card2) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    color: var(--text) !important;
}

/* ── caption */
.stCaption { color: var(--text-muted) !important; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────
#  데이터 정의
# ─────────────────────────────────────────────────────────
ITEMS = [
    {
        "name":    "치유약",
        "emoji":   "🧪",
        "story":   "생명의 풀잎으로 빚은 물약. 치유의 단어를 새겨야 효력이 깃든다.",
        "effect":  "체력을 30 회복합니다.",
        "slot":    "heal",
    },
    {
        "name":    "방패",
        "emoji":   "🛡️",
        "story":   "선대 기사의 고대 방패. 수호의 단어가 새겨져야 마법이 깃든다.",
        "effect":  "다음 턴 공격을 1번 막습니다.",
        "slot":    "shield",
    },
    {
        "name":    "화염병",
        "emoji":   "🔥",
        "story":   "봉인된 불꽃이 내부에서 요동친다. 해방의 단어를 외쳐야 터진다.",
        "effect":  "빌런에게 지속 화상 데미지를 줍니다.",
        "slot":    "fire",
    },
    {
        "name":    "바람의 망토",
        "emoji":   "🌀",
        "story":   "행운의 여신이 짠 망토. 믿음의 단어를 외쳐야 작동한다.",
        "effect":  "50% 확률로 공격을 피합니다.",
        "slot":    "cloak",
    },
]

GATES = [
    {
        "emoji":    "🌲",
        "location": "망각의 숲 입구",
        "desc":     "안개가 짙게 깔린 어두운 숲. 기억 잃은 자들의 신음이 들린다.",
        "guardian": "기억을 잃은 노병",
        "avatar":   "👴",
        "intro": [
            ("👴", "기억을 잃은 노병", "...누, 누구냐. 왜 내가 여기 있는지 모르겠다. 내 이름도... 잊었어."),
            ("👴", "기억을 잃은 노병", "젊은이... 혹시 단어를 기억하는가? 내가 단 하나만이라도 시험해보고 싶구나."),
        ],
        "pass_msg": "노병의 눈에 잠깐 빛이 돌아왔다. \"...고맙네. 젊은이, 무사하게나.\"",
        "fail_msg": "노병이 고개를 떨궜다. \"...역시 모두 잊혀가는군.\"",
    },
    {
        "emoji":    "🌉",
        "location": "침묵의 다리",
        "desc":     "말소리가 허공에서 사라지는 저주받은 다리. 발걸음 소리마저 지워진다.",
        "guardian": "언어를 잃은 마녀",
        "avatar":   "🧙‍♀️",
        "intro": [
            ("🧙‍♀️", "언어를 잃은 마녀", "쉬잇... 말은 조심해야 해. 여기선 단어가 사라지거든."),
            ("🧙‍♀️", "언어를 잃은 마녀", "내 마지막 주문을 완성시켜줘. 이 단어의 뜻을 알아야 통과할 수 있어."),
        ],
        "pass_msg": "마녀가 낮게 웃었다. \"잘 알고 있군... 조심해서 가.\"",
        "fail_msg": "마녀가 눈을 감았다. \"...결국 언어는 사라지는 것인지도.\"",
    },
    {
        "emoji":    "🏰",
        "location": "버베인 성문 앞",
        "desc":     "거대한 성문이 닫혀있다. 보이드의 기운이 성벽에서 흘러나온다.",
        "guardian": "보이드의 그림자 부하",
        "avatar":   "👤",
        "intro": [
            ("👤", "보이드의 그림자 부하", "...감히 여기까지 왔느냐. 주인님께서 예상하고 계셨다."),
            ("👤", "보이드의 그림자 부하", "통과하고 싶다면 증명해보여라. 네 언어의 힘을."),
        ],
        "pass_msg": "그림자 부하가 비틀거렸다. \"...크윽, 단어의 힘이...\" 성문이 천천히 열렸다.",
        "fail_msg": "부하가 비웃었다. \"역시 나약하군. 주인님의 영역은 넘볼 수 없어.\"",
    },
]

# ─────────────────────────────────────────────────────────
#  세션 초기화
# ─────────────────────────────────────────────────────────
def init_session():
    defaults = {
        "phase":           "word_setup",   # word_setup | intro | gate | battle | end
        "nickname":        "",
        "my_hp":           100,
        "villain_hp":      150,
        "my_items":        [],
        "is_burning":      False,
        "is_shielded":     False,
        "gate_index":      0,
        "battle_log":      [],
        # 단어장 {영단어: [뜻, ...]}
        "word_dict":       {},
        # 아이템슬롯→단어 매핑 {slot: {"word": str, "mean": [...]}}
        "item_word_map":   {},
        # 단어 입력 폼 상태
        "word_input_eng":  "",
        "word_input_kor":  "",
        # UI 플래그
        "show_item_select": False,
        "pending_item":    None,
        "gate_state":      "intro",  # intro | quiz | result
        "gate_result":     None,
        "battle_started":  False,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_session()
S = st.session_state

# ─────────────────────────────────────────────────────────
#  헬퍼
# ─────────────────────────────────────────────────────────
def add_log(msg, cls=""):
    tag = f'<p class="log-{cls}">{msg}</p>' if cls else f"<p>{msg}</p>"
    S.battle_log.append(tag)

def render_log():
    if S.battle_log:
        html = "<div class='log-box'>" + "".join(S.battle_log[-50:]) + "</div>"
        st.markdown(html, unsafe_allow_html=True)

def hp_bar(name, current, max_hp, kind="player"):
    pct = max(0, min(100, int(max(0, current) / max_hp * 100)))
    fill_cls = "hp-fill-player" if kind == "player" else "hp-fill-villain"
    st.markdown(f"""
    <div class="hp-section">
      <div class="hp-row">
        <div class="hp-info">
          <div class="hp-label-row">
            <span class="hp-name">{name}</span>
            <span class="hp-num">{max(0,current)} / {max_hp}</span>
          </div>
          <div class="hp-bar-bg">
            <div class="{fill_cls}" style="width:{pct}%"></div>
          </div>
        </div>
      </div>
    </div>""", unsafe_allow_html=True)

def bubble(avatar, name, text, side="left", style=""):
    cls = f"bubble-wrap {'right' if side == 'right' else ''}"
    text_cls = f"bubble-text {style}"
    st.markdown(f"""
    <div class="{cls}">
      <div class="bubble-avatar">{avatar}</div>
      <div class="bubble-content">
        <div class="bubble-name">{name}</div>
        <div class="{text_cls}">{text}</div>
      </div>
    </div>""", unsafe_allow_html=True)

def system_text(text):
    st.markdown(f"""
    <div class="bubble-wrap">
      <div class="bubble-content">
        <div class="bubble-text system">✦ {text} ✦</div>
      </div>
    </div>""", unsafe_allow_html=True)

def location_header(emoji, name, desc):
    st.markdown(f"""
    <div class="location-header">
      <span class="loc-emoji">{emoji}</span>
      <div class="loc-name">{name}</div>
      <div class="loc-desc">{desc}</div>
    </div>""", unsafe_allow_html=True)

def sec_title(text):
    st.markdown(f"<div class='sec-title'>{text}</div>", unsafe_allow_html=True)

def assign_words_to_items():
    """단어장에서 아이템 4개에 랜덤 배정 (중복 허용 시 재사용)"""
    words = list(S.word_dict.items())  # [(eng, [mean, ...]), ...]
    if not words:
        return
    # 아이템 수 = 4
    n = len(ITEMS)
    if len(words) >= n:
        chosen = random.sample(words, n)
    else:
        # 부족하면 순환하여 채움
        chosen = []
        pool = words.copy()
        while len(chosen) < n:
            chosen.extend(pool)
        chosen = chosen[:n]
        random.shuffle(chosen)

    S.item_word_map = {}
    for item, (eng, means) in zip(ITEMS, chosen):
        S.item_word_map[item["slot"]] = {"word": eng, "mean": means}

def villain_turn():
    if S.villain_hp <= 0:
        return
    if S.is_burning:
        S.villain_hp -= 10
        add_log("🔥 화상으로 빌런의 체력이 10 깎였습니다.", "item")
    v_dmg = random.randint(10, 20)
    if S.is_shielded:
        add_log("🛡️ 빌런의 공격을 막아냈습니다!", "heal")
        S.is_shielded = False
    else:
        S.my_hp -= v_dmg
        add_log(f"💥 빌런의 공격! {v_dmg}의 데미지를 입었습니다.", "dmg")
    # HP 구간 대사
    if S.villain_hp <= 30 and S.villain_hp > 0:
        add_log("😈 보이드: \"...이럴 수가. 단어의 힘이 이토록...\"", "sys")
    elif S.villain_hp <= 75 and S.villain_hp > 70:
        add_log("😈 보이드: \"아직도 기억하고 있느냐... 가상하군.\"", "sys")

# ─────────────────────────────────────────────────────────
#  공통 타이틀
# ─────────────────────────────────────────────────────────
def render_title():
    st.markdown("""
    <div class="title-wrap">
        <h1 class="title-main">⚔️ 단어 용사 어드벤처</h1>
        <div class="title-divider"></div>
        <p class="title-sub">Word Hero Adventure — Verbain Kingdom</p>
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────
#  Phase 0 : 영단어 등록 (단어장)
# ─────────────────────────────────────────────────────────
if S.phase == "word_setup":
    render_title()

    st.markdown("""
    <div class="game-card">
      <h2>📖 마법사 에코의 연구실</h2>
      <p>✦ 마법사 에코가 말했습니다.</p>
    </div>
    """, unsafe_allow_html=True)

    bubble("🧙", "마법사 에코",
           "단어가 곧 힘이야. 네가 기억하는 단어들이 곧 너의 무기가 될 거야.",
           style="")
    bubble("🧙", "마법사 에코",
           "영단어와 뜻을 여기 단어장에 등록해줘. 최소 1개만 있어도 되지만 많을수록 좋아. "
           "등록한 단어들은 랜덤으로 아이템에 배정될 거야.",
           style="")

    # ── 현재 단어장
    if S.word_dict:
        sec_title("📋 등록된 단어장")
        rows = "".join(
            f"<tr><td class='eng'>{e}</td><td class='kor'>{', '.join(m)}</td></tr>"
            for e, m in S.word_dict.items()
        )
        st.markdown(f"""
        <table class="word-table">
          <tr><th>영단어</th><th>뜻 (정답으로 인정되는 표현)</th></tr>
          {rows}
        </table><br>""", unsafe_allow_html=True)

    # ── 단어 추가 폼
    sec_title("✏️ 영단어 추가하기")

    with st.form("add_word_form", clear_on_submit=True):
        c1, c2 = st.columns([1, 2])
        eng = c1.text_input("영단어", placeholder="예: heal")
        kor = c2.text_input("뜻 (쉼표로 여러 개 가능)", placeholder="예: 치료하다, 낫게 하다")
        col_save, col_del = st.columns([3, 1])
        add_btn = col_save.form_submit_button("➕ 단어 추가", use_container_width=True, type="primary")
        # 단어 삭제 기능은 form 밖에서 처리

    if add_btn:
        e = eng.strip()
        m = [x.strip() for x in kor.split(",") if x.strip()]
        if not e or not m:
            st.error("영단어와 뜻을 모두 입력해주세요!")
        else:
            S.word_dict[e] = m
            st.rerun()

    # ── 단어 삭제
    if S.word_dict:
        sec_title("🗑️ 단어 삭제")
        del_cols = st.columns(min(len(S.word_dict), 4))
        for i, eng_key in enumerate(list(S.word_dict.keys())):
            col_idx = i % min(len(S.word_dict), 4)
            if del_cols[col_idx].button(f"✕ {eng_key}", key=f"del_{eng_key}", use_container_width=True):
                del S.word_dict[eng_key]
                st.rerun()

    st.divider()

    count = len(S.word_dict)
    if count == 0:
        st.markdown("<div class='warn-box'>⚠️ 단어가 하나도 없습니다. 최소 1개 이상 등록하세요.</div>", unsafe_allow_html=True)
        st.button("🎮 게임 시작", disabled=True, use_container_width=True)
    else:
        msg = f"✅ 단어 {count}개 등록됨 — 4개의 아이템에 랜덤으로 배정됩니다."
        if count < 4:
            msg += f" ({count}개만 있으므로 일부 단어가 반복될 수 있습니다.)"
        st.markdown(f"<div class='info-box'>{msg}</div>", unsafe_allow_html=True)
        if st.button("🎮 게임 시작 →", use_container_width=True, type="primary"):
            assign_words_to_items()
            S.phase = "intro"
            st.rerun()

# ─────────────────────────────────────────────────────────
#  Phase 1 : 프롤로그 + 닉네임
# ─────────────────────────────────────────────────────────
elif S.phase == "intro":
    render_title()

    location_header("🌅", "버베인 왕국 — 작은 마을", "평화롭던 마을에 이른 아침, 낯선 소식이 들려왔다.")

    system_text("오늘 아침, 옆집 노인이 내 이름을 잊었다.")
    system_text("어제는 시장 상인이 물건 이름을 몰라 울고 있었다.")
    system_text("그리고 오늘 밤 — 기사단이 내 문을 두드렸다.")

    st.markdown("<br>", unsafe_allow_html=True)
    bubble("👑", "왕의 사자",
           "왕국이 위기에 처했습니다. '망각의 군주 보이드'가 버베인 성을 점령하고 "
           "언어와 기억을 지우고 있습니다. 이미 왕국 절반이 말을 잃었습니다.")
    bubble("👑", "왕의 사자",
           "당신만이 단어를 기억하는 힘을 가지고 있습니다. 왕국의 마지막 희망으로 "
           "버베인 성으로 향해 '망각의 오브'를 파괴해주십시오.")

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div class="game-card">
      <h2>⚔️ 용사여, 이름을 밝혀라</h2>
      <p style="color:var(--text-muted)">당신의 이름은 이 왕국에 영원히 기억될 것입니다.</p>
    </div>
    """, unsafe_allow_html=True)

    with st.form("intro_form"):
        nick = st.text_input("용사의 이름", placeholder="이름을 입력하세요")
        col1, col2 = st.columns(2)
        start = col1.form_submit_button("⚔️ 모험 시작!", type="primary", use_container_width=True)
        back  = col2.form_submit_button("← 단어 재설정")

    if start:
        if not nick.strip():
            st.error("이름을 입력해주세요!")
        else:
            S.nickname = nick.strip()
            S.phase = "gate"
            S.gate_index = 0
            S.gate_state = "intro"
            S.gate_result = None
            st.rerun()

    if back:
        S.phase = "word_setup"
        st.rerun()

# ─────────────────────────────────────────────────────────
#  Phase 2 : 관문 (3개)
# ─────────────────────────────────────────────────────────
elif S.phase == "gate":
    gi = S.gate_index

    if gi >= len(GATES):
        S.phase = "battle"
        S.battle_started = False
        st.rerun()

    gate   = GATES[gi]
    item   = ITEMS[gi]
    slot   = item["slot"]
    winfo  = S.item_word_map.get(slot)

    render_title()
    st.progress((gi) / len(GATES), text=f"관문 {gi+1} / {len(GATES)}")
    location_header(gate["emoji"], gate["location"], gate["desc"])

    # ── 상태: intro
    if S.gate_state == "intro":
        for avatar, name, text in gate["intro"]:
            bubble(avatar, name, text)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(f"""
        <div class="game-card">
          <h2>{item['emoji']} {item['name']}</h2>
          <p style="color:var(--text-muted);font-style:italic">"{item['story']}"</p>
          <p style="font-size:13px;color:var(--text-muted);margin-top:8px">
            <span class='badge badge-gold'>아이템 효과</span> {item['effect']}
          </p>
        </div>
        """, unsafe_allow_html=True)

        bubble(gate["avatar"], gate["guardian"],
               f"이 단어의 뜻을 알면 통과시켜 주지. 단어는 — <b>{winfo['word']}</b>")

        if st.button("📖 뜻을 입력한다", use_container_width=True, type="primary"):
            S.gate_state = "quiz"
            st.rerun()
        if st.button("→ 건너뛰기 (아이템 없이 통과)", use_container_width=True):
            S.gate_state = "result"
            S.gate_result = "skip"
            st.rerun()

    # ── 상태: quiz
    elif S.gate_state == "quiz":
        for avatar, name, text in gate["intro"]:
            bubble(avatar, name, text)

        st.markdown(f"""
        <div class="game-card">
          <h2>🔤 단어 퀴즈</h2>
          <p>단어 <span class='badge badge-word'>{winfo['word']}</span> 의 한국어 뜻은?</p>
        </div>
        """, unsafe_allow_html=True)

        with st.form("gate_quiz_form"):
            ans = st.text_input("뜻을 입력하세요", placeholder="한국어로 입력")
            submitted = st.form_submit_button("✅ 확인", type="primary", use_container_width=True)

        if submitted:
            if ans.strip() in winfo["mean"]:
                S.gate_result = "pass"
                S.my_items.append(item["name"])
            else:
                S.gate_result = f"fail:{', '.join(winfo['mean'])}"
            S.gate_state = "result"
            st.rerun()

    # ── 상태: result
    elif S.gate_state == "result":
        res = S.gate_result

        if res == "pass":
            st.success(f"✨ 정답! [{item['name']}] 획득!")
            bubble(gate["avatar"], gate["guardian"], gate["pass_msg"])
        elif res == "skip":
            st.info("건너뛰었습니다. 아이템 없이 계속 진행합니다.")
        else:
            ans_shown = res.replace("fail:", "")
            st.error(f"💨 틀렸습니다. 정답: [{ans_shown}]")
            bubble(gate["avatar"], gate["guardian"], gate["fail_msg"])

        # 인벤토리
        if S.my_items:
            inv_html = " ".join(f"<span class='badge badge-item'>{i}</span>" for i in S.my_items)
            st.markdown(f"<br><b>🎒 현재 인벤토리:</b> {inv_html}", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("계속 진행 →", use_container_width=True, type="primary"):
            S.gate_index += 1
            S.gate_state = "intro"
            S.gate_result = None
            st.rerun()

# ─────────────────────────────────────────────────────────
#  Phase 3 : 보스전
# ─────────────────────────────────────────────────────────
elif S.phase == "battle":
    nick = S.nickname

    render_title()
    location_header("🏰", "버베인 성 꼭대기 — 망각의 오브 앞", "어둠이 짙게 깔린 성 꼭대기. 보이드가 기다리고 있다.")

    # 전투 시작 연출
    if not S.battle_started:
        bubble("😈", "망각의 군주 보이드",
               "...성 꼭대기에서 보이드가 느리게 고개를 돌렸다.", style="villain")
        bubble("😈", "망각의 군주 보이드",
               "오호... 여기까지 왔느냐. 단어를 기억하는 자. 하지만 결국 너도 나를 잊게 될 것이다.",
               style="villain")
        bubble("⚔️", nick,
               f"나는 {nick}! 버베인 왕국의 이름으로, 망각의 오브를 파괴하러 왔다!", side="right")

        if st.button("⚔️ 전투 시작!", use_container_width=True, type="primary"):
            S.battle_started = True
            add_log("⚔️ 전투가 시작되었다!", "sys")
            st.rerun()
        st.stop()

    # ── HP 바
    st.markdown("<br>", unsafe_allow_html=True)
    hp_bar(f"❤️ {nick}", S.my_hp, 100, "player")
    hp_bar("😈 망각의 군주 보이드", S.villain_hp, 150, "villain")

    # 인벤토리
    st.markdown("<br>", unsafe_allow_html=True)
    if S.my_items:
        inv_html = " ".join(f"<span class='badge badge-item'>{i}</span>" for i in S.my_items)
        st.markdown(f"**🎒 인벤토리:** {inv_html}", unsafe_allow_html=True)
    else:
        st.markdown("<span style='color:var(--text-muted);font-size:13px'>🎒 인벤토리가 비어있습니다.</span>", unsafe_allow_html=True)

    # 버프
    buffs = []
    if S.is_burning:  buffs.append("🔥 화상 지속 중")
    if S.is_shielded: buffs.append("🛡️ 방어 중")
    if buffs:
        st.markdown(" &nbsp;|&nbsp; ".join(f"<span class='effect-tag'>{b}</span>" for b in buffs),
                    unsafe_allow_html=True)

    st.divider()

    # 행동 버튼
    col_atk, col_item = st.columns(2)
    attacked  = col_atk.button("⚔️ 공격하기", use_container_width=True, type="primary")
    use_item  = col_item.button("🎒 아이템 사용", use_container_width=True,
                                disabled=(len(S.my_items) == 0))

    # ── 공격
    if attacked:
        dmg = random.randint(15, 25)
        S.villain_hp -= dmg
        add_log(f"⚔️ 일격! 빌런에게 <b>{dmg}</b>의 데미지!", "atk")
        villain_turn()
        if S.villain_hp <= 0:
            S.phase = "end"
            S.battle_log.append('<p class="log-win">🏆 빌런을 쓰러뜨렸습니다!</p>')
        elif S.my_hp <= 0:
            S.phase = "end"
            S.battle_log.append('<p class="log-lose">💀 쓰러졌습니다...</p>')
        st.rerun()

    # ── 아이템 선택 UI
    if use_item:
        S.show_item_select = True

    if S.show_item_select and S.my_items:
        st.markdown("**사용할 아이템을 선택하세요:**")
        item_cols = st.columns(len(S.my_items))
        for i, iname in enumerate(S.my_items):
            emoji = next((x["emoji"] for x in ITEMS if x["name"] == iname), "✨")
            if item_cols[i].button(f"{emoji} {iname}", key=f"pick_{iname}_{i}", use_container_width=True):
                S.pending_item = iname
                S.show_item_select = False
                st.rerun()

    # ── 아이템 퀴즈
    if S.pending_item:
        chosen = S.pending_item
        item_obj = next((x for x in ITEMS if x["name"] == chosen), None)
        slot = item_obj["slot"] if item_obj else None
        winfo = S.item_word_map.get(slot)

        st.markdown(f"""
        <div class="game-card">
          <h2>📢 [{chosen}] 마법 발동!</h2>
          <p>단어 <span class='badge badge-word'>{winfo['word']}</span> 의 뜻을 외쳐라!</p>
        </div>
        """, unsafe_allow_html=True)

        with st.form("item_quiz_form"):
            item_ans = st.text_input("뜻 입력", placeholder="한국어로 입력")
            c1, c2 = st.columns([3, 1])
            confirmed = c1.form_submit_button("💫 발동!", type="primary", use_container_width=True)
            cancelled = c2.form_submit_button("취소")

        if confirmed:
            if item_ans.strip() in winfo["mean"]:
                add_log(f"💫 <b>{chosen}</b> 마법 발동!", "item")
                S.my_items.remove(chosen)
                if chosen == "치유약":
                    S.my_hp = min(100, S.my_hp + 30)
                    add_log("❤️ 생명의 빛이 넘쳐흘렀다. 체력이 30 회복!", "heal")
                elif chosen == "방패":
                    S.is_shielded = True
                    add_log("🛡️ 고대의 방패가 빛을 발했다. 다음 공격을 막는다!", "heal")
                elif chosen == "화염병":
                    S.is_burning = True
                    add_log("🔥 봉인된 불꽃이 해방되었다! 빌런에게 화염 지속 데미지!", "item")
                elif chosen == "바람의 망토":
                    if random.random() < 0.5:
                        S.is_shielded = True
                        add_log("🎲 행운의 여신이 미소 지었다! 다음 공격을 피한다!", "heal")
                    else:
                        add_log("🎲 바람이 엇나갔다... 망토가 반응하지 않았다.", "sys")
            else:
                add_log(f"🚫 단어를 잘못 외쳤다! 정답: [{', '.join(winfo['mean'])}]", "dmg")

            villain_turn()
            S.pending_item = None
            if S.villain_hp <= 0:
                S.phase = "end"
                S.battle_log.append('<p class="log-win">🏆 빌런을 쓰러뜨렸습니다!</p>')
            elif S.my_hp <= 0:
                S.phase = "end"
                S.battle_log.append('<p class="log-lose">💀 쓰러졌습니다...</p>')
            st.rerun()

        if cancelled:
            S.pending_item = None
            st.rerun()

    st.divider()
    render_log()

# ─────────────────────────────────────────────────────────
#  Phase 4 : 엔딩
# ─────────────────────────────────────────────────────────
elif S.phase == "end":
    nick = S.nickname

    render_title()
    location_header("🏰", "버베인 성 꼭대기", "전투의 먼지가 가라앉고 있다...")

    hp_bar(f"❤️ {nick}", S.my_hp, 100, "player")
    hp_bar("😈 망각의 군주 보이드", S.villain_hp, 150, "villain")

    render_log()
    st.divider()

    if S.my_hp > 0:
        # 승리
        st.markdown(f"""
        <div class="ending-win">
          <div style="font-size:2.5rem;margin-bottom:12px">🏆</div>
          <p class="ending-text">
            망각의 오브가 산산이 부서졌다.<br>
            왕국 곳곳에서 사람들이 눈을 깜빡였다.<br>
            그리고 서로의 이름을 다시 부르기 시작했다.<br><br>
            <span style="color:var(--gold);font-size:1.1em;font-weight:700">
            ✦ {nick}의 이름도, 영원히 기억될 것이다. ✦
            </span>
          </p>
        </div>
        """, unsafe_allow_html=True)
        st.balloons()
    else:
        # 패배
        st.markdown(f"""
        <div class="ending-lose">
          <div style="font-size:2.5rem;margin-bottom:12px">💀</div>
          <p class="ending-text">
            단어가 흐릿해지기 시작했다...<br>
            <span style="color:var(--text-muted)">{nick}... {nick}...</span><br>
            그 이름도 이제 아무도 기억하지 못한다.<br><br>
            <span style="color:var(--red)">마을은 어둠에 잠겼습니다.</span>
          </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)

    if col1.button("🔄 다시 시작 (같은 단어장)", use_container_width=True, type="primary"):
        saved = S.word_dict.copy()
        for k in list(st.session_state.keys()):
            del st.session_state[k]
        init_session()
        st.session_state.word_dict = saved
        assign_words_to_items()
        st.session_state.phase = "intro"
        st.rerun()

    if col2.button("📝 단어장 재설정", use_container_width=True):
        for k in list(st.session_state.keys()):
            del st.session_state[k]
        init_session()
        st.rerun()
