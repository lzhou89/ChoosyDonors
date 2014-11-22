$(document).ready(function(){

  initSliders();

  var FJS = FilterJS(projects, '#projects', {
    template: '#project-template',
    // search: {ele: '#searchbox'},
    search: {ele: '#searchbox', fields: ['runtime']}, // With specific fields
    callbacks: {
      afterFilter: function(result){
        $('#total_movies').text(result.length);
      }
    }
  });

  FJS.addCallback('beforeAddRecords', function(){
    if(this.recordsCount >= 450){
      this.stopStreaming();
    }
  });

  FJS.addCallback('afterAddRecords', function(){
    var percent = (this.recordsCount - 250)*100/250;

    $('#stream_progress').text(percent + '%').attr('style', 'width: '+ percent +'%;');

    if (percent == 100){
      $('#stream_progress').parent().fadeOut(1000);
    }
  });

  FJS.setStreaming({
    data_url: '../data/stream_projects.json',
    stream_after: 1,
    batch_size: 50
  });

  FJS.addCriteria({field: 'year', ele: '#year_filter', type: 'range'});
  FJS.addCriteria({field: 'rating', ele: '#rating_filter', type: 'range'});
  FJS.addCriteria({field: 'runtime', ele: '#runtime_filter', type: 'range'});
  FJS.addCriteria({field: 'genre', ele: '#genre_criteria input:checkbox'});

  
   // * Add multiple criterial.
   //  FJS.addCriteria([
   //    {field: 'genre', ele: '#genre_criteria input:checkbox'},
   //    {field: 'year', ele: '#year_filter', type: 'range'}
   //  ])
  

  window.FJS = FJS;
});

function initSliders(){


  $('#genre_criteria :checkbox').prop('checked', true);
  $('#all_genre').on('click', function(){
    $('#genre_criteria :checkbox').prop('checked', $(this).is(':checked'));
  });
}

/*accordion menu*/
$(document).ready(function(){
  $("#accordion h3").click(function(){
    //slide up all the link lists
    $("#accordion ul ul").slideUp();
    //slide down the link list below the h3 clicked - only if its closed
    if(!$(this).next().is(":visible"))
    {
      $(this).next().slideDown();
    }
  });
});
$(document).ready(function(){
  $("#accordion ul ul li ").click(function(){
    $("#accordion ul ul li ul").slideUp();
    if(!$(this).next().is(":visible"))
    {
      $(this).next().slideDown();
    }
  });
});