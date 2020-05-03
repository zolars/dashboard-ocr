$(document).ready(function() {
  console.log("Params", Params);
  console.log("Urls", Urls);

  $(".card-body").each(function() {
    var R = Math.floor(Math.random() * 255);
    var G = Math.floor(Math.random() * 255);
    var B = Math.floor(Math.random() * 255);
    $(this).css("background-color", "rgb(" + R + "," + G + "," + B + ", 20%)");
  });

  $("a[name='delete']").click(function() {
    var device_id = $(this)[0].id.split("For")[1];
    data = { device_id: device_id };
    $.ajax({
      url: Urls.server.deleteDevice,
      type: "post",
      data: data,
      async: false,
      success: function() {
        flash("Device deleted Successfully!", "success");
        location.href = Urls.pages.manageDevice;
      },
      error: function(err) {
        flash(
          "Device deleted Failed! Error Msg:<br /><br />> " + err.statusText,
          "error"
        );
        console.log(err);
      },
    });
  });
});
