import streamlit as st
import streamlit.components.v1 as components

# ページ設定
st.set_page_config(page_title="ちびカニ・ピークアブー", layout="centered")

st.title("🦀 ちびカニさんが…ぴょこん！")
st.write("小さくなったカニさんが、穴からこっそり様子をうかがってるっち🍄")
st.write("（じーっと見てると、出てきてチョキチョキするよ！）")

# CSSアートとアニメーションを含んだHTML
html_code = """
<!DOCTYPE html>
<html lang="ja">
<head>
<style>
  body {
    background-color: #f0f2f6;
    display: flex;
    justify-content: center;
    align-items: center;
    height: 150px; /* 全体の高さを小さく調整 */
    margin: 0;
    overflow: hidden;
  }

  /* 描画エリア */
  .scene {
    position: relative;
    width: 300px;
    height: 300px;
    /* ★ここが魔法の呪文！★ */
    /* 全体を約1/3のサイズに縮小するだっち */
    transform: scale(0.333);
    /* 縮小の中心点を真ん中の下の方に合わせる */
    transform-origin: center 70%;
  }

  /* 穴（黒い背景） */
  .hole {
    position: absolute;
    bottom: 80px;
    left: 50%;
    transform: translateX(-50%);
    width: 140px;
    height: 40px;
    background-color: #333;
    border-radius: 50%;
    box-shadow: inset 0 5px 10px rgba(0,0,0,0.5);
    z-index: 1;
  }

  /* カニさんのステージ（この枠より下に行くと消える） */
  .crab-stage {
    position: absolute;
    bottom: 100px;
    left: 50%;
    transform: translateX(-50%);
    width: 200px;
    height: 300px;
    overflow: hidden;
    z-index: 2;
    pointer-events: none;
  }

  /* カニ全体コンテナ */
  .crab-container {
    position: absolute;
    top: 100%;
    left: 50%;
    transform: translateX(-50%);
    width: 120px;
    height: 100px;
    /* アニメーション設定 */
    animation: peekaboo 8s cubic-bezier(0.68, -0.55, 0.27, 1.55) infinite;
  }

  /* カニの体 */
  .body {
    position: absolute;
    bottom: 0;
    width: 120px;
    height: 80px;
    background-color: #ff6b6b;
    border-radius: 50% 50% 40% 40%;
    border: 3px solid #c0392b;
    box-shadow: inset -5px -5px 10px rgba(0,0,0,0.1);
  }

  /* 目（茎の部分） */
  .eye-stalk {
    position: absolute;
    top: -20px;
    width: 6px;
    height: 25px;
    background-color: #c0392b;
  }
  .eye-stalk.left { left: 30px; transform: rotate(-15deg); }
  .eye-stalk.right { right: 30px; transform: rotate(15deg); }

  /* 目（玉の部分） */
  .eye {
    position: absolute;
    top: -25px;
    width: 16px;
    height: 16px;
    background-color: white;
    border-radius: 50%;
    border: 2px solid #c0392b;
  }
  .eye::after { /* 黒目 */
    content: '';
    position: absolute;
    top: 4px;
    left: 4px;
    width: 6px;
    height: 6px;
    background-color: black;
    border-radius: 50%;
    animation: blink 4s infinite;
  }
  .eye.left { left: 24px; }
  .eye.right { right: 24px; }

  /* ハサミ */
  .claw {
    position: absolute;
    top: 10px;
    width: 35px;
    height: 25px;
    border: 3px solid #c0392b;
    background-color: #ff6b6b;
    border-radius: 50% 50% 10% 10%;
    transform-origin: bottom center;
  }
  
  /* 左ハサミ */
  .claw.left {
    left: -25px;
    transform: rotate(-30deg);
  }
  .claw.left::after {
    content: '';
    position: absolute;
    top: -15px;
    left: 0;
    width: 20px;
    height: 25px;
    background-color: #ff6b6b;
    border: 3px solid #c0392b;
    border-radius: 50% 10% 0 0;
    transform: rotate(-20deg);
    transform-origin: bottom right;
    animation: snip-left 0.5s infinite alternate;
  }

  /* 右ハサミ */
  .claw.right {
    right: -25px;
    transform: rotate(30deg);
  }
  .claw.right::after {
    content: '';
    position: absolute;
    top: -15px;
    right: 0;
    width: 20px;
    height: 25px;
    background-color: #ff6b6b;
    border: 3px solid #c0392b;
    border-radius: 10% 50% 0 0;
    transform: rotate(20deg);
    transform-origin: bottom left;
    animation: snip-right 0.5s infinite alternate;
  }

  /* 足 */
  .leg {
    position: absolute;
    bottom: 10px;
    width: 20px;
    height: 5px;
    background-color: #c0392b;
    border-radius: 5px;
  }
  .leg.left { left: -10px; transform: rotate(-20deg); }
  .leg.right { right: -10px; transform: rotate(20deg); }


  /* --- アニメーション定義 --- */
  @keyframes peekaboo {
    0% { top: 100%; }
    10% { top: 100%; }
    30% { top: 10px; }
    35% { top: 20px; }
    40% { top: 15px; }
    65% { top: 15px; }
    75% { top: 100%; }
    100% { top: 100%; }
  }
  @keyframes snip-left { from { transform: rotate(-10deg); } to { transform: rotate(-40deg); } }
  @keyframes snip-right { from { transform: rotate(10deg); } to { transform: rotate(40deg); } }
  @keyframes blink { 0%, 96%, 100% { transform: scaleY(1); } 98% { transform: scaleY(0.1); } }

</style>
</head>
<body>

<div class="scene">
  <div class="hole"></div>
  <div class="crab-stage">
    <div class="crab-container">
      <div class="leg left" style="bottom: 20px; left: -15px;"></div>
      <div class="leg right" style="bottom: 20px; right: -15px;"></div>
      <div class="leg left"></div>
      <div class="leg right"></div>
      <div class="claw left"></div>
      <div class="claw right"></div>
      <div class="body"></div>
      <div class="eye-stalk left"></div>
      <div class="eye-stalk right"></div>
      <div class="eye left"></div>
      <div class="eye right"></div>
    </div>
  </div>
</div>

</body>
</html>
"""

# HTMLを描画 (高さを小さく調整)
components.html(html_code, height=170)
