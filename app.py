import streamlit as st
import streamlit.components.v1 as components

# ページ設定（スマホライクな縦長レイアウトを意識）
st.set_page_config(page_title="ミニカニ・ライフ", layout="centered")

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
    overflow: hidden; /* スクロール禁止 */
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

  /* フィールド */
  .beach-scene {
    position: relative;
    width: 100%;
    height: 100%;
    max-width: 430px;
    max-height: 932px;
  }

  /* --- 穴（サイズを約半分に縮小＆配置基準を上からに変更） --- */
  .hole {
    position: absolute;
    top: 85%; /* 画面上から85%の位置（ここが中心） */
    left: 50%;
    transform: translate(-50%, -50%); /* 中心合わせ */
    width: 60px;  /* 120px -> 60px */
    height: 18px; /* 35px -> 18px */
    background-color: #4a3b2a;
    border-radius: 50%;
    box-shadow: inset 0 3px 6px rgba(0,0,0,0.6);
    z-index: 10;
  }

  /* カニステージ（マスク用。サイズと配置を調整） */
  .crab-stage {
    position: absolute;
    top: 85%; /* 穴と同じ基準点 */
    left: 50%;
    transform: translate(-50%, -50%); /* 中心合わせ */
    width: 80px; /* カニが収まるサイズ */
    height: 80px;
    overflow: hidden; /* 初期は隠す */
    z-index: 11;
    pointer-events: none;
    /* border: 1px solid blue; デバッグ用 */
  }

  /* カニコンテナ（動く箱。サイズを半分に） */
  .crab-container {
    position: absolute;
    top: 80px; /* 初期位置：ステージの底 */
    left: 50%;
    width: 50px;  /* 100px -> 50px */
    height: 40px; /* 80px -> 40px */
    margin-left: -25px; /* 中心合わせ */
    
    /* アニメーション設定 */
    transition: top 1.5s cubic-bezier(0.5, 0, 0.5, 1), left 1.5s linear;
    z-index: 20;
  }

  /* --- アクション用クラス --- */
  /* チョキチョキ（そのまま） */
  .crab-container.snipping .claw.left::after { animation: snip-left 0.2s infinite alternate; }
  .crab-container.snipping .claw.right::after { animation: snip-right 0.2s infinite alternate; }

  /* ★変更★ 歩きモーション（足だけ動かす） */
  .crab-container.walking .leg.L1 { animation: walk-leg 0.3s infinite alternate; }
  .crab-container.walking .leg.R1 { animation: walk-leg 0.3s infinite alternate 0.15s; }
  .crab-container.walking .leg.L2 { animation: walk-leg 0.3s infinite alternate 0.15s; }
  .crab-container.walking .leg.R2 { animation: walk-leg 0.3s infinite alternate; }
  /* 体の揺れ（walk-body）は削除したっち */


  /* --- カニのパーツ（全てサイズを約半分に！） --- */
  .body {
    position: absolute; bottom: 0;
    width: 50px; height: 33px;
    background-color: #ff6b6b; border-radius: 50% 50% 40% 40%; border: 2px solid #c0392b; box-shadow: inset -2px -2px 5px rgba(0,0,0,0.1);
  }
  .eye-stalk { position: absolute; top: -8px; width: 3px; height: 10px; background-color: #c0392b; transition: transform 0.3s; }
  .eye-stalk.left { left: 12px; transform: rotate(-15deg); } .eye-stalk.right { right: 12px; transform: rotate(15deg); }
  .eye { position: absolute; top: -10px; width: 8px; height: 8px; background-color: white; border-radius: 50%; border: 1px solid #c0392b; }
  .eye::after { content: ''; position: absolute; top: 2px; left: 2px; width: 4px; height: 4px; background-color: black; border-radius: 50%; animation: blink 4s infinite; }
  .eye.left { left: 9px; } .eye.right { right: 9px; }
  
  .claw { position: absolute; top: 3px; width: 16px; height: 12px; border: 2px solid #c0392b; background-color: #ff6b6b; border-radius: 50% 50% 10% 10%; transform-origin: bottom center; transition: transform 0.3s; }
  .claw.left { left: -10px; transform: rotate(-30deg); }
  .claw.left::after { content: ''; position: absolute; top: -6px; left: 0; width: 10px; height: 12px; background-color: #ff6b6b; border: 2px solid #c0392b; border-radius: 50% 10% 0 0; transform: rotate(-20deg); transform-origin: bottom right; }
  .claw.right { right: -10px; transform: rotate(30deg); }
  .claw.right::after { content: ''; position: absolute; top: -6px; right: 0; width: 10px; height: 12px; background-color: #ff6b6b; border: 2px solid #c0392b; border-radius: 10% 50% 0 0; transform: rotate(20deg); transform-origin: bottom left; }
  
  .leg { position: absolute; bottom: 4px; width: 10px; height: 3px; background-color: #c0392b; border-radius: 3px; transform-origin: right center;}
  .leg.left { transform-origin: right center; } .leg.right { transform-origin: left center; }
  .leg.L1 { left: -8px; transform: rotate(-20deg); }
  .leg.L2 { left: -3px; bottom: 2px; transform: rotate(-10deg); }
  .leg.R1 { right: -8px; transform: rotate(20deg); }
  .leg.R2 { right: -3px; bottom: 2px; transform: rotate(10deg); }


  /* --- 貝殻（サイズを半分に） --- */
  .shell { position: absolute; width: 18px; height: 15px; background: repeating-linear-gradient(90deg, #fff0f5 0px, #fff0f5 2px, #ffc1e3 3px, #ffc1e3 4px); border-radius: 50% 50% 10% 10%; box-shadow: 1px 1px 3px rgba(0,0,0,0.2); z-index: 5; }
  .shell::after { content: ''; position: absolute; bottom: -2px; left: 50%; transform: translateX(-50%); width: 4px; height: 3px; background-color: #ffc1e3; border-radius: 2px; }
  .shell-spiral { position: absolute; width: 0; height: 0; border-left: 4px solid transparent; border-right: 4px solid transparent; border-bottom: 18px solid #fff; border-radius: 50%; transform: rotate(45deg); filter: drop-shadow(1px 1px 2px rgba(0,0,0,0.2)); z-index: 5; }
  .shell-spiral::before { content: ''; position: absolute; top: 9px; left: -4px; width: 8px; height: 8px; background-color: #eee; border-radius: 50%; }

  /* --- アニメーション定義 --- */
  @keyframes snip-left { from { transform: rotate(-10deg); } to { transform: rotate(-40deg); } }
  @keyframes snip-right { from { transform: rotate(10deg); } to { transform: rotate(40deg); } }
  @keyframes blink { 0%, 96%, 100% { transform: scaleY(1); } 98% { transform: scaleY(0.1); } }
  @keyframes walk-leg { from { transform: rotate(-10deg); } to { transform: rotate(10deg); } }
  /* 体の揺れアニメーションは削除 */

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
      <div class="leg left L1"></div><div class="leg right R1"></div>
      <div class="leg left L2"></div><div class="leg right R2"></div>
      <div class="claw left"></div><div class="claw right"></div>
      <div class="body"></div>
      <div class="eye-stalk left"></div><div class="eye-stalk right"></div>
      <div class="eye left"></div><div class="eye right"></div>
    </div>
  </div>
</div>

<script>
  const crab = document.getElementById('crab');
  const stage = document.getElementById('stage');
  
  let mode = 'HOLE';
  
  // 穴の中心座標（画面上の%）
  const HOLE_X = 50;
  const HOLE_Y = 85; // CSSのtop指定と一致させる

  // 穴モードでの相対位置 (px) - サイズ縮小に合わせて調整
  const POS_HIDDEN_Y = '80px'; // ステージの底
  const POS_PEEK_Y   = '50px'; // キョロキョロ位置
  const POS_GROUND_Y = '10px'; // 穴の入り口（ステージ上端付近）

  setTimeout(decideNextAction, 1000);

  function decideNextAction() {
    let delay = 1000;

    if (mode === 'HOLE') {
      // --- 穴モード ---
      const dice = Math.random();
      if (dice < 0.4) {
        // ①キョロキョロ
        crab.style.top = POS_PEEK_Y;
        delay = 2000 + Math.random() * 1500;
        setTimeout(() => { if(mode==='HOLE') crab.style.top = POS_HIDDEN_Y; }, delay - 500);
      
      } else if (dice < 0.7) {
        // ②出てくる
        crab.style.top = POS_GROUND_Y; // まず穴の入り口まで上がる
        
        setTimeout(() => {
          stage.style.overflow = 'visible'; // マスク解除
          // 座標系を「穴の中」から「砂浜全体」へ切り替え
          crab.style.top = `${HOLE_Y}%`;
          crab.style.left = `${HOLE_X}%`;
          
          mode = 'BEACH';
          decideNextAction(); 
        }, 1500);
        return;

      } else {
        // ③隠れる
        crab.style.top = POS_HIDDEN_Y;
        delay = 2000;
      }

    } else if (mode === 'BEACH') {
      // --- 砂浜モード ---
      const dice = Math.random();

      if (dice < 0.2) {
        // ①じっとする
        delay = 1000 + Math.random() * 1500;

      } else if (dice < 0.6) {
        // ②ランダム移動（範囲拡大！）
        moveRandom();
        delay = 3500;

      } else if (dice < 0.8) {
        // ④チョキチョキ
        crab.classList.add('snipping');
        delay = 1500;
        setTimeout(() => { crab.classList.remove('snipping'); }, delay);

      } else {
        // ⑤帰宅
        returnHome();
        return; 
      }
    }
    setTimeout(decideNextAction, delay);
  }

  // 全方向ランダム移動
  function moveRandom() {
    crab.classList.add('walking');
    // ★変更★ 移動範囲を画面の上の方まで拡大 (5%〜95%)
    const targetX = 5 + Math.random() * 90; 
    const targetY = 5 + Math.random() * 90; 

    crab.style.left = `${targetX}%`;
    crab.style.top = `${targetY}%`;

    setTimeout(() => {
        crab.classList.remove('walking');
    }, 3000);
  }

  // ★変更★ 帰宅アクションを改善
  function returnHome() {
    crab.classList.add('walking');

    // 1. まず穴の真上（中心）まで歩いて戻る
    crab.style.left = `${HOLE_X}%`;
    crab.style.top = `${HOLE_Y}%`;

    // 移動完了を待つ
    setTimeout(() => {
      crab.classList.remove('walking'); // 歩き終了

      // 2. 座標系を「砂浜全体」から「穴の中」へ切り替える
      // 穴の真上は、穴モードでの「入り口(POS_GROUND_Y)」と同じ位置
      crab.style.left = '50%';
      crab.style.top = POS_GROUND_Y;
      
      // 3. マスクを有効にする（ここから体が隠れ始める）
      stage.style.overflow = 'hidden'; 
      mode = 'HOLE';
      
      // 4. 一呼吸おいてから、穴の底へ潜る
      setTimeout(() => {
          crab.style.top = POS_HIDDEN_Y; 
          setTimeout(decideNextAction, 2000); // 次の行動へ
      }, 100); 

    }, 3000); // 帰宅の移動時間
  }

</script>
</body>
</html>
"""

# HTMLを描画（高さはスマホ画面を想定して大きめに）
components.html(html_code, height=932)
