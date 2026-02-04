import streamlit as st
import streamlit.components.v1 as components
import random

# ページ設定
st.set_page_config(
    page_title="のんびりカニカニ観察日記",
    page_icon="🦀",
    layout="wide",
)

st.title("🦀 のんびりカニカニ観察日記")
st.write("穴から出たり入ったり、たまにハサミをチョキチョキしてるカニさんを眺めるアプリだっち🍄")

# カニの数（穴の数）
NUM_CRABS = 12

# CSSとHTMLを生成する関数
def render_crab_beach():
    
    # Pythonでランダムな動き（アニメーションの開始時間や速度）を生成
    crab_divs = ""
    for i in range(NUM_CRABS):
        # 出現するタイミングをずらす (0秒〜5秒の遅延)
        delay = random.uniform(0, 5)
        # 出現している時間（アニメーション全体の長さ）を少しばらつかせる
        duration = random.uniform(4, 7)
        # チョキチョキするタイミングもずらす
        snip_delay = random.uniform(0, 2)
        
        # 穴とカニのHTMLを作成
        # styleタグの中に直接Pythonの変数を埋め込んで、個体差を出す
        crab_divs += f"""
        <div class="hole-container">
            <div class="hole"></div>
            <div class="crab-wrapper" style="animation-delay: -{delay}s; animation-duration: {duration}s;">
                <div class="crab" style="animation-delay: -{snip_delay}s;">🦀</div>
            </div>
        </div>
        """

    # 全体のHTML/CSS
    html_code = f"""
    <style>
        /* 砂浜の背景 */
        .beach-container {{
            background-color: #fceeb5; /* 砂色 */
            padding: 40px;
            border-radius: 20px;
            display: flex;
            flex-wrap: wrap;
            justify-content: center;
            gap: 40px; /* 穴同士の間隔 */
            box-shadow: inset 0 0 20px rgba(196, 164, 132, 0.5);
        }}

        /* 穴とカニを包むコンテナ */
        .hole-container {{
            position: relative;
            width: 80px;
            height: 80px;
            display: flex;
            justify-content: center;
            align-items: flex-end; /* 下揃え */
        }}

        /* 穴の見た目 */
        .hole {{
            position: absolute;
            bottom: 0;
            width: 80px;
            height: 30px;
            background-color: #5c4033;
            border-radius: 50%;
            z-index: 1; /* カニより手前か奥か...今回は穴が一番奥、カニが出る感じにするので調整 */
        }}

        /* カニを上下させるラッパー */
        .crab-wrapper {{
            position: absolute;
            bottom: 10px; /* 穴の底 */
            z-index: 2; /* 穴より手前 */
            animation-name: peek;
            animation-timing-function: ease-in-out;
            animation-iteration-count: infinite;
        }}

        /* カニ本体（チョキチョキ担当） */
        .crab {{
            font-size: 50px;
            user-select: none;
            animation-name: snip;
            animation-duration: 1.5s;
            animation-iteration-count: infinite;
            transform-origin: center bottom;
        }}

        /* 上下に出たり入ったりするアニメーション */
        @keyframes peek {{
            0%, 10% {{ transform: translateY(100%); opacity: 0; }} /* 穴の中 */
            20% {{ opacity: 1; }}
            30%, 70% {{ transform: translateY(-10px); opacity: 1; }} /* 顔を出している時間 */
            80% {{ opacity: 1; }}
            90%, 100% {{ transform: translateY(100%); opacity: 0; }} /* 戻る */
        }}

        /* 左右に揺れてチョキチョキしてる風のアニメーション */
        @keyframes snip {{
            0%, 100% {{ transform: rotate(-5deg) scale(1); }}
            50% {{ transform: rotate(5deg) scale(1.1); }}
        }}
    </style>

    <div class="beach-container">
        {crab_divs}
    </div>
    """
    
    # Streamlitに埋め込み（スクロールバーが出ないように高さを確保）
    components.html(html_code, height=600, scrolling=True)

# 実行
render_crab_beach()

# リロードボタン（配置を変えるため）
if st.button("配置をシャッフルするカニ🦀"):
    st.rerun()
