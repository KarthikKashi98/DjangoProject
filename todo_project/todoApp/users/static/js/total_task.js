
$(function(){

       $.ajax(
    {
        type:"POST",
        url: "/total_tasks/",

        success: function( json )
        {
          console.log(json)
          var data = json.my_data
          var cols = json.my_cols
          $(".tab2").html('<table id="myTable1" class="table table-bordered table-striped"><tr><th>high</th></tr></table> ')
            $("#myTable1").DataTable({
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
                    "target":7,
                     "render": function (data, type, full, meta) {
                            if (full[5] =="Completed"){
                                 return `<a class="btn btn-info btn-sm" href=/delete_task/` + full[0] + `/>` + `Delete` + `</a>&nbsp; <a class="btn btn-info btn-sm" href=/revert_task/` + full[0] + `>` + `Revert` + `</a>`;

                             }

                             else{
                                        return `<a class="btn btn-info btn-sm" href=/delete_task/` + full[0] + `/>` + `Delete` + `</a>&nbsp;<a class="btn btn-info btn-sm" href=/completed_task/` + full[0] + `>` + `finished` + `</a>`;

                             }



                          }
                     }




                ]
            })
             $('#myTable1').on('draw.dt', function () {
                    $('[data-toggle="tooltip"]').tooltip();
                });
        }
     })


})

