$(document).ready(function () {
  let calibrateResult = false;
  if (Params.deviceName != null) {
    $("input#deviceName").val(Params.deviceName);
  }
  if (Params.deviceAddress != null) {
    $("input#deviceAddress").val(Params.deviceAddress);
  }

  $("a#testDevice").click(function () {
    const data = {
      deviceName: $("input#deviceName").val(),
      deviceAddress: $("input#deviceAddress").val(),
    };

    let url = data.deviceAddress + Params.op.status;

    $.ajax({
      url: url,
      type: "get",
      data: "",
      dataType: "json",
      async: true,
      timeout: 2000,
      success: function (response) {
        flash("Connection Success!", "success");

        $("div#configDevice_choose").css("display", "block");
        $("a#resetDevice").css("display", "table");
        $("a#testDevice").css("display", "none");
        $("a#webcamConfig").css("display", "table");
        $("input#deviceName").attr("disabled", "disabled");
        $("input#deviceAddress").attr("disabled", "disabled");
        $("p#collapseLabel_nameAndAddress").text(
          "New device's name and its network address is as below. "
        );
        if (response.curvals.torch == "off") {
          $("a#switchTorch").addClass("btn-warning");
        } else {
          $("a#switchTorch").addClass("btn-danger");
        }
      },
      error: function (err) {
        flash(
          "Connection Failed! Error Msg:<br /><br />> " + err.statusText,
          "error"
        );
        console.log(err);
      },
    });
  });

  $("a#resetDevice").click(function () {
    location.href = Urls.pages.addDevice;
  });

  $("a#refresh").click(function () {
    const data = {
      deviceName: $("input#deviceName").val(),
      deviceAddress: $("input#deviceAddress").val(),
    };
    $("div#floatLayer").show();
    $.ajax({
      url: Urls.server.calibrate,
      type: "post",
      data: data,
      dataType: "json",
      async: false,
      success: function (result) {
        img = $("img#calibration");
        src = Urls.server.getCalibrate;
        img.attr("src", src + "?r=" + new Date().getTime());
        $("div#floatLayer").hide();
        console.log(result);
        calibrateResult = result;

        flash("Refresh Success!", "success");
      },
      error: function (err) {
        $("div#floatLayer").hide();

        flash(
          "Refresh Failed! Error Msg:<br /><br />> " + err.statusText,
          "error"
        );
        console.log(err);
      },
    });
  });

  $("a#webcamConfig").click(function () {
    const data = {
      deviceName: $("input#deviceName").val(),
      deviceAddress: $("input#deviceAddress").val(),
    };
    $("div#configDevice_webcam").css("display", "block");
    $("img#videoPanel").attr("src", data.deviceAddress + Params.op.video);
  });

  $("a#closeWebcamConfig").click(function () {
    $("div#configDevice_webcam").css("display", "none");
    $("img#videoPanel").attr("src", "");
  });

  $("a#switchTorch").click(function () {
    const data = {
      deviceName: $("input#deviceName").val(),
      deviceAddress: $("input#deviceAddress").val(),
    };
    let url;
    if ($("a#switchTorch").hasClass("btn-warning")) {
      url = data.deviceAddress + Params.op.enabletorch;
      $("a#switchTorch").removeClass("btn-warning");
      $("a#switchTorch").addClass("btn-danger");
    } else {
      url = data.deviceAddress + Params.op.disabletorch;
      $("a#switchTorch").removeClass("btn-danger");
      $("a#switchTorch").addClass("btn-warning");
    }
    $.ajax({
      url: url,
      type: "get",
      async: true,
      success: function () {
        flash("Operation Success!", "success");
      },
      error: function (err) {
        flash(
          "Operation Failed! Error Msg:<br /><br />> " + err.statusText,
          "error"
        );
        console.log(err);
      },
    });
  });

  $("input#zoom").slider({
    formatter: function (value) {
      if (value == 0) {
        return;
      }
      const data = {
        deviceName: $("input#deviceName").val(),
        deviceAddress: $("input#deviceAddress").val(),
      };
      $.ajax({
        url: data.deviceAddress + Params.op.ptz.format({ zoom: value }),
        type: "get",
        data: "",
        dataType: "text",
        async: true,
        success: function () {
          $("span#zoomShow").text(value);
        },
        error: function (err) {
          console.log(err);
        },
      });
    },
  });

  $("a#saveDevice").click(function () {
    if (!calibrateResult) {
      flash("Please refresh the calibration once", "error");
      return;
    }
    const data = {
      deviceName: $("input#deviceName").val(),
      deviceAddress: $("input#deviceAddress").val(),
      minAngle: parseInt($("input#minAngle").val()),
      maxAngle: parseInt($("input#maxAngle").val()),
      minValue: parseInt($("input#minValue").val()),
      maxValue: parseInt($("input#maxValue").val()),
      unit: $("input#unit").val(),
      description: $("input#description").val(),
      x: calibrateResult.x,
      y: calibrateResult.y,
      r: calibrateResult.r,
    };

    if (
      data.minAngle >= 0 &&
      data.minAngle <= 360 &&
      data.maxAngle >= 0 &&
      data.maxAngle <= 360 &&
      data.minAngle < data.maxAngle &&
      data.minValue < data.maxValue
    ) {
      console.log(data);
      $.ajax({
        url: Urls.server.saveDevice,
        type: "post",
        data: data,
        async: false,
        success: function () {
          flash("Device saved Successfully!", "success");
          location.href = Urls.pages.manageDevice;
        },
        error: function (err) {
          flash(
            "Device saved Failed! Error Msg:<br /><br />> " + err.statusText,
            "error"
          );
          console.log(err);
        },
      });
    } else {
      flash("Your input is incorrect. Please check again.", "error");
    }
  });
});
