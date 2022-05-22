const container = document.querySelector('#twitch')
const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value

async function deleteChannel(channelId) {
  try {
    const res = await fetch('/twitch/channels', {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrfToken
      },
      body: JSON.stringify({ id: channelId })
    })

    return await res.json()
  } catch (err) {
    console.error(err.message)
  }
}

async function bootstrap() {
  const res = await fetch('/twitch/channels', {
    method: 'GET'
  })
  const channels = await res.json()

  for (const channel of channels.streamers) {
    const column = document.createElement('div')
    column.classList.add('column', 'is-half')
    column.innerHTML = `
      <article class="message is-dark">
        <div class="message-header">
          <p>${channel.streamer}</p>
          <div>
            <div class="dropdown is-hoverable is-right">
              <div class="dropdown-trigger">
                <button class="button is-dark has-text-white" aria-haspopup="true" aria-controls="dropdown-menu">
                  <span class="icon is-small">
                    <i class="fa-solid fa-ellipsis-vertical"></i>
                  </span>
                </button>
              </div>
              <div class="dropdown-menu" id="dropdown-menu" role="menu">
                <div class="dropdown-content">
                  <a id="fullscreen-${channel.streamer}" class="dropdown-item">
                    <span class="icon is-small">
                      <i class="fa-solid fa-up-right-and-down-left-from-center"></i>
                    </span>
                    На весь экран
                  </a>
                  <hr class="dropdown-divider">
                  <a class="dropdown-item has-text-link" href="https://twitch.tv/${channel.streamer}" target="_blank">
                    <span class="icon is-small">
                      <i class="fa-solid fa-arrow-up-right-from-square"></i>
                    </span>
                    Перейти на канал
                  </a>
                  <a class="dropdown-item" href="https://www.twitch.tv/popout/${channel.streamer}/chat?popout=" target="_blank">
                    <span class="icon is-small">
                      <i class="fa-solid fa-message"></i>
                    </span>
                    Открыть чат
                  </a>
                  <hr class="dropdown-divider">
                  <a id="delete-${channel.streamer}" class="dropdown-item has-text-danger">
                    <span class="icon is-small">
                      <i class="fas fa-eye-slash"></i>
                    </span>
                    Удалить 
                  </a>
                </div>
              </div>
            </div>
          </div>
        </div>
        <figure class="image is-16by9" style="padding-top: 100%;"></figure>
      </article>
    `

    const embed = new Twitch.Embed(column, {
      theme: 'dark',
      layout: 'video-with-chat',
      autoplay: false,
      muted: true,
      channel: channel.streamer
    })

    const frame = embed._iframe
    frame.classList.add('has-ratio')

    column
      .querySelector('figure')
      .appendChild(frame)

    column
      .querySelector(`#fullscreen-${channel.streamer}`)
      .addEventListener('click', () => {
        if (frame.requestFullscreen) {
          frame.requestFullscreen()
        } else if (frame.webkitRequestFullscreen) {
          frame.webkitRequestFullscreen()
        } else if (frame.mozRequestFullScreen) {
          frame.mozRequestFullScreen()
        }
      })

    column
      .querySelector(`#delete-${channel.streamer}`)
      .addEventListener('click', () => {
        deleteChannel(channel.id)
          .then(() => {
            embed.pause()
            embed.disableCaptions()
            column.remove()
          })
          .catch((err) => {
            console.error(err)
          })
      })


    container.appendChild(column)
  }
}

bootstrap()
