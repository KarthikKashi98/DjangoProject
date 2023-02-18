$(function(){


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


                        }
                    })



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



})


