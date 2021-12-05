let settings = document.getElementById('setting').value;
if (settings) {
    load(settings);
}
document.getElementById('setting').style.display = 'none';
let context = window.location.href.split('/')[3];

function select_charge() {
    let query_type = document.getElementById("query_type").value;
    let filters = document.getElementsByClassName('filter');
    if (query_type === '0' || query_type === '2' || query_type === '4') {
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
}

function load(setting) {
    let filters = document.getElementsByClassName('filter');
    let inputs = document.getElementsByTagName("input");
    let sets = setting.split(',');
    if (sets[0] === '0') {
        document.getElementById("query_type").options[0].selected = true;
        //inputs[0].value = null;
        inputs[0].value = sets[1];
        inputs[1].value = null;
        inputs[2].value = null;
        filters[1].style.display = 'none';
        filters[2].style.display = '';
        filters[3].style.display = 'none';
        filters[4].style.display = 'none';
    }
    if (sets[0] === '1') {
        document.getElementById("query_type").options[1].selected = true;
        //inputs[0].value = null;
        inputs[0].value = null;
        inputs[1].value = sets[1];
        inputs[2].value = null;
        filters[1].style.display = 'none';
        filters[2].style.display = 'none';
        filters[3].style.display = '';
        filters[4].style.display = 'none';
    }
    if (sets[0] === '2') {
        document.getElementById("query_type").options[2].selected = true;
        //inputs[0].value = null;
        inputs[0].value = sets[1];
        inputs[1].value = null;
        inputs[2].value = null;
        filters[1].style.display = 'none';
        filters[2].style.display = '';
        filters[3].style.display = 'none';
        filters[4].style.display = 'none';
    }
    if (sets[0] === '3') {
        document.getElementById("query_type").options[3].selected = true;
        //inputs[0].value = sets[1];
        inputs[0].value = null;
        inputs[1].value = null;
        inputs[2].value = sets[2];
        filters[1].style.display = '';
        filters[2].style.display = 'none';
        filters[3].style.display = 'none';
        filters[4].style.display = '';
    }
    if (sets[0] === '4') {
        document.getElementById("query_type").options[4].selected = true;
        //inputs[0].value = null;
        inputs[0].value = sets[1];
        inputs[1].value = null;
        inputs[2].value = null;
        filters[1].style.display = 'none';
        filters[2].style.display = '';
        filters[3].style.display = 'none';
        filters[4].style.display = 'none';
    }
}

function search() {
    let query_type = document.getElementById("query_type").value;
    let filters = document.getElementsByTagName("input");
    let request_url = '';
    if (query_type === '0' || query_type === '2') {
        //let question_id = filters[0].value;
        let answer_id = filters[0].value.trim();
        if (!answer_id) {
            $.Toast('请输入回答Id', 'error');
            return
        }
        request_url = '/answer?aId=' + answer_id;
    }
    if (query_type === '1'){
        let user_id = filters[1].value.trim();
        if (!user_id || user_id === '0') {
            $.Toast('请输入用户 Id 或 url token', 'error');
            return
        }
        request_url = '/comment?userId=' + user_id;
    }
    if (query_type === '3'){
        let venture = document.getElementById("venture").value;
        let key_word = filters[2].value.trim();
        if (!key_word) {
            $.Toast('请输入关键词', 'error');
            return
        }
        request_url = '/find?venture='+ venture + '&keyWord=' + key_word;
    }
    if (query_type === '4'){
        let answer_id = filters[0].value.trim();
        if (!answer_id) {
            $.Toast('请输入回答Id', 'error');
            return
        }
        request_url = '/images?aId=' + answer_id;
    }
    window.location.href = '/' + context + request_url + '&type=' + query_type;
}

function to_next_page() {
    let sets = settings.split(',');
    let page = parseInt(sets[2]) + 1;
    let request_url = '';
    if (sets[0] === '0' || sets[0] === '2') {
        request_url = '/answer?aId=' + sets[1] + '&type=' + sets[0] + '&page=' + page;
    }
    if (sets[0] === '1'){
        request_url = '/comment?userId=' + sets[1] + '&type=' + sets[0] + '&page=' + page;
    }
    if (sets[0] === '3'){
        page = parseInt(sets[3]) + 1;
        request_url = '/find?venture='+ sets[1] + '&keyWord=' + sets[2] + '&type=' + sets[0] + '&page=' + page;
    }
    if (sets[0] === '4'){
        request_url = '/images?aId=' + sets[1] + '&type=' + sets[0] + '&page=' + page;
    }
    window.location.href = '/' + context + request_url;
}

function to_up_page() {
    let sets = settings.split(',');
    let page = parseInt(sets[2]) - 1;
    let request_url = '';
    if (sets[0] === '0' || sets[0] === '2') {
        request_url = '/answer?aId=' + sets[1] + '&type=' + sets[0] + '&page=' + page;
    }
    if (sets[0] === '1'){
        request_url = '/comment?userId=' + sets[1] + '&type=' + sets[0] + '&page=' + page;
    }
    if (sets[0] === '3'){
        page = parseInt(sets[3]) - 1;
        request_url = '/find?venture='+ sets[1] + '&keyWord=' + sets[2] + '&type=' + sets[0] + '&page=' + page;
    }
    if (sets[0] === '4'){
        request_url = '/images?aId=' + sets[1] + '&type=' + sets[0] + '&page=' + page;
    }
    window.location.href = '/' + context + request_url;
}
