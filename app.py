import streamlit as st
import streamlit.components.v1 as components

# ページ設定
st.set_page_config(page_title="カニカニ・マルチホールライフ", layout="centered")

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

  /* 穴クラス（位置は個別に指定） */
  .hole {
    position: absolute;
    transform: translate(-50%, -50%);
    width: 60px;
    height: 18px;
    background-color: #4a3b2a;
    border-radius: 50%;
    box-shadow: inset 0 3px 6px rgba(0,0,0,0.6);
    z-index: 10;
  }

  /* カニステージ（マスク兼移動フィールド） 
     初期状態は「穴1（下）」の位置にあるマスクとして機能
  */
  .crab-stage {
    position: absolute;
    /* 初期位置：下の穴 */
    top: 85%; 
    left: 50%;
    transform: translate(-50%, 0); /* 上端基準 */
    width: 80px; 
    height: 100px;
    overflow: hidden; /* マスク有効 */
    z-index: 11;
    pointer-events: none;
    /* transition: all 0s; 切り替えは瞬時に行う */
  }

  /* カニコンテナ */
  .crab-container {
    position: absolute;
    /* 初期位置：穴の底 */
    top: 100px; 
    left: 50%;
    width: 50px;
    height: 40px;
    margin-left: -25px; /* 中心合わせ */
    
    /* アニメーション設定：durationはJSで制御するからCSSでは基本設定のみ */
    transition-timing-function: linear; 
    z-index: 20;
  }

  /* --- アクション用クラス --- */
  .crab-container.snipping .claw.left::after { animation: snip-left 0.2s infinite alternate; }
  .crab-container.snipping .claw.right::after { animation: snip-right 0.2s infinite alternate; }

  /* 足だけ動く歩きモーション */
  .crab-container.walking .leg.L1 { animation: walk-leg 0.3s infinite alternate; }
  .crab-container.walking .leg.R1 { animation: walk-leg 0.3s infinite alternate 0.15s; }
  .crab-container.walking .leg.L2 { animation: walk-leg 0.3s infinite alternate 0.15s; }
  .crab-container.walking .leg.R2 { animation: walk-leg 0.3s infinite alternate; }


  /* --- カニのパーツ --- */
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

  <div class="hole" style="top: 85%; left: 50%;"></div>
  <div class="hole" style="top: 50%; left: 20%;"></div>
  <div class="hole" style="top: 25%; left: 75%;"></div>
    
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
  
  // 穴の定義 (x, yは画面上の%)
  const holes = [
    { id: 0, x: 50, y: 85 }, // 元の穴
    { id: 1, x: 20, y: 50 }, // 左
    { id: 2, x: 75, y: 25 }  // 右上
  ];

  // 現在の状態
  let mode = 'HOLE';
  let currentHoleIndex = 0; // 最初は下の穴にいる

  // 穴の中での相対位置 (px)
  const POS_HIDDEN_Y = '100px'; 
  const POS_PEEK_Y   = '60px'; 
  const POS_ENTRANCE_Y = '0px';  // 穴の入り口（ステージの上端）

  setTimeout(decideNextAction, 1000);

  function decideNextAction() {
    let delay = 1000;

    if (mode === 'HOLE') {
      // --- 穴モード ---
      const dice = Math.random();
      if (dice < 0.4) {
        // ①キョロキョロ
        setCrabTransition(1.5); // 通常速度
        crab.style.top = POS_PEEK_Y;
        delay = 2000 + Math.random() * 1500;
        setTimeout(() => { if(mode==='HOLE') crab.style.top = POS_HIDDEN_Y; }, delay - 500);
      
      } else if (dice < 0.7) {
        // ②出てくる -> 砂浜モードへ
        setCrabTransition(1.5);
        crab.style.top = POS_ENTRANCE_Y;
        
        setTimeout(() => {
          // ★魔法の切り替え★
          // 1. ステージを画面全体に広げる（マスク解除）
          stage.style.overflow = 'visible'; 
          stage.style.top = '0';
          stage.style.left = '0';
          stage.style.width = '100%';
          stage.style.height = '100%';
          stage.style.transform = 'none';

          // 2. カニの座標を「現在の穴の座標」に合わせて再設定
          // これで見た目の位置を変えずに、座標系だけ画面全体に切り替える！
          setCrabTransition(0); // 瞬間移動させるのでアニメーションOFF
          crab.style.top = holes[currentHoleIndex].y + '%';
          crab.style.left = holes[currentHoleIndex].x + '%';
          
          // 強制再描画（ブラウザに座標変更を認識させる）
          crab.offsetHeight; 

          mode = 'BEACH';
          decideNextAction(); 
        }, 1500);
        return;

      } else {
        // ③隠れる
        setCrabTransition(1.5);
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
        // ②ランダム移動（のんびり）
        moveRandom();
        delay = 5000; // 移動時間を考慮して待つ
      } else if (dice < 0.8) {
        // ④チョキチョキ
        crab.classList.add('snipping');
        delay = 1500;
        setTimeout(() => { crab.classList.remove('snipping'); }, delay);
      } else {
        // ⑤どこかの穴へ帰宅
        returnHome();
        return; 
      }
    }
    setTimeout(decideNextAction, delay);
  }

  // アニメーション速度調整用関数
  function setCrabTransition(duration) {
    crab.style.transition = `top ${duration}s linear, left ${duration}s linear`;
  }

  // 全方向ランダム移動
  function moveRandom() {
    crab.classList.add('walking');
    setCrabTransition(4.0); // 4秒かけてのんびり移動

    const targetX = 5 + Math.random() * 90;
    const targetY = 5 + Math.random() * 90;

    crab.style.left = `${targetX}%`;
    crab.style.top = `${targetY}%`;

    setTimeout(() => {
        crab.classList.remove('walking');
    }, 4000);
  }

  // 帰宅関数
  function returnHome() {
    crab.classList.add('walking');
    
    // 次の穴をランダムに決定 (自分を含む)
    const nextHoleIndex = Math.floor(Math.random() * holes.length);
    const targetHole = holes[nextHoleIndex];
    currentHoleIndex = nextHoleIndex; // 次の家を記録

    // 距離を計算して、遠いときは時間をかける（一定の速度感を出す）
    // 現在位置取得
    const currentX = parseFloat(crab.style.left);
    const currentY = parseFloat(crab.style.top);
    // 距離 (簡易計算)
    const dist = Math.sqrt(Math.pow(targetHole.x - currentX, 2) + Math.pow(targetHole.y - currentY, 2));
    // 速度係数 (距離100あたり5秒くらい)
    const duration = Math.max(2.5, dist * 0.08); 

    setCrabTransition(duration); // 計算した時間で移動

    // 穴の位置へ移動
    crab.style.left = `${targetHole.x}%`;
    crab.style.top = `${targetHole.y}%`;

    setTimeout(() => {
      crab.classList.remove('walking');
      
      // ★魔法の切り替え（逆）★
      // 1. ステージを「次の穴」の位置にセット（小さなマスクに戻す）
      stage.style.top = targetHole.y + '%';
      stage.style.left = targetHole.x + '%';
      stage.style.width = '80px';
      stage.style.height = '100px';
      stage.style.transform = 'translate(-50%, 0)'; // 上端基準
      
      // 2. カニをステージ内の座標に戻す
      // 穴の入り口（POS_ENTRANCE_Y）に瞬間移動
      setCrabTransition(0); 
      crab.style.top = POS_ENTRANCE_Y;
      crab.style.left = '50%'; // ステージの左右中央

      // 強制再描画
      crab.offsetHeight; 

      // 3. マスク有効化して潜る準備
      stage.style.overflow = 'hidden'; 
      mode = 'HOLE';
      
      // 4. 一呼吸おいて、穴の奥へ潜る
      setTimeout(() => {
          setCrabTransition(1.5); // 潜る速度は普通に
          crab.style.top = POS_HIDDEN_Y; 
          setTimeout(decideNextAction, 2000);
      }, 500); 

    }, duration * 1000); // 移動完了を待つ
  }

</script>
</body>
</html>
"""

# HTMLを描画
components.html(html_code, height=932)
