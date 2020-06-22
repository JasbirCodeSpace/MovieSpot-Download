$(document).ready(function () {
	let recommendation_form = document.getElementById('recommendation-form')
	const csrftoken = $('[name=csrfmiddlewaretoken').val()

	recommendation_form.addEventListener('submit', (event) => {
		event.preventDefault()
		let movie_name = document.getElementById('movie-name').value
		let loader = `<div id="ftco-loader" class="show">
		<svg class="circular" width="48px" height="48px">
		<circle class="path-bg" cx="24" cy="24" r="22" fill="none" stroke-width="4" stroke="#eeeeee"/>
		<circle class="path" cx="24" cy="24" r="22" fill="none" stroke-width="4" stroke-miterlimit="10" stroke="#F96D00"/>
		</svg></div>`
		let movie_section = document.getElementById('similar-movies-section')
		movie_section.innerHTML = loader
		$.ajax({
			type: 'POST',
			url: recommendation_form.getAttribute('data-url'),
			headers: {
				'X-CSRFToken': csrftoken
			},
			data: {
				'movie-name': movie_name
			},
			success: function (result) {
				if (result.status === true) {
					let movies = JSON.parse(result.data)

					let movie_container = `
					<div class="text-center"><h2 class="purple-heading">Recommended Movies</h2></div>
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
					scrollToTargetAdjusted('similar-movies-section')

				} else {
					let movie_container = `
					<div class="text-center"><h2 class="purple-heading">No Match Found</h2></div>`
					movie_section.innerHTML = ``
					movie_section.insertAdjacentHTML('beforeend', movie_container)
					scrollToTargetAdjusted('similar-movies-section')
				}
			},
			error: function (error) {
				let movie_container = `
					<div class="text-center"><h2 class="purple-heading">No Match Found</h2></div>`
				movie_section.innerHTML = ``
				movie_section.insertAdjacentHTML('beforeend', movie_container)
				scrollToTargetAdjusted('similar-movies-section')
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

	})
	const redirect_to_movie = (target) => {
		let ids = target.id.split('-')
		let url = document.getElementById('similar-movies-section').getAttribute('data-url')
		url = url.replace('imdb_id', ids[1])
		url = url.replace('id', ids[0])
		window.open(url,'_blank')
	}

	const scrollToTargetAdjusted = (id)=>{
    var element = document.getElementById(id);
    var headerOffset = 150;
    var elementPosition = element.getBoundingClientRect().top;
    var offsetPosition = elementPosition - headerOffset;

    window.scrollTo({
         top: offsetPosition,
         behavior: "smooth"
    });
}
})