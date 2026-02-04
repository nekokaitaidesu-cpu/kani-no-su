import streamlit as st
import streamlit.components.v1 as components

# ページ設定
st.set_page_config(page_title="カニカニ・複数穴ライフ修正版", layout="centered")

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
  #hole3 { bottom: 150px; left: 50%; } /* 下中央（初期穴・完璧な位置） */

  /* --- カニステージ（マスク用・共通スタイル） --- */
  .crab-stage {
    position: absolute;
    transform: translateX(-50%);
    width: 80px;
    height: 100px;
    overflow: hidden;
    z-index: 11;
    pointer-events: none;
    /* border: 1px solid red; デバッグ用 */
  }
  /* ★修正ポイント★
     真ん中の穴（#stage3）は、穴の位置より9px上に配置されています（bottom指定なので+9px）。
     左右の穴も同様に、穴の位置より9px上に配置されるよう修正します。
     top指定の場合は、数値を小さくすることで上に行きます。
  */
  #stage1 { top: calc(60% - 9px); left: 25%; } /* 修正: +9px から -9px へ */
  #stage2 { top: calc(40% - 9px); left: 75%; } /* 修正: +9px から -9px へ */
  #stage3 { bottom: 159px; left: 50%; } /* 完璧な位置（bottom: 150px + 9px） */

  /* カニコンテナ */
  .crab-container {
    position: absolute;
    top: 100px; /* 初期位置 */
    left: 50%;
    width: 50px;
    height: 40px;
    margin-left: -25px;
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
  const holes = [
    { id: 1, x: 25, y: 60, stageId: 'stage1' }, // 左上
    { id: 2, x: 75, y: 40, stageId: 'stage2' }, // 右上
    { id: 3, x: 50, y: 85, stageId: 'stage3' }  // 下中央 (初期)
  ];
  let currentHoleId = 3; // 現在のホーム穴ID

  let mode = 'HOLE';

  // 穴の中での相対位置 (px)
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

    if (mode === 'HOLE') {
      // --- 穴モード ---
      const dice = Math.random();
      const currentStage = document.getElementById(holes.find(h => h.id === currentHoleId).stageId);

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

  // いずれかの穴へゆっくり帰宅する
  function returnToAnyHole() {
    crab.classList.add('walking');
    // ランダムにターゲットの穴を選ぶ
    const targetHole = holes[Math.floor(Math.random() * holes.length)];
    
    // 移動速度をゆっくりにする
    crab.style.transition = SPEED_SLOW;
    
    // ターゲットの穴の位置へ移動
    crab.style.left = `${targetHole.x}%`;
    crab.style.top = `${targetHole.y}%`;

    // 移動完了後 (時間がかかるので待ち時間を長く設定)
    setTimeout(() => {
      crab.classList.remove('walking');
      
      // 1. カニの所属ステージを変更する
      const targetStage = document.getElementById(targetHole.stageId);
      targetStage.appendChild(crab);
      
      // 2. 速度設定を一時的に無効化して座標系を切り替える
      crab.style.transition = 'none'; 
      crab.style.top = POS_GROUND_Y; 
      crab.style.left = '50%';
      
      // 3. マスクを有効化して、現在の穴IDを更新
      targetStage.style.overflow = 'hidden'; 
      currentHoleId = targetHole.id;
      mode = 'HOLE';
      
      // 4. 一呼吸おいて、速度設定を戻して潜る
      setTimeout(() => {
          crab.style.transition = SPEED_NORMAL;
          crab.style.top = POS_HIDDEN_Y; 
          setTimeout(decideNextAction, 2000);
      }, 100); 
    }, 8000); // 移動時間に合わせて待つ
  }

</script>
</body>
</html>
"""

# HTMLを描画
components.html(html_code, height=932)
