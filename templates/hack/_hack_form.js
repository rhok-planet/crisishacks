// need to add 'is_other' to repos so we can make this work

String.prototype.startsWith = function(str){
    return (this.indexOf(str) === 0);
}

$("#id_repo_url").focus();
$("#div_id_repo").hide();

var repo_urls = eval({{ repos|safe }});


$("#id_repo_url").keyup(function(e) {
    var url = $("#id_repo_url").val();
    if (url.startsWith("https://")) {
        url = url.replace("https", "http");
        $("#id_repo_url").val(url);
    };
});
    
$("#id_repo_url").change(function(e) {
 
    $("#target").text($("#id_repo_url").val());      

    $.each(repo_urls, function(key, value) {         
    
        var url = $("#id_repo_url").val();
        var url_array = url.split('/');
        if (url.startsWith(key)){
            if (url !== key){
                $("#id_repo").val(value);
                if ($("#id_title").val().length === 0) {
                    $("#id_title").val(url_array[url_array.length-1]);
                };
                var slug = URLify(url_array[url_array.length-1]);
                $("#id_slug").val(slug);
                $("#package-form-message").text("Your package is hosted at " + key)
            };
        };
    });
});

$("#package-form").submit(function(e) {
    
    // TODO - make this work off a database change where we add the is_other boolean to repos
    var repo = $("#id_repo").val();
    if (repo.length === 0){
        $("#id_repo").val("4");
    };
    
    return true
});
