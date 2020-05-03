$(document).ready(function() {
  if (Params.existedUsername != null) {
    $("input#username").val(Params.existedUsername);
  }
  if (Params.existedPassword != null) {
    $("input#password").val(Params.existedPassword);
  }

  $("a#testDatabase").click(function() {
    const data = {
      username: $("input#username").val(),
      password: $("input#password").val(),
    };
    $.ajax({
      url: Urls.server.testDatabase,
      type: "post",
      data: data,
      async: true,
      success: function(msg) {
        if (msg == "Ok") {
          flash("Connection Success!", "success");
        } else if (msg == "error") {
          flash("Connection Failed!", "error");
        }
      },
      error: function(err) {
        console.log(err);
      },
    });
  });

  $("a#saveDatabase").click(function() {
    const data = {
      username: $("input#username").val(),
      password: $("input#password").val(),
    };
    $.ajax({
      url: Urls.server.saveDatabase,
      type: "post",
      data: data,
      async: true,
      success: function(msg) {
        if (msg == "Ok") {
          flash("Connection saved Successfully!", "success");
        } else if (msg == "error") {
          flash("Saving Connection Failed! Please check again.", "error");
        }
      },
      error: function(err) {
        console.log(err);
      },
    });
  });

  $("a#initDatabase").click(function() {
    $.ajax({
      url: Urls.server.initDatabase,
      type: "post",
      async: true,
      success: function(msg) {
        if (msg == "Ok") {
          flash("Initialization Success!", "success");
        } else {
          flash("Initialization Failed! Error Msg:<br /><br />" + msg, "error");
        }
      },
      error: function(err) {
        console.log(err);
      },
    });
  });

  $("a#resetDatabase").click(function() {
    var checkbox = PNotify.error({
      title: "Confirmation Needed",
      text: "Reset the database means delete all existed data. Are you sure?",
      icon: "fas fa-exclamation-triangle",
      hide: false,
      stack: {
        modal: true,
        overlayClose: true,
      },
      modules: {
        Confirm: {
          confirm: true,
        },
        Buttons: {
          closer: false,
          sticker: false,
        },
        History: {
          history: false,
        },
      },
    });

    checkbox.on("pnotify.confirm", function() {
      $.ajax({
        url: Urls.server.resetDatabase,
        type: "post",
        async: true,
        success: function(msg) {
          if (msg == "Ok") {
            flash("Reset Success!", "success");
          } else {
            flash("Reset Failed! Error Msg:<br /><br />" + msg, "error");
          }
        },
        error: function(err) {
          console.log(err);
        },
      });
    });
    checkbox.on("pnotify.cancel", function() {
      checkbox.close();
    });
  });
});
