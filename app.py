import streamlit as st
import streamlit.components.v1 as components

# ページ設定
st.set_page_config(page_title="カニと愉快な仲間たち（全部乗せ）", layout="centered")

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
    touch-action: manipulation;
    user-select: none;
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

  /* --- 共通: タップできる要素 --- */
  .interactive {
    cursor: pointer;
    -webkit-tap-highlight-color: transparent;
    touch-action: none;
  }

  /* =========================================
     1. メインのカニ & 穴
     ========================================= */
  .hole { position: absolute; bottom: 150px; left: 50%; transform: translateX(-50%); width: 60px; height: 18px; background-color: #4a3b2a; border-radius: 50%; box-shadow: inset 0 3px 6px rgba(0,0,0,0.6); z-index: 10; }
  .crab-stage { position: absolute; bottom: 159px; left: 50%; transform: translateX(-50%); width: 80px; height: 100px; overflow: hidden; z-index: 20; pointer-events: none; }
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

  /* =========================================
     2. 謎の生き物 (Hermit)
     ========================================= */
  .hermit-container { position: absolute; width: 40px; height: 35px; z-index: 18; }
  .hermit-container.walking-right { transform: scaleX(-1); }
  .hermit-body { position: absolute; bottom: 0; left: 10px; width: 25px; height: 15px; background-color: #ffccbc; border-radius: 50% 50% 20% 20%; border: 1px solid #e64a19; z-index: 1; }
  .hermit-eye { position: absolute; top: -8px; width: 4px; height: 4px; background-color: white; border: 1px solid #e64a19; border-radius: 50%; }
  .hermit-eye::after { content: ''; position: absolute; top: 1px; left: 1px; width: 2px; height: 2px; background-color: black; border-radius: 50%; }
  .hermit-eye.left { left: 5px; } .hermit-eye.right { right: 5px; }
  .hermit-leg { position: absolute; bottom: -2px; width: 8px; height: 3px; background-color: #e64a19; border-radius: 2px; }
  .hermit-leg.L1 { left: 0px; transform: rotate(-10deg); } .hermit-leg.L2 { left: 5px; transform: rotate(10deg); } .hermit-leg.L3 { left: 15px; transform: rotate(10deg); }
  .hermit-container.walking .hermit-leg { animation: hermit-walk 0.5s infinite alternate; }
  .hermit-container.walking .hermit-body { animation: hermit-bob 0.5s infinite alternate; }
  /* 焦り */
  .hermit-container.struggling .hermit-leg { animation: hermit-panic 0.05s infinite alternate; }
  .hermit-container.struggling .hermit-body { animation: hermit-shake 0.05s infinite alternate; }
  /* 逃走 */
  .hermit-container.running .hermit-leg { animation: hermit-panic 0.05s infinite alternate; }
  .hermit-container.running .hermit-body { animation: hermit-bob 0.1s infinite alternate; }

  /* =========================================
     3. チンアナゴ (Eel)
     ========================================= */
  .eel-container {
    position: absolute;
    width: 10px; height: 40px;
    z-index: 5; /* 砂と同じくらい */
    transform-origin: bottom center;
    transition: transform 0.2s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  }
  .eel-body {
    position: absolute; bottom: 0; left: 0; width: 100%; height: 100%;
    background: repeating-linear-gradient(0deg, #fff 0px, #fff 4px, #333 4px, #333 5px);
    border-radius: 5px 5px 0 0;
    animation: eel-sway 3s infinite ease-in-out alternate;
  }
  .eel-eye {
    position: absolute; top: 5px; width: 3px; height: 3px; background: black; border-radius: 50%;
  }
  .eel-eye.left { left: 1px; } .eel-eye.right { right: 1px; }
  /* 引っ込むアニメーション */
  .eel-container.hiding {
    transform: scaleY(0); /* 縦に潰れて消える */
  }

  /* =========================================
     4. エビ (Shrimp)
     ========================================= */
  .shrimp-container {
    position: absolute;
    width: 25px; height: 20px;
    z-index: 19;
  }
  .shrimp-body {
    width: 100%; height: 100%;
    border-radius: 50%;
    border-top: 4px solid #ff9f43; /* 曲がった背中 */
    border-left: 2px solid transparent;
    border-right: 2px solid transparent;
    transform: rotate(-15deg);
  }
  /* ピョンピョン跳ねる */
  .shrimp-container.hopping {
    animation: shrimp-hop 0.5s infinite alternate;
  }
  /* 吹っ飛ぶ */
  .shrimp-container.flying {
    transition: all 0.5s ease-out;
    opacity: 0;
  }

  /* =========================================
     5. ヒトデ (Starfish)
     ========================================= */
  .starfish-container {
    position: absolute;
    width: 30px; height: 30px;
    z-index: 4; /* 地面這う */
    opacity: 0.9;
  }
  .starfish-shape {
    width: 100%; height: 100%;
    background: #ff6b81;
    clip-path: polygon(50% 0%, 61% 35%, 98% 35%, 68% 57%, 79% 91%, 50% 70%, 21% 91%, 32% 57%, 2% 35%, 39% 35%);
    transition: transform 0.5s;
  }
  /* 回転 */
  .starfish-container.spinning .starfish-shape {
    animation: spin 0.5s infinite linear;
  }


  /* =========================================
     エフェクト & アニメーション
     ========================================= */
  .sweat { position: absolute; font-size: 20px; pointer-events: none; z-index: 30; animation: sweat-pop 0.6s linear forwards; }
  
  @keyframes eel-sway { from { transform: rotate(-5deg); } to { transform: rotate(5deg); } }
  @keyframes shrimp-hop { from { transform: translateY(0); } to { transform: translateY(-15px); } }
  @keyframes spin { 100% { transform: rotate(360deg); } }
  
  /* 既存のアニメーション定義 */
  @keyframes snip-left { from { transform: rotate(-10deg); } to { transform: rotate(-40deg); } }
  @keyframes snip-right { from { transform: rotate(10deg); } to { transform: rotate(40deg); } }
  @keyframes blink { 0%, 96%, 100% { transform: scaleY(1); } 98% { transform: scaleY(0.1); } }
  @keyframes walk-leg { from { transform: rotate(-10deg); } to { transform: rotate(10deg); } }
  @keyframes hermit-walk { from { transform: rotate(-10deg); } to { transform: rotate(20deg); } }
  @keyframes hermit-bob { from { transform: translateY(0); } to { transform: translateY(-1px); } }
  @keyframes hermit-panic { from { transform: rotate(-30deg); } to { transform: rotate(30deg); } }
  @keyframes hermit-shake { from { transform: translateX(-2px) rotate(-5deg); } to { transform: translateX(2px) rotate(5deg); } }
  @keyframes sweat-pop {
    0% { transform: translate(0, 0) scale(0.5); opacity: 1; }
    50% { transform: translate(10px, -20px) scale(1.2); opacity: 0.8; }
    100% { transform: translate(20px, -40px) scale(0); opacity: 0; }
  }
</style>
</head>
<body>

<div class="beach-scene">
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
  const beachScene = document.querySelector('.beach-scene');

  // =========================================
  // 1. カニ (Crab) - 既存ロジック
  // =========================================
  const crab = document.getElementById('crab');
  const stage = document.getElementById('stage');
  let crabMode = 'HOLE';
  const HOLE_X = 50; const HOLE_Y = 85; 
  const POS_HIDDEN_Y = '100px'; const POS_PEEK_Y = '60px'; const POS_GROUND_Y = '20px';  
  setTimeout(decideCrabAction, 1000);

  function decideCrabAction() {
    let delay = 1000;
    if (crabMode === 'HOLE') {
      const dice = Math.random();
      if (dice < 0.4) {
        crab.style.top = POS_PEEK_Y; delay = 2000 + Math.random() * 1500; setTimeout(() => { if(crabMode==='HOLE') crab.style.top = POS_HIDDEN_Y; }, delay - 500);
      } else if (dice < 0.7) {
        crab.style.top = POS_GROUND_Y; setTimeout(() => { stage.style.overflow = 'visible'; crab.style.top = `${HOLE_Y}%`; crab.style.left = `${HOLE_X}%`; crabMode = 'BEACH'; decideCrabAction(); }, 1500); return;
      } else {
        crab.style.top = POS_HIDDEN_Y; delay = 2000;
      }
    } else if (crabMode === 'BEACH') {
      const dice = Math.random();
      if (dice < 0.2) { delay = 1000 + Math.random() * 1500;
      } else if (dice < 0.6) { moveCrabRandom(); delay = 3500;
      } else if (dice < 0.8) { crab.classList.add('snipping'); delay = 1500; setTimeout(() => { crab.classList.remove('snipping'); }, delay);
      } else { returnCrabHome(); return; }
    }
    setTimeout(decideCrabAction, delay);
  }
  function moveCrabRandom() {
    crab.classList.add('walking');
    const targetX = 5 + Math.random() * 90; const targetY = 5 + Math.random() * 90;
    crab.style.left = `${targetX}%`; crab.style.top = `${targetY}%`;
    setTimeout(() => { crab.classList.remove('walking'); }, 3000);
  }
  function returnCrabHome() {
    crab.classList.add('walking');
    crab.style.left = `${HOLE_X}%`; crab.style.top = `${HOLE_Y}%`;
    setTimeout(() => {
      crab.classList.remove('walking'); crab.style.top = POS_GROUND_Y; crab.style.left = '50%'; stage.style.overflow = 'hidden'; crabMode = 'HOLE';
      setTimeout(() => { crab.style.top = POS_HIDDEN_Y; setTimeout(decideCrabAction, 2000); }, 100); 
    }, 3000);
  }


  // =========================================
  // 2. 謎の生き物 (Hermit) - パニック機能付き
  // =========================================
  let activeHermits = 0; const MAX_HERMITS = 4; // 少し減らす
  setTimeout(startHermitLoop, 3000);

  function startHermitLoop() {
    const nextCheckTime = 3000 + Math.random() * 5000; 
    if (activeHermits < MAX_HERMITS) spawnHermit();
    setTimeout(startHermitLoop, nextCheckTime);
  }

  function spawnHermit() {
    activeHermits++;
    const hermit = document.createElement('div');
    hermit.classList.add('hermit-container', 'interactive');
    hermit.innerHTML = `<div class="hermit-body"><div class="hermit-eye left"></div><div class="hermit-eye right"></div><div class="hermit-leg L1"></div><div class="hermit-leg L2"></div><div class="hermit-leg L3"></div></div>`;
    beachScene.appendChild(hermit);

    hermit.addEventListener('click', onTapHermit);
    hermit.addEventListener('touchstart', onTapHermit, {passive: true});

    const spawnY = 10 + Math.random() * 70; 
    hermit.style.top = `${spawnY}%`;
    const startFromRight = Math.random() < 0.5;
    let startLeft = startFromRight ? '115%' : '-15%';
    let endLeft = startFromRight ? '-15%' : '115%';
    if (!startFromRight) hermit.classList.add('walking-right');
    hermit.style.left = startLeft;

    requestAnimationFrame(() => { requestAnimationFrame(() => {
      hermit.classList.add('walking');
      const duration = 20 + Math.random() * 20;
      hermit.style.transition = `left ${duration}s linear`;
      hermit.style.left = endLeft;
    });});

    hermit.addEventListener('transitionend', () => {
      if (!hermit.isEscaping) removeElement(hermit, () => activeHermits--);
      else removeElement(hermit, () => activeHermits--);
    });
  }

  function onTapHermit(e) {
    e.stopPropagation(); // 他のクリックを邪魔しない
    const hermit = e.currentTarget;
    if (hermit.isEscaping) return;
    
    // 停止＆固定
    const computedStyle = window.getComputedStyle(hermit);
    hermit.style.transition = 'none';
    hermit.style.left = computedStyle.left;
    
    // パニック
    hermit.isEscaping = true;
    hermit.classList.remove('walking');
    hermit.classList.add('struggling');
    hermit.sweatInterval = setInterval(() => createSweat(hermit), 150);

    // 逃走
    setTimeout(() => {
      hermit.classList.remove('struggling');
      if (hermit.sweatInterval) clearInterval(hermit.sweatInterval);
      
      hermit.classList.add('running');
      const currentLeft = parseFloat(hermit.style.left);
      const parentWidth = beachScene.clientWidth;
      const targetLeft = currentLeft < parentWidth / 2 ? -100 : parentWidth + 100;
      if (targetLeft > 0) hermit.classList.add('walking-right');
      else hermit.classList.remove('walking-right');

      requestAnimationFrame(() => {
        hermit.style.transition = 'left 0.5s ease-in';
        hermit.style.left = `${targetLeft}px`;
      });
    }, 500);
  }


  // =========================================
  // 3. チンアナゴ (Eels) - 固定位置
  // =========================================
  function spawnEels() {
    for (let i = 0; i < 4; i++) {
        const eel = document.createElement('div');
        eel.classList.add('eel-container', 'interactive');
        eel.innerHTML = `<div class="eel-body"><div class="eel-eye left"></div><div class="eel-eye right"></div></div>`;
        
        // 画面下部に配置
        const x = 5 + Math.random() * 90;
        const y = 80 + Math.random() * 15; // 80%~95%の高さ
        eel.style.left = `${x}%`;
        eel.style.top = `${y}%`;
        
        eel.addEventListener('click', (e) => {
            e.stopPropagation();
            if (eel.classList.contains('hiding')) return;
            // 引っ込む
            eel.classList.add('hiding');
            // しばらくしたら戻る
            setTimeout(() => eel.classList.remove('hiding'), 3000 + Math.random() * 2000);
        });
        // スマホ対応
        eel.addEventListener('touchstart', (e) => { eel.click(); }, {passive: true});

        beachScene.appendChild(eel);
    }
  }
  spawnEels();


  // =========================================
  // 4. エビ (Shrimp) - 飛び跳ねて吹っ飛ぶ
  // =========================================
  setTimeout(startShrimpLoop, 8000); // ちょっと遅れて開始
  function startShrimpLoop() {
    const nextCheck = 10000 + Math.random() * 10000;
    spawnShrimp();
    setTimeout(startShrimpLoop, nextCheck);
  }

  function spawnShrimp() {
    const shrimp = document.createElement('div');
    shrimp.classList.add('shrimp-container', 'hopping', 'interactive');
    shrimp.innerHTML = `<div class="shrimp-body"></div>`;
    beachScene.appendChild(shrimp);

    const startFromRight = Math.random() < 0.5;
    shrimp.style.top = `${20 + Math.random() * 60}%`;
    shrimp.style.left = startFromRight ? '110%' : '-10%';
    if (!startFromRight) shrimp.style.transform = 'scaleX(-1)'; // 向き

    shrimp.addEventListener('click', (e) => {
        e.stopPropagation();
        // 吹っ飛ぶ
        shrimp.classList.add('flying');
        shrimp.style.transform += 'translateY(-200px) rotate(720deg) scale(0)';
        setTimeout(() => removeElement(shrimp), 500);
    });
    shrimp.addEventListener('touchstart', (e) => { shrimp.click(); }, {passive: true});

    requestAnimationFrame(() => { requestAnimationFrame(() => {
        const duration = 15 + Math.random() * 10;
        shrimp.style.transition = `left ${duration}s linear`;
        shrimp.style.left = startFromRight ? '-10%' : '110%';
    });});

    shrimp.addEventListener('transitionend', () => {
        if (!shrimp.classList.contains('flying')) removeElement(shrimp);
    });
  }


  // =========================================
  // 5. ヒトデ (Starfish) - 流れて回転
  // =========================================
  setTimeout(startStarfishLoop, 5000);
  function startStarfishLoop() {
    const nextCheck = 15000 + Math.random() * 15000; // レアキャラ
    spawnStarfish();
    setTimeout(startStarfishLoop, nextCheck);
  }

  function spawnStarfish() {
    const starfish = document.createElement('div');
    starfish.classList.add('starfish-container', 'interactive');
    starfish.innerHTML = `<div class="starfish-shape"></div>`;
    beachScene.appendChild(starfish);

    // 斜めに流れる
    const startX = Math.random() * 100;
    const startY = -10;
    const endX = startX + (Math.random() - 0.5) * 50;
    const endY = 110;

    starfish.style.left = `${startX}%`;
    starfish.style.top = `${startY}%`;

    starfish.addEventListener('click', (e) => {
        e.stopPropagation();
        starfish.classList.add('spinning');
        setTimeout(() => starfish.classList.remove('spinning'), 1000);
    });
    starfish.addEventListener('touchstart', (e) => { starfish.click(); }, {passive: true});

    requestAnimationFrame(() => { requestAnimationFrame(() => {
        const duration = 20 + Math.random() * 20; // ゆっくり
        starfish.style.transition = `top ${duration}s linear, left ${duration}s linear`;
        starfish.style.top = `${endY}%`;
        starfish.style.left = `${endX}%`;
    });});

    starfish.addEventListener('transitionend', () => removeElement(starfish));
  }


  // =========================================
  // ユーティリティ
  // =========================================
  function removeElement(el, callback) {
    if (el.parentNode) {
        el.parentNode.removeChild(el);
        if (callback) callback();
    }
  }

  function createSweat(parent) {
    const sweat = document.createElement('div');
    sweat.innerText = '💦';
    sweat.classList.add('sweat');
    const dx = (Math.random() - 0.5) * 40;
    sweat.style.left = `calc(50% + ${dx}px)`;
    sweat.style.top = '-20px';
    parent.appendChild(sweat);
    setTimeout(() => { if(sweat.parentNode) sweat.parentNode.removeChild(sweat); }, 600);
  }

</script>
</body>
</html>
"""

# HTMLを描画
components.html(html_code, height=932)
