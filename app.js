'use strict';
const form = document.getElementById('tracking-form');
const input = document.getElementById('tracking-number');
const result = document.getElementById('result');
const message = document.getElementById('message');
const photo = document.getElementById('photo');
photo.addEventListener('error', () => {
  message.textContent = 'The item photo could not load. Please refresh and try again.';
});
input.addEventListener('input', () => {
  result.hidden = true;
  message.textContent = '';
});
form.addEventListener('submit', event => {
  event.preventDefault();
  result.hidden = true;
  message.textContent = '';
  if (input.value !== 'YSL-AU-20261117-48291') {
    message.textContent = 'Tracking number not found. Please check the number and try again.';
    return;
  }
  photo.src = 'ysl-bag.jpg';
  result.hidden = false;
});
