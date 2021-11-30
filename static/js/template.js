function select_charge() {
    let query_type = document.getElementById("query_type").value;
    let filters = document.getElementsByClassName('filter');
    if (query_type === '0' || query_type === '2') {
        filters[1].style.display = 'none';
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
        filters[1].style.display = '';
        filters[2].style.display = 'none';
        filters[3].style.display = 'none';
        filters[4].style.display = '';
    }
    if (query_type === '4'){
        filters[1].style.display = 'none';
        filters[2].style.display = '';
        filters[3].style.display = '';
        filters[4].style.display = 'none';
    }
}

function search() {
    let query_type = document.getElementById("query_type").value;
    let filters = document.getElementsByTagName("input");
    let request_url = '';
    if (query_type === '0' || query_type === '2') {
        //let question_id = filters[0].value;
        let answer_id = filters[1].value;
        request_url = '/answer?aId=' + answer_id;
    }
    if (query_type === '1'){
        let user_id = filters[2].value;
        request_url = '/comment?userId=' + user_id;
    }
    if (query_type === '3'){
        let question_id = filters[0].value;
        let key_word = filters[3].value;
        request_url = '/find?qId='+ question_id + 'keyWord=' + key_word;
    }
    if (query_type === '4'){
        let answer_id = filters[1].value;
        let user_id = filters[2].value;
        request_url = '/images?aId=' + answer_id + '&userId=' + user_id;
    }
    window.location.href = request_url;
}