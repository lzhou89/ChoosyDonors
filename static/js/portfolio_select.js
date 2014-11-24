$(document).ready(function(){
  var options = {
    valueNames: ['checkbox'],
    page: 20,
    plugins: [
      ListPagination({})
    ]
  };

  var listObj = new List('results', options);

  $("#add").submit(getCheckboxes);
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
  }
  console.log(selected);
  console.log(input);

  $.ajax({
    type: "POST",
    url: "/mid_portfolio",
    data: input
  });

}