var editor = null;

function pretty() {
    $('table.docutils').addClass('table table-striped');
    $('p.admonition-title').hide();
    $('div.warning').addClass('alert');
    $('div.danger').addClass('alert alert-danger');
    $('div.note').addClass('alert alert-info');
}

function initjs() {
    $('#table-list tr').hover(
    function() {
        $(".item-operation[data-id='"+$(this).attr('data-id')+"']").show();
    },
    function() {
        $(".item-operation[data-id='"+$(this).attr('data-id')+"']").hide();
    });
}

//============================================================================
// Feedback
//============================================================================

function flash(type, msg) {
    alert(type+': '+msg);
}

//============================================================================
// Functions
//============================================================================

function refresh() {
    location.reload(true);
}

function create_folder() {
    var name = prompt("Folder Name:", "");
    if (!name) return;

    var path = $('#resource_path').val();

    $.getJSON('/_create_folder', {
        name: name,
        path: path,
    }, function(data) {
        if (data.result == 'ok') {
            refresh();
        } else {
            flash('error', data.motive);
        }
    });
}

function rename_folder(old_name) {
    var new_name = prompt("New Folder Name:", "");
    if (!new_name) return;
    var path = $('#resource_path').val();

    $.getJSON('/_rename_folder', {
        old_name: old_name,
        new_name: new_name,
        path: path,
    }, function(data) {
        if (data.result == 'ok') {
            refresh();
        } else {
            flash('error', data.motive);
        }
    });
}

function remove_folder(name) {
    if (!name) return;
    var path = $('#resource_path').val();
    if (confirm('Delete folder "'+name+'"?')) {
        $.getJSON('/_remove_folder', {
            name: name,
            path: path,
        }, function(data) {
            if (data.result == 'ok') {
                refresh();
            } else {
                flash('error', data.motive);
            }
        });
    }
}

function create_file() {
    var name = prompt("Document Name:", "New Document.rst");
    if (!name) return;
    var path = $('#resource_path').val();

    $.getJSON('/_create_file', {
        name: name,
        path: path,
    }, function(data) {
        if (data.result == 'ok') {
            refresh();
        } else {
            flash('error', data.motive);
        }
    });
}

function rename_file(old_name) {
    var new_name = prompt("New Folder Name:", "");
    if (!new_name) return;
    var path = $('#resource_path').val();

    $.getJSON('/_rename_file', {
        old_name: old_name,
        new_name: new_name,
        path: path,
    }, function(data) {
        if (data.result == 'ok') {
            refresh();
        } else {
            flash('error', data.motive);
        }
    });
}

function remove_file(name) {
    if (!name) return;
    var path = $('#resource_path').val();
    if (confirm('Delete file "'+name+'"?')) {
        $.getJSON('/_remove_file', {
            name: name,
            path: path,
        }, function(data) {
            if (data.result == 'ok') {
                refresh();
            } else {
                flash('error', data.motive);
            }
        });
    }
}

function open_folder(name) {
    var path = $('#resource_path').val();

    $.getJSON('/_open_folder', {
        name: name,
        path: path,
    }, function(data) {});
}

function open_file(name) {
    var path = $('#resource_path').val();

    $.getJSON('/_open_file', {
        name: name,
        path: path,
    }, function(data) {});
}