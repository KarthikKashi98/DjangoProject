
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
function getCSRFToken() {
var cookieValue = null;
if (document.cookie && document.cookie != '') {
    var cookies = document.cookie.split(';');
        for (var i1 = 0; i1 < cookies.length; i1++) {
            var cookie = jQuery.trim(cookies[i1]);
                if (cookie.substring(0, 10) == ('csrftoken' + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(10));
                            break;
                            }
                            }
                            }
                            return cookieValue;
                }


function csrfSafeMethod(method) {
                        // these HTTP methods do not require CSRF protection
                            return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
                            }
//function group_task_page(member_id,member_name){
//
//
//                    csrf_token = getCSRFToken()
//                    $.ajax({
//                            method:'POST',
//                            url:'/manage_group/members_task/',
//
//                            data: JSON.stringify({
//                                'member_name':member_name,
//                               "member_id":member_id,
//
//                                'csrfmiddlewaretoken': csrf_token,
//                                }),
//                            beforeSend: function(xhr, settings) {
//                                if (!csrfSafeMethod(settings.type)) {
//                                xhr.setRequestHeader("X-CSRFToken", csrf_token);
//                                }
//                                },
//
//
//                            success: function(response) {
//
////                                     var newWindow = window.open('/manage_group/members_task/');
//                            var newWindow = window.open();
//                            newWindow.document.write(response.html);
//                              $(newWindow).on("load", function() {
//                                    setTimeout(function() {
//                                        // Put your JavaScript code here
//                                        console.log("jQuery is working in the new window");
//                                    }, 100);
//                                });
////
//
//
//                                },
//
//                            error: function(jqXHR, textStatus, errorThrown) {
//                                    console.log('Error:', error);
//                                  }
//                            })
//
//
//
//
//
//}

function fun(){
//    console.log("hhhhhhhhhhhhhhhhhhhhhh")


        $("#add_member_model").modal('show');
    }





$(document).ready(function(){


function get_group_info(){


              $.ajax({
                            method:'GET',
                            url:'/manage_group/get_group/',
                          contentType: 'application/json; charset=utf-8',
                        dataType: 'json',

                        success: function(data) {
                                const a=  JSON.stringify(data)

                                sessionStorage.current_user_group_info = JSON.stringify(data);
//                                assign_the_task()
//                                alert(data["group_info"])

                        },
                         error:function(err) {
                                console.log('Oh noooo!!');
                                console.log(err);
                              }
                        });

   }



//if (typeof sessionStorage.current_user_group_info == 'undefined') {
//
//        get_group_info().then(
//
//            alert("page_reloaded",sessionStorage.current_user_group_info)
//        )
//
//}
//else{
//
////                        sessionStorage.removeItem(current_user_group_info);
//        get_group_info().then(
//              alert("page_reloaded",sessionStorage.current_user_group_info)
//         )
////                        alert("page_reloaded")
//
//}
get_group_info()
var name; // global variable that keeps the name
new Autocomplete('#autocomplete1', {
search: input => {
const url = `/search/?name=${input}`;
return new Promise(resolve => {
fetch(url).then(response => response.json()).then(data => {
    resolve(data.name);
})
})
},

onSubmit: result => {
name = result; //pass clicked result to global

li = []
$("#container .name").each(function(i,obj){console.log(i,$(obj).text().trim());li.push($(obj).text().trim())})

if(li.includes(name)){

alert("person is already exist")

}
else{
sessionStorage.creating_member_name = name;
$("#select_memb1").text(`



        ${name}


`)

}

}
})
$('#ull').click(function (e) {

$.ajax({
url: '',
type: 'GET',
data: {
valname: name,
},
success: function (response) {
//                window.location = response.urlLink;
}
})

})

$("#add_member").on("click",function(){
if(sessionStorage.current_user_group_info==undefined){
    get_group_info()
}
username = sessionStorage.creating_member_name;
group_id =  sessionStorage.current_group_id;

data=JSON.stringify({
    "username":username,
    "group_id":group_id
})



$.ajax({
    method:'POST',
    url:'/manage_group/members/create/',
       contentType: 'application/json; charset=utf-8',
    data:data,
    dataType: 'json',
    success: function(data) {

       if(data.success){
            alert("successful")
              $("#add_member_model").modal('hide');
            manage_group_lay_out()


       }
        }
    })







})



const members_list = (id,from) => {
data =get_group_info()

$.ajax({
method:'GET',
url:'/manage_group/members/'+id,
contentType: 'application/json; charset=utf-8',
dataType: 'json',
success: function(data) {
   category =   ` <div><b>group_members-${data.group_name}</b> <div class="row">`
   console.log(data.group_members)
   console.log(data["group_members"].length)
    if(from=="from_group_manager"){
    category +=  `<div class="col-3 card" style = "min-height:100px;font-weight:bold;display: grid; place-items: center; ">`

            category += `<span style="font-weight:bold;display: grid; place-items: center; "><a href="#" onclick="fun()"><i class="fas fa-plus"></i></a></span>`

            category += `</div>`
            }

    sessionStorage.current_group_id= data["group_id"];
    for (let i = 0; i <  data["group_members"].length; i++) {
            category +=  `<div class="col-3 card" style = "min-height:100px">`
            category += `<span style="font-weight:bold">${data["group_members"][i]["member_name"]}</span>`
            category += `<span style="">(${data["group_members"][i]["designation"]})</span>`

            if ((data["group_members"][i]["designation"]=="Member") && (from=="from_group_manager")){
                category += `<hr>`
                category+=`<div>`
                category+= `<span style="display:inline-block"><a href="/manage_group/members/delete/${data['group_members'][i]['id']}" onclick="return confirm('Are you sure you want to delete the member?')" style="font-size:13px;display:inline-block"> Delete </a></span>&nbsp;|&nbsp;<span style="display:inline-block"><a href="/manage_group/members_task/${data['group_members'][i]['id']}" style="font-size:13px;display:inline-block"  target="_blank">AssignedTask</a></span>`
                category+=`</div>`
            }
            category += `</div>`
            }
     category += `</div>`
    $(".dashboard_group").html(category)





    },
  error:function(err) {
        console.log('Oh noooo!!');
        console.log(err);
      }
})


};



function create_group_layout(){

category =  `<div>
                <b>Create Group</b>
                <hr>
                <div class="row">
                    <div class="col-7" style="border-right:1px solid yellow">


                        <div style="text-align:left;padding:3px"> Enter the group name: &nbsp;<input id="create_group_name" type="text">
                        </div>
                        <br>
                        <br>
                        <div style="text-align:left;padding:3px;border :1px solid black;width:100%;height:200px;overflow:auto" id="select_memb">


                        </div>
                        <br>
                        <br>
                        <button class="btn btn-primary" style="float:right" id="grp_create_btn">Create</button>
                    </div>
                    <div class="col-4">

                        <!--<label for="groups">select your group</label>-->
                        <!--<select name="groups" id="groups" style="min-width:100%">-->

                        <!--<option value=""></option>-->



                        <!--</select>-->

                        <div id="autocomplete" class="autocomplete" style="width:100%; margin:40px auto;">
                            <input class="autocomplete-input" />
                            <ul id="ull" class="autocomplete-result-list" style="color:red;"></ul>
                        </div>

                    </div>
                </div>
</div>`


$(".dashboard_group").html(category)




var name; // global variable that keeps the name
new Autocomplete('#autocomplete', {
    search: input => {
        const url = `/search/?name=${input}`;
        return new Promise(resolve => {
            fetch(url).then(response => response.json()).then(data => {
                resolve(data.name);
            })
        })
    },

    onSubmit: result => {
        name = result; //pass clicked result to global

        li = []
        $("#container .name").each(function(i,obj){console.log(i,$(obj).text().trim());li.push($(obj).text().trim())})

        if(li.includes(name)){

        alert("person is already exist")

        }
        else{
        $("#select_memb").append(`


         <div id="container">
                <button id="x">x</button>
                <div class="name">
                    ${name}
                </div>
         </div>


        `)

        }

    }
})
$('#ull').click(function (e) {

    $.ajax({
        url: '',
        type: 'GET',
        data: {
            valname: name,
        },
        success: function (response) {
//                window.location = response.urlLink;
        }
    })

})


function registerClickHandler() {
// Implement the click handler here for button of class 'remove'
$('#select_memb').on("click","#x",function() {
$(this).parent().remove();
});
}

registerClickHandler();
$('button').click("#grp_create_btn",function() {


list_group_member = $(".name")
li1=[]
list_group_member.each(function(idx, li) {
console.log("------->",li)
li1.push($(li).text().trim())
});
data=JSON.stringify({
"group_name":$("#create_group_name").val(),
"list_group_member":li1
})



$.ajax({
method:'POST',
url:'/create_group/',
contentType: 'application/json; charset=utf-8',
data:data,
dataType: 'json',
success: function(data) {

if(data.success){
get_group_info()
alert("group is created successfully")
manage_group_lay_out()


}
}
})

})




}

function manage_group_lay_out(){

data = JSON.parse(sessionStorage.current_user_group_info)



category =   ` <div><b>Manage your groups</b> <div class="row">`

for (let i = 0; i <  data["group_info"].length; i++) {
category +=  `<div class="col-3 card" style = "min-height:100px">`
category += `<span style="font-weight:bold">${data["group_info"][i]["group_name"]}</span>`
category += `<hr>`
category+= `<span style="display:inline-block">Members: &nbsp;<span style="font-weight:bold"><a id="${data['group_info'][i]['id']}"  class="member_list_call" href ="#" >${data["group_info"][i]["members"].length}</a></span></span>`
category+=`<a href="/manage_group/group_task/${data['group_info'][i]['id']}" style="color: #ffffff;margin-top: 10px;font-size: 13px;" target="_blank">Total Task </a>`
category += `</div>`
}
category+=`</div></div>`
$(".dashboard_group").html(category)

}


function view_group_lay_out(){


$.ajax({
method:'GET',
url:'/manage_group/view_other_group/',
contentType: 'application/json; charset=utf-8',
dataType: 'json',
success: function(data) {
//alert("success")
    category =   ` <div><b>view your groups</b> <div class="row">`
          for (let i = 0; i <  data["group_info"].length; i++) {

                category +=  `<div class="col-3 card" style = "min-height:100px">`
                category += `<span style="font-weight:bold">${data["group_info"][i]["group_name"]}</span>`
                category += `<hr>`
                category+= `members:<span style="font-weight:bold"><a id="${data['group_info'][i]['id']}"  class="member_list_call1" href ="#" >${data["group_info"][i]["count_members"]}</a></span>`
                category += `</div>`
                }
     category+=`</div></div>`
    $(".dashboard_group").html(category)





    },
  error:function(err) {
        console.log('Oh noooo!!');
        console.log(err);
      }
})

}
function assign_the_task(){

let result;

//         get_group_info()
data = JSON.parse(sessionStorage.current_user_group_info);

console.log(data)

let category1 =  `<div><b>Assign Task</b><br><br>

        <div class="row" style="margin-top:2px">
            <div class="col-2">* Task :</div>
              <div class="col-8"><textarea rows="3"  style="width: 100%;" id= "task_desc"></textarea></div>
         </div>

         <div class="row" style="margin-top:2px">
            <div class="col-2">Comments:</div>
              <div class="col-8"><textarea rows="1"  style="width: 100%;" id = "task_comments"></textarea></div>
         </div>
         <div class="row" style="margin-top:2px">
            <div class="col-2">Target Date</div>
              <div class="col-8" style="text-align:left;min-width:180px"><input type="date" name="dto" id="task_target_date"></div>
         </div>
         <div class="row"  style="margin-top:4px">
            <div class="col-2">status</div>
              <div class="col-8" style="text-align:left">
                        <select name="Task status" id="task_status" style="min-width:180px">
                          <option value="Not_Yet_Started">Not_Yet_Started</option>
                          <option value="Started">Started</option>
                          <option value="Interrupted">Interrupted</option>
                          <option value="Completed">Completed</option>
                        </select>

              </div>
         </div>

         <div class="row" style="margin-top:4px">
            <div class="col-2">Note:</div>
              <div class="col-8"><textarea rows="1"  style="width: 100%;" id="task_note"></textarea></div>
         </div>

         <div class="row" style="margin-top:4px">
            <div class="col-2">Priority:</div>
              <div class="col-8" style="text-align:left">
                        <select name="Task priority" id="task_priority" style="min-width:180px">
                          <option value="">Select Priority</option>
                          <option value="Low">Low</option>
                          <option value="High">High</option>
                          <option value="Medium">Medium</option>
                        </select>

              </div>
         </div>

         <div class="row" style="margin-top:4px">
            <div class="col-2">*Select Group:</div>
              <div class="col-3" style="text-align:left">
                        <select name="group_name" id="task_group_name" style="min-width:180px">`


groups=[]

category2=`<option value="">Select your group</option>`
for (let i = 0; i <  data["group_info"].length; i++) {
    console.log("kjnkj")
    groups.push(data["group_info"][i]["group_name"])
    category2 = category2 + `<option value="${data['group_info'][i]['group_name']}">${data['group_info'][i]['group_name']}</option>`

}

category3=`</select>
              </div>

               <div class="col-2">*Select name:</div>
              <div class="col-3" style="text-align:left">
                        <select name="member_name" id="task_member_name" style="min-width:180px">


                        </select>

              </div>
         </div>
          <div class="row" style="margin-top:4px">
            <div class="col-10" style="align:right">
          <button class="btn btn-sm btn-primary"  style="width:auto;float:right" id = "Group_Add_Task"> Add task </button>
          </div>
          </div>
          </div>`
$(".dashboard_group").html(category1+category2+category3)


}



function delete_group_lay_out(){





$.ajax({
            method:'GET',
            url:'/manage_group/get_group/',
          contentType: 'application/json; charset=utf-8',
        dataType: 'json',
        success: function(data) {
         category =   ` <div><b>Your group members</b><div class="row">`

        for (let i = 0; i <  data["group_info"].length; i++) {
            category +=  `<div class="col-3 card" style = "min-height:100px">`
            category += `<span style="font-weight:bold">${data["group_info"][i]["group_name"]}</span>`
            category += `<hr>`
            category+= `<a href="/manage_group/delete_group/${data['group_info'][i]['id']}" onclick="return confirm('Are you sure you want to delete this?')"> Delete </a>`
            category += `</div>`
        }
             category+=`</div></div>`
            $(".dashboard_group").html(category)




            },
          error:function(err) {
                console.log('Oh noooo!!');
                console.log(err);
              }
        })




}

$.ajax({
            method:'POST',
            url:'/dashboard/',
               contentType: 'application/json; charset=utf-8',
            data:JSON.stringify({
            'id':1,

                  }),
        dataType: 'json',
        success: function(data) {

            $("#total_count").text(data.total_count)
            $("#uncompleted_count").text(data.incomplete_task)
            $("#Completed_count").text(data.completed_task)
            $("#interrupted_task").text(data.interrupted_task)
//            var data1 = {{ data.graph_data|safe }};
              var graph_data = JSON.parse(data.graph_data);
//
            var data = [{
              values: [data.incomplete_task, data.interrupted_task, data.completed_task],
              labels: ['incomplete_task', 'interrupted_task', 'completed_task'],
              type: 'pie'
            }];

            var layout = {
//              height: 400,
//              width: 500,
             paper_bgcolor:'rgba(0,0,0,0)',
             plot_bgcolor:'rgba(0,0,0,0)'
            };

            Plotly.newPlot('dashboard_group', data, layout);






            }
        })


//    members_list(2)
    $(".manage").on("click",function(){manage_group_lay_out()});
    $(".create").on("click",function(){create_group_layout()});
    $(".delete").on("click",function(){delete_group_lay_out()});
    $(".assign_task").on("click",function(){assign_the_task()});
    $(".view_groups").on("click",function(){view_group_lay_out()});
    $(".dashboard_group").on("click",".member_list_call",function(){members_list($(this).attr("id"),"from_group_manager")});
    $(".dashboard_group").on("click",".member_list_call1",function(){members_list($(this).attr("id"),"from_group_member")});

    $(".dashboard_group").on("click","#Group_Add_Task",function(){
           task1=$("#task_desc").val()
           comments1 =$("#task_comments").val()
           note1 = $("#task_note").val()
           target_date1 = $("#task_target_date").val()
           status1 = $("#task_status").val()

           priority1 = $("#task_priority").val()
           group_name1 = $("#task_group_name").val()
           member_name1 = $("#task_member_name").val()


           if( task1=="" || group_name1=="" ||  priority1==""){
                    alert("fill the mandatory values")


                    }

            else{

//                data=

                    console.log(task1,comments1,note1,target_date1,status1,group_name1,member_name1)

                        function getCSRFToken() {
                            var cookieValue = null;
                            if (document.cookie && document.cookie != '') {
                                var cookies = document.cookie.split(';');
                                    for (var i1 = 0; i1 < cookies.length; i1++) {
                                        var cookie = jQuery.trim(cookies[i1]);
                                            if (cookie.substring(0, 10) == ('csrftoken' + '=')) {
                                                    cookieValue = decodeURIComponent(cookie.substring(10));
                                                        break;
                                                        }
                                                        }
                                                        }
                                                        return cookieValue;
                                            }


                         function csrfSafeMethod(method) {
                            // these HTTP methods do not require CSRF protection
                                return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));}
                        csrf_token = getCSRFToken()
                    $.ajax({
                            method:'POST',
                            url:'/manage_group/add_task_from_group/',

                            data: JSON.stringify({
                                'task1':$("#task_desc").val(),
                               'comments1' :$("#task_comments").val(),
                               'note1' : $("#task_note").val(),
                               'target_date1' : $("#task_target_date").val(),
                               'status1' : $("#task_status").val(),

                               'priority1' : $("#task_priority").val(),
                               'group_name1' : $("#task_group_name").val(),
                               'member_name1' : $("#task_member_name").val(),
                                'csrfmiddlewaretoken': csrf_token,
                                }),
                            beforeSend: function(xhr, settings) {
                                if (!csrfSafeMethod(settings.type)) {
                                xhr.setRequestHeader("X-CSRFToken", csrf_token);
                                }
                                },


                            success: function(data) {

                                if(data.success){

                                  alert("successfully assigned the task ");
                                   manage_group_lay_out()
                                  }
                               else{

                                   alert(data.reason);
            //
            //
                                 }


                                },

                            error: function(jqXHR, textStatus, errorThrown) {
                                    console.log('Error:', error);
                                  }
                            })


            }





           if($("#task_comments").val()){



           }

    })



})



$(document).ready(function(){

data = JSON.parse(sessionStorage.current_user_group_info);

$(".dashboard_group").on("change","#task_group_name",function(){

        console.log($("#task_group_name").val())
        data = JSON.parse(sessionStorage.current_user_group_info)
        members = data["group_info"]
        for(let i=0;i<data["group_info"].length;i++){
            if(data["group_info"][i]["group_name"] == $("#task_group_name").val()){
                members=data["group_info"][i]["members"]
                break
            }
        }


      // Select the select element
      var selectElement = $('#task_member_name');
       selectElement.html("<option value=''>select member </option>")


      // Loop over the options array and append new option elements to the select element
      $.each(members, function(index, value) {
        var newOption = $('<option>', {
          value: value,
          text: value
        });
        selectElement.append(newOption);
      });





    })





$("#grp_create_btn").on("click",function(){

//    alert("kjhkjhj")
})



})

