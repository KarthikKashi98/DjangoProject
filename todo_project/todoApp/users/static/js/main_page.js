

    $(".nav-link a").on("click", function(){
   $(".nav-link ").find(".active").removeClass("active");
   $(this).parent().addClass("active");


});

function load_table(){
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
                            return type === 'display'? '<div title="' + full[3] + '">' + data : data;
                     },
                      "width": 500

                  },

                  {
                    "target":6,
                    "render": function (data, type, full, meta) {


                            return `<progress id="alpha" value="`+full[6]+`" max="100">`+full[6]+`</progress>`

                    }
                    }
                    ,
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
     }
$(function(){


//    let url = "{% url 'users:homepage1' %}";
        load_table()


   var choices = ["Not_Yet_Started","Started","Interrupted","Completed"]

     $("#task_to_do_edit_btn").on("click",function(){

//          alert(this.text)
        if ($("#task_to_do_edit_btn").text()=="Edit mode"){


                $("#task_to_do_edit_btn").text("Exit Edit mode")
                 $.ajax(
                        {
                            type:"GET",
                            url: "/todo1",

                            success: function( json )
                            {
//                              console.log(json)
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

//                                      {
//                                      "target": 2,
//                                         "render": function (data, type, full, meta) {
//                                                return type === 'display'? '<div title="' + full[3] + '">' + data : data;
//                                         },
//                                          "width": 500
//
//                                      },

                                      {
                                            "target":4,
                                             "render": function (data, type, full, meta) {
//                                                console.log(full[4])
                                                return `<input type="date" value= ${full[4]} id="target_date_`+full[0]+`" >`


                                             }

                                      },

                                      {
                                        "target":5,
                                        "render": function (data, type, full, meta) {

                                            html_stmt = `<select id="status_`+full[0]+`">`
                                            for (i of choices){
//                                                console.log(i)
                                                if (full[5] == i){
                                                html_stmt+=`<option value="`+i+`" selected>`+i+`</option>`
                                                }
                                                else{
                                                     html_stmt+=`<option value="`+i+`">`+i+`</option>`
                                                }


                                            }
                                            return html_stmt



//
//                                                return `<input type="number" value="`+full[6]+`" id="percentage_`+full[0]+`" max=100 min=0>`
//
////                                                return `<progress id="alpha" value="`+full[6]+`" max="100">`+full[6]+`</progress>`

                                        }
                                        },
                                        {
                                        "target":2,
                                          "width": 500,
                                        "render": function (data, type, full, meta) {

                                                return `<textarea id = "task_description_${full[0]}"  style="width:100%; height:30px;" >${full[2]}</textarea>`

//                                                return `<progress id="alpha" value="`+full[6]+`" max="100">`+full[6]+`</progress>`

                                        }
                                        },
                                      {
                                        "target":6,
                                        "render": function (data, type, full, meta) {
                                                return `<input type="number" value="`+full[6]+`" id="percentage_`+full[0]+`" max=100 min=0>`

//                                                return `<progress id="alpha" value="`+full[6]+`" max="100">`+full[6]+`</progress>`

                                        }
                                        }
                                        ,
                                      {
                                        "target":7,

                                         "render": function (data, type, full, meta) {
                                                 console.log("btn")
                                                 return `<a class="btn btn-info btn-sm" href=/delete_task/` + full[0] + `/>` + `Delete` + `</a>&nbsp;<a class="btn btn-info btn-sm" href=/completed_task/` + full[0] + `>` + `finished` + `</a>&nbsp;<button class="btn btn-info btn-sm save_btn" id ="` + full[0] + `">` + `Save` + `</button>`;
                                         }


                                                          }

                                    ]
                                })
                                 $('#myTable').on('draw.dt', function () {
                                        $('[data-toggle="tooltip"]').tooltip();
                                    });
                            }
                         })


              }

         else{
                    $("#task_to_do_edit_btn").text("Edit mode") ;
                      load_table()


             }



     })


})

$(document).ready(function() {
            $("input").focusout(function() {
                if($(this).val()=='') {
                    $(this).css('border', 'solid 2px red');
                }
                else {

                    // If it is not blank.
                    $(this).css('border', 'solid 2px green');
                }
            }) .trigger("focusout");


            $('.tab1').on("click",".save_btn",function(e) {



                    var id = $(e.target).attr("id")
                    $.ajax({
                        method:'POST',
                        url:'/save_edit/',
                           contentType: 'application/json; charset=utf-8',
                        data:JSON.stringify({
                        id:id,
                        status:$("#status_"+id).val(),
                        task_description:$("#task_description_"+id).val(),
                        target_date:$("#target_date_"+id).val(),
                        status:$("#status_"+id).val(),
                        percentage:$("#percentage_"+id).val()
                    }),
                    dataType: 'json',
                    success: function(data) {
                    if(data.success){
//                                alert(data.success)
                                alert('Data Successfully Posted');
                                 document.location.href = '/todo/';
                            }
                     else{
                       alert(data.reason);
//
//
                     }
                    },
                    });



                });






        });







//jQuery(function($){
//
//$('button').click("#save_btn_4",function() {
//    alert("jhgjhjghj")
//});


//const onClick = (event) => {
//  if (event.target.nodeName === 'BUTTON') {
//    console.log(event.target.id);
//  }
//}
//window.addEventListener('click', onClick);



