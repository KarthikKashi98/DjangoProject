// $(".nav li").on("click", function() {
//      $(".nav li").removeClass("active");
//      $(this).addClass("active");
//    });




//    $(".navbar-nav").on('click',a,function(){
//        alert("jkhkjhk")
//        $(this).addClass("active");
//        $(".nav-item a.active").removeClass("active");
//        // remove classname 'active' from all li who already has classname 'active'
//
//        // adding classname 'active' to current click li
////        $(this).addClass("active");
//    });


$(function(){

    var current = location.pathname;
    $('#navMenus li a').each(function(){
        var $this = $(this);
        // if the current path is like this link, make it active
        if($this.attr('href').indexOf(current) !== -1){
            $this.addClass('active');
        }
    })


})



