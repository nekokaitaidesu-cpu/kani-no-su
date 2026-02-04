import streamlit as st
import streamlit.components.v1 as components

# ページ設定（ワイドモードにして広々と！）
st.set_page_config(page_title="カニカニ・ビーチ", layout="wide")

st.title("🏖️ 砂浜にカニが一匹…")
st.write("広～い砂浜になったっち！貝殻も落ちてるね🐚")
st.write("（カニさんは相変わらず穴の中に隠れてるみたい…じっと見てみてね🍄）")

# CSSアートとアニメーションを含んだHTML
html_code = """
<!DOCTYPE html>
<html lang="ja">
<head>
<style>
  body {
    margin: 0;
    overflow: hidden;
    background-color: #f6d7b0; /* 砂の色 */
    /* 砂の粒々感を出すためのノイズ */
    background-image: 
      radial-gradient(circle at 50% 50%, #e6c288 1px, transparent 1px),
      radial-gradient(circle at 20% 80%, #dcb 1px, transparent 1px);
    background-size: 20px 20px, 30px 30px;
    display: flex;
    justify-content: center;
    align-items: center;
    height: 400px; /* 表示エリアの高さ */
  }

  /* ★広いフィールドの設定★
     全体を大きく作って、transform: scale() でキュッと縮小して表示する作戦だっち！
     こうすると、パーツの配置は大きな座標で考えられるから楽なんだっち。
  */
  .beach-scene {
    position: relative;
    width: 1000px; /* 横に広ーく！ */
    height: 400px;
    transform: scale(0.5); /* 全体を0.5倍（小さめ）で表示 */
    transform-origin: center center;
  }

  /* --- ここからカニ＆穴セット（中央配置） --- */
  .crab-home {
    position: absolute;
    bottom: 50px;
    left: 50%;
    transform: translateX(-50%);
    width: 300px;
    height: 300px;
  }

  /* 穴 */
  .hole {
    position: absolute;
    bottom: 80px;
    left: 50%;
    transform: translateX(-50%);
    width: 140px;
    height: 40px;
    background-color: #4a3b2a; /* 砂浜に合わせて少し茶色っぽく */
    border-radius: 50%;
    box-shadow: inset 0 5px 10px rgba(0,0,0,0.6);
    z-index: 10;
  }

  /* カニさんが出入りするステージ（マスク用） */
  .crab-stage {
    position: absolute;
    bottom: 100px;
    left: 50%;
    transform: translateX(-50%);
    width: 200px;
    height: 300px;
    overflow: hidden; /* 下にはみ出たら消える */
    z-index: 11;
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
    animation: peekaboo 8s cubic-bezier(0.68, -0.55, 0.27, 1.55) infinite;
  }

  /* カニのパーツ（前回と同じ） */
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
  .eye-stalk { position: absolute; top: -20px; width: 6px; height: 25px; background-color: #c0392b; }
  .eye-stalk.left { left: 30px; transform: rotate(-15deg); }
  .eye-stalk.right { right: 30px; transform: rotate(15deg); }
  .eye { position: absolute; top: -25px; width: 16px; height: 16px; background-color: white; border-radius: 50%; border: 2px solid #c0392b; }
  .eye::after { content: ''; position: absolute; top: 4px; left: 4px; width: 6px; height: 6px; background-color: black; border-radius: 50%; animation: blink 4s infinite; }
  .eye.left { left: 24px; } .eye.right { right: 24px; }
  .claw { position: absolute; top: 10px; width: 35px; height: 25px; border: 3px solid #c0392b; background-color: #ff6b6b; border-radius: 50% 50% 10% 10%; transform-origin: bottom center; }
  .claw.left { left: -25px; transform: rotate(-30deg); }
  .claw.left::after { content: ''; position: absolute; top: -15px; left: 0; width: 20px; height: 25px; background-color: #ff6b6b; border: 3px solid #c0392b; border-radius: 50% 10% 0 0; transform: rotate(-20deg); transform-origin: bottom right; animation: snip-left 0.5s infinite alternate; }
  .claw.right { right: -25px; transform: rotate(30deg); }
  .claw.right::after { content: ''; position: absolute; top: -15px; right: 0; width: 20px; height: 25px; background-color: #ff6b6b; border: 3px solid #c0392b; border-radius: 10% 50% 0 0; transform: rotate(20deg); transform-origin: bottom left; animation: snip-right 0.5s infinite alternate; }
  .leg { position: absolute; bottom: 10px; width: 20px; height: 5px; background-color: #c0392b; border-radius: 5px; }
  .leg.left { left: -10px; transform: rotate(-20deg); } .leg.right { right: -10px; transform: rotate(20deg); }


  /* --- 貝殻（CSSアート） --- */
  .shell {
    position: absolute;
    width: 40px;
    height: 35px;
    background: repeating-linear-gradient(
      90deg, 
      #fff0f5 0px, 
      #fff0f5 4px, 
      #ffc1e3 5px, 
      #ffc1e3 6px
    );
    border-radius: 50% 50% 10% 10%; /* 扇形 */
    box-shadow: 2px 2px 5px rgba(0,0,0,0.2);
  }
  /* 貝殻の根本のちょぼ */
  .shell::after {
    content: '';
    position: absolute;
    bottom: -5px;
    left: 50%;
    transform: translateX(-50%);
    width: 10px;
    height: 6px;
    background-color: #ffc1e3;
    border-radius: 2px;
  }

  /* 白い巻貝タイプ */
  .shell-spiral {
    position: absolute;
    width: 0;
    height: 0;
    border-left: 10px solid transparent;
    border-right: 10px solid transparent;
    border-bottom: 40px solid #fff;
    border-radius: 50%;
    transform: rotate(45deg);
    filter: drop-shadow(2px 2px 2px rgba(0,0,0,0.2));
  }
  .shell-spiral::before {
    content: '';
    position: absolute;
    top: 20px;
    left: -10px;
    width: 20px;
    height: 20px;
    background-color: #eee;
    border-radius: 50%;
  }

  /* --- アニメーション --- */
  @keyframes peekaboo {
    0% { top: 100%; } 10% { top: 100%; } 30% { top: 10px; } 35% { top: 20px; } 40% { top: 15px; } 65% { top: 15px; } 75% { top: 100%; } 100% { top: 100%; }
  }
  @keyframes snip-left { from { transform: rotate(-10deg); } to { transform: rotate(-40deg); } }
  @keyframes snip-right { from { transform: rotate(10deg); } to { transform: rotate(40deg); } }
  @keyframes blink { 0%, 96%, 100% { transform: scaleY(1); } 98% { transform: scaleY(0.1); } }

</style>
</head>
<body>

<div class="beach-scene">
  
  <div class="shell" style="top: 300px; left: 200px; transform: rotate(-20deg);"></div>
  <div class="shell" style="top: 150px; left: 800px; transform: rotate(10deg); background: repeating-linear-gradient(90deg, #fff 0px, #fff 4px, #aee 5px, #aee 6px);"></div>
  <div class="shell-spiral" style="top: 250px; left: 700px; transform: rotate(60deg);"></div>
  <div class="shell-spiral" style="top: 100px; left: 150px; transform: rotate(-30deg);"></div>
  <div class="shell" style="top: 350px; left: 600px; transform: rotate(180deg); opacity: 0.8;"></div>

  <div class="crab-home">
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

</div>

</body>
</html>
"""

# HTMLを描画
components.html(html_code, height=450)
