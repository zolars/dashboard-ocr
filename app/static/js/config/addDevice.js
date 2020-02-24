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

    let url = data.deviceAddress + Params.op.status;

    $.ajax({
      url: url,
      type: "get",
      data: "",
      dataType: "json",
      async: false,
      success: function(response) {
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
        // $("img#videoPanel").attr("src", data.deviceAddress + Params.op.video);
        // console.log(response.curvals.torch);
        // if (response.curvals.torch == "off") {
        //   $("a#switchTorch").addClass("btn-success");
        // } else {
        //   $("a#switchTorch").addClass("btn-danger");
        // }
      },
      error: function(err) {
        opts.text = "Connection Failed! Error Msg:<br /><br />> " + err;
        opts.type = "error";
        PNotify.alert(opts);
        console.log(err);
      }
    });
  });

  $("a#switchTorch").click(function() {
    const data = {
      deviceName: $("input#deviceName").val(),
      deviceAddress: $("input#deviceAddress").val()
    };
    let url;
    if ($("a#switchTorch").hasClass("btn-success")) {
      url = data.deviceAddress + Params.op.enabletorch;
      $("a#switchTorch").removeClass("btn-success");
      $("a#switchTorch").addClass("btn-danger");
    } else {
      url = data.deviceAddress + Params.op.disabletorch;
      $("a#switchTorch").removeClass("btn-danger");
      $("a#switchTorch").addClass("btn-success");
    }
    $.ajax({
      url: url,
      type: "get",
      data: "",
      dataType: "text",
      async: false,
      success: function() {
        opts.text = "Operation Success!";
        opts.type = "success";
        PNotify.alert(opts);
      },
      error: function(err) {
        opts.text = "Operation Failed! Error Msg:<br /><br />> " + err;
        opts.type = "error";
        PNotify.alert(opts);
        console.log(err);
      }
    });
  });

  $("input#zoom").slider({
    formatter: function(value) {
      if (value == 0) {
        return;
      }
      const data = {
        deviceName: $("input#deviceName").val(),
        deviceAddress: $("input#deviceAddress").val()
      };
      $.ajax({
        url: data.deviceAddress + Params.op.ptz.format({ zoom: value }),
        type: "get",
        data: "",
        dataType: "text",
        async: false,
        success: function() {
          $("span#zoomShow").text(value);
        },
        error: function(err) {
          console.log(err);
        }
      });
    }
  });

  $("a#saveDevice").click(function() {
    const data = {
      deviceName: $("input#deviceName").val(),
      deviceAddress: $("input#deviceAddress").val()
    };
  });
});
