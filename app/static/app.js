$("#btn").on('click', fetch_tasks);

function fetch_tasks(callback) {
        $.getJSON('/api/tasks', function (tasks) {
            callback(tasks);
        })
        .fail(function(xhr, status) {
            console.log("Failed: " + status);
        });
}

function fetch_users(callback) {
        $.getJSON('/api/users', function (users) {
            callback(users);
        })
        .fail(function(xhr, status) {
            console.log("Failed: " + status);
        });
}

function edit_form(id) {
        $.get('/edit_form/' + id, function (f) {
            console.log('f: ');
            console.log(f);
            return f;
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

$('#claimSubmit').on('click', function(event) {
    console.log($('#task_id').val());
});

$('#actionModal').on('shown.bs.modal', function(event) {
    console.log('SHOWN');
    var button = $(event.relatedTarget);
    var task_id = button.data('task_id');
    console.log(task_id);
    $('#task_id').val(task_id);
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
    $('#task_id').val(null);
});

function find_task_in_tasks(id) {
    for(var i=0; i < tasks_global.length; i++) {
        if(tasks_global[i]['id'] === id) {
            return tasks_global[i];
        }
    }
    return;
}

/*
function loop_users(selected_user) {
    var users_copy = users_global.slice();
    for(var i=0; i < users_copy.length; i++) {
        if(users_copy[i]['id'] === selected_user) {
            users_copy[i]['selected'] = true;
        }
    }
    return users_copy;
}
*/

$('#edit_modal')
.on('show.bs.modal', function(event) {
    console.log('editModal SHOW');
    var button = $(event.relatedTarget);
    var task_id = button.data('task_id');
    console.log(task_id);
    console.log(users_global);
    var task = find_task_in_tasks(task_id);
    console.log('task: ' + task);
    var data = {
            'task': task,
            'users': users_global
            };
    var options = $('#edit_assigned_to').prop('options');
    $('option', $('#edit_assigned_to')).remove();
    options[options.length] = new Option('', '');
    $.each(users_global, function(i, obj) {
        options[options.length] = new Option(obj['username'], obj['id']);
    });
    $('#edit_assigned_to').val(task['assigned_to_id']);
    $('#edit_status').val(task['status']);
    $('#edit_task_id').val(task_id);
    $('#edit_origin').val(task['origin']);
    $('#edit_destination').val(task['destination']);
    $('#edit_comment').val(task['comments']);
    $('#edit_estimated_price').val(task['estimated_price']);
    $('#edit_real_price').val(task['real_price']);
    $('#edit_time_to_arrive').val(task['time_to_arrive']);
})
.on('shown.bs.modal', function(event) {
    console.log('editModal SHOWN');
    console.log(f);
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

function create_new_task(assigned_to, origin, destination, comment, time_to_arrive, estimated_price, done_callback, fail_callback) {
    data = {
        'comment': comment,
        'assigned_to': assigned_to,
        'origin': origin,
        'destination': destination,
        'time_to_arrive': time_to_arrive,
        'estimated_price': estimated_price
    };
    $.ajax({
        type: 'POST',
        url: '/api/tasks',
        data: JSON.stringify(data),
        dataType: 'json',
        contentType: 'application/json'
    })
    .done(done_callback)
    .fail(fail_callback);
}

function update_task(task_id, assigned_to, origin, destination, status, comment, time_to_arrive, estimated_price, real_price, done_callback, fail_callback) {
    data = {
        'comment': comment,
        'assigned_to': assigned_to,
        'origin': origin,
        'destination': destination,
        'status': status,
        'time_to_arrive': time_to_arrive,
        'estimated_price': estimated_price,
        'real_price': real_price
    };
    $.ajax({
        type: 'POST',
        url: '/api/tasks/' + task_id,
        data: JSON.stringify(data),
        dataType: 'json',
        contentType: 'application/json'
    })
    .done(done_callback)
    .fail(fail_callback);
}
