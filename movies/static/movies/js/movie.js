$(document).ready(function () {

	let url_parts = window.location.href.split('/')
	let movie_id = url_parts[url_parts.length - 2]
	let movie_count = 6
	let loader = `<div id="ftco-loader" class="show">
		<svg class="circular" width="48px" height="48px">
		<circle class="path-bg" cx="24" cy="24" r="22" fill="none" stroke-width="4" stroke="#eeeeee"/>
		<circle class="path" cx="24" cy="24" r="22" fill="none" stroke-width="4" stroke-miterlimit="10" stroke="#F96D00"/>
		</svg></div>`
	let movie_section = document.getElementById('similar-movies-section')
	movie_section.innerHTML = loader
	$.ajax({
		type: 'POST',
		url: '/similar-movies',
		data: {
			movie_id: movie_id,
			movie_count: movie_count
		},
		success: function (result) {
			if (result.status === true) {
				let movies = JSON.parse(result.data)

				let movie_container = `
					<div class="text-center"><h2 class="purple-heading">Similar Movies</h2></div>
							<div class="container">
								<div class="cards">`
				for (let i = 0; i < movies.length; i++) {
					movie_container += `<div class="card" id="${movies[i].id}-${movies[i].imdb_code}">
			<div class="card__media">
				<img src="${movies[i].medium_cover_image}" class="responsive-img movie-card-image">
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
				movie_section.innerHTML = ``
				movie_section.insertAdjacentHTML('beforeend', movie_container)

			}
		},
		error: function (error) {
			console.log(error)
		},
		complete: function (data) {
			let movie_cards = document.getElementsByClassName('card')
			for (var i = 0; i < movie_cards.length; i++) {
				movie_cards[i].addEventListener('click', e => {
					redirect_to_movie(e.currentTarget)
				})
			}
		}
	})
	const redirect_to_movie = (target) => {
		let ids = target.id.split('-')
		let url = document.getElementById('similar-movies-section').getAttribute('data-url')
		url = url.replace('imdb_id', ids[1])
		url = url.replace('id', ids[0])
		window.location = url
	}
})