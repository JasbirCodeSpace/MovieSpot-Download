$(document).ready(function(){
	const form = document.getElementById('browse-movie-form')
	const csrftoken = $('[name=csrfmiddlewaretoken]').val()

	form.addEventListener('submit',(event)=>{
		event.preventDefault()
		let formdata = new FormData(document.getElementById('browse-movie-form'))
		let data = {}
		for (var [key, value] of formdata.entries()) { 
  			data[key] = value
		}
		$.ajax({
			type:'POST',
			url:form.getAttribute('data-url'),
			headers:{ 'X-CSRFToken' : csrftoken},
			data:data,
			success:function(result){
				console.log(result)
			},
			error:function(error){
				console.log(error)
			}
		})
	})
})