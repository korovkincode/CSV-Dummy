function generate() {
    let table = document.getElementsByTagName('table')[1];
    let trEl = document.createElement('tr');
    let cur = 0;
    if (table.getElementsByTagName('tr').length === 1) cur = 1;
    else cur = parseInt(table.getElementsByTagName('tr')[table.getElementsByTagName('tr').length - 1].getElementsByTagName('th')[0].innerText) + 1;
    trEl.innerHTML = `
    <th style="text-align: center;" scope="row">${cur}</th>
        <td style="text-align: center;">{{ now }}</td>
        <td style="text-align: center;">
            <span class="badge badge-pill badge-secondary">Processing</span>
        </td>
        <td style="text-align: center;"></td>
    `;
    table.appendChild(trEl);
    $.ajax(
    {
        type:"GET",
        url: "/scheme/{{ scheme_id }}/",
        data: {
            rows: document.getElementById("rows").value
        },
        success: function(data) 
        {
            console.log(data);
            table.getElementsByTagName('tr')[table.getElementsByTagName('tr').length - 1].getElementsByTagName('td')[1].innerHTML = '<span class="badge badge-pill badge-success">Ready</span>';
            table.getElementsByTagName('tr')[table.getElementsByTagName('tr').length - 1].getElementsByTagName('td')[2].innerHTML = `<a href="/static/${data}/" download>Download</a>`;
        }
    })
}