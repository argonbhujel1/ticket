// PGC front-end helpers
document.querySelectorAll('.class-option').forEach(el => {
  el.addEventListener('click', () => {
    document.querySelectorAll('.class-option').forEach(x => x.classList.remove('selected'));
    el.classList.add('selected');
  });
});
