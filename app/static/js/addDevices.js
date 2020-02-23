$(document).ready(function() {
  if (Params.deviceName != null) {
    $("input#deviceName").val(Params.deviceName);
  }
  if (Params.deviceAddress != null) {
    $("input#deviceAddress").val(Params.deviceAddress);
  }

  $("a#testDevice").click(function() {
    const data = {
      deviceName: $("input#deviceName").val(),
      deviceAddress: $("input#deviceAddress").val()
    };
    $.ajax({
      url: Urls.server.testDevice,
      type: "post",
      data: data,
      async: false,
      success: function(msg) {
        if (msg == "OK") {
          opts.text = "Connection Success!";
          opts.type = "success";
          PNotify.alert(opts);
          $("div#configDevice_2").css("display", "block");
          $("a#resetDevice").css("display", "table");
          $("a#testDevice").css("display", "none");
          $("input#deviceName").attr("disabled", "disabled");
          $("input#deviceAddress").attr("disabled", "disabled");
          $("p#collapseLabel_1").text(
            "New device's name and its network address is as below. "
          );
        } else {
          opts.text = "Connection Failed! Error Msg:<br /><br />> " + msg;
          opts.type = "error";
          PNotify.alert(opts);
        }
      },
      error: function(err) {
        console.log(err);
      }
    });
  });

  $("a#saveDevice").click(function() {
    const data = {
      deviceName: $("input#deviceName").val(),
      deviceAddress: $("input#deviceAddress").val()
    };
  });
});