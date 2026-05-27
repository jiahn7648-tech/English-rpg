import streamlit as st
import random

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
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700&display=swap');

html, body, [class*="css"] { font-family: 'Noto Sans KR', sans-serif; }

/* 메인 카드 */
.game-card {
    background: #1a1a2e;
    border: 1px solid #e94560;
    border-radius: 12px;
    padding: 1.5rem 2rem;
    margin-bottom: 1rem;
    color: #eee;
}
.game-card h2 { color: #e94560; margin-top: 0; }

/* HP 바 */
.hp-bar-wrap { margin: 6px 0 12px; }
.hp-label { font-size: 13px; color: #aaa; margin-bottom: 4px; }
.hp-bar-bg { background: #333; border-radius: 6px; height: 18px; overflow: hidden; }
.hp-bar-fill-player  { background: linear-gradient(90deg,#00c9ff,#92fe9d); height:100%; border-radius:6px; transition:width .4s; }
.hp-bar-fill-villain { background: linear-gradient(90deg,#e94560,#f5a623); height:100%; border-radius:6px; transition:width .4s; }

/* 배지 */
.badge {
    display: inline-block;
    padding: 3px 10px;
    border-radius: 20px;
    font-size: 13px;
    font-weight: 500;
    margin: 3px 4px 3px 0;
}
.badge-item   { background:#2d2d5e; color:#a78bfa; border:1px solid #a78bfa; }
.badge-box    { background:#1e3a2e; color:#4ade80; border:1px solid #4ade80; }
.badge-word   { background:#3a1e2e; color:#f472b6; border:1px solid #f472b6; }

/* 로그 */
.log-box {
    background: #111827;
    border: 1px solid #374151;
    border-radius: 8px;
    padding: 1rem;
    max-height: 220px;
    overflow-y: auto;
    font-size: 14px;
    line-height: 1.8;
    color: #d1d5db;
}
.log-box p { margin: 2px 0; }
.log-atk   { color:#60a5fa; }
.log-dmg   { color:#f87171; }
.log-heal  { color:#34d399; }
.log-item  { color:#a78bfa; }
.log-sys   { color:#fbbf24; }
.log-win   { color:#4ade80; font-weight:700; font-size:16px; }
.log-lose  { color:#f87171; font-weight:700; font-size:16px; }

/* 단어 등록 테이블 */
.word-table { width:100%; border-collapse:collapse; font-size:14px; }
.word-table th { background:#2d2d5e; color:#a78bfa; padding:8px 12px; text-align:left; border-bottom:1px solid #374151; }
.word-table td { padding:8px 12px; border-bottom:1px solid #1f2937; color:#d1d5db; }
.word-table tr:hover td { background:#1f2937; }

/* 섹션 타이틀 */
.section-title {
    font-size: 18px;
    font-weight: 700;
    color: #e94560;
    margin: 1.5rem 0 0.5rem;
    border-left: 4px solid #e94560;
    padding-left: 10px;
}

/* 경고 */
.warn-box {
    background: #3a1e1e;
    border: 1px solid #e94560;
    border-radius: 8px;
    padding: 0.7rem 1rem;
    color: #fca5a5;
    font-size: 14px;
    margin-bottom: 0.5rem;
}

/* Streamlit 버튼 전체 스타일 덮어쓰기 */
div.stButton > button {
    border-radius: 8px !important;
    font-family: 'Noto Sans KR', sans-serif !important;
    font-weight: 500 !important;
    transition: all .15s !important;
}
div.stButton > button:hover { opacity: 0.85; transform: translateY(-1px); }
div.stButton > button:active { transform: scale(0.97); }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────
#  기본 아이템 데이터 (단어를 사용자 정의로 교체)
# ─────────────────────────────────────────────────────────
DEFAULT_BOXES = [
    {"name": "치유약",        "desc": "체력을 30 회복합니다."},
    {"name": "방패",          "desc": "다음 턴 공격을 1번 막습니다."},
    {"name": "화염병",        "desc": "빌런에게 지속 화상 데미지를 줍니다."},
    {"name": "도박의 투명망토","desc": "50% 확률로 공격을 피합니다."},
]

ITEM_QUIZ_SLOTS = ["치유약", "방패", "화염병", "도박의 투명망토"]

# ─────────────────────────────────────────────────────────
#  세션 초기화
# ─────────────────────────────────────────────────────────
def init_session():
    defaults = {
        "phase": "word_setup",       # word_setup | intro | treasure | battle | end
        "nickname": "",
        "my_hp": 100,
        "villain_hp": 150,
        "my_items": [],
        "is_burning": False,
        "is_shielded": False,
        "box_index": 0,
        "battle_log": [],
        # 사용자 정의 단어: {슬롯명: {"word": str, "mean": [str, ...]}}
        "custom_words": {},
        # 단어 등록 UI 상태
        "word_editing_slot": None,
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
        html = "<div class='log-box'>" + "".join(S.battle_log[-40:]) + "</div>"
        st.markdown(html, unsafe_allow_html=True)

def hp_bar(label, current, max_hp, kind="player"):
    pct = max(0, min(100, int(current / max_hp * 100)))
    color_cls = "hp-bar-fill-player" if kind == "player" else "hp-bar-fill-villain"
    st.markdown(f"""
    <div class="hp-bar-wrap">
        <div class="hp-label">{label}  {max(0,current)} / {max_hp}</div>
        <div class="hp-bar-bg"><div class="{color_cls}" style="width:{pct}%"></div></div>
    </div>""", unsafe_allow_html=True)

def get_word_for_slot(slot):
    """슬롯에 등록된 단어 반환. 없으면 None."""
    return S.custom_words.get(slot)

def all_slots_filled():
    return len(S.custom_words) >= len(ITEM_QUIZ_SLOTS)

def villain_attack():
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

# ─────────────────────────────────────────────────────────
#  Phase 0 : 영단어 등록
# ─────────────────────────────────────────────────────────
if S.phase == "word_setup":
    st.markdown("# ⚔️ 단어 용사 어드벤처")
    st.markdown("게임을 시작하기 전에 **아이템에 쓸 영단어**를 등록하세요.")
    st.caption("각 아이템 슬롯마다 단어 1개와 정답 뜻(쉼표 구분)을 입력합니다.")

    # ── 현재 등록 현황 테이블
    if S.custom_words:
        st.markdown("<div class='section-title'>📋 등록된 단어</div>", unsafe_allow_html=True)
        rows = ""
        for slot in ITEM_QUIZ_SLOTS:
            info = S.custom_words.get(slot)
            if info:
                rows += f"<tr><td>{slot}</td><td><b>{info['word']}</b></td><td>{', '.join(info['mean'])}</td></tr>"
        st.markdown(f"""
        <table class="word-table">
          <tr><th>아이템 슬롯</th><th>단어</th><th>정답 뜻</th></tr>
          {rows}
        </table>""", unsafe_allow_html=True)
        st.markdown("")

    # ── 슬롯 선택 버튼들
    st.markdown("<div class='section-title'>✏️ 영단어 등록하기</div>", unsafe_allow_html=True)

    cols = st.columns(len(ITEM_QUIZ_SLOTS))
    for i, slot in enumerate(ITEM_QUIZ_SLOTS):
        filled = slot in S.custom_words
        label = f"{'✅' if filled else '📝'} {slot}"
        if cols[i].button(label, key=f"slot_btn_{slot}", use_container_width=True):
            S.word_editing_slot = slot

    # ── 선택된 슬롯 입력 폼
    if S.word_editing_slot:
        slot = S.word_editing_slot
        existing = S.custom_words.get(slot, {})
        st.markdown(f"<div class='section-title'>🔤 [{slot}] 단어 입력</div>", unsafe_allow_html=True)

        with st.form(key="word_form"):
            word_in = st.text_input(
                "영단어",
                value=existing.get("word", ""),
                placeholder="예: heal",
            )
            mean_in = st.text_input(
                "정답 뜻 (쉼표로 구분)",
                value=", ".join(existing.get("mean", [])),
                placeholder="예: 치료, 치료하다",
            )
            save_col, del_col = st.columns([3, 1])
            saved = save_col.form_submit_button("💾 저장", use_container_width=True, type="primary")
            deleted = del_col.form_submit_button("🗑️ 삭제", use_container_width=True)

        if saved:
            w = word_in.strip()
            m = [x.strip() for x in mean_in.split(",") if x.strip()]
            if not w or not m:
                st.error("단어와 뜻을 모두 입력해주세요!")
            else:
                S.custom_words[slot] = {"word": w, "mean": m}
                S.word_editing_slot = None
                st.rerun()

        if deleted and slot in S.custom_words:
            del S.custom_words[slot]
            S.word_editing_slot = None
            st.rerun()

    st.divider()

    # ── 게임 시작 버튼
    if not all_slots_filled():
        remaining = [s for s in ITEM_QUIZ_SLOTS if s not in S.custom_words]
        st.markdown(
            f"<div class='warn-box'>⚠️ 아직 등록 안 된 슬롯: {', '.join(remaining)}<br>"
            "모든 슬롯을 채워야 게임을 시작할 수 있습니다.</div>",
            unsafe_allow_html=True
        )
        st.button("🎮 게임 시작", disabled=True, use_container_width=True)
    else:
        if st.button("🎮 게임 시작 →", use_container_width=True, type="primary"):
            S.phase = "intro"
            st.rerun()

# ─────────────────────────────────────────────────────────
#  Phase 1 : 닉네임 입력
# ─────────────────────────────────────────────────────────
elif S.phase == "intro":
    st.markdown("# 🔥 평화롭던 마을이 파괴되었습니다")
    st.markdown("마을을 구할 **용사의 이름**을 입력하세요.")

    with st.form("intro_form"):
        nick = st.text_input("용사 이름", placeholder="이름을 입력하세요")
        start = st.form_submit_button("모험 시작!", type="primary", use_container_width=True)

    if start:
        if not nick.strip():
            st.error("이름을 입력해주세요!")
        else:
            S.nickname = nick.strip()
            S.phase = "treasure"
            S.box_index = 0
            st.rerun()

    if st.button("← 단어 다시 설정"):
        S.phase = "word_setup"
        st.rerun()

# ─────────────────────────────────────────────────────────
#  Phase 2 : 보물상자 파밍
# ─────────────────────────────────────────────────────────
elif S.phase == "treasure":
    idx = S.box_index

    if idx >= len(DEFAULT_BOXES):
        S.phase = "battle"
        st.rerun()

    box = DEFAULT_BOXES[idx]
    slot_name = ITEM_QUIZ_SLOTS[idx]
    word_info = get_word_for_slot(slot_name)

    # 진행 바
    st.progress(idx / len(DEFAULT_BOXES), text=f"보물상자 {idx+1} / {len(DEFAULT_BOXES)}")

    st.markdown(f"## 🎁 보물상자 발견!")
    st.markdown(
        f"<div class='game-card'>"
        f"<h2>📦 {box['name']}</h2>"
        f"<p style='color:#aaa'>{box['desc']}</p>"
        f"<p>단어 <span class='badge badge-word'>{word_info['word']}</span> 의 뜻을 입력하면 상자가 열립니다.</p>"
        f"</div>",
        unsafe_allow_html=True
    )

    with st.form(f"treasure_form_{idx}"):
        ans = st.text_input("뜻을 입력하세요", placeholder="한국어로 입력")
        col1, col2 = st.columns(2)
        submit = col1.form_submit_button("📦 상자 열기", type="primary", use_container_width=True)
        skip   = col2.form_submit_button("건너뛰기 →", use_container_width=True)

    if submit:
        if ans.strip() in word_info["mean"]:
            st.success(f"✨ 짤랑! [{box['name']}] 획득!")
            S.my_items.append(box["name"])
        else:
            st.error(f"💨 꽝! 정답은 [{', '.join(word_info['mean'])}] 이었습니다.")
        S.box_index += 1
        st.rerun()

    if skip:
        st.info(f"💨 상자를 건너뛰었습니다.")
        S.box_index += 1
        st.rerun()

    # 현재 인벤토리
    if S.my_items:
        inv_html = " ".join(f"<span class='badge badge-item'>{i}</span>" for i in S.my_items)
        st.markdown(f"**🎒 현재 인벤토리:** {inv_html}", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────
#  Phase 3 : 전투
# ─────────────────────────────────────────────────────────
elif S.phase == "battle":
    nick = S.nickname

    st.markdown(f"## 😈 빌런 '다크 스포일러' VS {nick}")

    # HP 바
    hp_bar(f"❤️ {nick}", S.my_hp, 100, "player")
    hp_bar("😈 다크 스포일러", S.villain_hp, 150, "villain")

    # 인벤토리
    if S.my_items:
        inv_html = " ".join(f"<span class='badge badge-item'>{i}</span>" for i in S.my_items)
        st.markdown(f"**🎒 인벤토리:** {inv_html}", unsafe_allow_html=True)
    else:
        st.caption("🎒 인벤토리가 비어있습니다.")

    # 버프 표시
    buff_msgs = []
    if S.is_burning:  buff_msgs.append("🔥 화상 지속 중")
    if S.is_shielded: buff_msgs.append("🛡️ 방어 중")
    if buff_msgs:
        st.markdown(" &nbsp;|&nbsp; ".join(f"**{b}**" for b in buff_msgs), unsafe_allow_html=True)

    st.divider()

    # ── 행동 버튼
    col_atk, col_item = st.columns(2)
    attacked = col_atk.button("⚔️ 공격하기", use_container_width=True, type="primary")
    use_item  = col_item.button("🎒 아이템 사용", use_container_width=True,
                                disabled=len(S.my_items) == 0)

    # ── 공격
    if attacked:
        dmg = random.randint(15, 25)
        S.villain_hp -= dmg
        add_log(f"⚔️ 일격! 빌런에게 <b>{dmg}</b>의 데미지!", "atk")
        villain_attack()
        if S.villain_hp <= 0:
            S.phase = "end"
            S.battle_log.append('<p class="log-win">🏆 빌런을 쓰러뜨렸습니다!</p>')
        elif S.my_hp <= 0:
            S.phase = "end"
            S.battle_log.append('<p class="log-lose">💀 쓰러졌습니다...</p>')
        st.rerun()

    # ── 아이템 사용 → 슬롯 선택 UI
    if use_item:
        S["show_item_select"] = True

    if S.get("show_item_select") and S.my_items:
        st.markdown("**사용할 아이템을 선택하세요:**")
        item_cols = st.columns(len(S.my_items))
        for i, item in enumerate(S.my_items):
            if item_cols[i].button(f"✨ {item}", key=f"pick_{item}", use_container_width=True):
                S["pending_item"] = item
                S["show_item_select"] = False
                st.rerun()

    # ── 선택된 아이템 → 단어 퀴즈
    if S.get("pending_item"):
        chosen = S["pending_item"]
        word_info = get_word_for_slot(chosen)

        st.markdown(
            f"<div class='game-card'>"
            f"<h2>📢 [{chosen}] 사용 퀴즈</h2>"
            f"단어 <span class='badge badge-word'>{word_info['word']}</span> 의 뜻은?"
            f"</div>",
            unsafe_allow_html=True
        )
        with st.form("item_quiz_form"):
            item_ans = st.text_input("뜻 입력", placeholder="한국어로 입력")
            confirmed = st.form_submit_button("사용!", type="primary", use_container_width=True)
            cancelled = st.form_submit_button("취소")

        if confirmed:
            if item_ans.strip() in word_info["mean"]:
                add_log(f"💫 <b>{chosen}</b> 효과 발동!", "item")
                S.my_items.remove(chosen)
                if chosen == "치유약":
                    S.my_hp = min(100, S.my_hp + 30)
                    add_log("❤️ 체력이 30 회복되었습니다.", "heal")
                elif chosen == "방패":
                    S.is_shielded = True
                    add_log("🛡️ 다음 공격을 막습니다.", "heal")
                elif chosen == "화염병":
                    S.is_burning = True
                    add_log("🔥 빌런에게 화염을 던졌습니다!", "item")
                elif chosen == "도박의 투명망토":
                    if random.random() < 0.5:
                        S.is_shielded = True
                        add_log("🎲 도박 성공! 다음 공격을 피합니다.", "heal")
                    else:
                        add_log("🎲 도박 실패...", "sys")
            else:
                add_log(f"🚫 틀렸습니다! 정답: [{', '.join(word_info['mean'])}]", "dmg")

            villain_attack()
            S["pending_item"] = None
            if S.villain_hp <= 0:
                S.phase = "end"
                S.battle_log.append('<p class="log-win">🏆 빌런을 쓰러뜨렸습니다!</p>')
            elif S.my_hp <= 0:
                S.phase = "end"
                S.battle_log.append('<p class="log-lose">💀 쓰러졌습니다...</p>')
            st.rerun()

        if cancelled:
            S["pending_item"] = None
            st.rerun()

    st.divider()
    render_log()

# ─────────────────────────────────────────────────────────
#  Phase 4 : 엔딩
# ─────────────────────────────────────────────────────────
elif S.phase == "end":
    nick = S.nickname

    hp_bar(f"❤️ {nick}", S.my_hp, 100, "player")
    hp_bar("😈 다크 스포일러", S.villain_hp, 150, "villain")

    render_log()

    if S.my_hp > 0:
        st.success(f"🏆 승리! **{nick}** 용사님 덕분에 마을이 구해졌습니다!")
        st.balloons()
    else:
        st.error("💀 패배했습니다... 마을은 어둠에 잠겼습니다.")

    st.divider()
    col1, col2 = st.columns(2)
    if col1.button("🔄 다시 시작 (같은 단어)", use_container_width=True, type="primary"):
        saved_words = S.custom_words.copy()
        for k in list(st.session_state.keys()):
            del st.session_state[k]
        init_session()
        st.session_state.custom_words = saved_words
        st.session_state.phase = "intro"
        st.rerun()

    if col2.button("📝 단어 다시 설정", use_container_width=True):
        for k in list(st.session_state.keys()):
            del st.session_state[k]
        init_session()
        st.rerun()
