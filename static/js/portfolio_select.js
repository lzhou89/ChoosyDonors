$(document).ready(function(){
  $("#add").submit(getCheckboxes);
  $("#number").submit(getProjects);
});

function getProjects(e){
  e.preventDefault();
  var numberArea = $("#proj_number");
  if(numberArea.val()===""){
    alert("Please enter a number.");
  }
  else {
    var proj_number = numberArea.val();
    var cluster_id = numberArea.attr('name');
    console.log(proj_number);
    console.log(cluster_id);

    $.ajax({
      type: "POST",
      url: "/load_projects",
      data: {"number": proj_number, "id": cluster_id}
    })
    .done(function(results) {
      var output = JSON.parse(results);
      $('#results').html("<ul class='list' id='projects'></ul>");
    // var rDiv = document.createElement('div');

      if (output.length < proj_number){
        alert("This topic does not have that many projects. All available projects are listed below.");
      }

      for (var i=0; i < output.length; i++) {
        var rDiv = document.createElement('div');
        rDiv.className = "checkbox";
        $('#projects').append(rDiv);
        if (output.length === 0) {
        rDiv.innerHTML = "No results found.";
        break;
        } else{
          rDiv.innerHTML = "<input type='checkbox' id="+output[i]["id"]+" value="+output[i]["id"]+">"+
            "<dl>"+
              "<dd><a href='/project/"+output[i]["id"]+"'>"+output[i]["title"]+"</a></dd>"+
              "<dt>Teacher Name:</dt><dd>"+output[i]["teacher"]+"</dd>"+
              "<dt>School Name:</dt><dd>"+output[i]["school"]+"</dd>"+
              "<dt>School Location:</dt><dd>"+output[i]["location"]+"</dd>"+
              "<dt>Grade Level:</dt><dd>"+output[i]["grade"]+"</dd>"+
              "<dt>Matching Icon:</dt><dd>"+output[i]["matching"]+"</dd>"+
              "<dt>Keywords:</dt><dd></dd>"+
              "<dt>Needs:</dt><dd>"+output[i]["needs"]+"</dd>"+
            "</dl>";
        }
        
      }
      var rUl = document.createElement('ul');
      rUl.className = "pagination";
      $('#results').append(rUl);
      var options = {
        valueNames: ['checkbox'],
        page: 5,
        plugins: [
          ListPagination({})
        ]
      };
      var listObj = new List('results', options);

      $('#add').attr("style", "visibility:visible");
    });
  }
}


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
      url: "/mid_portfolio",
      data: input
    })
    .done(function(url) {
      window.location.href = url;
    });
  }
  else{
    alert("No projects selected.");
  }
  

}