const searchField = document.querySelector('#searchField');

searchField.addEventListener('keyup', (e)=> {
    const searchValue = e.target.value;

    if(searchValue.trim().length > 0){
        console.log('searchValue', searchValue);

        // make an API call to our server
        fetch('/expenses/search-expenses', {
            body: JSON.stringify({ searchText: searchValue }),
            method:"POST",
        })
            .then(res=>res.json())
            .then(data=>{
                console.log('data', data)
        });

    }
});