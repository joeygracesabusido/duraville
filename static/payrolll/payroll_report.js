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
                    // $('#table_payroll_report').DataTable();
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
    $('#table_payroll_report').DataTable();
    // $('#table_payroll_report').DataTable( {
    //     dom: 'LBfrtip',
    //     buttons: [
    //         { // COPY
    //             extend : 'copy',
    //             text: 'Copy',
    //             className: 'btn btn-secondary',
    //             titleArttr: 'Copy',
    //             exportOptions: {
    //                 columns: [0,1,2,3]
    //             },
    //         },
    //         { // EXCEL
    //             extend : 'excel',
    //             text: 'Export Excel',
    //             className: 'btn btn-success',
    //             titleArttr: 'Excel',
    //             exportOptions: {
    //                 columns: [0,1,2,3]
    //             },
    //         },
    //         { // Print
    //             extend : 'print',
    //             text: 'Print',
    //             className: 'btn btn-danger',
    //             titleArttr: 'Print',
    //             exportOptions: {
    //                 columns: [0,1,2,3]
    //             },
    //         },

        
    //     ]

    // } );

    
};


function payrollListExcel(type){
    var data = document.getElementById('table_payroll_report');
    var file = XLSX.utils.table_to_book(data,{sheet: "sheet1"});
    XLSX.write(file,{ booktype: type, bookSST: true, type: 'base64'});
    XLSX.writeFile(file, 'payroll_list.' + type);

}

