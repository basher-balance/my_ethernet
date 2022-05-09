const dropdowns = document.querySelectorAll('.dropdown')

dropdowns.forEach((dropdown) => {
  const button = dropdown.querySelector('.dropdown-trigger')
  button.addEventListener('click', (event) => {
    event.stopPropagation()
    const isActive = dropdown.classList.contains('is-active')
    if (isActive) {
      dropdown.classList.remove('is-active')
    } else {
      closeDropdowns()
      dropdown.classList.toggle('is-active')
    }
  })
})

document.addEventListener('click', closeDropdowns)

function closeDropdowns() {
  dropdowns.forEach((dropdown) => {
    dropdown.classList.remove('is-active')
  })
}
