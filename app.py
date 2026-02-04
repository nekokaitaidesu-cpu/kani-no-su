import streamlit as st
import streamlit.components.v1 as components

# ページ設定
st.set_page_config(page_title="カニカニ・パーフェクトワールド", layout="centered")

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

  /* --- 穴（共通スタイル） --- */
  .hole {
    position: absolute;
    transform: translateX(-50%);
    width: 60px;
    height: 18px;
    background-color: #4a3b2a;
    border-radius: 50%;
    box-shadow: inset 0 3px 6px rgba(0,0,0,0.6);
    z-index: 10;
  }
  /* 各穴の位置 */
  #hole1 { top: 60%; left: 25%; } /* 左上 */
  #hole2 { top: 40%; left: 75%; } /* 右上 */
  #hole3 { bottom: 150px; left: 50%; } /* 下中央（真ん中の穴：絶対維持） */

  /* --- カニステージ（マスク用・共通スタイル） --- */
  .crab-stage {
    position: absolute;
    width: 80px;
    height: 100px;
    overflow: hidden; /* 初期状態はマスク有効 */
    z-index: 11;
    pointer-events: none;
    /* background: rgba(255,0,0,0.2); デバッグ用 */
  }
  /* 各ステージの位置 */
  /* 左右の穴は、穴の中心座標とステージの中心を合わせることで位置ズレを解消 */
  #stage1 { top: 60%; left: 25%; transform: translate(-50%, -50%); }
  #stage2 { top: 40%; left: 75%; transform: translate(-50%, -50%); }
  /* 真ん中のステージは元の設定を完全に維持 */
  #stage3 { bottom: 159px; left: 50%; transform: translateX(-50%); }

  /* カニコンテナ */
  .crab-container {
    position: absolute;
    /* ステージ内での初期位置（POS_HIDDEN_Yと同じ） */
    top: 100px; 
    left: 50%;
    width: 50px;
    height: 40px;
    margin-left: -25px;
    /* transitionはJSで制御 */
    z-index: 20;
  }

  /* --- アクション用クラス --- */
  .crab-container.snipping .claw.left::after { animation: snip-left 0.2s infinite alternate; }
  .crab-container.snipping .claw.right::after { animation: snip-right 0.2s infinite alternate; }
  .crab-container.walking .leg.L1 { animation: walk-leg 0.3s infinite alternate; }
  .crab-container.walking .leg.R1 { animation: walk-leg 0.3s infinite alternate 0.15s; }
  .crab-container.walking .leg.L2 { animation: walk-leg 0.3s infinite alternate 0.15s; }
  .crab-container.walking .leg.R2 { animation: walk-leg 0.3s infinite alternate; }

  /* --- カニのパーツ（変更なし） --- */
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

  /* --- 貝殻（変更なし） --- */
  .shell { position: absolute; width: 25px; height: 20px; background: repeating-linear-gradient(90deg, #fff0f5 0px, #fff0f5 2px, #ffc1e3 3px, #ffc1e3 4px); border-radius: 50% 50% 10% 10%; box-shadow: 1px 1px 3px rgba(0,0,0,0.2); z-index: 5; }
  .shell::after { content: ''; position: absolute; bottom: -3px; left: 50%; transform: translateX(-50%); width: 6px; height: 4px; background-color: #ffc1e3; border-radius: 2px; }
  .shell-spiral { position: absolute; width: 0; height: 0; border-left: 6px solid transparent; border-right: 6px solid transparent; border-bottom: 25px solid #fff; border-radius: 50%; transform: rotate(45deg); filter: drop-shadow(1px 1px 2px rgba(0,0,0,0.2)); z-index: 5; }
  .shell-spiral::before { content: ''; position: absolute; top: 12px; left: -6px; width: 12px; height: 12px; background-color: #eee; border-radius: 50%; }

  /* --- アニメーション定義（変更なし） --- */
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

  <div id="hole1" class="hole"></div>
  <div id="hole2" class="hole"></div>
  <div id="hole3" class="hole"></div>
    
  <div id="stage1" class="crab-stage"></div>
  <div id="stage2" class="crab-stage"></div>
  <div id="stage3" class="crab-stage">
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
  
  // 穴のデータ（位置%と対応するステージID）
  // 左右の穴はステージの中心座標と一致させる
  // 真ん中の穴(id:3)のy座標は、bottom:150pxのおおよその位置
  const holes = [
    { id: 1, x: 25, y: 60, stageId: 'stage1' }, 
    { id: 2, x: 75, y: 40, stageId: 'stage2' }, 
    { id: 3, x: 50, y: 85, stageId: 'stage3' } 
  ];
  let currentHoleId = 3; // 初期は真ん中の穴

  let mode = 'HOLE';

  // 穴の中での相対位置 (px) - 維持する
  const POS_HIDDEN_Y = '100px'; 
  const POS_PEEK_Y   = '60px'; 
  const POS_GROUND_Y = '20px';  

  // 通常の移動速度
  const SPEED_NORMAL = 'top 1.5s cubic-bezier(0.5, 0, 0.5, 1), left 1.5s linear';
  // 穴への移動速度（ゆっくり）
  const SPEED_SLOW = 'top 8s linear, left 8s linear';

  // 初期設定
  crab.style.transition = SPEED_NORMAL;

  setTimeout(decideNextAction, 1000);

  function decideNextAction() {
    let delay = 1000;
    const currentStage = document.getElementById(holes.find(h => h.id === currentHoleId).stageId);

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
        crab.style.top = POS_GROUND_Y;
        setTimeout(() => {
          currentStage.style.overflow = 'visible'; // マスク解除
          // 座標系を画面全体へ切り替え
          const holeData = holes.find(h => h.id === currentHoleId);
          crab.style.top = `${holeData.y}%`;
          crab.style.left = `${holeData.x}%`;
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
      crab.style.transition = SPEED_NORMAL; // 速度を戻す

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
        // ⑤いずれかの穴へ帰宅
        returnToAnyHole();
        return; 
      }
    }
    setTimeout(decideNextAction, delay);
  }

  // 全方向ランダム移動
  function moveRandom() {
    crab.classList.add('walking');
    const targetX = 5 + Math.random() * 90; 
    const targetY = 5 + Math.random() * 90; 
    crab.style.left = `${targetX}%`;
    crab.style.top = `${targetY}%`;
    setTimeout(() => { crab.classList.remove('walking'); }, 3000);
  }

  // いずれかの穴へゆっくり帰宅し、真上から入る処理
  function returnToAnyHole() {
    crab.classList.add('walking');
    // ランダムにターゲットの穴を選ぶ
    const targetHole = holes[Math.floor(Math.random() * holes.length)];
    
    // 移動速度をゆっくりにする
    crab.style.transition = SPEED_SLOW;
    
    // 1. ターゲットの穴の真上位置へ移動
    crab.style.left = `${targetHole.x}%`;
    crab.style.top = `${targetHole.y}%`;

    // 移動完了後 (8秒後)
    setTimeout(() => {
      // 2. 穴の真上に到着。歩きを止める。
      crab.classList.remove('walking');
      
      // 3. 一瞬その場で停止して「着いた感」を出す (1秒待つ)
      setTimeout(() => {
          const targetStage = document.getElementById(targetHole.stageId);

          // 4. カニをターゲットのステージへ移動させる（所属変更）
          targetStage.appendChild(crab);
          
          // 5. 座標系切り替え時のワープを防ぐため、アニメーションを一時オフ
          crab.style.transition = 'none';
          
          // 6. カニの位置を「ステージ内の入り口（＝今までいた穴の真上）」に設定
          crab.style.top = POS_GROUND_Y; 
          crab.style.left = '50%';
          
          // 7. マスクを有効にして、穴モードへ移行
          targetStage.style.overflow = 'hidden'; 
          currentHoleId = targetHole.id;
          mode = 'HOLE';
          
          // 8. わずかな時間をおいて、潜るアニメーションを開始
          setTimeout(() => {
              // アニメーション速度を通常に戻す
              crab.style.transition = SPEED_NORMAL;
              // 穴の底へ移動させる（これで潜るアニメーションが再生される）
              crab.style.top = POS_HIDDEN_Y;

              // 9. 潜り終わった後の次の行動を予約
              setTimeout(decideNextAction, 2000);
          }, 50); // transition:none の適用を待つための短い待機

      }, 1000); // 穴の上での待機時間

    }, 8000); // 砂浜移動時間
  }

</script>
</body>
</html>
"""

# HTMLを描画
components.html(html_code, height=932)
