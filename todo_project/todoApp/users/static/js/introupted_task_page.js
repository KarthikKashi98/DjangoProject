var priority_choices = ['','High', 'Medium', 'Low']

function fun( a,id){
//    console.log("hhhhhhhhhhhhhhhhhhhhhh")
        console.log(a,id)
        $("#note_ta").val(unescape(a))
        $("#task_no_id").text(id)
        $("#noteModal").modal('show');
    }
$(function(){

       $.ajax(
    {
        type:"POST",
        url: "/interrupted_tasks/",

        success: function( json )
        {
          console.log(json)
          var data = json.my_data
          var cols = json.my_cols
          $(".tab6").html('<table id="myTable5" class="table table-bordered table-striped"><tr><th>high</th></tr></table> ')
            $("#myTable5").DataTable({
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
                      "width": 430

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
                              kk=String(full[9])
                              kk=escape(kk)
//                              console.log(kk)
                             return '<a class="btn btn-info btn-sm" href=/delete_task/' + full[0] + '/>' + 'Delete'+ '</a>&nbsp;<a class="btn btn-info btn-sm" href=/revert_task/' + full[0] + '>' + 'Revert'+ '</a>&nbsp;<button class="btn btn-info btn-sm" onClick="fun(`'+kk+'`,'+full[0]+')" >' + 'note' + '</button>';
                     }
//                    "render": function (data, type, full, meta) {
//                              kk=String(full[7])
//                              console.log(kk)
//                             return '<a class="btn btn-info btn-sm" href=/delete_task/' + full[0] + '/>' + 'Delete' + '</a>&nbsp;<a class="btn btn-info btn-sm" href=/completed_task/' + full[0] + '>' + 'finished' + '</a>&nbsp;<button class="btn btn-info btn-sm" onClick="fun(`'+kk+'`,'+full[0]+')" >' + 'note' + '</button>';
//                     }
//
    
                                      },
                   { "targets": [9], "visible": false},
                   { "target": 10,
                    "render": function (data, type, full, meta) {
                    console.log(full[10])
                    if (full[10]=="High"){
                            return(`<i class="fa-solid fa-star"></i><i class="fa-solid fa-star"></i><i class="fa-solid fa-star"></i>`)
                    }
                     else if(full[10]=="Medium"){
                        return(`<i class="fa-solid fa-star"></i><i class="fa-solid fa-star"></i>`)
                     }
                     else if(full[10]=="Low"){

                        return(`<i class="fa-solid fa-star"></i>`)

                     }
                     else{
                        return full[10]
                     }




                                      }
                                      },

                ]
            })
             $('#myTable5').on('draw.dt', function () {
                    $('[data-toggle="tooltip"]').tooltip();
                });
        }
     })


})