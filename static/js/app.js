const observer = new IntersectionObserver(
  (entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add("in");
      }
    });
  },
  { threshold: 0.15 }
);

document.querySelectorAll(".reveal").forEach((el, index) => {
  el.style.transitionDelay = `${index * 90}ms`;
  observer.observe(el);
});

function initMatrixRain() {
  const container = document.getElementById("matrix-rain");
  if (!container) return;

  const canvas = document.createElement("canvas");
  container.innerHTML = "";
  container.appendChild(canvas);

  const ctx = canvas.getContext("2d");
  if (!ctx) return;

  const chars = "0123456789";
  const fontSize = 14;
  let cols = 0;
  let drops = [];

  function resize() {
    const rect = container.getBoundingClientRect();
    canvas.width = Math.max(1, Math.floor(rect.width));
    canvas.height = Math.max(1, Math.floor(rect.height));
    cols = Math.max(1, Math.floor(canvas.width / fontSize));
    drops = Array.from({ length: cols }, () => Math.random() * -40);
  }

  function draw() {
    ctx.fillStyle = "rgba(12, 18, 14, 0.16)";
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    ctx.fillStyle = "rgba(170, 255, 205, 0.92)";
    ctx.font = `${fontSize}px "Courier New", monospace`;

    for (let i = 0; i < cols; i++) {
      const text = chars[Math.floor(Math.random() * chars.length)];
      const x = i * fontSize;
      const y = drops[i] * fontSize;
      ctx.fillText(text, x, y);

      if (y > canvas.height && Math.random() > 0.975) {
        drops[i] = Math.random() * -20;
      }
      drops[i] += 0.72;
    }

    requestAnimationFrame(draw);
  }

  resize();
  draw();
  window.addEventListener("resize", resize);
}

initMatrixRain();
