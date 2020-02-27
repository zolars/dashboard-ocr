$(document).ready(function() {
  console.log("Params", Params);
  console.log("Urls", Urls);

  $(".card-body").each(function() {
    var R = Math.floor(Math.random() * 255);
    var G = Math.floor(Math.random() * 255);
    var B = Math.floor(Math.random() * 255);
    $(this).css("background-color", "rgb(" + R + "," + G + "," + B + ", 20%)");
  });
});
