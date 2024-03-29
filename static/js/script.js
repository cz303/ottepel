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
					'item': $(this).closest('.product').find('.id').val(),
					'phone': result.value
				},
				success: function(data){
					if(data.toString().length>2) {
						window.location.href = data;	
					} else {
						swal(
						  'Спасибо за заказ!',
						  'Менеджер свяжется с вами!',
						  'success'
						)
					}
					
				}
			});
		  }
		})
	});
	$('.search').click(function(){
		window.location.href = 'https://dynamic-door.ru/search/'+$('#search').val();
	});
});
