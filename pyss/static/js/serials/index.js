const dropdowns = document.querySelectorAll('.dropdown')

dropdowns.forEach((dropdown) => {
  const button = dropdown.querySelector('.dropdown-trigger')
  button.addEventListener('click', () => {
    dropdown.classList.toggle('is-active')
  })
})
