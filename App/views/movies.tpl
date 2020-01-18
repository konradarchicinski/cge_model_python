% rebase('base.tpl', title='Python')
<div class="row">
	<div class="col-md-12">
	
	
	<h3>{{message}}</h3>
	Hello {{loginName}}
	
	% for movie in movies:
	<div>
	<h4>{{movie["title"]}}</h4>
	<span><b>{{movie["score"]}}</b></span>
	<p>{{movie["review"]}}</p>
	</div>

	% end
	
	
	
	
	
	</div>
</div>
