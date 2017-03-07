<script src="http://code.jquery.com/jquery.js"></script>
<script>


function displayResults(data){

    var searchResult = document.getElementById("searchresults");

    for (opp in data){
        console.log(data[opp]);
        var newA = document.createElement('a');
        var newBr = document.createElement('br');
        newA.setAttribute('href', "/opportunities/" + opp);
        newA.innerHTML = data[opp];
        searchResult.appendChild(newA);
        searchResult.append(newBr);
    }
}

function getSearchResults(event){
    event.preventDefault();
    var searchResult = document.getElementById("searchresults");
    searchResult.innerHTML = "";
    console.log("in getSearchResults");
    var searchquery = $('#searchquery').val();
    console.log(searchquery);
    $.get("/get-results", {searchquery: searchquery}, displayResults);
}


$("#search-form").on("submit", getSearchResults);

</script>