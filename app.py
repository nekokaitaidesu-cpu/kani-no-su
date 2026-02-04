import streamlit as st
import streamlit.components.v1 as components

# ページ設定
st.set_page_config(page_title="カニカニ・ミニライフ")

# JavaScriptとCSSを組み合わせたHTML
html_code = """
<!DOCTYPE html>
<html lang="ja">
<head>
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<style>
  /* スマホ画面全体の設定 */
  body {
    margin: 0;
    overflow: hidden;
    background-color: #f6d7b0;
    background-image: 
      radial-gradient(circle at 50% 50%, #e6c288 1px, transparent 1px),
      radial-gradient(circle at 20% 80%, #dcb 1px, transparent 1px);
    background-size: 20px 20px, 30px 30px;
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
    width: 100vw;
    touch-action: none;
  }

  .beach-scene {
    position: relative;
    width: 100%;
    height: 100%;
    max-width: 430px;
    max-height: 900px;
  }

  /* --- 穴 (サイズを縮小、配置を%に変更) --- */
  .hole {
    position: absolute;
    bottom: 20%; /* 画面下から20%の位置 */
    left: 50%;
    transform: translateX(-50%);
    width: 70px; /* サイズ縮小 */
    height: 20px;
    background-color: #4a3b2a;
    border-radius: 50%;
    box-shadow: inset 0 3px 6px rgba(0,0,0,0.6);
    z-index: 10;
  }

  /* カニのステージ (穴の位置に合わせる) */
  .crab-stage {
    position: absolute;
    bottom: 20%; /* 穴と同じ位置 */
    left: 50%;
    transform: translateX(-50%);
    width: 80px; /* サイズ縮小 */
    height: 150px; /* 潜るための深さを確保 */
    overflow: hidden;
    z-index: 11;
    pointer-events: none;
    /* background: rgba(255,0,0,0.2); デバッグ用 */
  }

  /* カニコンテナ (サイズ縮小) */
  .crab-container {
    position: absolute;
    top: 150px; /* 初期位置：ステージの底 */
    left: 50%;
    width: 60px; /* カニの幅 */
    height: 50px; /* カニの高さ */
    margin-left: -30px; /* 中心合わせ */
    
    /* アニメーション設定 */
    transition: top 1.5s cubic-bezier(0.5, 0, 0.5, 1), left 1.5s linear;
    z-index: 20;
  }

  /* --- アクション用クラス --- */
  .crab-container.snipping .claw.left::after { animation: snip-left 0.2s infinite alternate; }
  .crab-container.snipping .claw.right::after { animation: snip-right 0.2s infinite alternate; }
  .crab-container.walking .leg.L1 { animation: walk-leg 0.3s infinite alternate; }
  .crab-container.walking .leg.R1 { animation: walk-leg 0.3s infinite alternate 0.15s; }
  .crab-container.walking .leg.L2 { animation: walk-leg 0.3s infinite alternate 0.15s; }
  .crab-container.walking .leg.R2 { animation: walk-leg 0.3s infinite alternate; }
  .crab-container.walking .body { animation: walk-body 0.3s infinite alternate; }


  /* --- カニのパーツ (全体的にサイズを約半分に縮小) --- */
  .body {
    position: absolute; bottom: 0;
    width: 60px; height: 40px;
    background-color: #ff6b6b; border-radius: 50% 50% 40% 40%; border: 2px solid #c0392b; box-shadow: inset -3px -3px 6px rgba(0,0,0,0.1);
  }
  .eye-stalk { position: absolute; top: -10px; width: 3px; height: 15px; background-color: #c0392b; transition: transform 0.3s; }
  .eye-stalk.left { left: 15px; transform: rotate(-15deg); } .eye-stalk.right { right: 15px; transform: rotate(15deg); }
  .eye { position: absolute; top: -12px; width: 10px; height: 10px; background-color: white; border-radius: 50%; border: 1px solid #c0392b; }
  .eye::after { content: ''; position: absolute; top: 2px; left: 2px; width: 4px; height: 4px; background-color: black; border-radius: 50%; animation: blink 4s infinite; }
  .eye.left { left: 12px; } .eye.right { right: 12px; }
  
  .claw { position: absolute; top: 5px; width: 20px; height: 15px; border: 2px solid #c0392b; background-color: #ff6b6b; border-radius: 50% 50% 10% 10%; transform-origin: bottom center; transition: transform 0.3s; }
  .claw.left { left: -12px; transform: rotate(-30deg); }
  .claw.left::after { content: ''; position: absolute; top: -8px; left: 0; width: 12px; height: 15px; background-color: #ff6b6b; border: 2px solid #c0392b; border-radius: 50% 10% 0 0; transform: rotate(-20deg); transform-origin: bottom right; }
  .claw.right { right: -12px; transform: rotate(30deg); }
  .claw.right::after { content: ''; position: absolute; top: -8px; right: 0; width: 12px; height: 15px; background-color: #ff6b6b; border: 2px solid #c0392b; border-radius: 10% 50% 0 0; transform: rotate(20deg); transform-origin: bottom left; }
  
  .leg { position: absolute; bottom: 5px; width: 12px; height: 3px; background-color: #c0392b; border-radius: 3px; transform-origin: right center;}
  .leg.left { transform-origin: right center; } .leg.right { transform-origin: left center; }
  .leg.L1 { left: -8px; transform: rotate(-20deg); }
  .leg.L2 { left: -2px; bottom: 3px; transform: rotate(-10deg); }
  .leg.R1 { right: -8px; transform: rotate(20deg); }
  .leg.R2 { right: -2px; bottom: 3px; transform: rotate(10deg); }


  /* --- 貝殻 (サイズ縮小) --- */
  .shell { position: absolute; width: 25px; height: 20px; background: repeating-linear-gradient(90deg, #fff0f5 0px, #fff0f5 2px, #ffc1e3 3px, #ffc1e3 4px); border-radius: 50% 50% 10% 10%; box-shadow: 1px 1px 3px rgba(0,0,0,0.2); z-index: 5; }
  .shell::after { content: ''; position: absolute; bottom: -3px; left: 50%; transform: translateX(-50%); width: 6px; height: 4px; background-color: #ffc1e3; border-radius: 2px; }
  .shell-spiral { position: absolute; width: 0; height: 0; border-left: 6px solid transparent; border-right: 6px solid transparent; border-bottom: 25px solid #fff; border-radius: 50%; transform: rotate(45deg); filter: drop-shadow(1px 1px 2px rgba(0,0,0,0.2)); z-index: 5; }
  .shell-spiral::before { content: ''; position: absolute; top: 12px; left: -6px; width: 12px; height: 12px; background-color: #eee; border-radius: 50%; }

  /* --- アニメーション定義 --- */
  @keyframes snip-left { from { transform: rotate(-10deg); } to { transform: rotate(-40deg); } }
  @keyframes snip-right { from { transform: rotate(10deg); } to { transform: rotate(40deg); } }
  @keyframes blink { 0%, 96%, 100% { transform: scaleY(1); } 98% { transform: scaleY(0.1); } }
  @keyframes walk-leg { from { transform: rotate(-15deg); } to { transform: rotate(15deg); } }
  @keyframes walk-body { from { transform: translateY(0); } to { transform: translateY(-2px); } }

</style>
</head>
<body>

<div class="beach-scene">
  <div class="shell" style="top: 20%; left: 15%; transform: rotate(-20deg);"></div>
  <div class="shell" style="top: 10%; left: 75%; transform: rotate(10deg); background: repeating-linear-gradient(90deg, #fff 0px, #fff 2px, #aee 3px, #aee 4px);"></div>
  <div class="shell-spiral" style="top: 40%; left: 85%; transform: rotate(60deg);"></div>
  <div class="shell-spiral" style="top: 5%; left: 30%; transform: rotate(-30deg);"></div>
  <div class="shell" style="top: 30%; left: 50%; transform: rotate(180deg); opacity: 0.8;"></div>
  <div class="shell" style="top: 55%; left: 10%; transform: rotate(45deg); background: repeating-linear-gradient(90deg, #fff 0px, #fff 2px, #eec 3px, #eec 4px);"></div>
  <div class="shell-spiral" style="top: 65%; left: 70%; transform: rotate(-90deg) scale(0.8);"></div>

  <div class="hole"></div>
    
  <div id="stage" class="crab-stage">
    <div id="crab" class="crab-container">
      <div class="leg left L1"></div>
      <div class="leg right R1"></div>
      <div class="leg left L2"></div>
      <div class="leg right R2"></div>
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

<script>
  const crab = document.getElementById('crab');
  const stage = document.getElementById('stage');
  
  let mode = 'HOLE';
  
  // 座標設定 (%)
  const HOLE_X = 50;
  const HOLE_Y = 80; // bottom: 20% なので、上からは 80% の位置

  // 穴の中での相対位置 (px, stage基準)
  const POS_HIDDEN_Y = '150px'; // 奥底
  const POS_PEEK_Y   = '100px'; // ちょい出し
  const POS_GROUND_Y = '0px';   // 地上（stageの上端）

  setTimeout(decideNextAction, 1000);

  function decideNextAction() {
    let delay = 1000;

    if (mode === 'HOLE') {
      const dice = Math.random();
      if (dice < 0.4) {
        // ①キョロキョロ
        console.log("Action: Peek");
        crab.style.top = POS_PEEK_Y;
        delay = 2000 + Math.random() * 1500;
        setTimeout(() => { if(mode==='HOLE') crab.style.top = POS_HIDDEN_Y; }, delay - 500);
      
      } else if (dice < 0.7) {
        // ②出てくる -> 砂浜モードへ
        console.log("Action: Exit Hole");
        crab.style.top = POS_GROUND_Y;
        
        setTimeout(() => {
          stage.style.overflow = 'visible'; 
          // 座標系を「穴の中の相対座標」から「画面全体の%座標」へ変換
          crab.style.top = `${HOLE_Y}%`;
          crab.style.left = `${HOLE_X}%`;
          mode = 'BEACH';
          decideNextAction(); 
        }, 1500);
        return;

      } else {
        // ③隠れる
        console.log("Action: Hide");
        crab.style.top = POS_HIDDEN_Y;
        delay = 2000;
      }

    } else if (mode === 'BEACH') {
      const dice = Math.random();
      if (dice < 0.2) {
        // ①じっとする
        console.log("Action: Stay");
        delay = 1000 + Math.random() * 1500;

      } else if (dice < 0.6) {
        // ②ランダム移動 (範囲を拡大！)
        console.log("Action: Move Random");
        moveRandom();
        delay = 4000;

      } else if (dice < 0.8) {
        // ④チョキチョキ
        console.log("Action: Snip");
        crab.classList.add('snipping');
        delay = 1500;
        setTimeout(() => { crab.classList.remove('snipping'); }, delay);

      } else {
        // ⑤帰宅 (修正版)
        console.log("Action: Return Home");
        returnHome();
        return; 
      }
    }
    setTimeout(decideNextAction, delay);
  }

  // ランダム移動 (範囲拡大)
  function moveRandom() {
    crab.classList.add('walking');
    // 画面全体 (0%〜100%) を移動範囲に設定
    const targetX = Math.random() * 100;
    const targetY = Math.random() * 80; // 穴より下には行かないように調整

    crab.style.left = `${targetX}%`;
    crab.style.top = `${targetY}%`;

    setTimeout(() => {
        crab.classList.remove('walking');
    }, 3500);
  }

  // 帰宅関数 (修正版：穴の上まで歩いてから潜る)
  function returnHome() {
    crab.classList.add('walking');

    // 1. まず穴の真上 (HOLE_X, HOLE_Y) に向かって歩く
    crab.style.left = `${HOLE_X}%`;
    crab.style.top = `${HOLE_Y}%`;

    // 移動完了後
    setTimeout(() => {
      crab.classList.remove('walking'); // 歩き終了

      // 2. 座標系を「穴の中モード」に切り替える
      // 見た目の位置が変わらないように、stageの上端 (POS_GROUND_Y) に配置
      crab.style.top = POS_GROUND_Y;
      crab.style.left = '50%';
      stage.style.overflow = 'hidden'; // マスク有効化
      mode = 'HOLE';
      
      // 3. 少し待ってから穴の奥底へ潜るアニメーション
      setTimeout(() => {
          crab.style.top = POS_HIDDEN_Y;
          setTimeout(decideNextAction, 2000); // 次のループへ
      }, 100);

    }, 3500); // 帰宅の移動時間
  }

</script>
</body>
</html>
"""

# HTMLを描画
components.html(html_code, height=900)
