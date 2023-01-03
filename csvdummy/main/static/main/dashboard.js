function delScheme(scheme) {
    let schemeURL = scheme.parentElement.parentElement.getElementsByTagName('td')[0].getElementsByTagName('a')[0].getAttribute('href');
    $.ajax(
    {
        type:"GET",
        url: schemeURL + '/delete',
        data: {},
        success: function(data) 
        {
            scheme.parentElement.parentElement.remove();
        }
    });
}