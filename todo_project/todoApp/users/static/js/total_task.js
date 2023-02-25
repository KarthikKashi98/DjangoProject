
$(function(){
    $(".buttons-excel").html('Download')
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
                 dom: 'Bfrtip',
                    buttons: [
                     'excel'
                    ],

                "bJQueryUI":true,
                  "bSort":false,
                  "bPaginate":true,
                  "sPaginationType":"full_numbers",
                   "iDisplayLength": 10,
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
                        console.log(full[3],type)
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
                            if (full[5] =="Completed"){
                                 return `<a class="btn btn-info btn-sm" href=/delete_task/` + full[0] + `/>` + `Delete` + `</a>&nbsp; <a class="btn btn-info btn-sm" href=/revert_task/` + full[0] + `>` + `Revert` + `</a>`;

                             }

                             else{
                                        return `<a class="btn btn-info btn-sm" href=/delete_task/` + full[0] + `/>` + `Delete` + `</a>&nbsp;<a class="btn btn-info btn-sm" href=/completed_task/` + full[0] + `>` + `finished` + `</a>`;

                             }



                          }
                     },
                      { "targets": [7], "visible": false},
                      { "target":9,
                  "render": function (data, type, full, meta) {
                    if (full[9]=="High"){
                            return(`<i class="fa-solid fa-star"></i><i class="fa-solid fa-star"></i><i class="fa-solid fa-star"></i>`)
                    }
                     else if(full[9]=="Medium"){
                        return(`<i class="fa-solid fa-star"></i><i class="fa-solid fa-star"></i>`)
                     }
                     else if(full[9]=="Low"){

                        return(`<i class="fa-solid fa-star"></i>`)

                     }
                     else{
                        return full[9]
                     }
                     },


                 }




                ]
            })
             $('#myTable1').on('draw.dt', function () {
                    $('[data-toggle="tooltip"]').tooltip();
                });
        }
     })


})


    $(document).ready(function () {
   $(function(){
    var current = location.pathname;
    $('#nav li a').each(function(){
        var $this = $(this);
        // if the current path is like this link, make it active
        if($this.attr('href').indexOf(current) !== -1){
            $this.addClass('active');
        }
    })
})
    });
