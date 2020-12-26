

function comp(){
    var searchInput = document.getElementById('myInput');
    var suggestionPanel = document.getElementById('suggestion');
    searchInput.addEventListener('keyup', function(){
        var input = searchInput.value.toLowerCase();
        
        suggestionPanel.innerHTML = '';
        
        var suggestions = list_of_movies.filter(movie => movie.toLowerCase().startsWith(input)).slice(0, 5);;
        
        
        suggestions.forEach(function(suggested){
            const div = document.createElement('div');
            div.innerHTML = suggested;
            div.innerHTML += "<input type='hidden' value='" + suggested + "'>";
            div.addEventListener("click", function(e) {
              /*insert the value for the autocomplete text field:*/
              searchInput.value = this.getElementsByTagName("input")[0].value;
              
              
          });
            suggestionPanel.appendChild(div);
        });
        
        if(!input){
            suggestionPanel.innerHTML = '';
        }
        
    })
}

comp();