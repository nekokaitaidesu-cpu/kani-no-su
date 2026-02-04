import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="カニカニ・パーフェクトライフ最終版", layout="centered")

html_code = """
<!DOCTYPE html>
<html lang="ja">
<head>
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<style>
  body {
    margin: 0;
    overflow: hidden;
    background-color: #f6d7b0;
    background-image:
      radial-gradient(circle at 50% 50%, #e6c288 1px, transparent 1px),
      radial-gradient(circle at 20% 80%, #dcb 1px, transparent 1px);
    background-size: 20px 20px, 30px 30px;
    height: 100vh;
    width: 100vw;
  }

  .beach-scene {
    position: relative;
    width: 100%;
    height: 100%;
    max-width: 430px;
    max-height: 932px;
    margin: auto;
  }

  /* ===== 穴ラッパー（基準点） ===== */
  .hole-wrapper {
    position: absolute;
    left: 50%;
    top: 85%;
    transform: translate(-50%, -50%);
    width: 120px;
    height: 160px;
    pointer-events: none;
  }

  .hole {
    position: absolute;
    top: 0;
    left: 50%;
    transform: translateX(-50%);
    width: 70px;
    height: 20px;
    background-color: #4a3b2a;
    border-radius: 50%;
    box-shadow: inset 0 3px 6px rgba(0,0,0,0.6);
    z-index: 30;
  }

  .crab-mask {
    position: absolute;
    top: 10px;
    left: 50%;
    transform: translateX(-50%);
    width: 80px;
    height: 140px;
    overflow: hidden;
    z-index: 20;
  }

  .crab-container {
    position: absolute;
    left: 50%;
    transform: translateX(-50%);
    width: 50px;
    height: 40px;
    transition: top 1.5s cubic-bezier(0.5,0,0.5,1), left 1.5s linear;
  }

  /* ===== 状態 ===== */
  .peeking { animation: peek 2s infinite alternate; }

  @keyframes peek {
    0% { transform: translateX(-50%) rotate(0deg); }
    50% { transform: translateX(-50%) rotate(-5deg); }
    100% { transform: translateX(-50%) rotate(5deg); }
  }

  /* ===== カニ ===== */
  .body { position: absolute; bottom: 0; width: 50px; height: 33px; background:#ff6b6b;
    border-radius:50% 50% 40% 40%; border:2px solid #c0392b; }
  .eye { position:absolute; top:-10px; width:8px; height:8px; background:white;
    border-radius:50%; border:1px solid #c0392b; }
  .eye.left { left:9px; } .eye.right { right:9px; }

</style>
</head>
<body>

<div class="beach-scene">

  <div class="hole-wrapper" id="hole">
    <div class="hole"></div>
    <div class="crab-mask" id="mask">
      <div class="crab-container" id="crab">
        <div class="body"></div>
        <div class="eye left"></div>
        <div class="eye right"></div>
      </div>
    </div>
  </div>

</div>

<script>
  const crab = document.getElementById("crab");
  const mask = document.getElementById("mask");

  const HIDDEN = "110px";
  const PEEK   = "45px";
  const EXIT   = "0px";

  let mode = "HOLE";

  function next() {
    if (mode === "HOLE") {
      const r = Math.random();
      if (r < 0.4) {
        crab.style.top = PEEK;
        crab.classList.add("peeking");
        setTimeout(() => {
          crab.classList.remove("peeking");
          crab.style.top = HIDDEN;
          next();
        }, 2500);
      } else {
        crab.style.top = EXIT;
        setTimeout(() => {
          mask.style.overflow = "visible";
          crab.style.top = "-60px";
          mode = "BEACH";
          next();
        }, 1500);
      }
    } else {
      setTimeout(() => {
        mask.style.overflow = "hidden";
        crab.style.top = HIDDEN;
        mode = "HOLE";
        next();
      }, 3000);
    }
  }

  crab.style.top = HIDDEN;
  setTimeout(next, 1000);
</script>

</body>
</html>
"""

components.html(html_code, height=932)
