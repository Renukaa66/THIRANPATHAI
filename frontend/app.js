const API = ""; // same-origin, backend serves this file too

let state = { resumeSkills: [], resumeText: "", learnedSkills: [], companies: [], selectedCompanyId: null };
let authMode = "login"; // or "signup"
let authToken = localStorage.getItem("thiranpathai_token") || null;

/* ---------- Auth ---------- */
function authHeaders(){
  return authToken ? { "Authorization": "Bearer " + authToken } : {};
}

document.getElementById("authToggleBtn").addEventListener("click", ()=>{
  authMode = authMode === "login" ? "signup" : "login";
  document.getElementById("authTitle").textContent = authMode === "login" ? "Welcome back" : "Create your account";
  document.getElementById("authHint").textContent = authMode === "login"
    ? "Log in to save your resume and pick up where you left off."
    : "Sign up to save your resume and track your progress.";
  document.getElementById("signupNameWrap").style.display = authMode === "signup" ? "block" : "none";
  document.getElementById("authSubmitBtn").textContent = authMode === "login" ? "Log In" : "Sign Up";
  document.getElementById("authToggleBtn").textContent = authMode === "login" ? "New here? Create an account" : "Already have an account? Log in";
  document.getElementById("authError").textContent = "";
});

document.getElementById("authSubmitBtn").addEventListener("click", async ()=>{
  const email = document.getElementById("authEmail").value.trim();
  const password = document.getElementById("authPassword").value;
  const errEl = document.getElementById("authError");
  errEl.textContent = "";

  if(!email || !password){ errEl.textContent = "Please fill in email and password."; return; }

  const endpoint = authMode === "login" ? "/api/auth/login" : "/api/auth/signup";
  const body = authMode === "login"
    ? { email, password }
    : { name: document.getElementById("authName").value.trim(), email, password };

  if(authMode === "signup" && !body.name){ errEl.textContent = "Please enter your name."; return; }

  try{
    const res = await fetch(API + endpoint, {
      method: "POST", headers: {"Content-Type":"application/json"}, body: JSON.stringify(body)
    });
    const data = await res.json();
    if(!res.ok){ errEl.textContent = data.detail || "Something went wrong."; return; }
    authToken = data.access_token;
    localStorage.setItem("thiranpathai_token", authToken);
    enterApp();
  }catch(e){
    errEl.textContent = "Couldn't reach the server. Is the backend running?";
  }
});

document.getElementById("logoutBtn").addEventListener("click", ()=>{
  authToken = null;
  localStorage.removeItem("thiranpathai_token");
  state = { resumeSkills: [], resumeText: "", learnedSkills: [], companies: [], selectedCompanyId: null };
  document.getElementById("resumeInput").value = "";
  document.getElementById("authScreen").style.display = "block";
  document.getElementById("mainApp").style.display = "none";
  document.getElementById("logoutBtn").style.display = "none";
});

async function enterApp(){
  document.getElementById("authScreen").style.display = "none";
  document.getElementById("mainApp").style.display = "block";
  document.getElementById("logoutBtn").style.display = "inline-block";
  // try to restore a previously saved resume for this user
  try{
    const res = await fetch(API + "/api/resume/me", { headers: authHeaders() });
    if(res.ok){
      const data = await res.json();
      state.resumeText = data.text;
      state.resumeSkills = data.skills;
      document.getElementById("resumeInput").value = data.text;
      renderResumeSkills();
    }
  }catch(e){ /* no saved resume yet — fine */ }
  loadCompanies();
}

async function checkExistingSession(){
  if(!authToken) return; // show auth screen
  try{
    const res = await fetch(API + "/api/auth/me", { headers: authHeaders() });
    if(res.ok){ enterApp(); }
    else { authToken = null; localStorage.removeItem("thiranpathai_token"); }
  }catch(e){ /* backend not reachable yet, stay on auth screen */ }
}

function cap(s){ return s.replace(/\b\w/g, c => c.toUpperCase()); }

/* ---------- Tabs ---------- */
document.querySelectorAll("nav.tabs button").forEach(btn=>{
  btn.addEventListener("click", ()=> showTab(btn.dataset.tab));
});
function showTab(name){
  document.querySelectorAll(".screen").forEach(s=>s.classList.toggle("active", s.dataset.screen===name));
  document.querySelectorAll("nav.tabs button").forEach(b=>b.classList.toggle("active", b.dataset.tab===name));
  if(name==="companies") loadCompanies();
  if(name==="roadmap") renderRoadmap();
  if(name==="test") renderTestSetup();
}

/* ---------- Resume upload ---------- */
document.getElementById("resumeFile").addEventListener("change", async (evt)=>{
  const file = evt.target.files[0];
  const statusEl = document.getElementById("uploadStatus");
  if(!file) return;
  statusEl.textContent = "Uploading " + file.name + " ...";
  const form = new FormData();
  form.append("file", file);
  try{
    const res = await fetch(API + "/api/resume/parse", { method: "POST", headers: authHeaders(), body: form });
    const data = await res.json();
    if(!res.ok){ statusEl.textContent = data.detail || "Couldn't read that file."; return; }
    document.getElementById("resumeInput").value = data.text;
    state.resumeText = data.text;
    state.resumeSkills = data.skills;
    statusEl.textContent = "✓ Loaded " + file.name + " — " + data.skills.length + " skills detected.";
    renderResumeSkills();
  }catch(e){
    statusEl.textContent = "Couldn't reach the server. Is the backend running?";
  }
});

document.getElementById("extractBtn").addEventListener("click", async ()=>{
  const text = document.getElementById("resumeInput").value;
  const blob = new Blob([text], {type:"text/plain"});
  const form = new FormData();
  form.append("file", blob, "resume.txt");
  const res = await fetch(API + "/api/resume/parse", { method:"POST", headers: authHeaders(), body: form });
  const data = await res.json();
  state.resumeText = text;
  state.resumeSkills = data.skills || [];
  renderResumeSkills();
});

function renderResumeSkills(){
  const wrap = document.getElementById("resumeSkillsWrap");
  const all = Array.from(new Set(state.resumeSkills.concat(state.learnedSkills)));
  if(all.length===0){
    wrap.innerHTML = '<div class="empty">No known skills found yet. Upload a resume or edit the text above.</div>';
  } else {
    wrap.innerHTML = '<label class="field">Skills on file (' + all.length + ')</label>' +
      all.map(s=>`<span class="chip match">${cap(s)}</span>`).join("");
  }
}

/* ---------- Companies (from the database via API) ---------- */
async function loadCompanies(){
  const res = await fetch(API + "/api/companies");
  state.companies = await res.json();
  renderCompanies();
}

document.getElementById("addCompanyBtn").addEventListener("click", async ()=>{
  const name = document.getElementById("companyName").value.trim();
  const skillsRaw = document.getElementById("companySkills").value.trim();
  if(!name || !skillsRaw){ alert("Enter a company/role name and its required skills."); return; }
  const skills = skillsRaw.split(",").map(s=>s.trim().toLowerCase()).filter(Boolean);
  await fetch(API + "/api/companies", {
    method: "POST", headers: {"Content-Type":"application/json"},
    body: JSON.stringify({ name, role: "Custom search", skills })
  });
  document.getElementById("companyName").value = "";
  document.getElementById("companySkills").value = "";
  loadCompanies();
});

function fitLocal(required){
  const have = new Set(state.resumeSkills.concat(state.learnedSkills));
  const matched = required.filter(s=>have.has(s));
  const missing = required.filter(s=>!have.has(s));
  const pct = required.length ? Math.round((matched.length/required.length)*100) : 0;
  return { pct, matched, missing };
}

let editingId = null;
function renderCompanies(){
  const list = document.getElementById("companyList");
  list.innerHTML = "";
  if(state.resumeSkills.length===0 && state.learnedSkills.length===0){
    list.innerHTML = '<div class="empty">Add your resume in the Resume tab first, so we can calculate your fit.</div>';
  }
  state.companies.forEach(c=>{
    const div = document.createElement("div");
    div.className = "card";

    if(editingId===c.id){
      div.innerHTML = `
        <label class="field">Company / role name</label>
        <input type="text" id="editName${c.id}" value="${escapeAttr(c.name)}">
        <label class="field">Role</label>
        <input type="text" id="editRole${c.id}" value="${escapeAttr(c.role)}">
        <label class="field">Skills required (comma separated)</label>
        <input type="text" id="editSkills${c.id}" value="${escapeAttr(c.skills.join(', '))}">
        <div style="display:flex; gap:8px; margin-top:10px;">
          <button class="btn small" style="flex:1;" onclick="saveEditCompany(${c.id})">Save</button>
          <button class="btn ghost" style="flex:1;margin-top:0;" onclick="cancelEdit()">Cancel</button>
        </div>`;
      list.appendChild(div);
      return;
    }

    const {pct, matched, missing} = fitLocal(c.skills);
    const cls = pct>=70?"high":pct>=40?"mid":"low";
    const barColor = pct>=70?"var(--good)":pct>=40?"var(--amber)":"var(--bad)";
    div.innerHTML = `
      <div class="rowtop">
        <div><h3>${c.name}</h3><div class="role">${c.role}</div></div>
        <div class="fit ${cls}">${pct}%</div>
      </div>
      <div class="bar"><i style="width:${pct}%;background:${barColor}"></i></div>
      ${matched.map(s=>`<span class="chip match">✓ ${cap(s)}</span>`).join("")}
      ${missing.map(s=>`<span class="chip miss">✗ ${cap(s)}</span>`).join("")}
      <button class="btn small" style="margin-top:10px;width:100%;" onclick="selectCompany(${c.id})">View Roadmap →</button>
      <div style="display:flex; gap:8px; margin-top:8px;">
        <button class="btn ghost" style="flex:1;margin-top:0;" onclick="startEdit(${c.id})">Edit</button>
        <button class="btn ghost" style="flex:1;margin-top:0;color:var(--bad);" onclick="deleteCompany(${c.id})">Delete</button>
      </div>`;
    list.appendChild(div);
  });
}
function escapeAttr(s){ return String(s).replace(/&/g,"&amp;").replace(/"/g,"&quot;"); }
function startEdit(id){ editingId = id; renderCompanies(); }
function cancelEdit(){ editingId = null; renderCompanies(); }
async function saveEditCompany(id){
  const name = document.getElementById("editName"+id).value.trim();
  const role = document.getElementById("editRole"+id).value.trim();
  const skills = document.getElementById("editSkills"+id).value.split(",").map(s=>s.trim().toLowerCase()).filter(Boolean);
  if(!name || skills.length===0){ alert("Name and at least one skill are required."); return; }
  await fetch(API + "/api/companies/" + id, {
    method: "PUT", headers: {"Content-Type":"application/json"},
    body: JSON.stringify({ name, role, skills })
  });
  editingId = null;
  loadCompanies();
}
async function deleteCompany(id){
  const c = state.companies.find(x=>x.id===id);
  if(!confirm("Remove " + (c ? c.name : "this company") + "?")) return;
  await fetch(API + "/api/companies/" + id, { method: "DELETE" });
  if(state.selectedCompanyId===id) state.selectedCompanyId = null;
  loadCompanies();
}
function selectCompany(id){ state.selectedCompanyId = id; showTab("roadmap"); }

/* ---------- Roadmap ---------- */
async function renderRoadmap(){
  const hint = document.getElementById("roadmapHint");
  const list = document.getElementById("roadmapList");
  const btn = document.getElementById("updateResumeBtn");
  if(state.selectedCompanyId===null){
    hint.textContent = "Pick a company from the Companies tab to see your personalised roadmap.";
    list.innerHTML = ""; btn.style.display = "none"; return;
  }
  const c = state.companies.find(x=>x.id===state.selectedCompanyId) || (await (await fetch(API+"/api/companies")).json()).find(x=>x.id===state.selectedCompanyId);
  const {missing} = fitLocal(c.skills);
  hint.textContent = `Roadmap for ${c.name} — ${c.role}`;
  if(missing.length===0){
    list.innerHTML = '<div class="empty">You already match every required skill for this role. 🎉</div>';
    btn.style.display = "none"; return;
  }
  const known = Array.from(new Set(state.resumeSkills.concat(state.learnedSkills)));
  const res = await fetch(API + "/api/roadmap", {
    method: "POST", headers: {"Content-Type":"application/json"},
    body: JSON.stringify({ known_skills: known, missing_skills: missing })
  });
  const data = await res.json();
  list.innerHTML = data.steps.map((step, i)=>{
    const learned = state.learnedSkills.includes(step.skill);
    return `<div class="roadmap-item">
      <div class="top">
        <div><div class="step">Step ${i+1}</div><div class="skill">${cap(step.skill)}</div></div>
        ${learned ? '<span class="learned-tag">✓ Learned</span>' : `<button class="btn small" onclick="toggleLearned('${step.skill}')">Mark learned</button>`}
      </div>
      <div class="links">
        <a href="${step.resource}" target="_blank" rel="noopener">Direct source</a>
        <a href="${step.youtube}" target="_blank" rel="noopener">YouTube</a>
      </div>
    </div>`;
  }).join("");
  btn.style.display = state.learnedSkills.length ? "block" : "none";
}
function toggleLearned(skill){
  if(!state.learnedSkills.includes(skill)) state.learnedSkills.push(skill);
  renderRoadmap();
}
document.getElementById("updateResumeBtn").addEventListener("click", ()=>{
  if(state.learnedSkills.length===0) return;
  const add = state.learnedSkills.filter(s=>!state.resumeSkills.includes(s));
  state.resumeSkills = state.resumeSkills.concat(add);
  const ta = document.getElementById("resumeInput");
  ta.value += (ta.value ? "\n" : "") + "Additional skills: " + add.map(cap).join(", ");
  state.resumeText = ta.value;
  state.learnedSkills = [];
  renderResumeSkills();
  renderRoadmap();
  alert("Resume updated with your newly learned skills!");
});

/* ---------- Test ---------- */
let currentSkill = null, currentQuestions = [], qIndex = 0, qAnswers = [];
async function renderTestSetup(){
  const res = await fetch(API + "/api/quiz");
  const data = await res.json();
  const setup = document.getElementById("testSetup");
  setup.innerHTML = `<label class="field">Choose a skill to test</label>
    <select id="quizSkill" style="width:100%;padding:11px;border-radius:10px;border:1px solid var(--line);background:var(--card);color:var(--text);font-size:14px;">
      ${data.skills.map(s=>`<option value="${s}">${cap(s)}</option>`).join("")}
    </select>
    <button class="btn primary" id="startQuizBtn">Start Test</button>`;
  document.getElementById("testArea").innerHTML = "";
  document.getElementById("startQuizBtn").addEventListener("click", startQuiz);
}
async function startQuiz(){
  currentSkill = document.getElementById("quizSkill").value;
  const res = await fetch(API + "/api/quiz/" + encodeURIComponent(currentSkill));
  const data = await res.json();
  currentQuestions = data.questions;
  qIndex = 0; qAnswers = [];
  renderQuestion();
}
function renderQuestion(){
  const area = document.getElementById("testArea");
  if(qIndex>=currentQuestions.length){ finishQuiz(); return; }
  const q = currentQuestions[qIndex];
  area.innerHTML = `<div class="qcard">
    <div class="qn">Question ${qIndex+1} of ${currentQuestions.length}</div>
    <div class="qtext">${q.q}</div>
    ${q.o.map((opt,i)=>`<button class="opt" data-i="${i}">${opt}</button>`).join("")}
  </div>`;
  area.querySelectorAll(".opt").forEach(btn=>{
    btn.addEventListener("click", ()=>{
      qAnswers.push(parseInt(btn.dataset.i));
      area.querySelectorAll(".opt").forEach(b=>b.disabled=true);
      setTimeout(()=>{ qIndex++; renderQuestion(); }, 300);
    });
  });
}
async function finishQuiz(){
  const res = await fetch(API + "/api/quiz/" + encodeURIComponent(currentSkill) + "/submit", {
    method: "POST", headers: {"Content-Type":"application/json"},
    body: JSON.stringify(qAnswers)
  });
  const data = await res.json();
  document.getElementById("testArea").innerHTML = `<div class="qcard">
    <div class="score">${data.score}/${data.total}</div>
    <div class="scoreLbl">questions correct</div>
    <button class="btn primary" id="retryBtn">Try another skill</button>
  </div>`;
  document.getElementById("retryBtn").addEventListener("click", renderTestSetup);
}

/* init */
checkExistingSession();
window.addEventListener('load', () => {
  setTimeout(() => {
    const s = document.getElementById('splash');
    if (!s) return;
    s.classList.add('hide');
    setTimeout(() => s.remove(), 600);
  }, 2000);
});