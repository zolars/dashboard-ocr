$(document).ready(function() {
  if (Params.existedUsername != null) {
    $("input#username").val(Params.existedUsername);
  }
  if (Params.existedPassword != null) {
    $("input#password").val(Params.existedPassword);
  }

  $("#testDatabase").click(function() {
    const data = {
      username: $("input#username").val(),
      password: $("input#password").val()
    };
    $.ajax({
      url: Urls.server.testDatabase,
      type: "post",
      data: data,
      async: false,
      success: function(msg) {
        if (msg == "success") {
          opts.text = "Connection Success!";
          opts.type = "success";
          PNotify.alert(opts);
        } else if (msg == "error") {
          opts.text = "Connection Failed!";
          opts.type = "error";
          PNotify.alert(opts);
        }
      },
      error: function(err) {
        console.log(err);
      }
    });
  });

  $("#saveDatabase").click(function() {
    const data = {
      username: $("input#username").val(),
      password: $("input#password").val()
    };
    $.ajax({
      url: Urls.server.saveDatabase,
      type: "post",
      data: data,
      async: false,
      success: function(msg) {
        if (msg == "success") {
          opts.text = "Connection saved Successfully!";
          opts.type = "success";
          PNotify.alert(opts);
        } else if (msg == "error") {
          opts.text = "Saving Connection Failed! Please check again.";
          opts.type = "error";
          PNotify.alert(opts);
        }
      },
      error: function(err) {
        console.log(err);
      }
    });
  });

  $("#initDatabase").click(function() {
    $.ajax({
      url: Urls.server.initDatabase,
      type: "post",
      async: false,
      success: function(msg) {
        if (msg == "success") {
          opts.text = "Initialization Success!";
          opts.type = "success";
          PNotify.alert(opts);
        } else {
          opts.text =
            "Initialization Failed!<br /><br />> Error Msg:&nbsp;" + msg;
          opts.type = "error";
          PNotify.alert(opts);
        }
      },
      error: function(err) {
        console.log(err);
      }
    });
  });

  $("#resetDatabase").click(function() {
    var checkbox = PNotify.error({
      title: "Confirmation Needed",
      text: "Reset the database means delete all existed data. Are you sure?",
      icon: "fas fa-exclamation-triangle",
      hide: false,
      stack: {
        modal: true,
        overlayClose: true
      },
      modules: {
        Confirm: {
          confirm: true
        },
        Buttons: {
          closer: false,
          sticker: false
        },
        History: {
          history: false
        }
      }
    });

    checkbox.on("pnotify.confirm", function() {
      $.ajax({
        url: Urls.server.resetDatabase,
        type: "post",
        async: false,
        success: function(msg) {
          if (msg == "success") {
            opts.text = "Reset Success!";
            opts.type = "success";
            PNotify.alert(opts);
          } else {
            opts.text = "Reset Failed!<br /><br />> Error Msg:&nbsp;" + msg;
            opts.type = "error";
            PNotify.alert(opts);
          }
        },
        error: function(err) {
          console.log(err);
        }
      });
    });
    checkbox.on("pnotify.cancel", function() {
      checkbox.close();
    });
  });
});
