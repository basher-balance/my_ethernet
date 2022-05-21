// background
document.body.classList.add('weather-background')

// initial weather location
const WEATHER_CONFIG = {
  location: 'Петропавловск',
  lat: 54.89,
  lon: 69.18
}

async function bootstrap() {
  const { store, getStorage, setStorage } = weatherStorage()

  const fieldset = document.querySelector('fieldset')
  const input = document.querySelector('input')
  input.value = store.location

  fieldset.addEventListener('animationend', () => {
    fieldset.classList.remove('input-shake')
  })

  input.addEventListener('keydown', (event) => {
    if (event.key === 'Enter') {
      submit.click()
    }
  })

  const setLocationInDom = (location) => {
    const title = document.querySelector('.hero-body > .title')
    title.textContent = `Погода ${location}`
    input.value = location
  }

  const updateLocation = (store) => {
    setLocationInDom(store.location)
    setStorage(store)
    disableLoading()
  }

  const enableLoading = () => {
    fieldset.setAttribute('disabled', 'true')
    input.classList.remove('is-danger')
    input.parentNode.classList.add('is-loading')
  }

  const disableLoading = () => {
    fieldset.removeAttribute('disabled')
    input.parentNode.classList.remove('is-loading')
  }

  const shakeInput = () => {
    fieldset.classList.add('input-shake')
  }

  const fetchWeather = (location) => {
    weatherApi('/weather/forecast', location)
      .then((response) => {
        updateLocation(location)
        renderForecast(response)
      })
  }

  const searchWeather = (query) => {
    weatherApi('/weather/search', { query })
      .then(({ direct, weather }) => {
        const { local_names, lat, lon } = direct[0]
        const location = {
          location: local_names.ru ?? local_names.en,
          lat: Number(lat.toFixed(2)),
          lon: Number(lon.toFixed(2))
        }

        updateLocation(location)
        renderForecast(weather)
      })
      .catch(() => {
        shakeInput()
        disableLoading()
        input.classList.add('is-danger')
      })
  }

  const submit = document.querySelector('button')
  submit.addEventListener('click', () => {
    if (!input.value) {
      shakeInput()
      return
    }

    enableLoading()
    const currentStore = getStorage()

    if (currentStore.location === input.value) {
      fetchWeather(currentStore)
    } else {
      searchWeather(input.value)
    }
  })

  setLocationInDom(store.location)
  enableLoading()
  fetchWeather(store)
}

bootstrap()

function renderForecast(weather) {
  const section = document.querySelector('.section')
  const columns = document.createElement('div')
  columns.id = 'weather'
  columns.classList.add('columns', 'is-multiline')

  document
    .querySelectorAll('#weather')
    .forEach((column) => column.remove())

  if ('alerts' in weather) {
    const alerts = columns.cloneNode(true)
    alerts.append(...renderAlerts(weather.alerts))
    section.appendChild(alerts)
  }

  const current = renderCurrentlyWeather(weather.current)
  const daily = renderDailyWeather(weather.daily)
  columns.append(current, ...daily)
  section.appendChild(columns)
}

function weatherStorage() {
  const storageKey = 'geolocation'

  const getStorage = () => {
    const storageValue = localStorage.getItem(storageKey) ?? WEATHER_CONFIG

    try {
      return JSON.parse(storageValue)
    } catch {
      localStorage.removeItem(storageKey)
      return WEATHER_CONFIG
    }
  }

  const setStorage = (value) => {
    localStorage.setItem(storageKey, JSON.stringify(value))
  }

  return {
    store: getStorage(),
    getStorage,
    setStorage
  }
}

function renderAlerts(alerts) {
  const columns = []

  const weatherAlerts = alerts.reduce((acc, alert) => {
    if (!alert.description) return acc
    acc.set(alert.event, alert.description)
    return acc
  }, new Map())

  for (const [alertName, alertDescription] of weatherAlerts.entries()) {
    const column = document.createElement('div')
    column.classList.add('column')
    column.innerHTML = `
      <article class="message is-danger">
        <div class="message-header">
          <p>${alertName}</p>
        </div>
        <div class="message-body">
          ${firstUpper(alertDescription)}
        </div>
      </article>
    `

    columns.push(column)
  }

  return columns
}

function renderCurrentlyWeather(data) {
  const {
    dt,
    sunrise,
    temp,
    humidity,
    clouds,
    pressure,
    wind_speed,
    weather
  } = data
  const { icon, description } = weather[0]

  const column = document.createElement('div')
  column.classList.add('column', 'is-full')
  column.innerHTML = `
    <div class="card has-background-dark has-text-light mb-5">
      <div class="card-content">
        <div class="weather-title">
          <img src="https://openweathermap.org/img/wn/${icon}@2x.png" alt="${description}">
          <span class="is-size-2">${dateFormat(dt * 1000)}</span>
        </div>
        <span>Темп.: </span>${temp} °C<br></b>
        <span>Давление: </span>${Math.round(pressure * 0.75)} mmHg<br>
        <span>Восход: </span>${dateFormat(sunrise * 1000)}<br>
        <span>Влажность: </span>${humidity} %<br>
        <span>Облачность: </span>${clouds} %<br>
        <span>Скорость ветра: </span>${wind_speed} м/c<br>
        <span>Состояние: </span>${firstUpper(description)}<br>
      </div>
    </div>
  `

  return column
}

function renderDailyWeather(weathers) {
  const columns = []

  for (const weather of weathers) {
    const {
      dt,
      temp,
      sunset,
      sunrise,
      clouds,
      humidity,
      pressure,
      feels_like,
      wind_speed
    } = weather
    const { min, max, day } = temp
    const { icon, description } = weather.weather[0]

    const column = document.createElement('div')
    column.classList.add('column', 'is-one-third')
    column.innerHTML = `
      <div class="card has-background-dark has-text-light">
        <div class="card-content is-success">
          <div class="weather-title">
            <img src="http://openweathermap.org/img/wn/${icon}.png" alt="${description}">
            <span class="is-size-4">${dateFormat(dt * 1000)}</span>
          </div>
          <span class="has-text-weight-medium">Темп.: </span>${day} °C<br>
          <span class="has-text-weight-medium">Мин. темп.: </span>${min} °C<br>
          <span class="has-text-weight-medium">Макс. темп.: </span>${max} °C<br>
          <span class="has-text-weight-medium">Восход: </span>${dateFormat(sunrise * 1000)}<br>
          <span class="has-text-weight-medium">Закат: </span>${dateFormat(sunset * 1000)}<br>
        </div>
      </div>
    `

    columns.push(column)
  }

  return columns
}

async function weatherApi(url, body) {
  try {
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value
    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrfToken
      },
      body: JSON.stringify(body)
    })

    return await response.json()
  } catch (err) {
    throw err
  }
}
