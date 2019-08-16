;(function($){
  $('[data-toggle=tooltip]').tooltip();
  var max=10;
  
  function addShowMore($,v){
	$(v).nextUntil('li.nav-header').last().after(
		$('<li class="filter-multiselect"><a class="small filter-item" href="#"><input class="filter-col-1" type="checkbox"><span class="filter-col-2">更多</span></a></li>').click(function(e){
			console.log('abcdef');
			e.preventDefault();
			e.stopPropagation();
			$(v).nextUntil('li.nav-header').show();
			$(v).nextUntil('li.nav-header').last().remove();
			addShowLess($,v);
		})
	);
	$(v).nextUntil('li.nav-header').last().show();
  }
  
  function addShowLess($,v){
	$(v).nextUntil('li.nav-header').last().after(
		$('<li class="filter-multiselect"><a class="small filter-item" href="#"><input class="filter-col-1" type="checkbox"><span class="filter-col-2">收回</span></a></li>').click(function(e){
			e.preventDefault();
			e.stopPropagation();
			$(v).nextUntil('li.nav-header').filter(function(i){return !$(this).find('input').is(':checked');}).slice(max).hide();
			$(v).nextUntil('li.nav-header').last().remove();
			// $(v).scrollMinimal(3000);
			// alert(1);
			addShowMore($,v);
		})
	);
	$(v).nextUntil('li.nav-header').last().show();
  }
  
  $.each($('.nav-quickfilter li.nav-header'),function(i,v){
	  if ($(v).nextUntil('li.nav-header').size()>max) {
		$(v).nextUntil('li.nav-header').filter(function(i){return !$(this).find('input').is(':checked');}).slice(max).hide();
  		addShowMore($,v);
	  }
  });
  
  $('.nav-quickfilter li.nav-header').on('click',function(e) {
	  e.preventDefault();
	  e.stopPropagation();
	  $('.nav-quickfilter li.nav-header i').toggleClass('icon-chevron-right');
	  $('.nav-quickfilter li.nav-header i').toggleClass('icon-chevron-left');
	  $('#left-side').toggleClass('col-md-2');
	  $('#left-side').toggleClass('col-md-4');
	  $('#content-block').toggleClass('col-md-10');
	  $('#content-block').toggleClass('col-md-8');
  });
})(jQuery)