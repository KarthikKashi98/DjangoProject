
$(function(){

       $.ajax(
    {
        type:"POST",
        url: "/completed_tasks/",

        success: function( json )
        {
          console.log(json)
          var data = json.my_data
          var cols = json.my_cols
          $(".tab4").html('<table id="myTable4" class="table table-bordered table-striped"><tr><th>high</th></tr></table> ')
            $("#myTable4").DataTable({
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
                     console.log(full)
                            return type === 'display'? '<div title="' + full[3] + '">' + data : data;
                     },
                      "width": 470

                  },
                   {
                    "target":6,
                    "render": function (data, type, full, meta) {
                    return `<progress id="alpha" value="`+full[6]+`" max="100">`+full[6]+`</progress>`

                    }
                    },

                  {
                    "target":8,
                     "render": function (data, type, full, meta) {
                             return `<a class="btn btn-info btn-sm" href=/delete_task/` + full[0] + `/>` + `Delete` + `</a>&nbsp;<a class="btn btn-info btn-sm" href=/revert_task/` + full[0] + `>` + `Revert` + `</a>`;
                     }


                                      }

                ]
            })
             $('#myTable4').on('draw.dt', function () {
                    $('[data-toggle="tooltip"]').tooltip();
                });
        }
     })


})