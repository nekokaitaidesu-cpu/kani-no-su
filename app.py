import streamlit as st
import streamlit.components.v1 as components

# ページ設定
st.set_page_config(page_title="カニカニ・パーフェクトライフ修正版", layout="centered")

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

  /* フィールド */
  .beach-scene {
    position: relative;
    width: 100%;
    height: 100%;
    max-width: 430px;
    max-height: 932px;
  }

  /* 穴 */
  .hole {
    position: absolute;
    top: 85%; /* 画面の下の方 */
    left: 50%;
    transform: translate(-50%, -50%); /* 中心合わせ */
    width: 70px; /* 少し広くした */
    height: 20px;
    background-color: #4a3b2a;
    border-radius: 50%;
    box-shadow: inset 0 3px 6px rgba(0,0,0,0.6);
    z-index: 10;
  }

  /* カニステージ（穴モード時のマスク領域） */
  .crab-stage {
    position: absolute;
    top: 85%; /* 穴の位置に合わせる */
    left: 50%;
    transform: translate(-50%, 0); /* 上端を穴の中心に合わせる */
    width: 80px;
    height: 100px; /* 下方向に伸ばす */
    overflow: hidden; /* この枠外（つまり穴の上）は表示、下に行くと隠れる...逆だ！
       穴に入るときは「穴より下」に行きたい。
       でも overflow: hidden は「枠の外」を消す。
       なので、ステージを「穴の上側」に配置して、下に移動したら消えるようにする？
       いや、今回は「マスク解除」方式を使ってるから、
       シンプルに「穴の周辺」を隠すマスクとして配置するね。
    */
    transform: translate(-50%, -50%); /* 中心を穴に合わせる */
    z-index: 11;
    pointer-events: none;
    /* background: rgba(255,0,0,0.2); デバッグ用：赤枠が見える */
  }

  /* カニコンテナ */
  .crab-container {
    position: absolute;
    /* 初期位置 */
    top: 150%; 
    left: 50%;
    width: 50px;
    height: 40px;
    
    /* ★超重要修正★ 足元基準（Bottom Center）に変更！ 
       これで top: 85% のとき、足が 85% のラインに来るよ！ */
    transform: translate(-50%, -100%);
    
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

  /* --- カニのパーツ --- */
  .body { position: absolute; bottom: 0; width: 50px; height: 33px; background-color: #ff6b6b; border-radius: 50% 50% 40% 40%; border: 2px solid #c0392b; box-shadow: inset -2px -2px 5px rgba(0,0,0,0.1); }
  .eye-stalk { position: absolute; top: -8px; width: 3px; height: 10px; background-color: #c0392b; }
  .eye-stalk.left { left: 12px; transform: rotate(-15deg); } .eye-stalk.right { right: 12px; transform: rotate(15deg); }
  .eye { position: absolute; top: -10px; width: 8px; height: 8px; background-color: white; border-radius: 50%; border: 1px solid #c0392b; }
  .eye::after { content: ''; position: absolute; top: 2px; left: 2px; width: 4px; height: 4px; background-color: black; border-radius: 50%; animation: blink 4s infinite; }
  .eye.left { left: 9px; } .eye.right { right: 9px; }
  .claw { position: absolute; top: 3px; width: 16px; height: 12px; border: 2px solid #c0392b; background-color: #ff6b6b; border-radius: 50% 50% 10% 10%; transform-origin: bottom center; }
  .claw.left { left: -10px; transform: rotate(-30deg); } .claw.left::after { content: ''; position: absolute; top: -6px; left: 0; width: 10px; height: 12px; background-color: #ff6b6b; border: 2px solid #c0392b; border-radius: 50% 10% 0 0; transform: rotate(-20deg); transform-origin: bottom right; }
  .claw.right { right: -10px; transform: rotate(30deg); } .claw.right::after { content: ''; position: absolute; top: -6px; right: 0; width: 10px; height: 12px; background-color: #ff6b6b; border: 2px solid #c0392b; border-radius: 10% 50% 0 0; transform: rotate(20deg); transform-origin: bottom left; }
  .leg { position: absolute; bottom: 4px; width: 10px; height: 3px; background-color: #c0392b; border-radius: 3px; transform-origin: right center;}
  .leg.left { transform-origin: right center; } .leg.right { transform-origin: left center; }
  .leg.L1 { left: -8px; transform: rotate(-20deg); } .leg.L2 { left: -3px; bottom: 2px; transform: rotate(-10deg); }
  .leg.R1 { right: -8px; transform: rotate(20deg); } .leg.R2 { right: -3px; bottom: 2px; transform: rotate(10deg); }

  /* --- 貝殻 --- */
  .shell { position: absolute; width: 18px; height: 15px; background: repeating-linear-gradient(90deg, #fff0f5 0px, #fff0f5 2px, #ffc1e3 3px, #ffc1e3 4px); border-radius: 50% 50% 10% 10%; box-shadow: 1px 1px 3px rgba(0,0,0,0.2); z-index: 5; }
  .shell::after { content: ''; position: absolute; bottom: -2px; left: 50%; transform: translateX(-50%); width: 4px; height: 3px; background-color: #ffc1e3; border-radius: 2px; }
  .shell-spiral { position: absolute; width: 0; height: 0; border-left: 4px solid transparent; border-right: 4px solid transparent; border-bottom: 18px solid #fff; border-radius: 50%; transform: rotate(45deg); filter: drop-shadow(1px 1px 2px rgba(0,0,0,0.2)); z-index: 5; }
  .shell-spiral::before { content: ''; position: absolute; top: 9px; left: -4px; width: 8px; height: 8px; background-color: #eee; border-radius: 50%; }

  /* --- アニメーション定義 --- */
  @keyframes snip-left { from { transform: rotate(-10deg); } to { transform: rotate(-40deg); } }
  @keyframes snip-right { from { transform: rotate(10deg); } to { transform: rotate(40deg); } }
  @keyframes blink { 0%, 96%, 100% { transform: scaleY(1); } 98% { transform: scaleY(0.1); } }
  @keyframes walk-leg { from { transform: rotate(-10deg); } to { transform: rotate(10deg); } }
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
  const HOLE_X = 50; // %
  const HOLE_Y = 85; // %

  // ★座標修正（足元基準）★
  // ステージは top:85% (穴の中心) にあり、height:100px。
  // translate(-50%, -50%) しているので、ステージの上端は 85% - 50px、下端は 85% + 50px。
  // 足元基準(translate -50%, -100%)のカニにとって：
  // top: 50% (ステージ内) => 画面上の 85%。これが「穴の入り口」。
  // top: 150% (ステージ内) => 画面上の 85% + 50px (下)。これで隠れる。
  
  const POS_HIDDEN_Y = '150%'; // ステージの下へ消える
  const POS_PEEK_Y   = '80%';  // ちょい出し
  const POS_GROUND_Y = '50%';  // 地上（穴のラインぴったり）

  setTimeout(decideNextAction, 1000);

  function decideNextAction() {
    let delay = 1000;

    if (mode === 'HOLE') {
      const dice = Math.random();
      if (dice < 0.4) {
        // キョロキョロ
        crab.style.top = POS_PEEK_Y;
        delay = 2000 + Math.random() * 1500;
        setTimeout(() => { if(mode==='HOLE') crab.style.top = POS_HIDDEN_Y; }, delay - 500);
      } else if (dice < 0.7) {
        // 出てくる
        crab.style.top = POS_GROUND_Y;
        setTimeout(() => {
          stage.style.overflow = 'visible';
          // 座標系切り替え：見た目は変わらず、基準が画面全体になる
          crab.style.top = `${HOLE_Y}%`;
          crab.style.left = `${HOLE_X}%`;
          mode = 'BEACH';
          decideNextAction(); 
        }, 1500);
        return;
      } else {
        // 隠れる
        crab.style.top = POS_HIDDEN_Y;
        delay = 2000;
      }
    } else if (mode === 'BEACH') {
      const dice = Math.random();
      if (dice < 0.2) {
        // じっとする
        delay = 1000 + Math.random() * 1500;
      } else if (dice < 0.6) {
        // ランダム移動
        moveRandom();
        delay = 3500;
      } else if (dice < 0.8) {
        // チョキチョキ
        crab.classList.add('snipping');
        delay = 1500;
        setTimeout(() => { crab.classList.remove('snipping'); }, delay);
      } else {
        // 帰宅
        returnHome();
        return; 
      }
    }
    setTimeout(decideNextAction, delay);
  }

  // 全方向ランダム移動
  function moveRandom() {
    crab.classList.add('walking');
    
    // ★移動範囲の修正★
    // 上の方（Y座標の小さい値）が出やすいように、そして画面端まで行くように調整
    // 5% 〜 85% (穴より上) の範囲でランダム
    const targetX = 5 + Math.random() * 90; 
    const targetY = 5 + Math.random() * 80; 

    crab.style.left = `${targetX}%`;
    crab.style.top = `${targetY}%`;

    setTimeout(() => {
        crab.classList.remove('walking');
    }, 3000);
  }

  // 帰宅アクション
  function returnHome() {
    crab.classList.add('walking');
    
    // 足元基準にしたので、topにHOLE_Y(85%)を指定すれば、足がドンピシャで穴の中心に来る！
    crab.style.left = `${HOLE_X}%`;
    crab.style.top = `${HOLE_Y}%`;

    setTimeout(() => {
      crab.classList.remove('walking');
      
      // 座標系をステージ内に戻す
      crab.style.left = '50%'; // ステージの左右中央
      crab.style.top = POS_GROUND_Y; // ステージの上下中央（入り口）
      
      stage.style.overflow = 'hidden'; 
      mode = 'HOLE';
      
      setTimeout(() => {
          crab.style.top = POS_HIDDEN_Y; // 潜る
          setTimeout(decideNextAction, 2000);
      }, 100); 
    }, 3000);
  }
</script>
</body>
</html>
"""

# HTMLを描画
components.html(html_code, height=932)
