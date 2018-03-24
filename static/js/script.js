$(document).ready(function(){
	$('.buy').click(function(){
		swal({
		  title: 'Введите ваш номер телефона',
		  input: 'tel',
		  showCancelButton: true,
		  cancelButtonText: 'Отмена',
		  confirmButtonText: 'К оплате',
		}).then((result) => {
		  if (result.value) {
		    $.ajax({
				type: "POST",
				url: "/buy",	
				data: {
					'price': $(this).closest('.product').find('.id').val(),
					'phone': result.value
				},
				success: function(data){
					window.location.href = data;
				}
			});
		  }
		})
	});
});
