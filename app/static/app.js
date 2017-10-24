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

$('#actionModal').on('shown.bs.modal', function(event) {
    console.log('SHOWN');
    var button = $(event.relatedTarget);
    var task_id = button.data('task_id');
    console.log(task_id);
    var available_actions_str = button.data('available_actions');
    console.log(available_actions_str);
    var available_actions = available_actions_str.split(',');
    if (available_actions.includes('can_claim') === true) {
        $('#claimSubmit').show();
    }
    if (available_actions.includes('can_start_progress') === true) {
        $('#startProgressSubmit').show();
    }
    if (available_actions.includes('can_request_call_customer') === true) {
        $('#requestCallCustomerSubmit').show();
    }
    if (available_actions.includes('can_request_call_me') === true) {
        $('#requestCallMeSubmit').show();
    }
    if (available_actions.includes('can_change_route') === true) {
        $('#changeRouteSubmit').show();
    }
    if (available_actions.includes('can_finish_task') === true) {
        $('#finishSubmit').show();
    }

/*
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
*/
})
.on('show.bs.modal', function(event) {
    console.log('SHOW');
    $('#claimSubmit').hide();
    $('#finishSubmit').hide();
    $('#startProgressSubmit').hide();
    $('#requestCallCustomerSubmit').hide();
    $('#requestCallMeSubmit').hide();
    $('#changeRouteSubmit').hide();
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
