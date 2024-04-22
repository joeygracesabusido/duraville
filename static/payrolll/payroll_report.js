// this is to display table
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
                        getPayrollAllApi {
                            name
                            grossPay
                            netPay
                            payrollDate
                        }
                    }
                `
            }),
            success: function(response) {
                if (response && response.data && response.data.getPayrollAllApi && Array.isArray(response.data.getPayrollAllApi)) {
                    console.log('Data received from server:', response.data.getPayrollAllApi);
                    var tableBody = $('#table_payroll_report tbody');
                    tableBody.empty(); // Clear table body

                    // Populate table rows with data
                    response.data.getPayrollAllApi.forEach(function(item) {
                        // var formattedAmount = parseFloat(item.amountDeduction).toFixed(2).replace(/\d(?=(\d{3})+\.)/g, '$&,');
                        var formattedGrossPayAmount = parseFloat(item.grossPay).toLocaleString(undefined, {
                            minimumFractionDigits: 2,
                            maximumFractionDigits: 2
                        });
                        var row = '<tr>' +
                            '<td>'  + item.payrollDate + '</td>' + 
                            '<td>'  + item.name + '</td>' + 
                            '<td>' + formattedGrossPayAmount + '</td>' +
                            '<td>' + (Number(item.netPay).toLocaleString('en-US', {minimumFractionDigits: 2, maximumFractionDigits: 2})) + '</td>' +
                           
                            '</tr>';
                        tableBody.append(row);
                    });
                    // Initialize DataTable after populating the table
                    $('#table_payroll_report').DataTable();
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
