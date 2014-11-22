$(document).ready(function(){
  $("#search-keywords").submit(getSearchTerms);
  $("#search-zipcode").submit(getSearchTerms);
  $(":checkbox").click(getCheckboxes);

  /*accordion menu*/
  $("#accordion h3").click(function(){
    //slide up all the link lists
    $("#accordion ul ul").slideUp();
    //slide down the link list below the h3 clicked - only if its closed
    if(!$(this).next().is(":visible"))
    {
      $(this).next().slideDown();
    }
  });

  $("#accordion ul ul li").click(function(){
    $("#accordion ul ul li ul").slideUp();
    if(!$(this).next().is(":visible"))
    {
      $(this).next().slideDown();
    }
  });

  // $(":checkbox").click(function() {
  //   var item = this;
  //   var id = item.id;

  //   getByArea(id)
  // });
});

/*search*/
function getSearchTerms(e){
  e.preventDefault();
  var input = {};
  var keywordArea = $("#searchbox");
  if(keywordArea.val()!==""){
    input["keyword"] = keywordArea.val();
  }
  var zipArea = $("#zipcode");
  if(zipArea.val()!==""){
    input["zipcode"] = zipArea.val();
  }

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
    url: "/keyword_search",
    data: input
  })
  .done(function( msg ) {
    console.log(msg);
  });
}

function getCheckboxes(){
  var input = {};
  var keywordArea = $("#searchbox");
  if(keywordArea.val()!==""){
    input["keyword"] = keywordArea.val();
  }
  var zipArea = $("#zipcode");
  if(zipArea.val()!==""){
    input["zipcode"] = zipArea.val();
  }

  // $("input:checked").each(function() {
  //   var checked = $(this);
  //   input["checkbox"] = checked.val();
  // });

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
    url: "/keyword_search",
    data: input
  })
  .done(function( msg ) {
    console.log(msg);
  });

}

// function getSearchKeywords(e){
//   e.preventDefault();
//   var searchArea = $("#searchbox");
//   var keyword = searchArea.val();

//   console.log("search keywords: ", keyword);
//   $.ajax({
//     type: "POST",
//     url: "/keyword_search",
//     data: { keyword: keyword }
//   })
//   .done(function( msg ) {
//     console.log(msg);
//   });

// }

// function getSearchZipCode(e){
//   e.preventDefault();
//   var searchArea = $("#zipcode");
//   var zipcode = searchArea.val();

//   console.log("search zipcode: ", zipcode);
//   $.ajax({
//     type: "POST",
//     url: "/zipcode_search",
//     data: { zipcode: zipcode }
//   })
//   .done(function( msg ) {
//     console.log(msg);
//   });

// }

// function getByArea(id){

//   var name = "#"+id;
//   var clicked = $(name);
//   var area = clicked.val();
  
//   console.log("search area: ", area);
//   $.ajax({
//     type: "POST",
//     url:"/area_search",
//     data: { area: area }
//   })
//   .done(function( msg ){
//     console.log(msg);
//   });
// }