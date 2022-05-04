   // For the loading animation modal
   $body = $("body");

   // Events for the loading animation
   $(document).on({
       ajaxStart: function() { $body.addClass("loading");    },
       ajaxStop: function() { $body.removeClass("loading"); }    
   });

   // This displays the uploaded picture
   document.getElementById('image-uploader').addEventListener('change', readURL, true);
   function readURL(){
       var file = document.getElementById('image-uploader').files[0];
       var reader = new FileReader();

       reader.onloadend = function(){
           document.getElementById('resultImage').src = reader.result;
       }
       if(file){
           reader.readAsDataURL(file);
       }else{
       }
   };