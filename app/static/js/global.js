document.addEventListener('DOMContentLoaded', bootstrap)

function bootstrap() {
  initEgg()
  initNavbar()
  initDeleteButtons()
}

function initDeleteButtons() {
  const buttons = document.querySelectorAll('#delete-button')
  buttons.forEach((button) => {
    button.addEventListener('click', acceptDelete)
  })
}

function initNavbar() {
  const navbar = document.querySelector('#navbar')
  const navbarBurger = document.querySelector('.navbar-burger')

  navbarBurger.addEventListener('click', () => {
    navbarBurger.classList.toggle('is-active')
    navbar.classList.toggle('is-active')
  })

  const navbarLinks = document.querySelectorAll('.navbar-link')
  navbarLinks.forEach((el) => {
    const navbarDropdown = el.nextElementSibling
    navbarDropdown.classList.add('hidden')

    el.addEventListener('click', () => {
      navbarDropdown.classList.toggle('hidden')
    })
  })
}

function dateFormat(date) {
  return new Intl.DateTimeFormat('ru', {
    year: 'numeric',
    hour: 'numeric',
    minute: 'numeric',
    second: 'numeric',
    day: '2-digit',
    month: '2-digit',
    hour12: false
  }).format(new Date(date))
}

function acceptDelete(event) {
  event.preventDefault()
  const isConfirm = confirm('Вы точно уверены?')
  if (isConfirm) {
    location.href = event.currentTarget.href
  }
}

function firstUpper(str) {
  return str[0].toUpperCase() + str.substr(1)
}

function randomInt(min, max) {
  return Math.floor(min + Math.random() * (max + 1 - min))
}

function initEgg() {
  const target = document.querySelector('.navbar-brand > .navbar-item')
  const images = [
    'bulma.png',
    'internet.png',
    'bad-idea.png'
  ]

  target.addEventListener('mouseenter', (event) => {
    if (event.altKey && event.ctrlKey) {
      const modal = document.createElement('div')
      modal.classList.add('modal', 'is-active')
      modal.innerHTML = `
        <div class="modal-background"></div>
        <div class="modal-content">
          <p class="image is-4by3">
            <img src="/static/images/${images[randomInt(0, images.length - 1)]}">
          </p>
        </div>
      `
      const closeButton = document.createElement('button')
      closeButton.classList.add('modal-close', 'is-large')
      closeButton.addEventListener('click', () => modal.remove())

      modal.appendChild(closeButton)
      document.body.appendChild(modal)
    }
  })
}
