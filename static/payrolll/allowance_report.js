$(document).ready(function() {
    // Function to fetch data and populate table
    function populateTable() {
        $.ajax({
            url: '/graphql', // Replace with your GraphQL endpoint
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({
                query: `
                    query {
                        getAllowanceList {
                            id
                            firstName
                            lastName
                            allowance
                            mealAllowance
                            developmental
                            holidayRdotPay
                            allowanceDeduction
                            allowanceAdjustment
                            netAllow
                        }
                    }
                `
            }),
            success: function(response) {
                if (response && response.data && response.data.getAllowanceList && Array.isArray(response.data.getAllowanceList)) {
                    console.log('Data received from server:', response.data.getAllowanceList);
                    var tableBody = $('#table_allowance_report tbody');
                    tableBody.empty(); // Clear table body

                    // Populate table rows with data
                    response.data.getAllowanceList.forEach(function(item) {
                        var row = '<tr>' +
                            
                            
                            '<td>'  + item.firstName + '</td>' +
                            '<td>'  + item.lastName + '</td>' +
                            '<td>'  + item.allowance + '</td>' +
                            '<td>'  + item.mealAllowance + '</td>' +
                            '<td>'  + item.developmental + '</td>' +
                            '<td>'  + item.holidayRdotPay + '</td>' +
                            '<td>'  + item.allowanceDeduction + '</td>' +
                            '<td>'  + item.allowanceAdjustment + '</td>' +
                            '<td>'  + (Number(item.netAllow).toLocaleString('en-US', {minimumFractionDigits: 2, maximumFractionDigits: 2})) + '</td>' +
                            
                            '</tr>';
                        tableBody.append(row);
                    });
                    initializeDataTable()
                } else {
                    console.error('Data format error or empty data received from server.');
                }
            },
            error: function(error) {
                console.error('GraphQL request failed:', error);
            }
        });
    }

    // Call populateTable function on document ready
    populateTable();
});


const initializeDataTable = () => {
    $('#table_allowance_report').DataTable();
    
    
};


function payrollListExcel(type){
    var data = document.getElementById('table_allowance_report');
    var file = XLSX.utils.table_to_book(data,{sheet: "sheet1"});
    XLSX.write(file,{ booktype: type, bookSST: true, type: 'base64'});
    XLSX.writeFile(file, 'allowance_list.' + type);

}

