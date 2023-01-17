

$(function(){


    let url = "{% url 'users:homepage1' %}";


       $.ajax(
    {
        type:"GET",
        url: "/todo1",

        success: function( json )
        {
          console.log(json)
          var data = json.my_data
          var cols = json.my_cols
          $(".tab1").html('<table id="myTable" class="table table-bordered table-striped"><tr><th>high</th></tr></table> ')
            $("#myTable").DataTable({
                order :[[1,"asc"]],
                "data":data,
                "columns":cols,
                "columnDefs":[
                 { "targets": [3], "visible": false},
                {

                    "target":0,
                    "serchable":true,
                    "orderable":false

                    },

                    { "width": 20, "target": 1 },
                    { "width": 20, "target": 4 },

                  {
                  "target": 2,
                     "render": function (data, type, full, meta) {
                            return type === 'display'? '<div title="' + full.comments + '">' + data : data;
                     },
                      "width": 500

                  },
                  {
                    "target":7,
                     "render": function (data, type, full, meta) {
                             return `<a class="btn btn-info btn-sm" href=/delete_task/` + full[0] + `/>` + `Delete` + `</a>&nbsp;<a class="btn btn-info btn-sm" href=/completed_task/` + full[0] + `>` + `finished` + `</a>`;
                     }


                                      }

                ]
            })
             $('#myTable').on('draw.dt', function () {
                    $('[data-toggle="tooltip"]').tooltip();
                });
        }
     })
})