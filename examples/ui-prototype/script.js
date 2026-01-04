document.addEventListener('DOMContentLoaded', ()=>{
  const input = document.getElementById('cmd-input');
  const send = document.getElementById('cmd-send');
  const content = document.getElementById('content');
  const app = document.getElementById('app');

  // Detect browser / platform and apply variant classes
  const ua = navigator.userAgent || navigator.vendor || window.opera;
  function detectVariant() {
    const u = ua.toLowerCase();
    if (/firefox/.test(u)) return 'variant-firefox';
    if (/edg\//.test(u)) return 'variant-edge';
    if (/chrome\//.test(u) && !/edg\//.test(u)) return 'variant-chrome';
    if (/safari/.test(u) && !/chrome\//.test(u)) return 'variant-safari';
    if (/android/.test(u)) return 'variant-android';
    return 'variant-generic';
  }
  const variant = detectVariant();
  app.classList.add(variant);

  // Apply functional differences per-variant (demo)
  if (app.classList.contains('variant-firefox')) {
    // Firefox: left-anchored command bar with subtle bounce
    document.querySelector('.cmdbar').style.borderRadius = '8px';
  }
  if (app.classList.contains('variant-chrome')) {
    // Chrome: compact command bar and faster animation feel
    document.documentElement.style.setProperty('--gap','10px');
  }
  if (app.classList.contains('variant-safari')) {
    // Safari: emphasize glass effect
    document.documentElement.style.setProperty('--glass','rgba(255,255,255,0.07)');
  }
  if (app.classList.contains('variant-android')) {
    // Android: one-hand mode default (move mobilebar visible)
    document.querySelector('.mobilebar').setAttribute('aria-hidden','false');
  }

  // keyboard shortcut
  window.addEventListener('keydown', (e)=>{
    if((e.ctrlKey||e.metaKey) && e.code === 'Space'){
      e.preventDefault(); input.focus();
    }
  });

  send.addEventListener('click', runCommand);
  input.addEventListener('keydown', (e)=>{ if(e.key==='Enter') runCommand(); });

  function runCommand(){
    const v = input.value.trim();
    if(!v) return; input.value='';
    // simple intent parse (mirror of manva_core small parser) — demo only
    let out='Unknown command';
    if(/^search\s+/i.test(v)){
      out = 'Searching for: ' + v.replace(/^search\s+/i,'') + '\n(Results simulated)';
    } else if(/^open\s+/i.test(v)){
      out = 'Opening: ' + v.replace(/^open\s+/i,'');
    } else if(/summarize|summary/i.test(v)){
      out = 'Summary: This is a short demo summary generated locally.';
    }
    // Adjust output styling per variant to demonstrate differing UX
    const p = document.createElement('div');
    p.className='card';
    if (app.classList.contains('variant-firefox')) p.style.boxShadow = '0 6px 18px rgba(0,0,0,0.45)';
    if (app.classList.contains('variant-chrome')) p.style.border = '1px solid rgba(255,255,255,0.03)';
    if (app.classList.contains('variant-safari')) p.style.backdropFilter = 'blur(8px)';
    p.innerHTML = `<h3>Command result</h3><p style="white-space:pre-wrap">${escapeHtml(out)}</p>`;
    content.appendChild(p); p.scrollIntoView({behavior:'smooth',block:'end'});
  }

  function escapeHtml(s){ return s.replace(/[&<>"']/g, c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":"&#39;"})[c]); }
});
