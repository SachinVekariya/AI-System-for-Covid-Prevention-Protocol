$("#img1").change(function(){
    var reader = new FileReader();
    const file = this.files[0];
    reader.readAsDataURL(file);

    reader.onload = function(){
        var img = new Image();
        img.src = reader.result;
        var canvas = document.createElement('canvas');
        canvas.width = 500;
        canvas.height = 500;
        var ctx = canvas.getContext('2d');
        
        img.onload = function(){
            ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
            const newImage = canvas.toDataURL('image/jpg');
            $("#display_img1").attr("src",newImage);

            var img_data = new FormData();
            img_data.append('img',newImage);

            jQuery.ajax({
                url: '/api/detection_mask_photo/',
                data: img_data,
                cache: false,
                contentType: false,
                processData: false,
                method: 'POST',
                type:'POST',
                success: function(data,status){
                    $("#detected_img1").attr("src",'data:image/jpg;base64,' + data.img);
                    // Create Table

                    if(data.mask.length >0){
                        var table = '<table class="table table-striped table-hover"><thead><tr><th>Index</th><th>Mask</th><th>Confidence</th><th>Entry</th></tr></thead><tbody>';
                        for(var i=0;i<data.mask.length;i++){
                            table += '<tr><th>'+i+'</th>';
                            table += '<td>'+ data.mask[i] +'</td>';
                            table += '<td>'+ data.confidence[i].toFixed(2) +'</td>';
                            table += '<td>'+ data.entry[i] +'</td></tr>';
                        }
                        table += '</tbody></table>';

                        $("#info_table1").html(table);
                    }
                    else{
                        $("#info_table1").html('<h4 style="text-align:center;color:red;" class="justify-content-center">No person Detected</h4>');
                    }
                    
                }
            });
        };
    };
});




var interval;
$("#start_stop_cam").change(function(){
    let check = $("#start_stop_cam").prop("checked");
    
    if(check){
        navigator.mediaDevices.getUserMedia({
            video: true
        })
        .then(stream => {
            window.localStream = stream;
            document.querySelector('#display_img2').srcObject = stream;
        })
        .catch((err) => {
        console.log(err);
        });
        $("#start_cam").attr("disabled",true);
        $("#stop_cam").attr("disabled",false);
    
        interval = setInterval(fps_10,100);
    }
    else{
        localStream.getVideoTracks()[0].stop();
        $("#start_cam").attr("disabled",false);
        $("#stop_cam").attr("disabled",true);
        clearInterval(interval);
    }
});


function fps_10(){
    const canvas = document.createElement('canvas');
    const video = document.querySelector('#display_img2');

    canvas.width = 512;
    canvas.height = 384;
    var ctx = canvas.getContext('2d');
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

    const newImage = canvas.toDataURL('image/jpg');
    $("#display_img22").attr("src",newImage);
    var img_data = new FormData();

    img_data.append('img',newImage);

    jQuery.ajax({
        url: '/api/detection_mask_video/',
        data: img_data,
        cache: false,
        contentType: false,
        processData: false,
        method: 'POST',
        type:'POST',
        success: function(data,status){
            $("#detected_img2").attr("src",'data:image/jpg;base64,' + data.img);

            // Create Table
            if(data.mask.length >0){
                var table = '<table class="table table-striped table-hover"><thead><tr><th>Index</th><th>Mask</th><th>Confidence</th><th>Entry</th></tr></thead><tbody>';

                for(var i=0;i<data.mask.length;i++){
                    table += '<tr><th>'+i+'</th>';
                    table += '<td>'+ data.mask[i] +'</td>';
                    table += '<td>'+ data.confidence[i].toFixed(2) +'</td>';
                    table += '<td>'+ data.entry[i] +'</td></tr>';
                }
                table += '</tbody></table>';

                $("#info_table2").html(table);
            }
            else{
                $("#info_table2").html('<h4 style="text-align:center;color:red;" class="justify-content-center">No person Detected</h4>');
            }
            
        }
    });
};



var optical_img;
var thermal_img;

$("#optical_img").change(function(){
    optical_img = this.files[0];
    var reader = new FileReader();
    reader.readAsDataURL(optical_img);

    reader.onload = function(){
        $("#display_optical").attr("src",reader.result);
    }
});

$("#thermal_img").change(function(){
    thermal_img = this.files[0];
    var reader = new FileReader();
    reader.readAsDataURL(thermal_img);

    reader.onload = function(){
        $("#display_thermal").attr("src",reader.result);
    }
});

$("#submit_btn").click(function(event){
    event.preventDefault();

    var img_data = new FormData();
    img_data.append('optical',optical_img);
    img_data.append('thermal',thermal_img);

    jQuery.ajax({
        url: '/api/detection_mask_temp/',
        data: img_data,
        cache: false,
        contentType: false,
        processData: false,
        method: 'POST',
        type:'POST',
        success: function(data,status){
            $("#display_detected").attr("src",'data:image/jpg;base64,' + data.img);

            // Create Table
            if(data.mask.length >0){
                var table = '<table class="table table-striped table-hover"><thead><tr><th>Index</th><th>Temperature</th><th>Mask</th><th>Entry</th><th>Reason</th></tr></thead><tbody>';

                for(var i=0;i<data.temp.length;i++){
                    table += '<tr><th>'+i+'</th>';
                    table += '<td>'+ data.temp[i].toFixed(2)+'°C'+'</td>';
                    table += '<td>'+ data.mask[i] +'</td>';
                    table += '<td>'+ data.entry[i] +'</td>';
                    table += '<td>'+ data.reason[i] +'</td></tr>';
                }
                table += '</tbody></table>';

                $("#info_table3").html(table);
            }
            else{
                $("#info_table3").html('<h4 style="text-align:center;color:red;" class="justify-content-center">No person Detected</h4>');
            }
        }
    });
});

