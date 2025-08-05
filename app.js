let workDuration = 25 * 60;
let shortBreakDuration = 5 * 60;
let longBreakDuration = 15 * 60;
let currentTimer = workDuration;
let interval = null;
let currentMode = 'work';
let isPaused = true;
let sessionCount = 0;

const timerDisplay = document.getElementById('timer');
const statusDisplay = document.getElementById('status');
const startBtn = document.getElementById('start');
const pauseBtn = document.getElementById('pause');
const resetBtn = document.getElementById('reset');
const add2Btn = document.getElementById('add2');
const add5Btn = document.getElementById('add5');
const sessionCountDisplay = document.getElementById('sessionCount');

function updateDisplay() {
  const minutes = Math.floor(currentTimer / 60).toString().padStart(2, '0');
  const seconds = (currentTimer % 60).toString().padStart(2, '0');
  timerDisplay.textContent = `${minutes}:${seconds}`;
  statusDisplay.textContent = currentMode === 'work' ? 'Focus' : (currentMode === 'longBreak' ? 'Long Break' : 'Break');
  sessionCountDisplay.textContent = `Session: ${sessionCount}`;
}

function switchMode() {
  if (currentMode === 'work') {
    sessionCount++;
    if (sessionCount % 4 === 0) {
      currentMode = 'longBreak';
      currentTimer = longBreakDuration;
    } else {
      currentMode = 'shortBreak';
      currentTimer = shortBreakDuration;
    }
  } else {
    currentMode = 'work';
    currentTimer = workDuration;
  }
  updateDisplay();
}

function tick() {
  if (currentTimer > 0) {
    currentTimer--;
    updateDisplay();
  } else {
    switchMode();
  }
}

startBtn.addEventListener('click', () => {
  if (!interval) {
    interval = setInterval(tick, 1000);
    isPaused = false;
    startBtn.disabled = true;
    pauseBtn.disabled = false;
  }
});

pauseBtn.addEventListener('click', () => {
  if (isPaused) {
    interval = setInterval(tick, 1000);
    pauseBtn.textContent = 'Pause';
    isPaused = false;
  } else {
    clearInterval(interval);
    interval = null;
    pauseBtn.textContent = 'Resume';
    isPaused = true;
  }
});

resetBtn.addEventListener('click', () => {
  clearInterval(interval);
  interval = null;
  currentMode = 'work';
  currentTimer = workDuration;
  sessionCount = 0;
  isPaused = true;
  startBtn.disabled = false;
  pauseBtn.disabled = true;
  pauseBtn.textContent = 'Pause';
  updateDisplay();
});

add2Btn.addEventListener('click', () => {
  currentTimer += 2 * 60;
  updateDisplay();
});

add5Btn.addEventListener('click', () => {
  currentTimer += 5 * 60;
  updateDisplay();
});

document.getElementById('applySettings').addEventListener('click', () => {
  const w = parseInt(document.getElementById('workDuration').value, 10);
  const s = parseInt(document.getElementById('shortBreakDuration').value, 10);
  const l = parseInt(document.getElementById('longBreakDuration').value, 10);
  if (!isNaN(w) && w >= 15 && w <= 60) workDuration = w * 60;
  if (!isNaN(s) && s >= 5 && s <= 30) shortBreakDuration = s * 60;
  if (!isNaN(l) && l >= 15 && l <= 60) longBreakDuration = l * 60;
  if (currentMode === 'work') currentTimer = workDuration;
  if (currentMode === 'shortBreak') currentTimer = shortBreakDuration;
  if (currentMode === 'longBreak') currentTimer = longBreakDuration;
  updateDisplay();
});

updateDisplay();
