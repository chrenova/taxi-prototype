$(function () {
    $("#btn").on('click', fetch_tasks);
    fetch_tasks();
    window.setInterval(fetch_tasks, 10000);
});


function fetch_tasks() {
        $.getJSON('/api/tasks', function (tasks) {
            var template = $("#mp_template").html();
            var text = Mustache.render(template, tasks);
            $("#tasks").html(text);
        })
        .fail(function(xhr, status) {
            console.log("Failed: " + status);
        });
}


function add_comment(task_id, comment) {
    data = {'comment': comment};
    $.ajax({
        type: 'PUT',
        url: '/api/tasks/' + task_id + '/comment',
        data: JSON.stringify(data),
        dataType: 'json',
        contentType: 'application/json'
    })
    .done(function(xhr, status) {
        console.log('Done: ' + status);
        $('#addCommentModal').modal('hide');
        fetch_tasks();
    })
    .fail(function(xhr, status) {
        console.log('Fail: ' + status);
        $('#errorMessage').text('FAIL');
    });
}

function start_progress(task_id, comment) {
    data = {'comment': comment};
    $.ajax({
        type: 'PUT',
        url: '/api/tasks/' + task_id + '/status/processing',
        data: JSON.stringify(data),
        dataType: 'json',
        contentType: 'application/json'
    })
    .done(function(xhr, status) {
        console.log('Done: ' + status);
        $('#startProgressModal').modal('hide');
        fetch_tasks();
    })
    .fail(function(xhr, status) {
        console.log('Fail: ' + status);
        $('#errorMessage').text('FAIL');
    });
}

function finish_task(task_id, comment, price) {
    data = {'comment': comment, 'price': price};
    $.ajax({
        type: 'PUT',
        url: '/api/tasks/' + task_id + '/status/finished',
        data: JSON.stringify(data),
        dataType: 'json',
        contentType: 'application/json'
    })
    .done(function(xhr, status) {
        console.log('Done: ' + status);
        $('#finishTaskModal').modal('hide');
        fetch_tasks();
    })
    .fail(function(xhr, status) {
        console.log('Fail: ' + status);
        console.log('Fail: ' + xhr.responseText);
        $('#errorMessage').text('FAIL');
    });
}

function archive_task(task_id, comment) {
    data = {'comment': comment};
    $.ajax({
        type: 'PUT',
        url: '/api/tasks/' + task_id + '/archived',
        data: JSON.stringify(data),
        dataType: 'json',
        contentType: 'application/json'
    })
    .done(function(xhr, status) {
        console.log('Done: ' + status);
        $('#archiveTaskModal').modal('hide');
        fetch_tasks();
    })
    .fail(function(xhr, status) {
        console.log('Fail: ' + status);
        $('#errorMessage').text('FAIL');
    });
}


$('#addCommentModal').on('show.bs.modal', function(event) {
  $('#message-text').val("");
  $('#addCommentSubmit').unbind();
  $('#addCommentSubmit').on('click', function(){
    var button = $(event.relatedTarget);
    var task_id = button.data('task_id');
    //addCommnet(event.relatedTarget);
    $(event.relatedTarget).addClass("btn-info");
    //todo sem by malo prist ajaxove volanie ulozenia komentaru
    add_comment(task_id, $('#message-text').val());
  });
});

$('#startProgressModal').on('show.bs.modal', function(event) {
  $('#message-text').val("");
  $('#startProgressSubmit').unbind();
  $('#startProgressSubmit').on('click', function(){
    var button = $(event.relatedTarget);
    var task_id = button.data('task_id');
    //addCommnet(event.relatedTarget);
    $(event.relatedTarget).addClass("btn-info");
    //todo sem by malo prist ajaxove volanie ulozenia komentaru
    start_progress(task_id, $('#message-text').val());
  });
});

$('#finishTaskModal').on('show.bs.modal', function(event) {
  $('#message-text').val("");
  $('#price').val("");
  $('#finishTaskSubmit').unbind();
  $('#finishTaskSubmit').on('click', function(){
    var button = $(event.relatedTarget);
    var task_id = button.data('task_id');
    //addCommnet(event.relatedTarget);
    $(event.relatedTarget).addClass("btn-info");
    //todo sem by malo prist ajaxove volanie ulozenia komentaru
    finish_task(task_id, $('#message-text').val(), $('#price').val());
  });
});

$('#archiveTaskModal').on('show.bs.modal', function(event) {
  $('#message-text').val("");
  $('#archiveTaskSubmit').unbind();
  $('#archiveTaskSubmit').on('click', function(){
    var button = $(event.relatedTarget);
    var task_id = button.data('task_id');
    //addCommnet(event.relatedTarget);
    $(event.relatedTarget).addClass("btn-info");
    //todo sem by malo prist ajaxove volanie ulozenia komentaru
    archive_task(task_id, $('#message-text').val());
  });
});


function addCommnet(element){
  var commentEl = $(element).closest('td').siblings('.koment');
  var previousText = commentEl.html();

  var addedText = $('#message-text').val();
  if(previousText){
      commentEl.html(previousText);
      commentEl.append("<br/>").append(addedText);
  }
  else{
    commentEl.append(addedText);
  }
  $('#exampleModal').modal('toggle');
}
