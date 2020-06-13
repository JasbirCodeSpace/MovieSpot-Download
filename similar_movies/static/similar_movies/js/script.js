$(document).ready(function(){

	const form = document.getElementById('search-form')
	const csrftoken = $("[name=csrfmiddlewaretoken]").val();

	form.addEventListener('submit',(event)=>{
		event.preventDefault()
		let movieName = document.getElementById('movie-name').value
		$.ajax({
			type:'POST',
			url: form.getAttribute('data-url'),
	        headers:{
	        	"X-CSRFToken": csrftoken
	        },
	        data:{
	        	'movie-name':movieName
	        },
	        dataType:'json',
			success:function(results){
				movies = results.data
				let moviesContainer = document.getElementById('movie-search-result-container')
				moviesContainer.innerHTML = ''
				for (var i = 0; i < movies.length; i++) {
					if(movies[i].poster_path && movies[i].release_date && movies[i].overview){
					let htmlData = `<div class="movie_card" id='${ movies[i].id }'>
					<div class="info_section">
					<div class="movie_header">
					<img class="locandina" src="https://image.tmdb.org/t/p/w500${ movies[i].poster_path}" />
					<h2> ${movies[i].original_title} </h2>
					<h4> ${movies[i].release_date.substring(0,4)} </h4>
					<span class="minutes">117 min</span>
            		<p class="type">Action, Crime, Fantasy</p>
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
		    }

				}
			},
			error:function(error){
				console.log(error)
			}
		})
	})
})