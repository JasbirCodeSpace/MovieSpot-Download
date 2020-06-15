$(document).ready(function () {
	const form = document.getElementById('browse-movie-form')
	const csrftoken = $('[name=csrfmiddlewaretoken]').val()

	form.addEventListener('submit', (event) => {
		event.preventDefault()
		let formdata = new FormData(document.getElementById('browse-movie-form'))
		let data = {}
		for (var [key, value] of formdata.entries()) {
			data[key] = value
		}
		$.ajax({
			type: 'POST',
			url: form.getAttribute('data-url'),
			headers: {
				'X-CSRFToken': csrftoken
			},
			data: data,
			success: function (result) {
				if (result.status === true) {
					let movies = result.data.data.movies
					console.log(movies)
					let movie_container = `
							<div class="container">
								<div class="cards">`
					for (var i = 0; i < movies.length; i++) {
						movie_container += `<div class="card">
			<div class="card__media">
				<img src="${movies[i].medium_cover_image}" class="responsive-img">
			</div>
			<div class="card__header">
				<h6 class="card__header-title">${movies[i].title}</h6>
				<p class="card__header-meta">${movies[i].year}</p>
				<div class="card__header-icon">
					<svg viewbox="0 0 28 25">
						<path fill="#fff" d="M13.145 2.13l1.94-1.867 12.178 12-12.178 12-1.94-1.867 8.931-8.8H.737V10.93h21.339z"/>
					</svg>
				</div>
			</div></div>`
					}
					movie_container += `</div></div>`

					let movie_section = document.getElementById('browse-movie-section')
					movie_section.innerHTML = ``
					movie_section.insertAdjacentHTML('beforeend', movie_container)
				}
			},
			error: function (error) {
				console.log(error)
			}
		})
	})
})