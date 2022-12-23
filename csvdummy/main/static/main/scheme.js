function formSubmit() {
    event.preventDefault();
    if (document.getElementsByTagName('tr').length === 2) {
        let trEl = document.getElementsByTagName('tr')[1];
        let errorEl = document.createElement('td');
        errorEl.setAttribute(
            'style',
            'color: red; border: none; text-align: center;'
        );
        errorEl.setAttribute(
            'class',
            'error'
        );
        errorEl.innerHTML = "<h6>Create at least one column!</h6>";
        trEl.appendChild(errorEl);
    } else {
        document.getElementsByTagName('form')[0].submit();
    }
}
let form = document.getElementsByTagName('form')[0];
form.addEventListener("submit", formSubmit);
function check() {
    let orders = Array();
    for (errorEl of document.getElementsByClassName('error')) {
        errorEl.setAttribute(
            'style',
            'display: none'
        );
    }
    for (trEl of document.getElementsByTagName('tr')) {
        if (trEl.getElementsByTagName('input')[1] === undefined) continue;
        if (trEl.getElementsByTagName('input')[0].value === "") {
            let errorEl = document.createElement('td');
            errorEl.setAttribute(
                'style',
                'color: red; border: none; text-align: center;'
            );
            errorEl.setAttribute(
                'class',
                'error'
            );
            errorEl.innerHTML = "<h6>Column name can't be empty!</h6>";
            trEl.appendChild(errorEl);
            return 0;
        } 
        let curOrder = trEl.getElementsByTagName('input')[1].value;
        if (orders.includes(curOrder)) {
            let errorEl = document.createElement('td');
            errorEl.setAttribute(
                'style',
                'color: red; border: none; text-align: center;'
            );
            errorEl.setAttribute(
                'class',
                'error'
            );
            errorEl.innerHTML = "<h6>Orders must be distinct numbers!</h6>";
            trEl.appendChild(errorEl);
            return 0;
        }
        orders.push(curOrder);
    }
    return 1;
}
const delRow = (el) => {
    el.parentElement.parentElement.remove()
}
function add() {
    let checkV = check();
    if (checkV === 0) return 0;
    let prevColumn = document.getElementsByTagName('tr')[document.getElementsByTagName('tr').length - 1];
    let delEl = document.createElement('td');
    delEl.setAttribute(
        'style',
        'border: none; text-align: center;'
    );
    delEl.innerHTML = '<button onclick="delRow(this)" style="background: none; border: none; color: red">Delete</button>';
    prevColumn.appendChild(delEl);
    let newColumn = document.createElement('tr');
    let tdEl = document.createElement('td');
    tdEl.setAttribute(
        'style',
        'border: none; text-align: center;'
    );
    tdEl.innerHTML = "<input name='columnName' type='text' class='form-control'>";
    document.getElementById('table').appendChild(newColumn);
    newColumn.appendChild(tdEl);
    tdEl = document.createElement('td');
    tdEl.setAttribute(
        'style',
        'border: none; text-align: center;'
    );
    tdEl.innerHTML = '<select name="datatype" class="form-select form-select-sm" aria-label=".form-select-sm example">\
                            <option name="datatype" value="Full name">Full name</option>\
                            <option name="datatype" value="Job">Job</option>\
                            <option name="datatype" value="Domain name">Domain name</option>\
                            <option name="datatype" value="Company name">Company name</option>\
                            <option name="datatype" value="Address">Address</option>\
                        </select>';
    newColumn.appendChild(tdEl);
    tdEl = document.createElement('td');
    tdEl.setAttribute(
        'style',
        'border: none; text-align: center;'
    );
    tdEl.innerHTML = '<input name="order" type="number" value="0" min="0">';
    newColumn.appendChild(tdEl);
}