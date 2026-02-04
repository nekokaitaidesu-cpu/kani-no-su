import streamlit as st
import streamlit.components.v1 as components

# ページ設定
st.set_page_config(page_title="カニとヤドカリの海辺", layout="centered")

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

  /* --- メインのカニ用：穴（サイズを約半分に） --- */
  .hole {
    position: absolute;
    bottom: 150px;
    left: 50%;
    transform: translateX(-50%);
    width: 60px;
    height: 18px;
    background-color: #4a3b2a;
    border-radius: 50%;
    box-shadow: inset 0 3px 6px rgba(0,0,0,0.6);
    z-index: 10;
  }

  /* カニステージ（マスク用） */
  .crab-stage {
    position: absolute;
    bottom: 159px;
    left: 50%;
    transform: translateX(-50%);
    width: 80px;
    height: 100px;
    overflow: hidden;
    z-index: 11;
    pointer-events: none;
  }

  /* カニコンテナ */
  .crab-container {
    position: absolute;
    top: 100px; /* 初期位置 */
    left: 50%;
    width: 50px;
    height: 40px;
    margin-left: -25px; /* 中心合わせ */
    transition: top 1.5s cubic-bezier(0.5, 0, 0.5, 1), left 1.5s linear;
    z-index: 20;
  }

  /* --- アクション用クラス --- */
  .crab-container.snipping .claw.left::after { animation: snip-left 0.2s infinite alternate; }
  .crab-container.snipping .claw.right::after { animation: snip-right 0.2s infinite alternate; }

  /* 歩きモーション */
  .crab-container.walking .leg.L1 { animation: walk-leg 0.3s infinite alternate; }
  .crab-container.walking .leg.R1 { animation: walk-leg 0.3s infinite alternate 0.15s; }
  .crab-container.walking .leg.L2 { animation: walk-leg 0.3s infinite alternate 0.15s; }
  .crab-container.walking .leg.R2 { animation: walk-leg 0.3s infinite alternate; }

  /* --- カニのパーツ --- */
  .body { position: absolute; bottom: 0; width: 50px; height: 33px; background-color: #ff6b6b; border-radius: 50% 50% 40% 40%; border: 2px solid #c0392b; box-shadow: inset -2px -2px 5px rgba(0,0,0,0.1); }
  .eye-stalk { position: absolute; top: -8px; width: 3px; height: 10px; background-color: #c0392b; transition: transform 0.3s; }
  .eye-stalk.left { left: 12px; transform: rotate(-15deg); } .eye-stalk.right { right: 12px; transform: rotate(15deg); }
  .eye { position: absolute; top: -10px; width: 8px; height: 8px; background-color: white; border-radius: 50%; border: 1px solid #c0392b; }
  .eye::after { content: ''; position: absolute; top: 2px; left: 2px; width: 4px; height: 4px; background-color: black; border-radius: 50%; animation: blink 4s infinite; }
  .eye.left { left: 9px; } .eye.right { right: 9px; }
  .claw { position: absolute; top: 3px; width: 16px; height: 12px; border: 2px solid #c0392b; background-color: #ff6b6b; border-radius: 50% 50% 10% 10%; transform-origin: bottom center; transition: transform 0.3s; }
  .claw.left { left: -10px; transform: rotate(-30deg); } .claw.left::after { content: ''; position: absolute; top: -6px; left: 0; width: 10px; height: 12px; background-color: #ff6b6b; border: 2px solid #c0392b; border-radius: 50% 10% 0 0; transform: rotate(-20deg); transform-origin: bottom right; }
  .claw.right { right: -10px; transform: rotate(30deg); } .claw.right::after { content: ''; position: absolute; top: -6px; right: 0; width: 10px; height: 12px; background-color: #ff6b6b; border: 2px solid #c0392b; border-radius: 10% 50% 0 0; transform: rotate(20deg); transform-origin: bottom left; }
  .leg { position: absolute; bottom: 4px; width: 10px; height: 3px; background-color: #c0392b; border-radius: 3px; transform-origin: right center;}
  .leg.left { transform-origin: right center; } .leg.right { transform-origin: left center; }
  .leg.L1 { left: -8px; transform: rotate(-20deg); } .leg.L2 { left: -3px; bottom: 2px; transform: rotate(-10deg); }
  .leg.R1 { right: -8px; transform: rotate(20deg); } .leg.R2 { right: -3px; bottom: 2px; transform: rotate(10deg); }


  /* --- 貝殻 --- */
  .shell { position: absolute; width: 25px; height: 20px; background: repeating-linear-gradient(90deg, #fff0f5 0px, #fff0f5 2px, #ffc1e3 3px, #ffc1e3 4px); border-radius: 50% 50% 10% 10%; box-shadow: 1px 1px 3px rgba(0,0,0,0.2); z-index: 5; }
  .shell::after { content: ''; position: absolute; bottom: -3px; left: 50%; transform: translateX(-50%); width: 6px; height: 4px; background-color: #ffc1e3; border-radius: 2px; }
  .shell-spiral { position: absolute; width: 0; height: 0; border-left: 6px solid transparent; border-right: 6px solid transparent; border-bottom: 25px solid #fff; border-radius: 50%; transform: rotate(45deg); filter: drop-shadow(1px 1px 2px rgba(0,0,0,0.2)); z-index: 5; }
  .shell-spiral::before { content: ''; position: absolute; top: 12px; left: -6px; width: 12px; height: 12px; background-color: #eee; border-radius: 50%; }

  /* --- ★追加★ ヤドカリさん --- */
  .hermit-container {
    position: absolute;
    top: 50%; /* JSでランダムに変更 */
    left: -100px; /* 初期位置は画面外（左） */
    width: 40px;
    height: 35px;
    z-index: 15; /* カニより少し奥、穴より手前 */
    /* 移動アニメーションはJSで制御 */
  }
  
  /* 青い巻貝 */
  .hermit-shell {
    position: absolute;
    top: -15px;
    left: 5px;
    width: 0;
    height: 0;
    border-left: 8px solid transparent;
    border-right: 8px solid transparent;
    border-bottom: 35px solid #6fa3ef; /* 青色 */
    border-radius: 40%;
    transform: rotate(55deg); /* 右向き */
    filter: drop-shadow(2px 2px 2px rgba(0,0,0,0.2));
    z-index: 2;
  }
  .hermit-shell::before {
    content: ''; position: absolute; top: 18px; left: -7px; width: 14px; height: 14px; background-color: #cce0ff; border-radius: 50%;
  }

  /* ヤドカリの体（ちょこっと出てる） */
  .hermit-body {
    position: absolute;
    bottom: 0;
    left: 10px;
    width: 25px;
    height: 15px;
    background-color: #ffccbc; /* 薄いオレンジ */
    border-radius: 50% 50% 20% 20%;
    border: 1px solid #e64a19;
    z-index: 1;
  }
  
  /* ヤドカリの目 */
  .hermit-eye {
    position: absolute;
    top: -8px;
    width: 4px;
    height: 4px;
    background-color: white;
    border: 1px solid #e64a19;
    border-radius: 50%;
  }
  .hermit-eye::after { content: ''; position: absolute; top: 1px; left: 1px; width: 2px; height: 2px; background-color: black; border-radius: 50%; }
  .hermit-eye.left { left: 5px; }
  .hermit-eye.right { right: 5px; }

  /* ヤドカリの足（歩くとき動く） */
  .hermit-leg {
    position: absolute;
    bottom: -2px;
    width: 8px;
    height: 3px;
    background-color: #e64a19;
    border-radius: 2px;
  }
  .hermit-leg.L1 { left: 0px; transform: rotate(-10deg); }
  .hermit-leg.L2 { left: 5px; transform: rotate(10deg); }
  .hermit-leg.L3 { left: 15px; transform: rotate(10deg); }
  
  /* ヤドカリの歩きアニメーション */
  .hermit-container.walking .hermit-leg { animation: hermit-walk 0.5s infinite alternate; }
  .hermit-container.walking .hermit-shell { animation: hermit-bob 0.5s infinite alternate; }

  @keyframes hermit-walk { from { transform: rotate(-10deg); } to { transform: rotate(20deg); } }
  @keyframes hermit-bob { from { transform: rotate(55deg) translateY(0); } to { transform: rotate(55deg) translateY(-1px); } }

  /* 既存アニメーション */
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

  <div id="hermit" class="hermit-container">
    <div class="hermit-shell"></div>
    <div class="hermit-body">
        <div class="hermit-eye left"></div>
        <div class="hermit-eye right"></div>
        <div class="hermit-leg L1"></div>
        <div class="hermit-leg L2"></div>
        <div class="hermit-leg L3"></div>
    </div>
  </div>

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
  /* --- メインのカニのロジック（そのまま） --- */
  const crab = document.getElementById('crab');
  const stage = document.getElementById('stage');
  
  let mode = 'HOLE';
  const HOLE_X = 50; 
  const HOLE_Y = 85; 

  const POS_HIDDEN_Y = '100px'; 
  const POS_PEEK_Y   = '60px'; 
  const POS_GROUND_Y = '20px';  

  setTimeout(decideNextAction, 1000);

  function decideNextAction() {
    let delay = 1000;

    if (mode === 'HOLE') {
      const dice = Math.random();
      if (dice < 0.4) {
        // ①キョロキョロ
        crab.style.top = POS_PEEK_Y;
        delay = 2000 + Math.random() * 1500;
        setTimeout(() => { if(mode==='HOLE') crab.style.top = POS_HIDDEN_Y; }, delay - 500);
      } else if (dice < 0.7) {
        // ②出てくる
        crab.style.top = POS_GROUND_Y;
        setTimeout(() => {
          stage.style.overflow = 'visible'; 
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
      const dice = Math.random();
      if (dice < 0.2) {
        // ①じっとする
        delay = 1000 + Math.random() * 1500;
      } else if (dice < 0.6) {
        // ②ランダム移動
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

  function moveRandom() {
    crab.classList.add('walking');
    const targetX = 5 + Math.random() * 90;
    const targetY = 5 + Math.random() * 90;
    crab.style.left = `${targetX}%`;
    crab.style.top = `${targetY}%`;
    setTimeout(() => { crab.classList.remove('walking'); }, 3000);
  }

  function returnHome() {
    crab.classList.add('walking');
    crab.style.left = `${HOLE_X}%`;
    crab.style.top = `${HOLE_Y}%`;
    setTimeout(() => {
      crab.classList.remove('walking');
      crab.style.top = POS_GROUND_Y; 
      crab.style.left = '50%';
      stage.style.overflow = 'hidden'; 
      mode = 'HOLE';
      setTimeout(() => {
          crab.style.top = POS_HIDDEN_Y; 
          setTimeout(decideNextAction, 2000);
      }, 100); 
    }, 3000);
  }


  /* --- ★追加★ ヤドカリさんのロジック --- */
  const hermit = document.getElementById('hermit');
  
  // ヤドカリライフ開始
  setTimeout(startHermitLoop, 5000); // 最初は5秒後にチェック開始

  function startHermitLoop() {
    // 次の出現までのランダムな時間（10秒〜30秒後）
    const nextSpawnTime = 10000 + Math.random() * 20000;
    
    // ヤドカリ出現！
    spawnHermit();
    
    // 次のループを予約（移動時間25秒 + ランダム待機時間）
    setTimeout(startHermitLoop, 25000 + nextSpawnTime);
  }

  function spawnHermit() {
    // 画面のどこかの高さ（Y軸）に出現させる（上の方〜下の方）
    const spawnY = 10 + Math.random() * 70; 
    
    // アニメーションのリセット
    hermit.style.transition = 'none';
    hermit.style.top = `${spawnY}%`;
    hermit.style.left = '-15%'; // 画面左外
    hermit.classList.remove('walking');

    // ブラウザにスタイル適用を認識させるための一瞬のウェイト
    requestAnimationFrame(() => {
      requestAnimationFrame(() => {
        // ゆーっくり移動開始（左から右へ）
        hermit.classList.add('walking');
        hermit.style.transition = 'left 25s linear'; // 25秒かけて横断
        hermit.style.left = '115%'; // 画面右外へ
      });
    });
  }

</script>
</body>
</html>
"""

# HTMLを描画
components.html(html_code, height=932)
