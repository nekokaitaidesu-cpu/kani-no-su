import streamlit as st
import streamlit.components.v1 as components

# ページ設定
st.set_page_config(page_title="カニと謎の生き物（捕獲完全版）", layout="centered")

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
    touch-action: none; /* スクロール無効化 */
    user-select: none; /* 選択無効化 */
    -webkit-user-select: none;
  }

  /* フィールド */
  .beach-scene {
    position: relative;
    width: 100%;
    height: 100%;
    max-width: 430px;
    max-height: 932px;
  }

  /* --- メインのカニ関連 --- */
  .hole { position: absolute; bottom: 150px; left: 50%; transform: translateX(-50%); width: 60px; height: 18px; background-color: #4a3b2a; border-radius: 50%; box-shadow: inset 0 3px 6px rgba(0,0,0,0.6); z-index: 10; }
  .crab-stage { position: absolute; bottom: 159px; left: 50%; transform: translateX(-50%); width: 80px; height: 100px; overflow: hidden; z-index: 16; pointer-events: none; }
  .crab-container { position: absolute; top: 100px; left: 50%; width: 50px; height: 40px; margin-left: -25px; transition: top 1.5s cubic-bezier(0.5, 0, 0.5, 1), left 1.5s linear; z-index: 20; }
  .crab-container.snipping .claw.left::after { animation: snip-left 0.2s infinite alternate; }
  .crab-container.snipping .claw.right::after { animation: snip-right 0.2s infinite alternate; }
  .crab-container.walking .leg.L1 { animation: walk-leg 0.3s infinite alternate; }
  .crab-container.walking .leg.R1 { animation: walk-leg 0.3s infinite alternate 0.15s; }
  .crab-container.walking .leg.L2 { animation: walk-leg 0.3s infinite alternate 0.15s; }
  .crab-container.walking .leg.R2 { animation: walk-leg 0.3s infinite alternate; }
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

  /* --- 背景の貝殻 --- */
  .shell { position: absolute; width: 25px; height: 20px; background: repeating-linear-gradient(90deg, #fff0f5 0px, #fff0f5 2px, #ffc1e3 3px, #ffc1e3 4px); border-radius: 50% 50% 10% 10%; box-shadow: 1px 1px 3px rgba(0,0,0,0.2); z-index: 5; }
  .shell::after { content: ''; position: absolute; bottom: -3px; left: 50%; transform: translateX(-50%); width: 6px; height: 4px; background-color: #ffc1e3; border-radius: 2px; }
  .shell-spiral { position: absolute; width: 0; height: 0; border-left: 6px solid transparent; border-right: 6px solid transparent; border-bottom: 25px solid #fff; border-radius: 50%; transform: rotate(45deg); filter: drop-shadow(1px 1px 2px rgba(0,0,0,0.2)); z-index: 5; }
  .shell-spiral::before { content: ''; position: absolute; top: 12px; left: -6px; width: 12px; height: 12px; background-color: #eee; border-radius: 50%; }

  /* --- ★謎の生き物★ --- */
  .hermit-container {
    position: absolute;
    width: 40px;
    height: 35px;
    z-index: 15;
    cursor: grab;
    touch-action: none; 
  }
  .hermit-container:active {
    cursor: grabbing;
  }
  /* 右向き */
  .hermit-container.walking-right {
    transform: scaleX(-1);
  }
  
  .hermit-body {
    position: absolute; bottom: 0; left: 10px; width: 25px; height: 15px; background-color: #ffccbc; border-radius: 50% 50% 20% 20%; border: 1px solid #e64a19; z-index: 1;
  }
  .hermit-eye { position: absolute; top: -8px; width: 4px; height: 4px; background-color: white; border: 1px solid #e64a19; border-radius: 50%; }
  .hermit-eye::after { content: ''; position: absolute; top: 1px; left: 1px; width: 2px; height: 2px; background-color: black; border-radius: 50%; }
  .hermit-eye.left { left: 5px; } .hermit-eye.right { right: 5px; }
  .hermit-leg { position: absolute; bottom: -2px; width: 8px; height: 3px; background-color: #e64a19; border-radius: 2px; }
  .hermit-leg.L1 { left: 0px; transform: rotate(-10deg); } .hermit-leg.L2 { left: 5px; transform: rotate(10deg); } .hermit-leg.L3 { left: 15px; transform: rotate(10deg); }
  
  /* 通常歩行 */
  .hermit-container.walking .hermit-leg { animation: hermit-walk 0.5s infinite alternate; }
  .hermit-container.walking .hermit-body { animation: hermit-bob 0.5s infinite alternate; }

  /* ★焦り（掴まれている時） - 高速バタバタ */
  .hermit-container.struggling .hermit-leg {
    animation: hermit-panic 0.08s infinite alternate; 
  }
  .hermit-container.struggling .hermit-body {
    animation: hermit-shake 0.08s infinite alternate;
  }

  /* ★全力逃走 - 高速バタバタ */
  .hermit-container.running .hermit-leg {
    animation: hermit-panic 0.08s infinite alternate;
  }
  .hermit-container.running .hermit-body {
    animation: hermit-bob 0.1s infinite alternate;
  }

  /* 汗エフェクト */
  .sweat {
    position: absolute;
    font-size: 20px;
    pointer-events: none;
    z-index: 30;
    animation: sweat-pop 0.6s linear forwards;
  }

  @keyframes hermit-walk { from { transform: rotate(-10deg); } to { transform: rotate(20deg); } }
  @keyframes hermit-bob { from { transform: translateY(0); } to { transform: translateY(-1px); } }
  
  @keyframes hermit-panic { from { transform: rotate(-30deg); } to { transform: rotate(30deg); } }
  @keyframes hermit-shake { from { transform: translateX(-1px) rotate(-2deg); } to { transform: translateX(1px) rotate(2deg); } }
  
  @keyframes sweat-pop {
    0% { transform: translate(0, 0) scale(0.5); opacity: 1; }
    50% { transform: translate(10px, -20px) scale(1.2); opacity: 0.8; }
    100% { transform: translate(20px, -40px) scale(0); opacity: 0; }
  }

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
  /* --- メインのカニ（そのまま） --- */
  const crab = document.getElementById('crab');
  const stage = document.getElementById('stage');
  let mode = 'HOLE';
  const HOLE_X = 50; const HOLE_Y = 85; 
  const POS_HIDDEN_Y = '100px'; const POS_PEEK_Y = '60px'; const POS_GROUND_Y = '20px';  
  setTimeout(decideNextAction, 1000);
  function decideNextAction() {
    let delay = 1000;
    if (mode === 'HOLE') {
      const dice = Math.random();
      if (dice < 0.4) {
        crab.style.top = POS_PEEK_Y; delay = 2000 + Math.random() * 1500; setTimeout(() => { if(mode==='HOLE') crab.style.top = POS_HIDDEN_Y; }, delay - 500);
      } else if (dice < 0.7) {
        crab.style.top = POS_GROUND_Y; setTimeout(() => { stage.style.overflow = 'visible'; crab.style.top = `${HOLE_Y}%`; crab.style.left = `${HOLE_X}%`; mode = 'BEACH'; decideNextAction(); }, 1500); return;
      } else {
        crab.style.top = POS_HIDDEN_Y; delay = 2000;
      }
    } else if (mode === 'BEACH') {
      const dice = Math.random();
      if (dice < 0.2) { delay = 1000 + Math.random() * 1500;
      } else if (dice < 0.6) { moveRandom(); delay = 3500;
      } else if (dice < 0.8) { crab.classList.add('snipping'); delay = 1500; setTimeout(() => { crab.classList.remove('snipping'); }, delay);
      } else { returnHome(); return; }
    }
    setTimeout(decideNextAction, delay);
  }
  function moveRandom() {
    crab.classList.add('walking');
    const targetX = 5 + Math.random() * 90; const targetY = 5 + Math.random() * 90;
    crab.style.left = `${targetX}%`; crab.style.top = `${targetY}%`;
    setTimeout(() => { crab.classList.remove('walking'); }, 3000);
  }
  function returnHome() {
    crab.classList.add('walking');
    crab.style.left = `${HOLE_X}%`; crab.style.top = `${HOLE_Y}%`;
    setTimeout(() => {
      crab.classList.remove('walking'); crab.style.top = POS_GROUND_Y; crab.style.left = '50%'; stage.style.overflow = 'hidden'; mode = 'HOLE';
      setTimeout(() => { crab.style.top = POS_HIDDEN_Y; setTimeout(decideNextAction, 2000); }, 100); 
    }, 3000);
  }


  /* --- ★謎の生き物ロジック（修正版） --- */
  const beachScene = document.querySelector('.beach-scene');
  let activeHermits = 0; 
  const MAX_HERMITS = 5; 

  // ドラッグ管理
  let draggedHermit = null;
  let shiftX = 0; // タップ位置と要素左上のズレ
  let shiftY = 0;

  // グローバルイベントリスナー
  document.addEventListener('mousemove', onDragMove);
  document.addEventListener('mouseup', onDragEnd);
  document.addEventListener('touchmove', onDragMove, {passive: false});
  document.addEventListener('touchend', onDragEnd);

  setTimeout(startHermitLoop, 3000);

  function startHermitLoop() {
    const nextCheckTime = 3000 + Math.random() * 4000; 
    if (activeHermits < MAX_HERMITS) {
        spawnHermit();
    }
    setTimeout(startHermitLoop, nextCheckTime);
  }

  function spawnHermit() {
    activeHermits++;
    const hermit = document.createElement('div');
    hermit.classList.add('hermit-container');
    
    hermit.innerHTML = `
      <div class="hermit-body">
          <div class="hermit-eye left"></div><div class="hermit-eye right"></div>
          <div class="hermit-leg L1"></div><div class="hermit-leg L2"></div><div class="hermit-leg L3"></div>
      </div>
    `;
    beachScene.appendChild(hermit);

    // イベント登録
    hermit.addEventListener('mousedown', onDragStart);
    hermit.addEventListener('touchstart', onDragStart, {passive: false});

    // 初期配置 (ランダム)
    const spawnY = 10 + Math.random() * 70; 
    hermit.style.top = `${spawnY}%`;

    const startFromRight = Math.random() < 0.5;
    let startLeft, endLeft;

    if (startFromRight) {
        startLeft = '115%'; endLeft = '-15%';
    } else {
        startLeft = '-15%'; endLeft = '115%';
        hermit.classList.add('walking-right');
    }
    hermit.style.left = startLeft;

    // 移動開始（アニメーション）
    requestAnimationFrame(() => {
      requestAnimationFrame(() => {
        hermit.classList.add('walking');
        const duration = 20 + Math.random() * 20;
        hermit.style.transition = `left ${duration}s linear`;
        hermit.style.left = endLeft;
      });
    });

    // 画面外削除
    hermit.addEventListener('transitionend', () => {
        if (!hermit.isCaught && !hermit.isEscaping) {
             removeHermit(hermit);
        }
        if (hermit.isEscaping) {
             removeHermit(hermit);
        }
    });
  }

  function removeHermit(hermit) {
      if (hermit.parentNode) {
          hermit.parentNode.removeChild(hermit);
          activeHermits--;
          if (hermit.sweatInterval) clearInterval(hermit.sweatInterval);
      }
  }

  /* --- ドラッグ処理（シフト計算による吸着方式） --- */

  function onDragStart(e) {
    if(e.cancelable) e.preventDefault();
    
    const hermit = e.currentTarget;
    if (hermit.isEscaping) return;

    draggedHermit = hermit;
    draggedHermit.isCaught = true;

    // 1. 移動アニメーションを停止
    draggedHermit.style.transition = 'none';

    // 2. タップ位置の座標を取得
    const clientX = e.type.includes('mouse') ? e.clientX : e.touches[0].clientX;
    const clientY = e.type.includes('mouse') ? e.clientY : e.touches[0].clientY;

    // 3. 要素の現在の画面上の位置(Rect)を取得
    const rect = draggedHermit.getBoundingClientRect();

    // 4. 「指の位置」と「要素の左上」のズレ(shift)を計算して保存
    shiftX = clientX - rect.left;
    shiftY = clientY - rect.top;

    // 5. 要素を現在の見た目の位置に固定する（これがないと変な場所に飛ぶ）
    // 親要素(beach-scene)に対する相対位置に変換してセット
    const parentRect = beachScene.getBoundingClientRect();
    draggedHermit.style.left = `${clientX - shiftX - parentRect.left}px`;
    draggedHermit.style.top  = `${clientY - shiftY - parentRect.top}px`;

    // 6. 焦り演出
    startPanic(draggedHermit);
  }

  function onDragMove(e) {
    if (!draggedHermit) return;
    if(e.cancelable) e.preventDefault();

    const clientX = e.type.includes('mouse') ? e.clientX : e.touches[0].clientX;
    const clientY = e.type.includes('mouse') ? e.clientY : e.touches[0].clientY;

    // 親要素の位置
    const parentRect = beachScene.getBoundingClientRect();

    // 新しい位置 = 現在の指の位置 - 最初のズレ - 親要素の位置
    const newLeft = clientX - shiftX - parentRect.left;
    const newTop  = clientY - shiftY - parentRect.top;

    draggedHermit.style.left = `${newLeft}px`;
    draggedHermit.style.top  = `${newTop}px`;
  }

  function onDragEnd(e) {
    if (!draggedHermit) return;
    
    // 焦り終了 -> 全力逃走へ
    stopPanic(draggedHermit);
    escapeRun(draggedHermit);

    draggedHermit = null;
  }

  /* --- 演出関連 --- */
  function startPanic(hermit) {
    hermit.classList.remove('walking');
    hermit.classList.add('struggling'); 
    hermit.sweatInterval = setInterval(() => { createSweat(hermit); }, 150); 
  }

  function stopPanic(hermit) {
    hermit.classList.remove('struggling');
    if (hermit.sweatInterval) clearInterval(hermit.sweatInterval);
  }

  function createSweat(hermit) {
    const sweat = document.createElement('div');
    sweat.innerText = '💦';
    sweat.classList.add('sweat');
    const dx = (Math.random() - 0.5) * 50;
    sweat.style.left = `calc(50% + ${dx}px)`;
    sweat.style.top = '-20px';
    hermit.appendChild(sweat);
    setTimeout(() => { if(sweat.parentNode) sweat.parentNode.removeChild(sweat); }, 600);
  }

  function escapeRun(hermit) {
    hermit.isEscaping = true;
    hermit.classList.add('running'); 

    // 現在位置(px)から一番近い壁へ逃げる
    const currentLeft = parseFloat(hermit.style.left);
    const parentWidth = beachScene.clientWidth;
    
    let targetLeft;
    // 画面中央より左なら左(-100px)へ、右なら右(width+100px)へ
    if (currentLeft < parentWidth / 2) {
        targetLeft = -100;
        hermit.classList.remove('walking-right'); // 左向き
    } else {
        targetLeft = parentWidth + 100;
        hermit.classList.add('walking-right'); // 右向き
    }

    // 全力で逃げる（0.5秒で画面外へ）
    requestAnimationFrame(() => {
        hermit.style.transition = 'left 0.5s ease-in'; 
        hermit.style.left = `${targetLeft}px`;
    });
  }

</script>
</body>
</html>
"""

# HTMLを描画
components.html(html_code, height=932)
