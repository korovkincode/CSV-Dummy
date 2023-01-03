function delScheme(scheme) {
    let schemeURL = scheme.parentElement.getElementsByTagName('td')[1].getAttribute('href');
    $.ajax(
    {
        type:"GET",
        url: schemeURL,
        data: {},
        success: function(data) 
        {
            console.log(data);
            scheme.parentElement.parentElement.remove();
        }
    });
}