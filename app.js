'use strict';
const form = document.getElementById('tracking-form');
const input = document.getElementById('tracking-number');
const result = document.getElementById('result');
const message = document.getElementById('message');
const photo = document.getElementById('photo');
const button = document.getElementById('track-button');
const loading = document.getElementById('loading');
let timer = null;
function setLoading(active) {
  loading.hidden = !active;
  button.disabled = active;
  button.textContent = active ? 'Loading…' : 'Track';
  form.setAttribute('aria-busy', String(active));
}
photo.addEventListener('error', () => {
  if (!result.hidden) {
    message.textContent = 'The item photo could not load. Please refresh and try again.';
  }
});
input.addEventListener('input', () => {
  clearTimeout(timer);
  timer = null;
  setLoading(false);
  result.hidden = true;
  message.textContent = '';
});
form.addEventListener('submit', event => {
  event.preventDefault();
  if (timer !== null) return;
  result.hidden = true;
  message.textContent = '';
  const submittedNumber = input.value;
  setLoading(true);
  // A short presentation delay, not a request to a live carrier API.
  timer = setTimeout(() => {
    timer = null;
    setLoading(false);
    if (submittedNumber !== 'YSL-AU-20261117-48291') {
      message.textContent = 'Tracking number not found. Please check the number and try again.';
      return;
    }
    result.hidden = false;
    photo.src = 'ysl-bag.jpg';
  }, 1500);
});
