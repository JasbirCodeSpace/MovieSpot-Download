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
		let movie_section = document.getElementById('browse-movie-section')
		let loader = `<div id="ftco-loader" class="show">
		<svg class="circular" width="48px" height="48px">
		<circle class="path-bg" cx="24" cy="24" r="22" fill="none" stroke-width="4" stroke="#eeeeee"/>
		<circle class="path" cx="24" cy="24" r="22" fill="none" stroke-width="4" stroke-miterlimit="10" stroke="#F96D00"/>
		</svg></div>`
		movie_section.innerHTML = loader

		$.ajax({
			type: 'POST',
			url: browse_movie_form.getAttribute('data-url'),
			headers: {
				'X-CSRFToken': csrftoken
			},
			data: data,
			success: function (result) {
				if (result.status === true) {
					let result_data = result.data.data
					let movies = result_data.movies
					let movie_container = `
					<div class="text-center">`
					if(result_data.movie_count ===0)
						movie_container+=`<h2 class="purple-heading">No Match found</h2>`
					else if(result_data.movie_count ===1)
						movie_container+=`<h2 class="purple-heading">${movies.length} Movie found</h2>`
					else
						movie_container+=`<h2 class="purple-heading">${movies.length} Movies found</h2>`

					movie_container+=`</div>
							<div class="container">
								<div class="cards">`
					for (var i = 0; i < result_data.movie_count; i++) {
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
					scrollToTargetAdjusted('browse-movie-section')

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