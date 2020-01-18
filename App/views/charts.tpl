% rebase('base.tpl', title='Python')
<div class="row">
	<div class="col-md-12">
	
<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.1.4/Chart.min.js"></script>
        
<canvas id="myChart"></canvas>

        <script>
var ctx = document.getElementById('myChart').getContext('2d');
var myChart = new Chart(ctx, {
    

    
  type: 'line',
  data: {
    labels: {{!chartData["labels"]}},
    datasets: [
% chartColors = ['"rgba(244, 66, 66,0.4)"', '"rgba(21, 186, 13,0.4)"', '"rgba(13, 13, 186,0.4)"', '"rgba(13, 168, 186,0.4)"', '"rgba(255, 0, 250,0.4)"']
	% for i, (key, value) in enumerate(chartData["data"].items()):
    {
      label: '{{key}}',
      data: {{!value}},
      backgroundColor: {{!chartColors[i]}}
                        },

	% end
        
]
  }
});
        </script>
	
	
	
	</div>
</div>
