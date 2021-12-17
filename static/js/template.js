let ventures = {"100":0
,"120":1
,"193":2
,"160":3
,"110":4
,"180":5
,"152":6
,"112":7
,"140":8
,"141":9
,"130":10
,"111":11
,"121":12
,"122":13
,"150":14
,"151":15
,"131":16
,"181":17
,"132":18
,"171":19
,"172":20
,"161":21
,"176":22
,"182":23
,"183":24
,"173":25
,"174":26
,"175":27
,"190":28
,"191":29
,"192":30
,"170":31}
/**let settings = document.getElementById('setting').value;
if (settings) {
    load(settings);
}
document.getElementById('setting').style.display = 'none';**/
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
        document.getElementById("venture").options[ventures[sets[1]]].selected = true;
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
    if (query_type === '0') {
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
    if (query_type === '2') {
        //let question_id = filters[0].value;
        let answer_id = filters[0].value.trim();
        if (!answer_id) {
            $.Toast('请输入回答Id', 'error');
            return
        }
        request_url = '/similarity?aId=' + answer_id;
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

function to_next_page(settings) {
    let sets = settings.split(',');
    let page = parseInt(sets[2]) + 1;
    let request_url = '';
    if (sets[0] === '0') {
        request_url = '/answer?aId=' + sets[1] + '&type=' + sets[0] + '&page=' + page;
    }
    if (sets[0] === '1'){
        request_url = '/comment?userId=' + sets[1] + '&type=' + sets[0] + '&page=' + page;
    }
    if (sets[0] === '2') {
        request_url = '/similarity?aId=' + sets[1] + '&type=' + sets[0] + '&page=' + page;
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

function to_up_page(settings) {
    let sets = settings.split(',');
    let page = parseInt(sets[2]) - 1;
    let request_url = '';
    if (sets[0] === '0') {
        request_url = '/answer?aId=' + sets[1] + '&type=' + sets[0] + '&page=' + page;
    }
    if (sets[0] === '1'){
        request_url = '/comment?userId=' + sets[1] + '&type=' + sets[0] + '&page=' + page;
    }
    if (sets[0] === '2'){
        request_url = '/similarity?aId=' + sets[1] + '&type=' + sets[0] + '&page=' + page;
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

function forum() {
    window.location.href = '/' + context + '/forum';
}

function course() {
    window.location.href = '/' + context + '/course';

}

function submit() {
    document.getElementById("reply-comment").style.display = 'none';
    let v_input = document.getElementById("v-input").value;
    if (!v_input) {
        $.Toast("请输入内容", 'error');
        return;
    }
    let data = {
        id: null,
        content: v_input
    }
    $.ajax({
        type: "post",
        url: "addComment",
        data: JSON.stringify(data),
        dataType: "json",
        contentType: "application/json; charset=utf-8",
        success: function (data) {
            if (data['code'] === 1) {
                $.Toast(data['msg'], 'success');
            } else {
                $.Toast(data['msg'], 'error');
                return;
            }
            window.location.href = 'forum';
        }
    })
}

function replys(user_id, user_name) {
    document.getElementById("reply-comment").style.display = '';
    document.getElementById("submit-comment").style.display = 'none';
    document.getElementById("v-reply").setAttribute("placeholder", "回复 用户 " + user_name + "：")
    document.getElementById("v-reply").className = user_id;
}

function reply() {
    let v_input = document.getElementById("v-reply").value;
    let user_id = document.getElementById("v-reply").className;
    if (!v_input) {
        $.Toast("请输入内容", 'error');
        return;
    }
    let data = {
        id: user_id,
        content: v_input
    }
    $.ajax({
        type: "post",
        url: "addComment",
        data: JSON.stringify(data),
        dataType: "json",
        contentType: "application/json; charset=utf-8",
        success: function (data) {
            if (data['code'] === 1) {
                $.Toast(data['msg'], 'success');
            } else {
                $.Toast(data['msg'], 'error');
                return;
            }
            window.location.href = 'forum';
        }
    })
}

function to_next_comment(page) {
    page = parseInt(page) + 1;
    window.location.href = '/' + context + '/forum?page=' + page;
}

function to_up_comment(page) {
    page = parseInt(page) - 1;
    window.location.href = '/' + context + '/forum?page=' + page;
}

function connect_modal() {
    let modal = document.getElementById('myModal');
    let close_a = document.getElementsByClassName("close")[0];
    let cancel_a = document.getElementsByClassName("cancel")[0];
    let submit_a = document.getElementsByClassName("submit")[0];

    modal.style.display = "block";

    close_a.onclick = function() {
        modal.style.display = "none";
    }
    cancel_a.onclick = function() {
        modal.style.display = "none";
    }

    submit_a.onclick = function() {
        let wechat = document.getElementById("wechat").value;
        let content = document.getElementById("submit_content").value;

        if (!wechat || !content) {
            console.log(123);
            $.Toast('所有内容都要填写哦 ~ ', 'error');
            return;
        }

        let post_data = {
            tel: wechat,
            content: content
        }

        $.ajax({
            type: "POST",
            url: "addConnect",
            data: JSON.stringify(post_data),
            dataType: "json",
            contentType: "application/json; charset=utf-8",
            success: function (data) {
                if (data['code'] === 1) {
                    $.Toast(data['msg'], 'success');
                    modal.style.display = "none";
                } else {
                    $.Toast(data['msg'], 'error');
                    return;
                }
            }
        })
    }


    window.onclick = function(event) {
        if (event.target == modal) {
            modal.style.display = "none";
        }
    }
}
