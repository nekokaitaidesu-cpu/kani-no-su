import streamlit as st
import streamlit.components.v1 as components

# ページ設定
st.set_page_config(page_title="カニカニ・ライフ", layout="wide")

st.title("🦀 気ままなカニの日常")
st.write("カニさんが自分で考えて動くようになったっち！🍄")
st.write("穴から様子を伺ったり、お散歩したり、急に帰ったり…ずっと見てられるカニ〜。")

# JavaScriptとCSSを組み合わせたHTML
html_code = """
<!DOCTYPE html>
<html lang="ja">
<head>
<style>
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
    height: 500px;
  }

  /* 広いフィールド */
  .beach-scene {
    position: relative;
    width: 1500px;
    height: 800px;
    transform: scale(0.5);
    transform-origin: center center;
  }

  /* --- 穴 --- */
  .hole {
    position: absolute;
    bottom: 80px;
    left: 50%;
    transform: translateX(-50%);
    width: 140px;
    height: 40px;
    background-color: #4a3b2a;
    border-radius: 50%;
    box-shadow: inset 0 5px 10px rgba(0,0,0,0.6);
    z-index: 10;
  }

  /* カニの可動域（マスク） 
     初期状態は overflow: hidden だが、地上に出たら JS で visible に切り替える
  */
  .crab-stage {
    position: absolute;
    bottom: 100px;
    left: 50%;
    transform: translateX(-50%); /* 中央配置 */
    width: 200px; /* 穴の周辺 */
    height: 300px;
    overflow: hidden; /* 最初は隠れるモード */
    z-index: 11;
    pointer-events: none;
    /* transitionの設定はJS制御のために最小限に */
  }

  /* カニコンテナ（実際に動く箱） */
  .crab-container {
    position: absolute;
    top: 300px; /* 初期位置：穴の底（隠れてる） */
    left: 50%;  /* ステージの中央 */
    width: 120px;
    height: 100px;
    margin-left: -60px; /* 自身の半分の幅で中央寄せ補正 */
    
    /* 動きの滑らかさ設定 */
    transition: top 1s cubic-bezier(0.5, 0, 0.5, 1), left 1.5s linear, transform 0.5s;
  }

  /* チョキチョキ中のクラス（JSで付与） */
  .crab-container.snipping .claw.left::after { animation: snip-left 0.2s infinite alternate; }
  .crab-container.snipping .claw.right::after { animation: snip-right 0.2s infinite alternate; }

  /* --- カニのパーツ --- */
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
  .eye-stalk { position: absolute; top: -20px; width: 6px; height: 25px; background-color: #c0392b; transition: transform 0.3s; }
  .eye-stalk.left { left: 30px; transform: rotate(-15deg); }
  .eye-stalk.right { right: 30px; transform: rotate(15deg); }
  .eye { position: absolute; top: -25px; width: 16px; height: 16px; background-color: white; border-radius: 50%; border: 2px solid #c0392b; }
  .eye::after { content: ''; position: absolute; top: 4px; left: 4px; width: 6px; height: 6px; background-color: black; border-radius: 50%; animation: blink 4s infinite; }
  .eye.left { left: 24px; } .eye.right { right: 24px; }
  
  .claw { position: absolute; top: 10px; width: 35px; height: 25px; border: 3px solid #c0392b; background-color: #ff6b6b; border-radius: 50% 50% 10% 10%; transform-origin: bottom center; transition: transform 0.3s; }
  .claw.left { left: -25px; transform: rotate(-30deg); }
  .claw.left::after { content: ''; position: absolute; top: -15px; left: 0; width: 20px; height: 25px; background-color: #ff6b6b; border: 3px solid #c0392b; border-radius: 50% 10% 0 0; transform: rotate(-20deg); transform-origin: bottom right; }
  .claw.right { right: -25px; transform: rotate(30deg); }
  .claw.right::after { content: ''; position: absolute; top: -15px; right: 0; width: 20px; height: 25px; background-color: #ff6b6b; border: 3px solid #c0392b; border-radius: 10% 50% 0 0; transform: rotate(20deg); transform-origin: bottom left; }
  
  .leg { position: absolute; bottom: 10px; width: 20px; height: 5px; background-color: #c0392b; border-radius: 5px; transition: transform 0.2s;}
  .leg.left { left: -10px; transform: rotate(-20deg); } .leg.right { right: -10px; transform: rotate(20deg); }

  /* 貝殻など */
  .shell { position: absolute; width: 40px; height: 35px; background: repeating-linear-gradient(90deg, #fff0f5 0px, #fff0f5 4px, #ffc1e3 5px, #ffc1e3 6px); border-radius: 50% 50% 10% 10%; box-shadow: 2px 2px 5px rgba(0,0,0,0.2); z-index: 5; }
  .shell::after { content: ''; position: absolute; bottom: -5px; left: 50%; transform: translateX(-50%); width: 10px; height: 6px; background-color: #ffc1e3; border-radius: 2px; }
  .shell-spiral { position: absolute; width: 0; height: 0; border-left: 10px solid transparent; border-right: 10px solid transparent; border-bottom: 40px solid #fff; border-radius: 50%; transform: rotate(45deg); filter: drop-shadow(2px 2px 2px rgba(0,0,0,0.2)); z-index: 5; }
  .shell-spiral::before { content: ''; position: absolute; top: 20px; left: -10px; width: 20px; height: 20px; background-color: #eee; border-radius: 50%; }

  /* --- アニメーション定義（瞬きとハサミ用） --- */
  @keyframes snip-left { from { transform: rotate(-10deg); } to { transform: rotate(-40deg); } }
  @keyframes snip-right { from { transform: rotate(10deg); } to { transform: rotate(40deg); } }
  @keyframes blink { 0%, 96%, 100% { transform: scaleY(1); } 98% { transform: scaleY(0.1); } }

</style>
</head>
<body>

<div class="beach-scene">
  <div class="shell" style="top: 300px; left: 200px; transform: rotate(-20deg);"></div>
  <div class="shell" style="top: 150px; left: 900px; transform: rotate(10deg); background: repeating-linear-gradient(90deg, #fff 0px, #fff 4px, #aee 5px, #aee 6px);"></div>
  <div class="shell-spiral" style="top: 500px; left: 1100px; transform: rotate(60deg);"></div>
  <div class="shell-spiral" style="top: 100px; left: 350px; transform: rotate(-30deg);"></div>
  <div class="shell" style="top: 450px; left: 600px; transform: rotate(180deg); opacity: 0.8;"></div>
  <div class="shell" style="top: 600px; left: 150px; transform: rotate(45deg); background: repeating-linear-gradient(90deg, #fff 0px, #fff 4px, #eec 5px, #eec 6px);"></div>
  <div class="shell-spiral" style="top: 700px; left: 800px; transform: rotate(-90deg) scale(0.8);"></div>
  <div class="shell" style="top: 250px; left: 1300px; transform: rotate(15deg) scale(1.2);"></div>

  <div class="crab-home" style="position: absolute; bottom: 200px; left: 50%; transform: translateX(-50%) scale(0.6); transform-origin: bottom center; width: 300px; height: 300px; z-index: 20;">
    <div class="hole"></div>
    
    <div id="stage" class="crab-stage">
      <div id="crab" class="crab-container">
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

<script>
  const crab = document.getElementById('crab');
  const stage = document.getElementById('stage');
  
  // 状態管理
  // mode: 'HOLE' (穴の中/付近) or 'BEACH' (砂浜)
  let mode = 'HOLE';
  let currentX = 0; // ステージ中央からのオフセット(px)
  
  // 定数（高さ制御用）
  const POS_HIDDEN = '300px'; // 穴の奥底
  const POS_PEEK   = '250px'; // ちょい出し（キョロキョロ）
  const POS_GROUND = '200px'; // 地上（足が地面につく位置）

  // メインループ開始
  setTimeout(decideNextAction, 1000);

  function decideNextAction() {
    let delay = 1000; // 次の行動までの待ち時間（デフォルト）

    if (mode === 'HOLE') {
      // --- 穴モードの行動パターン ---
      // ①キョロキョロ ②出てくる ③隠れる
      const dice = Math.random();

      if (dice < 0.4) {
        // 行動①：キョロキョロ (40%)
        console.log("Action: Peek");
        crab.style.top = POS_PEEK;
        delay = 2000 + Math.random() * 2000;
        // キョロキョロ終わったら隠す
        setTimeout(() => { if(mode==='HOLE') crab.style.top = POS_HIDDEN; }, delay - 500);
      
      } else if (dice < 0.7) {
        // 行動②：出てくる (30%)
        console.log("Action: Exit Hole");
        crab.style.top = POS_GROUND;
        
        // 地上に出たら、少し待ってからマスクを解除して砂浜モードへ
        setTimeout(() => {
          stage.style.overflow = 'visible'; // 枠外移動解禁！
          mode = 'BEACH';
          decideNextAction(); // 即座に次の行動へ
        }, 1000);
        return; // 次の行動予約は setTimeout 内で行うのでここで終了

      } else {
        // 行動③：隠れる (30%)
        console.log("Action: Hide");
        crab.style.top = POS_HIDDEN;
        delay = 2000;
      }

    } else if (mode === 'BEACH') {
      // --- 砂浜モードの行動パターン ---
      // ①じっとする ②右移動 ③左移動 ④チョキチョキ ⑤帰宅
      const dice = Math.random();

      if (dice < 0.2) {
        // 行動①：じっとする (20%)
        console.log("Action: Stay");
        delay = 1000 + Math.random() * 2000;

      } else if (dice < 0.5) {
        // 行動②：右へ移動 (30%)
        console.log("Action: Move Right");
        moveRandom(1); // 正方向
        delay = 2000;

      } else if (dice < 0.8) {
        // 行動③：左へ移動 (30%)
        console.log("Action: Move Left");
        moveRandom(-1); // 負方向
        delay = 2000;

      } else if (dice < 0.9) {
        // 行動④：チョキチョキ (10%)
        console.log("Action: Snip");
        crab.classList.add('snipping');
        delay = 1500;
        setTimeout(() => { crab.classList.remove('snipping'); }, delay);

      } else {
        // 行動⑤：帰宅 (10%)
        console.log("Action: Return Home");
        returnHome();
        return; // 特別なフローなのでここで終了
      }
    }

    // 次の行動を予約
    setTimeout(decideNextAction, delay);
  }

  // 左右移動関数
  function moveRandom(direction) {
    const dist = 50 + Math.random() * 200; // 50px 〜 250px 移動
    let targetX = currentX + (dist * direction);

    // 画面外に行き過ぎないよう制限 (±700pxくらい)
    if (targetX > 700) targetX = 700;
    if (targetX < -700) targetX = -700;

    currentX = targetX;
    // 50% で中心位置(left:50%) + オフセット(px)
    crab.style.left = `calc(50% + ${currentX}px)`;
  }

  // 帰宅関数
  function returnHome() {
    // まず穴の真上(X=0)に戻る
    currentX = 0;
    crab.style.left = `50%`; // 中央に戻す

    // 移動時間を待ってから穴に入る
    setTimeout(() => {
      stage.style.overflow = 'hidden'; // マスク有効化（これ重要！）
      mode = 'HOLE';
      crab.style.top = POS_HIDDEN; // 潜る
      
      // 潜った後、また次のループへ
      setTimeout(decideNextAction, 2000);
    }, 1500); // 1.5秒かけて戻る想定
  }

</script>
</body>
</html>
"""

# HTMLを描画
components.html(html_code, height=500)
