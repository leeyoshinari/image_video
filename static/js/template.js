function select_charge() {
    let query_type = document.getElementById("query_type").value;
    let filters = document.getElementsByClassName('filter');
    if (query_type === '0' || query_type === '2') {
        filters[1].style.display = '';
        filters[2].style.display = '';
        filters[3].style.display = 'none';
        filters[4].style.display = 'none';
    }
    if (query_type === '1'){
        filters[1].style.display = 'none';
        filters[2].style.display = 'none';
        filters[3].style.display = '';
        filters[4].style.display = 'none';
    }
    if (query_type === '3'){
        filters[1].style.display = 'none';
        filters[2].style.display = 'none';
        filters[3].style.display = 'none';
        filters[4].style.display = '';
    }
    if (query_type === '4'){
        filters[1].style.display = '';
        filters[2].style.display = 'none';
        filters[3].style.display = '';
        filters[4].style.display = 'none';
    }

}