import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="🕳ここに家にはいないかに！", layout="centered")

html = """
<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<style>
body {
  background: #0f172a;
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
}

.field {
  display: grid;
  grid-template-columns: repeat(3, 120px);
  gap: 30px;
}

.hole {
  width: 120px;
  height: 60px;
  background: #020617;
  border-radius: 50%;
  position: relative;
  overflow: hidden;
}

.crab {
  position: absolute;
  bottom: -40px;
  left: 50%;
  transform: translateX(-50%);
  font-size: 40px;
  animation: pop 6s infinite;
}

/* 個体差 */
.crab.delay1 { animation-delay: 1s; }
.crab.delay2 { animation-delay: 2.5s; }
.crab.delay3 { animation-delay: 4s; }

@keyframes pop {
  0%   { bottom: -40px; }
  20%  { bottom: 10px; }
  40%  { bottom: 10px; }
  50%  { content: "🦀✌️"; }
  60%  { bottom: 10px; }
  100% { bottom: -40px; }
}
</style>
</head>
<body>

<div class="field">
  <div class="hole"><div class="crab delay1">🦀</div></div>
  <div class="hole"><div class="crab delay2">🦀</div></div>
  <div class="hole"><div class="crab delay3">🦀</div></div>
  <div class="hole"><div class="crab delay2">🦀</div></div>
  <div class="hole"><div class="crab delay1">🦀</div></div>
  <div class="hole"><div class="crab delay3">🦀</div></div>
</div>

</body>
</html>
"""

components.html(html, height=450)
