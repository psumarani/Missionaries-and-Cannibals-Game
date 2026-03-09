import streamlit as st

# ─── Page config ────────────────────────────────────────────────────────────
st.set_page_config(page_title="Missionaries & Cannibals", page_icon="⛵", layout="centered")

# ─── Custom CSS ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
  body { background-color: #0a1628; }
  .stApp { background: linear-gradient(180deg, #0a1628 0%, #1a3a5c 100%); }

  h1 { color: #f0c040 !important; text-align: center; font-size: 2.2rem !important; }

  .river-scene {
    background: linear-gradient(180deg, #87ceeb 0%, #87ceeb 40%, #1e90ff 40%, #1e90ff 70%, #8B7355 70%, #8B7355 100%);
    border-radius: 16px;
    padding: 20px 10px;
    margin: 16px 0;
    box-shadow: 0 4px 24px #0006;
    min-height: 180px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    position: relative;
  }

  .bank {
    background: #8B7355;
    border-radius: 12px;
    padding: 10px 14px;
    min-width: 110px;
    text-align: center;
    box-shadow: 0 2px 8px #0004;
  }

  .bank-label { color: #f0c040; font-weight: bold; font-size: 1rem; margin-bottom: 6px; }
  .figure-row { font-size: 1.7rem; letter-spacing: 2px; min-height: 32px; }
  .count-row { color: #fff; font-size: 0.82rem; margin-top: 4px; }

  .boat-area {
    flex: 1;
    text-align: center;
    position: relative;
  }

  .boat {
    font-size: 2.4rem;
    display: inline-block;
    transition: transform 0.5s;
    filter: drop-shadow(0 2px 6px #0008);
  }

  .boat-left  { transform: translateX(-40px); }
  .boat-right { transform: translateX( 40px); }

  .boat-passengers { font-size: 1.3rem; letter-spacing: 1px; min-height: 28px; }
  .river-label { color: #cceeff; font-size: 0.78rem; margin-top: 4px; opacity: 0.8; }

  .status-box {
    border-radius: 12px;
    padding: 14px 20px;
    text-align: center;
    font-size: 1.1rem;
    font-weight: bold;
    margin: 10px 0;
  }
  .status-playing { background: #1e3a5f; color: #7ec8e3; border: 1px solid #2e6a9e; }
  .status-win     { background: #1a4a2a; color: #6ddc8b; border: 1px solid #2e8a4e; font-size: 1.4rem; }
  .status-lose    { background: #4a1a1a; color: #ff7c7c; border: 1px solid #8a2e2e; font-size: 1.4rem; }

  .move-history {
    background: #0d2137;
    border-radius: 10px;
    padding: 10px 16px;
    max-height: 160px;
    overflow-y: auto;
    font-size: 0.82rem;
    color: #aac8e0;
    border: 1px solid #1e4060;
  }

  .rules-box {
    background: #0d2137;
    border-radius: 10px;
    padding: 12px 18px;
    color: #aac8e0;
    font-size: 0.85rem;
    border: 1px solid #1e4060;
    margin-bottom: 10px;
  }

  div[data-testid="stButton"] button {
    border-radius: 8px !important;
    font-weight: bold !important;
    transition: 0.2s !important;
  }
</style>
""", unsafe_allow_html=True)

# ─── Emoji helpers ───────────────────────────────────────────────────────────
def render_figures(missionaries: int, cannibals: int) -> str:
    return "🧑‍⚖️" * missionaries + "💀" * cannibals or "—"

# ─── Session state init ──────────────────────────────────────────────────────
def init_state():
    st.session_state.ml = 0   # missionaries left bank
    st.session_state.cl = 0   # cannibals left bank
    st.session_state.mr = 3   # missionaries right bank
    st.session_state.cr = 3   # cannibals right bank
    st.session_state.boat = "right"   # boat side
    st.session_state.game_over = False
    st.session_state.won = False
    st.session_state.message = ""
    st.session_state.history = []
    st.session_state.move_count = 0
    st.session_state.boat_m = 0
    st.session_state.boat_c = 0

if "ml" not in st.session_state:
    init_state()

# ─── Game logic ──────────────────────────────────────────────────────────────
def make_move(m: int, c: int):
    s = st.session_state
    if s.game_over:
        return

    total = m + c
    if total not in (1, 2):
        s.message = "⚠️ Boat carries 1 or 2 people only!"
        return
    if m < 0 or c < 0:
        s.message = "⚠️ Numbers can't be negative!"
        return

    if s.boat == "right":
        if m > s.mr or c > s.cr:
            s.message = "⚠️ Not enough people on the Right bank!"
            return
        s.boat_m, s.boat_c = m, c
        s.mr -= m;  s.cr -= c
        s.ml += m;  s.cl += c
        s.boat = "left"
        direction = "Right → Left"
    else:
        if m > s.ml or c > s.cl:
            s.message = "⚠️ Not enough people on the Left bank!"
            return
        s.boat_m, s.boat_c = m, c
        s.ml -= m;  s.cl -= c
        s.mr += m;  s.cr += c
        s.boat = "right"
        direction = "Left → Right"

    s.move_count += 1
    s.history.append(f"Move {s.move_count}: {direction} — 🧑‍⚖️×{m} 💀×{c}")

    # Check lose condition
    if (s.mr > 0 and s.cr > s.mr) or (s.ml > 0 and s.cl > s.ml):
        s.message = "💀 Cannibals outnumber missionaries — YOU LOSE!"
        s.game_over = True
        return

    # Check win condition
    if s.ml == 3 and s.cl == 3:
        s.message = "🎉 All safely crossed — YOU WIN!"
        s.game_over = True
        s.won = True
        return

    s.message = f"✅ Move {s.move_count} done! Boat is now on the {'Left' if s.boat=='left' else 'Right'}."

# ─── UI ──────────────────────────────────────────────────────────────────────
st.title("⛵ Missionaries & Cannibals")

# Rules
with st.expander("📜 How to Play", expanded=False):
    st.markdown("""
<div class="rules-box">
<b>Goal:</b> Move all 3 missionaries 🧑‍⚖️ and 3 cannibals 💀 from the <b>Right</b> bank to the <b>Left</b> bank.<br><br>
<b>Rules:</b><br>
• The boat holds <b>1 or 2 people</b> and cannot cross empty.<br>
• Cannibals must <b>never outnumber</b> missionaries on either bank (unless there are 0 missionaries there).<br>
• Enter <b>10 missionaries</b> to quit.<br><br>
<b>Tip:</b> The puzzle can be solved in <b>11 moves</b>!
</div>
""", unsafe_allow_html=True)

s = st.session_state

# ─── River Scene ─────────────────────────────────────────────────────────────
boat_class = "boat-left" if s.boat == "left" else "boat-right"
boat_passengers = render_figures(s.boat_m, s.boat_c) if s.move_count > 0 else ""

st.markdown(f"""
<div class="river-scene">
  <div class="bank">
    <div class="bank-label">🏝️ Left Bank</div>
    <div class="figure-row">{render_figures(s.ml, s.cl)}</div>
    <div class="count-row">🧑‍⚖️ {s.ml} &nbsp; 💀 {s.cl}</div>
  </div>

  <div class="boat-area">
    <div class="boat-passengers">{boat_passengers}</div>
    <div class="boat {boat_class}">⛵</div>
    <div class="river-label">🌊 ~ ~ ~ ~ ~ ~ 🌊</div>
  </div>

  <div class="bank">
    <div class="bank-label">🏝️ Right Bank</div>
    <div class="figure-row">{render_figures(s.mr, s.cr)}</div>
    <div class="count-row">🧑‍⚖️ {s.mr} &nbsp; 💀 {s.cr}</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ─── Status message ───────────────────────────────────────────────────────────
if s.message:
    if s.won:
        css_class = "status-win"
    elif s.game_over:
        css_class = "status-lose"
    else:
        css_class = "status-playing"
    st.markdown(f'<div class="status-box {css_class}">{s.message}</div>', unsafe_allow_html=True)

# ─── Controls ────────────────────────────────────────────────────────────────
if not s.game_over:
    side_label = "Right → Left" if s.boat == "right" else "Left → Right"
    st.markdown(f"**🚣 Boat is on the {'Right' if s.boat=='right' else 'Left'} bank — moving {side_label}**")

    col1, col2 = st.columns(2)
    with col1:
        m_input = st.number_input("🧑‍⚖️ Missionaries", min_value=0, max_value=3, value=0, step=1, key="m_in")
    with col2:
        c_input = st.number_input("💀 Cannibals", min_value=0, max_value=3, value=0, step=1, key="c_in")

    col_a, col_b, col_c = st.columns([2, 1, 1])
    with col_a:
        if st.button("🚣 Send Across", use_container_width=True):
            make_move(int(m_input), int(c_input))
            st.rerun()

    # Quick move buttons
    st.markdown("**Quick moves:**")
    qcols = st.columns(5)
    quick = [(1,0,"🧑‍⚖️1"),(0,1,"💀1"),(1,1,"🧑‍⚖️💀"),(2,0,"🧑‍⚖️2"),(0,2,"💀2")]
    for i,(qm,qc,lbl) in enumerate(quick):
        with qcols[i]:
            if st.button(lbl, key=f"q{i}", use_container_width=True):
                make_move(qm, qc)
                st.rerun()

else:
    if st.button("🔄 Play Again", use_container_width=True):
        init_state()
        st.rerun()

# ─── Move history ─────────────────────────────────────────────────────────────
if s.history:
    st.markdown("**📋 Move History**")
    history_html = "<div class='move-history'>" + "<br>".join(reversed(s.history)) + "</div>"
    st.markdown(history_html, unsafe_allow_html=True)

st.markdown(f"<center style='color:#4a7a9b;font-size:0.8rem;margin-top:20px;'>Moves: {s.move_count} | 🧑‍⚖️ = Missionary &nbsp; 💀 = Cannibal</center>", unsafe_allow_html=True)
