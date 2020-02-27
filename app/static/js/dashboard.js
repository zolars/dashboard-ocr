$(document).ready(function() {
  console.log("Params", Params);
  console.log("Urls", Urls);

  let charts = {};
  items = Params.deviceItems;

  for (const [key, value] of Object.entries(items)) {
    charts[value.id] = echarts.init(
      document.getElementById("chartFor" + value.id),
      "white",
      {
        renderer: "canvas"
      }
    );
  }

  function fetchData() {
    for (const [key, value] of Object.entries(items)) {
      let data = { id: value.id };
      $.ajax({
        type: "GET",
        url: Urls.server.data,
        data: data,
        dataType: "json",
        success: function(result) {
          console.log(result);
          // chart.setOption(result["chart"]);
        },
        error: function(err) {
          console.log(err.textStatus);
        }
      });
    }
  }

  $(function() {
    fetchData(false);
    setInterval(fetchData, 5000);
  });
});
