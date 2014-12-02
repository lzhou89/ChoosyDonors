$(document).ready(function(){
	var options = {
		valueNames: ['"well well-sm"'],
		page: 5,
		plugins: [
			ListPagination({})
		]
	};
	var listObj = new List('results', options);
  
  $("#clear_all").submit(function(e) {
	e.preventDefault();
	$.ajax({
		type: "GET",
		url: "/clear_all",
		})
	.done(function(msg) {
		console.log(msg);
		$("#results").load("/confirm_portfolio #results");
		});
	});
  $("#clear_projs").submit(getCheckboxes);
});

function getCheckboxes(e){
  e.preventDefault();
  var input = {};

  var selected = [];
  $("input:checked").each(function() {
    selected.push($(this).attr('id'));
  });
  if(selected.length > 0){
    selected = selected.toString();
    input["checkboxes"] = selected;

    console.log(selected);
    console.log(input);

    $.ajax({
      type: "POST",
      url: "/clear_selected",
      data: input
    })
    .done(function(msg) {
      $("#results").load("/confirm_portfolio #results");
    });
  }
  else {
    alert("No projects selected.");
  }

}