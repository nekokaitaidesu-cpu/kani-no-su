import streamlit as st
import streamlit.components.v1 as components

# ページ設定（スマホを意識してデフォルトのlayout="centered"に戻す）
st.set_page_config(page_title="カニカニ・スマホライフ")

# タイトルなどはシンプルに
# st.title("🦀") # タイトルがあるとスマホだと狭くなるので、あえて消してみるのもアリかも？

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
    /* 砂の質感 */
    background-image: 
      radial-gradient(circle at 50% 50%, #e6c288 1px, transparent 1px),
      radial-gradient(circle at 20% 80%, #dcb 1px, transparent 1px);
    background-size: 20px 20px, 30px 30px;
    /* スマホの縦長画面の中央に配置 */
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh; /* ビューポートの高さ一杯 */
    width: 100vw;  /* ビューポートの幅一杯 */
    touch-action: none; /* スマホでのスクロール操作などを無効化 */
  }

  /* フィールド（砂浜エリア）
     スマホ画面サイズ(約400x800)を想定して直接指定。
     scaleは使わず、実寸でレイアウトする形に変更したっち。
  */
  .beach-scene {
    position: relative;
    width: 100%;   /* 画面幅いっぱい */
    height: 100%;  /* 画面高さいっぱい */
    max-width: 430px; /* スマホの最大幅を想定 */
    max-height: 900px; /* スマホの最大高さを想定 */
    /* border: 2px solid red; デバッグ用枠線 */
  }

  /* --- 穴 --- */
  .hole {
    position: absolute;
    bottom: 150px; /* 下の方に配置 */
    left: 50%;
    transform: translateX(-50%);
    width: 120px; /* 少し小さく */
    height: 35px;
    background-color: #4a3b2a;
    border-radius: 50%;
    box-shadow: inset 0 5px 10px rgba(0,0,0,0.6);
    z-index: 10;
  }

  /* カニのステージ（初期は穴の中を隠すマスク） */
  .crab-stage {
    position: absolute;
    bottom: 165px; /* 穴の位置に合わせる */
    left: 50%;
    transform: translateX(-50%);
    width: 150px;
    height: 150px; /* 穴の周辺 */
    overflow: hidden; /* 初期は隠す */
    z-index: 11;
    pointer-events: none;
    /* border: 1px solid blue; デバッグ用 */
  }

  /* カニコンテナ（実際に動く箱） */
  .crab-container {
    position: absolute;
    /* 初期位置：ステージの下（穴の底） */
    top: 150px; 
    left: 50%;
    width: 100px; /* カニ本体も少し小さく */
    height: 80px;
    margin-left: -50px; /* 中心合わせ */
    
    /* 動きの滑らかさ設定 (top, leftをアニメーション) */
    transition: top 1.5s cubic-bezier(0.5, 0, 0.5, 1), left 1.5s linear;
    z-index: 20; /* 常に手前に */
  }

  /* --- アクション用のクラス（JSで付与） --- */
  /* チョキチョキ */
  .crab-container.snipping .claw.left::after { animation: snip-left 0.2s infinite alternate; }
  .crab-container.snipping .claw.right::after { animation: snip-right 0.2s infinite alternate; }

  /* ★追加★ 歩きモーション */
  .crab-container.walking .leg.L1 { animation: walk-leg 0.3s infinite alternate; }
  .crab-container.walking .leg.R1 { animation: walk-leg 0.3s infinite alternate 0.15s; /* タイミングをずらす */ }
  .crab-container.walking .leg.L2 { animation: walk-leg 0.3s infinite alternate 0.15s; }
  .crab-container.walking .leg.R2 { animation: walk-leg 0.3s infinite alternate; }
  /* 歩くときに体も少し揺らす */
  .crab-container.walking .body { animation: walk-body 0.3s infinite alternate; }


  /* --- カニのパーツ（サイズ調整） --- */
  .body {
    position: absolute; bottom: 0;
    width: 100px; height: 65px; /* 少し小さく */
    background-color: #ff6b6b; border-radius: 50% 50% 40% 40%; border: 3px solid #c0392b; box-shadow: inset -4px -4px 8px rgba(0,0,0,0.1);
  }
  .eye-stalk { position: absolute; top: -15px; width: 5px; height: 20px; background-color: #c0392b; transition: transform 0.3s; }
  .eye-stalk.left { left: 25px; transform: rotate(-15deg); } .eye-stalk.right { right: 25px; transform: rotate(15deg); }
  .eye { position: absolute; top: -20px; width: 14px; height: 14px; background-color: white; border-radius: 50%; border: 2px solid #c0392b; }
  .eye::after { content: ''; position: absolute; top: 3px; left: 3px; width: 6px; height: 6px; background-color: black; border-radius: 50%; animation: blink 4s infinite; }
  .eye.left { left: 20px; } .eye.right { right: 20px; }
  
  .claw { position: absolute; top: 5px; width: 30px; height: 20px; border: 3px solid #c0392b; background-color: #ff6b6b; border-radius: 50% 50% 10% 10%; transform-origin: bottom center; transition: transform 0.3s; }
  .claw.left { left: -20px; transform: rotate(-30deg); }
  .claw.left::after { content: ''; position: absolute; top: -12px; left: 0; width: 18px; height: 20px; background-color: #ff6b6b; border: 3px solid #c0392b; border-radius: 50% 10% 0 0; transform: rotate(-20deg); transform-origin: bottom right; }
  .claw.right { right: -20px; transform: rotate(30deg); }
  .claw.right::after { content: ''; position: absolute; top: -12px; right: 0; width: 18px; height: 20px; background-color: #ff6b6b; border: 3px solid #c0392b; border-radius: 10% 50% 0 0; transform: rotate(20deg); transform-origin: bottom left; }
  
  /* 足（4本に増やしてクラス名を付与） */
  .leg { position: absolute; bottom: 8px; width: 18px; height: 5px; background-color: #c0392b; border-radius: 5px; transform-origin: right center;}
  .leg.left { transform-origin: right center; } .leg.right { transform-origin: left center; }
  .leg.L1 { left: -15px; transform: rotate(-20deg); }
  .leg.L2 { left: -5px; bottom: 5px; transform: rotate(-10deg); }
  .leg.R1 { right: -15px; transform: rotate(20deg); }
  .leg.R2 { right: -5px; bottom: 5px; transform: rotate(10deg); }


  /* --- 貝殻（サイズ調整と配置） --- */
  .shell { position: absolute; width: 35px; height: 30px; background: repeating-linear-gradient(90deg, #fff0f5 0px, #fff0f5 3px, #ffc1e3 4px, #ffc1e3 5px); border-radius: 50% 50% 10% 10%; box-shadow: 2px 2px 4px rgba(0,0,0,0.2); z-index: 5; }
  .shell::after { content: ''; position: absolute; bottom: -4px; left: 50%; transform: translateX(-50%); width: 8px; height: 5px; background-color: #ffc1e3; border-radius: 2px; }
  .shell-spiral { position: absolute; width: 0; height: 0; border-left: 8px solid transparent; border-right: 8px solid transparent; border-bottom: 35px solid #fff; border-radius: 50%; transform: rotate(45deg); filter: drop-shadow(2px 2px 2px rgba(0,0,0,0.2)); z-index: 5; }
  .shell-spiral::before { content: ''; position: absolute; top: 18px; left: -8px; width: 16px; height: 16px; background-color: #eee; border-radius: 50%; }

  /* --- アニメーション定義 --- */
  @keyframes snip-left { from { transform: rotate(-10deg); } to { transform: rotate(-40deg); } }
  @keyframes snip-right { from { transform: rotate(10deg); } to { transform: rotate(40deg); } }
  @keyframes blink { 0%, 96%, 100% { transform: scaleY(1); } 98% { transform: scaleY(0.1); } }
  /* ★追加★ 足のパタパタ */
  @keyframes walk-leg { from { transform: rotate(-10deg); } to { transform: rotate(10deg); } }
  /* ★追加★ 体の揺れ */
  @keyframes walk-body { from { transform: translateY(0); } to { transform: translateY(-2px); } }

</style>
</head>
<body>

<div class="beach-scene">
  <div class="shell" style="top: 20%; left: 15%; transform: rotate(-20deg);"></div>
  <div class="shell" style="top: 10%; left: 75%; transform: rotate(10deg); background: repeating-linear-gradient(90deg, #fff 0px, #fff 3px, #aee 4px, #aee 5px);"></div>
  <div class="shell-spiral" style="top: 40%; left: 85%; transform: rotate(60deg);"></div>
  <div class="shell-spiral" style="top: 5%; left: 30%; transform: rotate(-30deg);"></div>
  <div class="shell" style="top: 30%; left: 50%; transform: rotate(180deg); opacity: 0.8;"></div>
  <div class="shell" style="top: 55%; left: 10%; transform: rotate(45deg); background: repeating-linear-gradient(90deg, #fff 0px, #fff 3px, #eec 4px, #eec 5px);"></div>
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
  
  // 状態管理
  let mode = 'HOLE';
  
  // 座標設定（スマホ画面での相対位置 %）
  // 穴の位置（画面下部中央）を基準とする
  const HOLE_X = 50; // %
  const HOLE_Y = 85; // % (画面下の方)

  // 穴の中での相対位置 (px)
  const POS_HIDDEN_Y = '150px'; // 奥底
  const POS_PEEK_Y   = '100px'; // ちょい出し
  const POS_GROUND_Y = '50px';  // 地上付近（出口）

  // メインループ開始
  setTimeout(decideNextAction, 1000);

  function decideNextAction() {
    let delay = 1000;

    if (mode === 'HOLE') {
      // --- 穴モード ---
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
          // マスクを解除して、カニをステージから出してbody直下に移動（座標系を変更）
          stage.style.overflow = 'visible'; 
          
          // 座標を「穴の中の相対座標」から「画面全体の%座標」へ変換
          crab.style.top = `${HOLE_Y}%`;
          crab.style.left = `${HOLE_X}%`;
          
          mode = 'BEACH';
          decideNextAction(); 
        }, 1500); // 出てくるアニメーション時間待つ
        return;

      } else {
        // ③隠れる
        console.log("Action: Hide");
        crab.style.top = POS_HIDDEN_Y;
        delay = 2000;
      }

    } else if (mode === 'BEACH') {
      // --- 砂浜モード ---
      const dice = Math.random();

      if (dice < 0.2) {
        // ①じっとする
        console.log("Action: Stay");
        delay = 1000 + Math.random() * 1500;

      } else if (dice < 0.6) {
        // ★変更★ ②ランダム移動（全方向）
        console.log("Action: Move Random");
        moveRandom();
        delay = 3500; // 移動時間を考慮して長めに

      } else if (dice < 0.8) {
        // ④チョキチョキ
        console.log("Action: Snip");
        crab.classList.add('snipping');
        delay = 1500;
        setTimeout(() => { crab.classList.remove('snipping'); }, delay);

      } else {
        // ⑤帰宅
        console.log("Action: Return Home");
        returnHome();
        return; 
      }
    }
    setTimeout(decideNextAction, delay);
  }

  // ★追加★ 全方向ランダム移動関数
  function moveRandom() {
    // 歩きモーション開始
    crab.classList.add('walking');

    // 画面内のランダムな位置を決定 (マージンを考慮して10%~90%の範囲)
    const targetX = 10 + Math.random() * 80; // %
    const targetY = 10 + Math.random() * 70; // % (上の方まで行けるように)

    // 移動 (CSS transitionでアニメーション)
    crab.style.left = `${targetX}%`;
    crab.style.top = `${targetY}%`;

    // 移動が終わったら歩きモーション終了 (transition時間に合わせて調整)
    setTimeout(() => {
        crab.classList.remove('walking');
    }, 3000);
  }

  // 帰宅関数
  function returnHome() {
    // 歩きモーション開始
    crab.classList.add('walking');

    // 穴の位置へ移動
    crab.style.left = `${HOLE_X}%`;
    crab.style.top = `${HOLE_Y}%`;

    // 移動完了後、穴に入る処理
    setTimeout(() => {
      crab.classList.remove('walking'); // 歩き終了

      // 座標系を元に戻す（穴の中の相対座標へ）
      crab.style.top = POS_GROUND_Y; 
      crab.style.left = '50%';

      // マスクを有効化して潜る
      stage.style.overflow = 'hidden'; 
      mode = 'HOLE';
      
      setTimeout(() => {
          crab.style.top = POS_HIDDEN_Y; // 潜る
          setTimeout(decideNextAction, 2000); // 次のループへ
      }, 100); // 座標切り替えの反映を少し待つ

    }, 3000); // 帰宅の移動時間
  }

</script>
</body>
</html>
"""

# HTMLを描画（heightをスマホ画面に合わせて大きく設定）
# 実際のスマホ表示ではiframeの高さが画面いっぱいになるようにCSSで調整しているため
# ここのheightは大きめに確保しておけばOKだっち。
components.html(html_code, height=900)
