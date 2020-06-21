$(document).ready(function () {
	let browse_movie_form = document.getElementById('browse-movie-form')
	const csrftoken = $('[name=csrfmiddlewaretoken]').val()

	browse_movie_form.addEventListener('submit', (event) => {
		event.preventDefault()
		let formdata = new FormData(document.getElementById('browse-movie-form'))
		let data = {}
		for (let [key, value] of formdata.entries()) {
			data[key] = value
		}
		$.ajax({
			type: 'POST',
			url: browse_movie_form.getAttribute('data-url'),
			headers: {
				'X-CSRFToken': csrftoken
			},
			data: data,
			success: function (result) {
				if (result.status === true) {
					let movies = result.data.data.movies
					console.log(movies)
					let movie_container = `
					<div class="text-center"><h2 class="purple-heading">${movies.length} Movies found</h2></div>
							<div class="container">
								<div class="cards">`
					for (var i = 0; i < movies.length; i++) {
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

					let movie_section = document.getElementById('browse-movie-section')
					movie_section.innerHTML = ``
					movie_section.insertAdjacentHTML('beforeend', movie_container)

				}
			},
			error: function (error) {
				console.log(error)
			},
			complete:function(data){
				let movie_cards = document.getElementsByClassName('card')
				for (var i = 0; i < movie_cards.length; i++) {
					movie_cards[i].addEventListener('click',e=>{
						redirect_to_movie(e.currentTarget)
					})
				}	
			}
		})
	})

	const redirect_to_movie = (target)=>{
		let ids = target.id.split('-')
		let url = document.getElementById('browse-movie-section').getAttribute('data-url')
		url = url.replace('imdb_id',ids[1])
		url = url.replace('id',ids[0])
		window.open(url,'_blank')
	}
})