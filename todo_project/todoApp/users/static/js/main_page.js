

    $(".nav-link a").on("click", function(){
   $(".nav-link ").find(".active").removeClass("active");
   $(this).parent().addClass("active");


});
function fun( a,id){
//    console.log("hhhhhhhhhhhhhhhhhhhhhh")
        console.log(a,id)
        $("#note_ta").val(unescape(a))
        $("#task_no_id").text(id)
        $("#noteModal").modal('show');
    }
function load_table(){
    $.ajax(
    {
        type:"GET",
        url: "/todo1",

        success: function( json )
        {
//          console.log(json)
          var data = json.my_data
          var cols = json.my_cols
          $(".tab1").html('<table id="myTable" class="table table-bordered table-striped"><tr><th>high</th></tr></table> ')
            var table   =  $("#myTable").DataTable({
            dom: 'lBfrtip',
            buttons: [
                'csv'
            ],
             "columns":cols,
             scrollY: '55vh',
            scrollCollapse: true,
            paging: true,
             searchHighlight: true,
//                order :[[1,"asc"]],
                order :false,
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
                            if(full[10]){
                                r = full[10]+": "

                            }
                            else{
                                r = ""
                            }
                            return type === 'display'? '<div title="' + full[3] + '"><span style="color:blue">' + r+'</span>'+data : data;
                     },
                      "width": "35%"

                  },

                  {
                    "target":6,
                    "render": function (data, type, full, meta) {


                            return `<progress id="alpha" value="`+full[6]+`" max="100">`+full[6]+`</progress>`

                    }
                    }
                    ,
                  {
                    "target":9,

                     "render": function (data, type, full, meta) {
                              kk=String(full[7])

//                              kk=kk.replace(/</g, '&lt;').replace(/>/g, '&gt;')
                              if(kk){
                              kk=escape(kk)
                              }
                              else{
                                kk=escape("  -  ")
                              }
                             return '<a class="btn btn-info btn-sm" href=/delete_task/' + full[0] + '/>' + 'Delete' + '</a>&nbsp;<a class="btn btn-info btn-sm" href=/completed_task/' + full[0] + '>' + 'finished' + '</a>&nbsp;<button class="btn btn-info btn-sm" onClick="fun(`'+kk+'`,'+full[0]+')" >' + 'note' + '</button>';
                     }
                   },

                 { "target": 7, "visible": false},
                 { "target":8,
                  "render": function (data, type, full, meta) {

                    if (full[8]=="High"){

                            return(`<i class="fa-solid fa-star"></i><i class="fa-solid fa-star"></i><i class="fa-solid fa-star"></i>`)
                    }
                     else if(full[8]=="Medium"){
                        return(`<i class="fa-solid fa-star"></i><i class="fa-solid fa-star"></i>`)
                     }
                     else if(full[8]=="Low"){

                        return(`<i class="fa-solid fa-star"></i>`)

                     }
                     else{
                        return full[8]
                     }
                     },


                 },

                  { "target": 10, "visible": false},

                ]
            })
             $('#myTable').on('draw.dt', function () {
                    $('[data-toggle="tooltip"]').tooltip();



                });






        }
     })
     }
$(function(){

    $("#save_note").click(function(){
        console.log("-----------------------")
        $.ajax({
                        method:'POST',
                        url:'/update_note/',
                           contentType: 'application/json; charset=utf-8',
                        data:JSON.stringify({
                        id:$("#task_no_id").text(),
                        note:$("#note_ta").val(),

                    }),
                    dataType: 'json',
                    success: function(data) {
                    if(data.success){

//                                alert(data.success)
                                $("#noteModal").modal('hide');
                                alert('Data Successfully Posted');
                                      location.reload(true);
                            }
                     else{
                       alert(data.reason);
//
//
                     }
                    },
                    });





    })


//    let url = "{% url 'users:homepage1' %}";
   load_table()
   var choices = ["Not_Yet_Started","Started","Interrupted","Completed"]
   var priority_choices = ['','High', 'Medium', 'Low']
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

                                    order :false,
                                    "data":data,
                                    "columns":cols,
                                    scrollY: '55vh',
                                    scrollCollapse: true,
                                    paging: true,
                                     searchHighlight: true,
                        //                order :[[1,"asc"]],
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
                                          "width": 315,
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
                                        "target":9,

                                         "render": function (data, type, full, meta) {
//                                                 console.log("btn")
                                                 return `<a class="btn btn-info btn-sm" href=/delete_task/` + full[0] + `/>` + `Delete` + `</a>&nbsp;<a class="btn btn-info btn-sm" href=/completed_task/` + full[0] + `>` + `finished` + `</a>&nbsp;<button class="btn btn-info btn-sm save_btn" id ="` + full[0] + `">` + `Save` + `</button>`;
                                         }


                                                          },
                                      { "target": 7, "visible": false},
                                      { "target": 8,

                                        "render": function (data, type, full, meta) {
                                             console.log(full[8])
                                            html_stmt = `<select id="priority_`+full[0]+`">`

                                            for (i of priority_choices){
//                                                console.log(i,full[10])

                                                if (full[8]  && (full[8] == i)){
                                                html_stmt+=`<option value="`+i+`" selected>`+i+`</option>`
                                                }
                                                else{
                                                     html_stmt+=`<option value="`+i+`">`+i+`</option>`
                                                }


                                            }
                                            return html_stmt



                                      }


                                      },
                                      { "target": 10, "visible": false},




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
                        percentage:$("#percentage_"+id).val(),
                        priority :$("#priority_"+id).val()
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