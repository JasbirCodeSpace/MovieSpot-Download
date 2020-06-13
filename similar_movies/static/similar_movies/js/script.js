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
			success:function(data){
				console.log(data)
			},
			error:function(error){
				console.log(error)
			}
		})
	})
})