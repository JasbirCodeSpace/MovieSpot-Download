$(document).ready(function(){

	let search_form = document.getElementById('search-form')
	const csrftoken = $("[name=csrfmiddlewaretoken]").val();
	let genre = {}

	const getGenre = ()=>{
		$.ajax({
			type:'GET',
			url:'/get-genre',
			headers:{
				"X-CSRFToken":csrftoken
			},
			success:function(data){
				genre = data.genres
				let mappedGenre = {};

				for (var i = 0, l = genre.length; i < l; i++) {
				    mappedGenre[genre[i].id] = genre[i];
				}
				genre = mappedGenre
			},
			error:function(error){
				console.log(error)
			}

		})
	}
	const genreIdToName = (genrelist)=>{
		let genreString = ''
		for (var i = 0; i < genrelist.length; i++) {
			genreString += genre[genrelist[i]].name
			if (i<genrelist.length-1) {genreString += ' , '}
		}
		return genreString
	}
	getGenre()

	search_form.addEventListener('submit',(event)=>{
		event.preventDefault()
		let movieName = document.getElementById('movie-name').value

		let loader = `<div id="ftco-loader" class="show">
		<svg class="circular" width="48px" height="48px">
		<circle class="path-bg" cx="24" cy="24" r="22" fill="none" stroke-width="4" stroke="#eeeeee"/>
		<circle class="path" cx="24" cy="24" r="22" fill="none" stroke-width="4" stroke-miterlimit="10" stroke="#F96D00"/>
		</svg></div>`
		let moviesContainer = document.getElementById('movie-search-result-container')
		moviesContainer.innerHTML = loader

		$.ajax({
			type:'POST',
			url: search_form.getAttribute('data-url'),
	        headers:{
	        	"X-CSRFToken": csrftoken
	        },
	        data:{
	        	'movie-name':movieName
	        },
	        dataType:'json',
			success:function(results){
				movies = results.data
				moviesContainer.innerHTML = ''
				for (var i = 0; i < movies.length; i++) {
					if(movies[i].poster_path && movies[i].release_date && movies[i].overview){
					console.log(movies[i])
					let htmlData = `<div class="movie_card" id='${ movies[i].id }'>
					<div class="info_section">
					<div class="movie_header">
					<img class="locandina" src="https://image.tmdb.org/t/p/w500${ movies[i].poster_path}" />
					<h2> ${movies[i].original_title} </h2>
					<h4> ${movies[i].release_date.substring(0,4)} </h4>
					<span class="minutes">117 min</span>
            		<p class="type">${genreIdToName(movies[i].genre_ids)}</p>
            		</div>
          			<div class="movie_desc">
          			<p class="text">
          			${movies[i].overview}
          			</p>
		          </div>
		          <div class="movie_social">
		            <ul>
		              <li><i class="material-icons">share</i></li>
		              <li><i class="material-icons">star_rate</i></li>
		              <li><i class="material-icons">chat_bubble</i></li>
		            </ul>
		          </div>
		        </div>
		        <div class="blur_back" style="background:url('https://image.tmdb.org/t/p/w500${ movies[i].poster_path}')"></div>`

		        moviesContainer.insertAdjacentHTML('beforeend',htmlData)
		        moviesContainer.scrollIntoView()
		    }

				}
			},
			error:function(error){
				console.log(error)
			}
		})
	})
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