  const container = document.querySelector('#twitch')

    async function deleteChannel(channelId) {
      try {
        const res = await fetch('/twitch/channels', {
          method: 'DELETE',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ id: channelId })
        })

        return await res.json()
      } catch (err) {
        console.error(err.message)
      }
    }

    async function main() {
      const res = await fetch('/twitch/channels', {
        method: 'GET'
      })
      const channels = await res.json()

      for (const channel of channels.streamers) {
        const player = document.createElement('div')
        player.classList.add('column')

        const button = document.createElement('button')
        button.classList.add('button', 'is-danger', 'is-outlined')

        const span = document.createElement('span')
        span.classList.add('icon', 'is-small')

        const icon = document.createElement('i')
        icon.classList.add('fas', 'fa-times')

        button.addEventListener('click', () => {
          const res = deleteChannel(channel.id)
          embed.pause()
          embed.disableCaptions()
          player.remove()
        })

        const embed = new Twitch.Embed(player, {
          theme: 'dark',
          autoplay: false,
          muted: true,
          width: 854,
          height: 480,
          channel: channel.streamer
        })

        player.appendChild(embed._iframe)
        span.appendChild(icon)
        button.appendChild(span)
        player.appendChild(button)
        container.appendChild(player)
      }
    }

    main()

