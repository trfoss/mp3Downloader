/*global $*/

/** FUNCTIONS **/
function getSearchResults(){
  $.ajax({

      type: "GET",
      // url: "getSearchResults.py",
      // for local testing :)
      url:  "http://127.0.0.1:5000/getSearchResults",
      dataType: "json",
      // data: { "": },

      success: function(data,status) {
          console.log(data["hello"]);
          $("#test").html("<center>Success !!!</center>w");

      },

      complete: function(data,status) { //optional, used for debugging purposes
          // console.log(status);
          // console.log(data);
      }

  });//ajax
}

function addTrackToTable(track){
  let str = '<tr>'+
            '<th scope="row"><input type="checkbox" name="download"></th>'+
            '<td>' + track["trackName"] + '</td>' +
            '<td>' + track["artistName"] + '</td>' +
            '<td>' + track["collectionName"] + '</td>' +
            '<td>' + track["trackId"] + '</td>' +
         '</tr>';
  $("#results").append(str);
}

function buildResults(data){
  if(data["resultCount"] == 0){
    // console.log("No Search Results...");
    $("#results").html("No Search Results...");
    $("#results").show();
    return;
  }


  for(let i = 0; i < data["resultCount"]; i++){
    let temp = data["results"][i];
    if(temp["wrapperType"] == "track")
      addTrackToTable(temp);
    else if(temp["wrapperType"] == "collection")
      getSongsOffAlbum(temp);

  }
  $("#results").show();
}

function generalSearch(query){
  $.ajax({
      type: "GET",

      url:  "https://itunes.apple.com/search",
      dataType: "json",
      data: {
        "term": query,
        "limit" : 200
      },
      success: function(data,status) {
          console.log(data);
          buildResults(data);
          // $("#test").html("<center>Success !!!</center>w");
      },
      complete: function(data,status) { //optional, used for debugging purposes
      }
  });//ajax
}

/** LINKING **/
$("#button").click(function(){
  // console.log("Click");
  // console.log($("#search").val().toLowerCase());
  // console.log("option: " + $("#menu").val());

  $("#results").html("");
  $("#table").show();

  let query = $("#search").val().toLowerCase();
  generalSearch(query);

});


/** MAIN **/
$("table").hide();